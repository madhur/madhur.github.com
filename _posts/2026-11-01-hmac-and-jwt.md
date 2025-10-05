---
layout: post
title: "HMAC and JWT"
excerpt: "HMAC and JWT"
disqus_id: /2026/11/01/hmac-and-jwt/
tags:
    - HMAC
    - JWT
---

> **Disclaimer**: This blog article has been generated with the assistance of AI. While the content is AI-generated, the software itself and the ideas behind it are the result of real development work and genuine user needs.

HMAC and JWT are fundamental building blocks in modern web authentication systems. This post examines how they work at a technical level and why they're designed the way they are.

## What is HMAC?

HMAC (Hash-based Message Authentication Code) is a mechanism for verifying both the authenticity and integrity of a message. It combines a cryptographic hash function with a secret key.

### HMAC's Purpose

HMAC answers two questions:
1. Did this message come from someone who knows the secret key?
2. Has the message been modified since it was created?

It does not encrypt the message—the data remains readable. HMAC is about verification, not confidentiality.

### The HMAC Algorithm

The standard HMAC construction follows this formula:

```
HMAC(K, m) = H((K ⊕ opad) || H((K ⊕ ipad) || m))
```

Where:
- `K` is the secret key
- `m` is the message
- `H` is a cryptographic hash function (SHA-256, SHA-1, etc.)
- `ipad` is the inner padding (0x36 repeated)
- `opad` is the outer padding (0x5C repeated)
- `⊕` represents XOR operation
- `||` represents concatenation

### Why Two Passes?

The two-pass design protects against length extension attacks that could exploit simpler constructions like `H(K || m)`. The nested structure with different padding values ensures that an attacker cannot append data to the message and compute a valid MAC without knowing the key.

**Inner hash (first pass):**
```
innerHash = H((K ⊕ ipad) || m)
```

**Outer hash (second pass):**
```
HMAC = H((K ⊕ opad) || innerHash)
```

### HMAC in Practice

When implementing HMAC, you typically use a cryptographic library rather than implementing the algorithm yourself. Here's how it looks in Java:

```java
Mac hmac = Mac.getInstance("HmacSHA256");
SecretKeySpec keySpec = new SecretKeySpec(secretKey, "HmacSHA256");
hmac.init(keySpec);
byte[] signature = hmac.doFinal(message);
```

The library handles the padding, XOR operations, and nested hashing internally.

### Common Use Cases

HMAC appears in various authentication scenarios:

**Webhook signatures**: Services like GitHub and Stripe send webhooks with HMAC signatures to prove authenticity.

```
signature = HMAC-SHA256(timestamp + "." + payload, shared_secret)
```

**API request signing**: AWS uses HMAC-SHA256 for request authentication, computing signatures over request parameters.

**Session tokens**: HMAC can verify that session data hasn't been tampered with.

## JSON Web Tokens (JWT)

JWT provides a standardized way to encode claims and verify their integrity. A JWT consists of three Base64URL-encoded parts separated by dots.

### JWT Structure

```
header.payload.signature
```

**Header** specifies the algorithm and token type:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload** contains claims (assertions about the subject):
```json
{
  "sub": "user123",
  "name": "Alice",
  "iat": 1516239022,
  "exp": 1516242622
}
```

**Signature** ensures integrity using the specified algorithm.

### JWT Signature Generation

For HMAC-based JWTs (HS256, HS384, HS512), the signature is computed as:

```
signature = HMAC-SHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

The complete JWT becomes:
```
base64UrlEncode(header) + "." + 
base64UrlEncode(payload) + "." + 
base64UrlEncode(signature)
```

### JWT Verification Process

Verifying a JWT involves:

1. Split the token on `.` to extract header, payload, and signature
2. Decode the header to determine the algorithm
3. Recompute the signature: `HMAC(header + "." + payload, secret)`
4. Compare the computed signature with the provided signature
5. Verify claims (expiration, issuer, audience, etc.)

If the signatures match and claims are valid, the token is trusted.

### Symmetric vs Asymmetric Algorithms

JWT supports multiple signing algorithms with different properties.

**Symmetric algorithms (HMAC-based):**
- HS256 (HMAC with SHA-256)
- HS384 (HMAC with SHA-384)  
- HS512 (HMAC with SHA-512)

The same secret is used for both signing and verification. Anyone with the secret can create valid tokens.

**Asymmetric algorithms:**
- RS256 (RSA with SHA-256)
- ES256 (ECDSA with SHA-256)

A private key signs tokens, while a public key verifies them. This allows verification without the ability to create tokens.

### Security Properties

**What JWT with HMAC provides:**
- **Integrity**: Any modification to header or payload invalidates the signature
- **Authenticity**: Only parties with the secret can create valid tokens

**What JWT does NOT provide:**
- **Confidentiality**: The payload is Base64-encoded, not encrypted. Anyone can decode and read it.

To see the payload:
```javascript
atob("eyJzdWIiOiJ1c2VyMTIzIn0")
// Result: {"sub":"user123"}
```

### Token Tampering

Without the secret key, you cannot:
- Create a new valid JWT
- Modify an existing JWT's claims
- Change the algorithm in the header

Any attempt to modify the token without recomputing the signature with the correct secret will fail verification:

```
Original: header.payload.validSignature
Modified: header.modifiedPayload.validSignature  ← fails verification
Modified: header.modifiedPayload.invalidSignature ← fails verification
```

### Standard Claims

JWT defines several standard claims (all optional):

- `iss` (issuer): Who created the token
- `sub` (subject): Who the token is about
- `aud` (audience): Who the token is intended for
- `exp` (expiration): When the token expires (Unix timestamp)
- `nbf` (not before): When the token becomes valid
- `iat` (issued at): When the token was created
- `jti` (JWT ID): Unique identifier for the token

Applications can also include custom claims.

### Stateless Authentication

JWT enables stateless authentication. The server doesn't need to store session data because all necessary information is in the token itself.

**Traditional session flow:**
1. User logs in
2. Server creates session ID and stores user data in database/cache
3. Server sends session ID to client
4. Client sends session ID with each request
5. Server looks up session data for each request

**JWT flow:**
1. User logs in
2. Server creates JWT containing user data and signs it
3. Server sends JWT to client
4. Client sends JWT with each request
5. Server verifies signature and trusts the payload data

No database lookup is required for each request. The trade-off is that you cannot easily invalidate individual tokens before expiration.

## Implementation Considerations

### Key Management

The security of HMAC and JWT depends entirely on keeping the secret key secure. The key should be:

- Randomly generated with sufficient entropy (at least 256 bits for HS256)
- Stored securely (environment variables, secret management systems)
- Never committed to version control
- Rotated periodically

### Timing Attacks

When comparing signatures, use constant-time comparison to prevent timing attacks:

```java
// Vulnerable
if (providedSignature.equals(computedSignature))

// Better
if (MessageDigest.isEqual(providedBytes, computedBytes))
```

Variable-time comparison could leak information about which bytes match, potentially allowing an attacker to forge signatures.

### Token Expiration

Always set expiration times on JWTs. Without expiration, a stolen token remains valid indefinitely. Common patterns:

- Short-lived access tokens (15 minutes to 1 hour)
- Longer-lived refresh tokens for obtaining new access tokens
- Store refresh tokens securely and implement revocation

### Algorithm Verification

Always verify the algorithm in the JWT header matches your expectations. Some libraries have been vulnerable to attacks where an attacker changes the algorithm from RS256 to HS256, causing the server to treat the public key as an HMAC secret.

```java
// Verify algorithm explicitly
if (!header.getAlgorithm().equals("HS256")) {
    throw new InvalidTokenException("Unexpected algorithm");
}
```

## Conclusion

HMAC provides a mathematically sound way to verify message authenticity and integrity using shared secrets. JWT builds on this foundation to create a standardized token format for transmitting verified claims.

Both HMAC and JWT are proven technologies when used correctly, but they require careful attention to implementation details like key management, timing attack prevention, and proper validation of all components.