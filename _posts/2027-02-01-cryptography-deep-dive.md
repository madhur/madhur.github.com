---
layout: blog-post
title: "Cryptography Deep Dive"
excerpt: "Cryptography Deep Dive"
disqus_id: /2027/02/01/cryptography-deep-dive/
tags:
    - Cryptography
---


## Table of Contents
- [Introduction: The Vault Complexity Problem](#introduction-the-vault-complexity-problem)
- [Part 1: Cryptography Fundamentals](#part-1-cryptography-fundamentals)
  - [Public and Private Keys: The Foundation](#public-and-private-keys-the-foundation)
  - [The Three Types of Cryptographic Operations](#the-three-types-of-cryptographic-operations)
- [Part 2: Understanding Initialization Vectors (IV)](#part-2-understanding-initialization-vectors-iv)
- [Part 3: The Mathematical Magic of ECDH](#part-3-the-mathematical-magic-of-ecdh)
- [Part 4: Digital Signatures Explained](#part-4-digital-signatures-explained)
- [Part 5: Complete Vault Architecture](#part-5-complete-vault-architecture)
- [Part 6: Real-World Implementation](#part-6-real-world-implementation)
- [Conclusion: When to Use Each Approach](#conclusion-when-to-use-each-approach)

---

## Introduction: The Vault Complexity Problem

When I first encountered a production vault service, I was confused by the complexity:

```java
// Why is this so complicated?
PublicKeyResponse vaultKey = vault.getPublicKey();
String bearerKey = registry.getBearerKey();
SecretKey sharedSecret = ECDH(myPrivate, vaultKey);
byte[] encrypted = AES.encrypt(data, sharedSecret, iv);
String signature = ECDSA.sign(metadata, myPrivate);
```

Why not just:

```java
// Wouldn't this be simpler?
String token = vault.encrypt(data);
```

By the end of this article, you'll understand:
- Why the complex approach is necessary for security
- How ECDH differs from RSA encryption
- What digital signatures provide that encryption doesn't
- Why initialization vectors are critical
- How all these pieces work together

Let's start with the fundamentals.

---

## Part 1: Cryptography Fundamentals

### Public and Private Keys: The Foundation

Before diving into vault architecture, we need to understand asymmetric cryptography.

#### The Basic Rules

In public-key cryptography, each party has two keys:
- **Private Key**: Secret, never shared
- **Public Key**: Shared freely with everyone

These keys work together but in specific ways depending on the operation.

#### Standard Asymmetric Encryption (RSA-style)

**For Encryption:**

| Key Type | Can Encrypt? | Can Decrypt? |
|----------|-------------|-------------|
| Public Key | ✅ Yes | ❌ No |
| Private Key | ❌ No | ✅ Yes |

**The Flow:**

```plaintext
Alice wants to send a secret to Bob:

Step 1: Alice obtains Bob's PUBLIC key
Step 2: Alice encrypts message with Bob's PUBLIC key
        ciphertext = encrypt(message, Bob_Public)
Step 3: Alice sends ciphertext to Bob
Step 4: Bob decrypts with Bob's PRIVATE key
        message = decrypt(ciphertext, Bob_Private)

Key Insight: Only Bob can decrypt because only he has the private key!
```

**Visual Diagram:**

```
┌─────────────────────────────────────────────────────────────┐
│                   RSA ENCRYPTION FLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ALICE                                    BOB               │
│  ┌──────────────┐                        ┌──────────────┐  │
│  │  "Hello Bob" │                        │  "Hello Bob" │  │
│  └──────────────┘                        └──────────────┘  │
│        ↓                                        ↑           │
│   Encrypt with                            Decrypt with      │
│   Bob's PUBLIC key                        Bob's PRIVATE key │
│        ↓                                        ↑           │
│  ┌──────────────┐                        ┌──────────────┐  │
│  │ "x7K9mP2q..." │  ───────────────────→  │ "x7K9mP2q..." │  │
│  │ (ciphertext)  │                        │ (ciphertext)  │  │
│  └──────────────┘                        └──────────────┘  │
│                                                             │
│  Attacker can intercept ciphertext but cannot decrypt      │
│  because they don't have Bob's private key                 │
└─────────────────────────────────────────────────────────────┘
```

#### Digital Signatures (Reverse Usage)

The same keys work in reverse for proving authenticity:

**For Signing:**

| Key Type | Can Sign? | Can Verify? |
|----------|-----------|-------------|
| Private Key | ✅ Yes | ❌ No |
| Public Key | ❌ No | ✅ Yes |

**The Flow:**

```plaintext
Alice wants to prove she wrote a document:

Step 1: Alice signs document with Alice's PRIVATE key
        signature = sign(document, Alice_Private)
Step 2: Alice publishes both document and signature
Step 3: Bob verifies signature using Alice's PUBLIC key
        isValid = verify(document, signature, Alice_Public)

Key Insight: Only Alice could have created this signature!
```

**Visual Diagram:**

```
┌─────────────────────────────────────────────────────────────┐
│                  DIGITAL SIGNATURE FLOW                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ALICE                                    BOB               │
│  ┌──────────────┐                        ┌──────────────┐  │
│  │  Document    │                        │  Document    │  │
│  │  "I owe $100"│                        │  "I owe $100"│  │
│  └──────────────┘                        └──────────────┘  │
│        ↓                                        ↓           │
│   Sign with                              Verify with        │
│   Alice's PRIVATE key                    Alice's PUBLIC key │
│        ↓                                        ↑           │
│  ┌──────────────┐                        ┌──────────────┐  │
│  │  Signature   │  ───────────────────→  │  Signature   │  │
│  │  "3x9F2..."  │                        │  "3x9F2..."  │  │
│  └──────────────┘                        └──────────────┘  │
│                                                ↓            │
│                                          ✅ Valid!          │
│                                          Proves Alice       │
│                                          wrote this         │
│                                                             │
│  Note: Document is NOT encrypted! Anyone can read it.      │
│  Signature only proves authenticity and integrity.          │
└─────────────────────────────────────────────────────────────┘
```

---

### The Three Types of Cryptographic Operations

Modern cryptography involves three distinct operations, often confused with each other:

#### 1. Asymmetric Encryption (e.g., RSA)

**Purpose:** Hide data from everyone except the recipient

**Example: RSA Encryption**
```java
PublicKey bobPublic = getBobPublicKey();
PrivateKey bobPrivate = getBobPrivateKey();

// Alice encrypts
byte[] ciphertext = RSA.encrypt("secret message", bobPublic);

// Bob decrypts
byte[] plaintext = RSA.decrypt(ciphertext, bobPrivate);
```

**Characteristics:**
- ✅ Provides confidentiality
- ❌ Does not prove sender identity
- 🐌 Slow (computational expensive)
- ❌ Limited data size (~190 bytes for 2048-bit RSA)

#### 2. Digital Signatures (e.g., RSA/ECDSA Signatures)

**Purpose:** Prove who created the data and that it hasn't been tampered with

**Example: ECDSA (ES256)**
```java
PrivateKey alicePrivate = getAlicePrivateKey();
PublicKey alicePublic = getAlicePublicKey();

// Alice signs
byte[] signature = ECDSA.sign(document, alicePrivate);

// Anyone verifies
boolean valid = ECDSA.verify(document, signature, alicePublic);
```

**Characteristics:**
- ✅ Provides authenticity (proves who signed)
- ✅ Provides integrity (detects tampering)
- ❌ Does NOT provide confidentiality (data is readable)
- ⚡ Fast (especially ECDSA)

#### 3. Key Agreement (e.g., ECDH)

**Purpose:** Two parties agree on a shared secret without transmitting it

**Example: ECDH**
```java
// Alice has
PrivateKey alicePrivate = generatePrivateKey();
PublicKey alicePublic = generatePublicKey(alicePrivate);

// Bob has
PrivateKey bobPrivate = generatePrivateKey();
PublicKey bobPublic = generatePublicKey(bobPrivate);

// They exchange PUBLIC keys (over insecure channel)
// Alice computes
SecretKey secret1 = ECDH(alicePrivate, bobPublic);

// Bob computes
SecretKey secret2 = ECDH(bobPrivate, alicePublic);

// Magical result: secret1 == secret2 !
// Then use this secret for symmetric encryption (AES)
byte[] encrypted = AES.encrypt(data, secret1);
```

**Characteristics:**
- ✅ Provides confidentiality (via subsequent AES)
- ✅ No secret transmitted over network
- ⚡ Fast (EC operations + symmetric encryption)
- ✅ Unlimited data size (via AES)
- ✅ Perfect forward secrecy (with ephemeral keys)

---

### Comparison Table: The Three Operations

| Feature | RSA Encryption | Digital Signature (ES256/RS256) | ECDH + AES |
|---------|---------------|--------------------------------|-----------|
| **Primary Goal** | Hide data | Prove authenticity | Hide data |
| **Confidentiality** | ✅ Yes | ❌ No | ✅ Yes |
| **Authentication** | ❌ No | ✅ Yes | ❌ No (unless combined) |
| **Integrity** | ❌ No | ✅ Yes | ✅ Yes (with GCM) |
| **Speed** | 🐌 Slow | 🐌 Slow (RSA)<br>⚡ Fast (ECDSA) | ⚡ Fast |
| **Data Size Limit** | ❌ ~190 bytes | ✅ Unlimited | ✅ Unlimited |
| **Key Size** | 2048-4096 bits | 2048-4096 bits (RSA)<br>256 bits (EC) | 256 bits |
| **Network Transmission** | Ciphertext | Signature + Data | Encrypted Data |
| **Modern Standard** | Legacy | ✅ Yes (ECDSA) | ✅ Yes |

---

## Part 2: Understanding Initialization Vectors (IV)

### The Problem IV Solves

Imagine encrypting the same data twice with the same key:

```java
// Encryption attempt 1
String data = "4532-1234-5678-9010";  // Credit card
SecretKey key = mySecretKey;
byte[] encrypted1 = AES.encrypt(data, key);
// Result: "x7K9mP2qL8vN4jR6..."

// Encryption attempt 2 (same data, same key)
String data = "4532-1234-5678-9010";  // Same credit card!
SecretKey key = mySecretKey;           // Same key!
byte[] encrypted2 = AES.encrypt(data, key);
// Result: "x7K9mP2qL8vN4jR6..."  // SAME CIPHERTEXT! 🚨
```

**Security Problems:**

1. **Pattern Detection**: Attacker sees two identical ciphertexts
   - "These must be the same plaintext"
   - Can build frequency analysis
   - Can recognize repeated data

2. **Replay Attacks**: Attacker can capture and replay encrypted messages

3. **Known Plaintext**: If attacker knows one plaintext, they can recognize others

**Example Attack:**

```plaintext
Attacker intercepts encrypted transactions:
- Transaction 1: "x7K9mP2qL8vN4jR6..." → $100 to Alice
- Transaction 2: "m3P8nX5qW9tR2kS..." → $50 to Bob
- Transaction 3: "x7K9mP2qL8vN4jR6..." → Same ciphertext!

Attacker knows: Transaction 3 is also $100 to Alice!
Can replay this transaction, cause fraud, etc.
```

---

### How IV Solves This

An **Initialization Vector (IV)** is a random value added to the encryption process:

```java
// Encryption with IV - Attempt 1
String data = "4532-1234-5678-9010";
SecretKey key = mySecretKey;
byte[] iv1 = generateRandomIV();  // [a3, f9, c2, d1, ...]
byte[] encrypted1 = AES.encrypt(data, key, iv1);
// Result: "x7K9mP2qL8vN4jR6..."

// Encryption with IV - Attempt 2 (same data, same key)
String data = "4532-1234-5678-9010";  // Same!
SecretKey key = mySecretKey;           // Same!
byte[] iv2 = generateRandomIV();       // [7b, 2e, 8f, 4a, ...] DIFFERENT!
byte[] encrypted2 = AES.encrypt(data, key, iv2);
// Result: "m3P8nX5qW9tR2kS..."  // DIFFERENT! ✅
```

**Result:** Same plaintext produces different ciphertext each time!

---

### IV Properties and Requirements

#### Critical Properties:

| Property | Requirement | Why |
|----------|------------|-----|
| **Uniqueness** | Must be different for each encryption | Prevents pattern detection |
| **Randomness** | Must be unpredictable | Prevents cryptanalysis |
| **Size** | 12 bytes (96 bits) for AES-GCM | Algorithm requirement |
| **Secrecy** | NOT secret, can be public | Only needs to be unique |
| **Transmission** | Sent with ciphertext | Needed for decryption |

#### Important: IV is NOT Secret!

```plaintext
What gets transmitted:
┌─────────────────────────────────────────┐
│  Ciphertext: "x7K9mP2qL8vN4jR6..."     │  ← Encrypted
│  IV: "a3f9c2d17e4b8f2a5c6d1e9b"        │  ← PLAINTEXT! Not encrypted!
└─────────────────────────────────────────┘

The IV is sent in the clear because:
- Receiver needs it to decrypt
- It doesn't need to be secret
- It just needs to be unique and random
```

---

### IV in AES-GCM Mode

AES-GCM (Galois/Counter Mode) is the modern standard. Here's how IV fits in:

```java
// Encryption
byte[] plaintext = "sensitive data".getBytes();
SecretKey key = generateKey();
byte[] iv = new byte[12];  // 12 bytes for GCM
new SecureRandom().nextBytes(iv);  // Random IV

Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
GCMParameterSpec spec = new GCMParameterSpec(128, iv);
cipher.init(Cipher.ENCRYPT_MODE, key, spec);
byte[] ciphertext = cipher.doFinal(plaintext);

// Store both ciphertext and IV
store(ciphertext, iv);
```

```java
// Decryption
byte[] ciphertext = retrieve("ciphertext");
byte[] iv = retrieve("iv");  // Must use the SAME IV!

Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
GCMParameterSpec spec = new GCMParameterSpec(128, iv);
cipher.init(Cipher.DECRYPT_MODE, key, spec);
byte[] plaintext = cipher.doFinal(ciphertext);
```

---

### Visual: IV in Action

```
┌───────────────────────────────────────────────────────────────┐
│               ENCRYPTION WITHOUT IV (Insecure)                │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Encryption 1:                                                │
│  Plaintext: "ATTACK AT DAWN"                                 │
│  Key:       "secret123"                                       │
│  Result:    "x7K9mP2qL8vN4jR6" ──┐                          │
│                                    │                          │
│  Encryption 2:                     │ SAME!                    │
│  Plaintext: "ATTACK AT DAWN"       │ Attacker notices         │
│  Key:       "secret123"            │ pattern!                 │
│  Result:    "x7K9mP2qL8vN4jR6" ──┘                          │
└───────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│                ENCRYPTION WITH IV (Secure)                    │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Encryption 1:                                                │
│  Plaintext: "ATTACK AT DAWN"                                 │
│  Key:       "secret123"                                       │
│  IV:        [a3, f9, c2, ...]  ← Random                      │
│  Result:    "x7K9mP2qL8vN4jR6"                               │
│                                                               │
│  Encryption 2:                                                │
│  Plaintext: "ATTACK AT DAWN"    ← Same plaintext             │
│  Key:       "secret123"         ← Same key                    │
│  IV:        [7b, 2e, 8f, ...]  ← Different random!           │
│  Result:    "m3P8nX5qW9tR2kS"  ← Different ciphertext! ✅    │
│                                                               │
│  Attacker cannot detect any pattern!                          │
└───────────────────────────────────────────────────────────────┘
```

---

### Common IV Mistakes

#### ❌ Mistake 1: Reusing IV with Same Key

```java
// WRONG! Security vulnerability!
byte[] iv = new byte[12];
Arrays.fill(iv, (byte) 0);  // Always zeros!

for (String message : messages) {
    encrypt(message, key, iv);  // Reusing same IV!
}
```

**Result:** All encryptions vulnerable to cryptanalysis.

#### ❌ Mistake 2: Sequential/Predictable IV

```java
// WRONG! Predictable IV!
byte[] iv = ByteBuffer.allocate(12)
    .putInt(counter++)  // Predictable!
    .array();
```

**Result:** Attacker can predict future IVs and mount attacks.

#### ✅ Correct: Random IV Every Time

```java
// CORRECT!
SecureRandom random = new SecureRandom();
for (String message : messages) {
    byte[] iv = new byte[12];
    random.nextBytes(iv);  // Fresh random IV each time!
    encrypt(message, key, iv);
}
```

---

## Part 3: The Mathematical Magic of ECDH

### What is ECDH?

**ECDH (Elliptic Curve Diffie-Hellman)** is a key agreement protocol that allows two parties to establish a shared secret over an insecure channel.

The "magic": Both parties compute the same secret without ever transmitting it!

---

### The Simple Analogy: Color Mixing

Before diving into the math, here's an intuitive analogy:

```
Public: Everyone knows YELLOW is the common color

ALICE:
1. Picks secret color: RED (never reveals this)
2. Mixes: YELLOW + RED = ORANGE
3. Sends ORANGE to Bob (publicly)

BOB:
1. Picks secret color: BLUE (never reveals this)
2. Mixes: YELLOW + BLUE = GREEN
3. Sends GREEN to Alice (publicly)

SHARED SECRET:
Alice: Takes Bob's GREEN + her secret RED = BROWN
Bob:   Takes Alice's ORANGE + his secret BLUE = BROWN

Both got BROWN! 🎉

Attacker sees: YELLOW, ORANGE, GREEN
Attacker cannot figure out: RED, BLUE, or BROWN
(In real cryptography, "unmixing" is mathematically impossible)
```

---

### ECDH with Simple Numbers (Diffie-Hellman)

Let's start with the original Diffie-Hellman using simple numbers:

```
PUBLIC PARAMETERS (everyone knows):
- Prime p = 23
- Generator g = 5

ALICE:
1. Picks secret: a = 6 (Alice's private key)
2. Computes: A = g^a mod p = 5^6 mod 23 = 15,625 mod 23 = 8
3. Publishes: A = 8 (Alice's public key)

BOB:
1. Picks secret: b = 15 (Bob's private key)
2. Computes: B = g^b mod p = 5^15 mod 23 = 19
3. Publishes: B = 19 (Bob's public key)

SHARED SECRET:
Alice computes: s = B^a mod p = 19^6 mod 23 = 47,045,881 mod 23 = 2
Bob computes:   s = A^b mod p = 8^15 mod 23 = 35,184,372,088,832 mod 23 = 2

Both got: s = 2 ✅
```

**Why it works mathematically:**

```
Alice: B^a = (g^b)^a = g^(b×a) mod p
Bob:   A^b = (g^a)^b = g^(a×b) mod p

Since a×b = b×a, both compute g^(a×b) mod p
```

**Why it's secure:**

```
Attacker sees:
- p = 23
- g = 5
- A = 8
- B = 19

Attacker needs to find:
- a or b (the "discrete logarithm problem")
- With large numbers (2048+ bits), this is computationally infeasible
- Even supercomputers would take billions of years
```

---

### ECDH with Elliptic Curves (The Real Thing)

Real ECDH uses elliptic curves instead of simple exponentiation. The math is more complex, but the principle is the same.

#### What is an Elliptic Curve?

An elliptic curve is defined by an equation:

```
y² = x³ + ax + b

Example (secp256k1, used in Bitcoin):
y² = x³ + 7
```

**Visualization:**

```
      y
      ↑
    3 |       ●
    2 |     ●   ●
    1 |   ●       ●
    0 |─●─────────●────→ x
   -1 |   ●       ●
   -2 |     ●   ●
   -3 |       ●

Points on this curve form a mathematical group
with special addition properties
```

#### Point Addition on Elliptic Curves

**Geometric Addition:**

```
To add point P and point Q:
1. Draw a line through P and Q
2. Find where the line intersects the curve (third point)
3. Reflect that point over the x-axis
4. Result is R = P + Q

Visual:
      y
      ↑
      |    P●
      |     
      |       
      |         ●Q
      |          \
      |           \
      |            ●R' (intersection)
    ──┼─────────────────→ x
      |            
      |            ●R (R = P + Q, reflected)
```

**Scalar Multiplication:**

```
k × P means: P + P + P + ... (k times)

Example: 5 × P = P + P + P + P + P
```

---

### ECDH Key Exchange Step-by-Step

Let's see how ECDH works with elliptic curves:

```
PUBLIC PARAMETERS (standardized, everyone knows):
- Elliptic curve: y² = x³ + 7 (secp256k1)
- Base point: G = (x: 55066..., y: 32670...)

ALICE (Client):
1. Generates random private key: ka = 12345...789 (256-bit random number)
2. Computes public key: Pa = ka × G
   (Add G to itself ka times using elliptic curve math)
   Result: Pa = (x: 98765..., y: 43210...)
3. Publishes: Pa

BOB (Vault):
1. Generates random private key: kb = 98765...432 (256-bit random number)
2. Computes public key: Pb = kb × G
   Result: Pb = (x: 11223..., y: 44556...)
3. Publishes: Pb

EXCHANGE PUBLIC KEYS:
Alice → Bob: Pa
Bob → Alice: Pb

SHARED SECRET:
Alice computes: S = ka × Pb = ka × (kb × G) = (ka × kb) × G
Bob computes:   S = kb × Pa = kb × (ka × G) = (kb × ka) × G

Both got the same point S! ✅

DERIVE SYMMETRIC KEY:
Take the x-coordinate of S
Hash it: SHA-256(S.x)
Result: 32-byte key for AES encryption
```

---

### The Complete ECDH Visual Flow

```
┌───────────────────────────────────────────────────────────────┐
│                      ECDH KEY EXCHANGE                        │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ALICE (Client)                        BOB (Vault)            │
│  ┌──────────────────┐                  ┌──────────────────┐  │
│  │ Private: ka      │                  │ Private: kb      │  │
│  │ (secret number)  │                  │ (secret number)  │  │
│  └──────────────────┘                  └──────────────────┘  │
│          ↓                                      ↓             │
│  Compute Pa = ka × G                   Compute Pb = kb × G   │
│          ↓                                      ↓             │
│  ┌──────────────────┐                  ┌──────────────────┐  │
│  │ Public: Pa       │                  │ Public: Pb       │  │
│  │ (EC point)       │                  │ (EC point)       │  │
│  └──────────────────┘                  └──────────────────┘  │
│          ↓                                      ↓             │
│          └──────── EXCHANGE ───────────────────┘             │
│                    (over insecure channel)                    │
│          ┌──────────────────────────────────────┐            │
│          │                                      │            │
│          ↓                                      ↓            │
│  ┌──────────────────┐                  ┌──────────────────┐  │
│  │ Received: Pb     │                  │ Received: Pa     │  │
│  └──────────────────┘                  └──────────────────┘  │
│          ↓                                      ↓             │
│  Compute S = ka × Pb                   Compute S = kb × Pa   │
│  = ka × (kb × G)                       = kb × (ka × G)       │
│  = (ka × kb) × G                       = (kb × ka) × G       │
│          ↓                                      ↓             │
│  ┌──────────────────┐                  ┌──────────────────┐  │
│  │ Shared Secret: S │                  │ Shared Secret: S │  │
│  │ (same point!)    │◄─────────────────┤ (same point!)    │  │
│  └──────────────────┘                  └──────────────────┘  │
│          ↓                                      ↓             │
│  SHA-256(S.x)                          SHA-256(S.x)          │
│          ↓                                      ↓             │
│  ┌──────────────────┐                  ┌──────────────────┐  │
│  │ AES Key          │                  │ AES Key          │  │
│  │ (32 bytes)       │◄═════════════════┤ (32 bytes)       │  │
│  └──────────────────┘                  └──────────────────┘  │
│                                                               │
│  Both parties now have the SAME AES key!                      │
│  This key was NEVER transmitted over the network!             │
└───────────────────────────────────────────────────────────────┘
```

---

### ECDH Security Explained

**What the attacker sees:**

```
Intercepted (public information):
- Elliptic curve parameters (standardized)
- Base point G
- Alice's public key: Pa = ka × G
- Bob's public key: Pb = kb × G
```

**What the attacker needs but can't get:**

```
To compute the shared secret, attacker needs:
- Alice's private key ka, OR
- Bob's private key kb

To find ka from Pa:
- Must solve: Pa = ka × G, find ka
- This is the "Elliptic Curve Discrete Logarithm Problem" (ECDLP)
- With 256-bit curve: requires ~2^128 operations
- Even fastest supercomputers: billions of years
```

**Security levels:**

| Key Size | Security Level | Equivalent RSA | Time to Break (theoretical) |
|----------|---------------|----------------|----------------------------|
| 160-bit EC | ~80 bits | 1024-bit RSA | Years with supercomputer |
| 224-bit EC | ~112 bits | 2048-bit RSA | Centuries |
| 256-bit EC | ~128 bits | 3072-bit RSA | Millions of years |
| 384-bit EC | ~192 bits | 7680-bit RSA | Age of universe × 10^20 |

---

### ECDH vs RSA: Why ECDH is Better

```
┌──────────────────────────────────────────────────────────────┐
│               ECDH + AES vs RSA ENCRYPTION                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  RSA Encryption:                                             │
│  ───────────────                                             │
│  ✅ Direct encryption/decryption                            │
│  ❌ Very slow (1000x slower than AES)                       │
│  ❌ Limited data size (~190 bytes for 2048-bit key)         │
│  ❌ Large keys needed (2048-4096 bits)                      │
│  ❌ No forward secrecy                                      │
│                                                              │
│  ECDH + AES:                                                 │
│  ───────────                                                 │
│  ✅ Fast (EC operations quick, AES very fast)               │
│  ✅ Unlimited data size                                      │
│  ✅ Small keys (256 bits as secure as 3072-bit RSA)         │
│  ✅ Perfect forward secrecy (with ephemeral keys)           │
│  ✅ Modern standard (TLS 1.3, Signal, WhatsApp)             │
│                                                              │
│  Winner: ECDH + AES for most modern applications! 🏆        │
└──────────────────────────────────────────────────────────────┘
```

---

## Part 4: Digital Signatures Explained

### What Are Digital Signatures?

Digital signatures solve a different problem than encryption:
- **Encryption**: Hides content (confidentiality)
- **Signature**: Proves who created it (authenticity) and it hasn't been tampered with (integrity)

---

### The Two Signature Algorithms

#### RS256: RSA Signature with SHA-256

```java
// Signing with RSA
PrivateKey privateKey = getPrivateKey();
Signature signature = Signature.getInstance("SHA256withRSA");
signature.initSign(privateKey);
signature.update(message.getBytes());
byte[] signatureBytes = signature.sign();

// Verification
PublicKey publicKey = getPublicKey();
Signature signature = Signature.getInstance("SHA256withRSA");
signature.initVerify(publicKey);
signature.update(message.getBytes());
boolean valid = signature.verify(signatureBytes);
```

**RS256 Process:**
```
1. Hash the message: hash = SHA-256(message)
2. "Encrypt" hash with private key: signature = RSA_Sign(hash, privateKey)
3. Attach signature to message

Verification:
1. Hash the message: hash = SHA-256(message)
2. "Decrypt" signature with public key: hash2 = RSA_Verify(signature, publicKey)
3. Compare: hash == hash2 ?
```

#### ES256: ECDSA with SHA-256

```java
// Signing with ECDSA
PrivateKey privateKey = getECPrivateKey();
Signature signature = Signature.getInstance("SHA256withECDSA");
signature.initSign(privateKey);
signature.update(message.getBytes());
byte[] signatureBytes = signature.sign();

// Verification
PublicKey publicKey = getECPublicKey();
Signature signature = Signature.getInstance("SHA256withECDSA");
signature.initVerify(publicKey);
signature.update(message.getBytes());
boolean valid = signature.verify(signatureBytes);
```

**ES256 Process:**
```
1. Hash the message: hash = SHA-256(message)
2. Sign with EC math: signature = ECDSA_Sign(hash, privateKey)
3. Attach signature to message

Verification:
1. Hash the message: hash = SHA-256(message)
2. Verify with EC math: valid = ECDSA_Verify(hash, signature, publicKey)
```

---

### Digital Signature Visual Flow

```
┌───────────────────────────────────────────────────────────────┐
│                    DIGITAL SIGNATURE FLOW                     │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ALICE (Signer)                                               │
│  ┌────────────────────────────────────────┐                  │
│  │  Document: "I owe Bob $100"            │                  │
│  └────────────────────────────────────────┘                  │
│                    ↓                                          │
│            SHA-256 Hash                                       │
│                    ↓                                          │
│  ┌────────────────────────────────────────┐                  │
│  │  Hash: "3a7f9c2d..."                   │                  │
│  └────────────────────────────────────────┘                  │
│                    ↓                                          │
│         Sign with Alice's PRIVATE key                         │
│                    ↓                                          │
│  ┌────────────────────────────────────────┐                  │
│  │  Signature: "9x3K2mP..."               │                  │
│  └────────────────────────────────────────┘                  │
│                    ↓                                          │
│  ┌────────────────────────────────────────┐                  │
│  │  Package: Document + Signature         │                  │
│  └────────────────────────────────────────┘                  │
│                    ↓                                          │
│          Sent to Bob (can be public)                          │
│                    ↓                                          │
│  ──────────────────────────────────────────────────────────  │
│                                                               │
│  BOB (Verifier)                                               │
│  ┌────────────────────────────────────────┐                  │
│  │  Receives: Document + Signature        │                  │
│  └────────────────────────────────────────┘                  │
│                    ↓                                          │
│            SHA-256 Hash Document                              │
│                    ↓                                          │
│  ┌────────────────────────────────────────┐                  │
│  │  Hash: "3a7f9c2d..."                   │                  │
│  └────────────────────────────────────────┘                  │
│                    ↓                                          │
│       Verify Signature with Alice's PUBLIC key                │
│                    ↓                                          │
│  ┌────────────────────────────────────────┐                  │
│  │  Verification Result: ✅ VALID         │                  │
│  │                                        │                  │
│  │  Proves:                               │                  │
│  │  1. Alice signed this (only she has    │                  │
│  │     the private key)                   │                  │
│  │  2. Document wasn't modified (hash     │                  │
│  │     matches)                           │                  │
│  └────────────────────────────────────────┘                  │
│                                                               │
│  Note: ANYONE can verify using Alice's public key!            │
│  But only Alice could have created the signature!             │
└───────────────────────────────────────────────────────────────┘
```

---

### What Signatures Protect Against

#### ✅ Attack 1: Impersonation

```
Attacker tries to forge Alice's signature:

WITHOUT Signature:
- Attacker: "Alice owes me $1000" (sends to bank)
- Bank: "OK, here's $1000" ❌ Fraud succeeded!

WITH Signature:
- Attacker: "Alice owes me $1000" + forged signature
- Bank verifies with Alice's PUBLIC key
- Verification: ❌ INVALID
- Bank: "This isn't from Alice!" ✅ Fraud prevented!
```

#### ✅ Attack 2: Tampering

```
Attacker intercepts message and modifies it:

WITHOUT Signature:
- Original: "Pay Bob $100"
- Attacker modifies: "Pay Eve $100"
- Recipient can't detect modification ❌

WITH Signature:
- Original: "Pay Bob $100" + signature
- Attacker modifies: "Pay Eve $100" + same signature
- Verification: ❌ INVALID (hash doesn't match)
- Recipient: "This was tampered with!" ✅
```

#### ❌ Attack 3: Eavesdropping (NOT protected!)

```
Signatures do NOT provide confidentiality:

Message: "Secret: my password is 12345" + signature
Attacker intercepts and reads: "my password is 12345"
Attacker knows the content! ❌

Signatures prove WHO sent it and INTEGRITY,
but do NOT hide the content!
```

---

### JWS (JSON Web Signature) Explained

Your code uses JWS, which is a standard way to sign JSON data.

**JWS Structure:**

```
HEADER.PAYLOAD.SIGNATURE

Where each part is Base64URL encoded.
```

**Example JWS:**

```
eyJhbGciOiJFUzI1NiIsImtpZCI6InZhdWx0LWtleS0wMDEifQ.eyJ2ZXJzaW9uIjoiMS4wIiwic2hhRW5jcnlwdGVkQmxvY2tPZkRhdGEiOiI4ZjNhOWMyZC4uLiJ9.Xr4k9mN2pQ8vL5jT6hR3gK1fD7cS9aB4eW8uY2iO5xZ
```

**Decoded Parts:**

```json
// HEADER (Base64 decoded)
{
  "alg": "ES256",
  "kid": "vault-key-001"
}

// PAYLOAD (Base64 decoded) - THIS IS READABLE!
{
  "version": "1.0",
  "shaEncryptedBlockOfData": "8f3a9c2d...",
  "payloadMetadata": {
    "algorithm": "AES-256-GCM",
    "iv": "r4nD0mIV12345==",
    "vaultKeyID": "vault-key-001",
    "bearerPublicKey": "MFkwEw..."
  }
}

// SIGNATURE (Base64)
Xr4k9mN2pQ8vL5jT6hR3gK1fD7cS9aB4eW8uY2iO5xZ
```

**Important:** The payload is NOT encrypted! Anyone can decode and read it. The signature only proves:
1. Who created it (has the private key)
2. It wasn't tampered with (hash matches)

---

## Part 5: Complete Vault Architecture

Now let's put everything together to understand the complete vault system.

### The Three Parties

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│     CLIENT       │     │      VAULT       │     │     BEARER       │
│  (E-commerce)    │     │    (Service)     │     │ (Payment Proc)   │
├──────────────────┤     ├──────────────────┤     ├──────────────────┤
│ Private Key: Kc  │     │ Private Key: Kv  │     │ Private Key: Kb  │
│ Public Key:  PC  │     │ Public Key:  PV  │     │ Public Key:  PB  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

### Phase 1: Token Generation (Client Side)

**Input:**
```java
PublicKeyResponse vaultPublicKey = {
    publicKey: "PV_base64_encoded",
    keyID: "vault-key-001"
};
String data = "4532-1234-5678-9010";  // Credit card
String bearerPublicKey = "PB_base64_encoded";
Long tenantId = 12345;
```

**Process:**

```
Step 1: Generate Random IV
├─ iv = [a3, f9, c2, d1, 7e, 4b, 8f, 2a, 5c, 6d, 1e, 9b]
└─ 12 random bytes for AES-GCM

Step 2: ECDH Key Agreement
├─ Client's private key: Kc = getPrivateKey(tenantId)
├─ Vault's public key: PV = vaultPublicKey
├─ Compute: sharedSecret = ECDH(Kc, PV)
└─ Result: 32-byte AES key

Step 3: Encrypt Data with AES-GCM
├─ Plaintext: "4532-1234-5678-9010"
├─ Key: sharedSecret
├─ IV: iv
├─ Algorithm: AES-256-GCM
└─ Result: encryptedData = "x7K9mP2qL8vN4jR6..."

Step 4: Build Metadata (DataContext)
├─ version: "1.0"
├─ shaEncryptedBlockOfData: SHA-256(encryptedData)
├─ algorithm: "AES-256-GCM"
├─ iv: Base64(iv) = "r4nD0mIV12345=="
├─ vaultKeyID: "vault-key-001"
└─ bearerPublicKey: "PB_base64" ← Stored as metadata!

Step 5: Sign Metadata with ES256
├─ Payload: DataContext (as JSON)
├─ Private key: Kc
├─ Algorithm: ES256 (ECDSA with SHA-256)
└─ Result: JWS = "eyJhbGci...Xr4k9mN..."

Step 6: Package Token
├─ encryptedBlockOfData: "x7K9mP2qL8vN4jR6..."
├─ jws: "eyJhbGci...Xr4k9mN..."
└─ sourceCertificate: [client's certificate chain]
```

**Output:**

```json
Token {
  "encryptedBlockOfData": "x7K9mP2qL8vN4jR6...",
  "jws": "eyJhbGciOiJFUzI1NiIsImtpZCI6InZhdWx0LWtleS0wMDEifQ.eyJ2ZXJzaW9uIjoiMS4wIiwic2hhRW5jcnlwdGVkQmxvY2tPZkRhdGEiOiI4ZjNhOWMyZC4uLiIsInBheWxvYWRNZXRhZGF0YSI6eyJhbGdvcml0aG0iOiJBRVMtMjU2LUdDTSIsIml2IjoicjRuRDBtSVYxMjM0NT09Iiwidm...Xr4k9mN2pQ8vL5jT6hR3gK1fD7cS9aB4eW8uY2iO5xZ",
  "sourceCertificate": [
    "-----BEGIN CERTIFICATE-----\nMIIC...",
    "-----BEGIN CERTIFICATE-----\nMIID..."
  ]
}
```

---

### Phase 2: Token Storage (Vault Side)

```
CLIENT ───────────────────────────────────► VAULT
        POST /vault/tokens
        Body: Token

VAULT:
├─ Receives Token
├─ Stores encryptedBlockOfData (cannot decrypt it!)
├─ Stores JWS (metadata is readable)
├─ Stores sourceCertificate
└─ Returns tokenId: "tok_123"

IMPORTANT: Vault CANNOT decrypt the data!
Why? Vault needs Client's cooperation (needs PC from certificate)
```

---

### Phase 3: Token Decryption (Vault Side)

**Input:**

```java
DecryptResponse {
    encryptedBlockOfData: "x7K9mP2qL8vN4jR6...",
    publicKeyCertificate: [
        "-----BEGIN CERTIFICATE-----\nMIIC...",
        "-----BEGIN CERTIFICATE-----\nMIID..."
    ],
    metadata: {
        iv: "r4nD0mIV12345==",
        algorithm: "AES-256-GCM",
        vaultKeyID: "vault-key-001",
        bearerPublicKey: "PB_base64"
    }
}
Long tenantId = 67890;  // Vault's tenant ID
```

**Process:**

```
Step 1: Extract Client's Public Key
├─ Parse certificate chain
├─ Extract leaf certificate
└─ Get public key: PC

Step 2: ECDH Key Agreement (Reverse Direction)
├─ Vault's private key: Kv = getPrivateKey(tenantId)
├─ Client's public key: PC
├─ Compute: sharedSecret = ECDH(Kv, PC)
└─ Result: SAME 32-byte AES key as client computed!

Step 3: Decrypt with AES-GCM
├─ Ciphertext: Base64.decode(encryptedBlockOfData)
├─ Key: sharedSecret
├─ IV: Base64.decode(metadata.iv)
├─ Algorithm: AES-256-GCM
└─ Result: plaintext = "4532-1234-5678-9010"
```

**Output:**

```java
String decrypted = "4532-1234-5678-9010";
```

---

### Complete End-to-End Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     COMPLETE VAULT FLOW                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PHASE 1: TOKEN GENERATION (CLIENT)                                     │
│  ═════════════════════════════════════                                  │
│                                                                         │
│  CLIENT                                                                 │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │ Input:                                                          │   │
│  │ - Credit card: "4532-1234-5678-9010"                          │   │
│  │ - Vault public key: PV (from API call)                        │   │
│  │ - Bearer public key: PB (from registry)                       │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                           ↓                                             │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │ Processing:                                                     │   │
│  │ 1. IV = random 12 bytes                                        │   │
│  │ 2. SharedSecret = ECDH(Kc, PV)                                 │   │
│  │ 3. Encrypted = AES-GCM(card, SharedSecret, IV)                 │   │
│  │ 4. Metadata = {IV, vaultKeyID, bearerPublicKey, ...}           │   │
│  │ 5. JWS = ES256-Sign(Metadata, Kc)                              │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                           ↓                                             │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │ Output: Token {                                                │   │
│  │   encryptedBlockOfData: "x7K9mP...",                          │   │
│  │   jws: "eyJhbGci...",                                          │   │
│  │   sourceCertificate: [...]                                     │   │
│  │ }                                                              │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                           ↓                                             │
│  ──────────────────────────────────────────────────────────────────────│
│                                                                         │
│  PHASE 2: TOKEN STORAGE (VAULT)                                        │
│  ═════════════════════════════════════                                  │
│                                                                         │
│  CLIENT ──────► VAULT                                                   │
│         POST /vault/tokens                                              │
│         Body: Token                                                     │
│                                                                         │
│                  VAULT                                                  │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │ Receives:                                                       │   │
│  │ - Encrypted data (CANNOT decrypt alone!)                       │   │
│  │ - JWS (can read metadata, verify signature)                    │   │
│  │ - Certificate (contains PC)                                    │   │
│  │                                                                 │   │
│  │ Stores everything in database                                  │   │
│  │ Returns: tokenId = "tok_123"                                   │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                           ↓                                             │
│  ──────────────────────────────────────────────────────────────────────│
│                                                                         │
│  PHASE 3: TOKEN DECRYPTION (VAULT)                                     │
│  ═════════════════════════════════════════                              │
│                                                                         │
│  Later, payment needed...                                               │
│                                                                         │
│  CLIENT ──────► VAULT                                                   │
│         POST /vault/decrypt                                             │
│         Body: {tokenId: "tok_123"}                                      │
│                                                                         │
│                  VAULT                                                  │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │ 1. Retrieve Token from database                                │   │
│  │ 2. Extract PC from certificate                                 │   │
│  │ 3. SharedSecret = ECDH(Kv, PC) ← SAME as client computed!      │   │
│  │ 4. Plaintext = AES-GCM-Decrypt(encrypted, SharedSecret, IV)    │   │
│  │ 5. Return: "4532-1234-5678-9010"                               │   │
│  └────────────────────────────────────────────────────────────────┘   │
│                           ↓                                             │
│  VAULT ──────► CLIENT                                                   │
│         Response: "4532-1234-5678-9010"                                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Why This Architecture?

Now we can answer the original question: "Why is this so complicated?"

#### ❌ Simple Vault (Bad)

```
CLIENT ──────────────────────────► VAULT
        "4532-1234-5678-9010"
        (plaintext!)
                                    │
                                    ├─ Vault sees plaintext ❌
                                    ├─ Vault employees can access ❌
                                    ├─ Vault breach = all data ❌
                                    ├─ Compliance nightmare ❌
                                    │
                                    ↓
                                DATABASE
```

#### ✅ ECDH Vault (Good)

```
CLIENT ──────────────────────────► VAULT
        "x7K9mP2qL8vN4jR6..."
        (already encrypted!)
                                    │
                                    ├─ Vault CANNOT see plaintext ✅
                                    ├─ Zero-knowledge architecture ✅
                                    ├─ Breach protection ✅
                                    ├─ Compliance friendly ✅
                                    │
                                    ↓
                                DATABASE

Vault can only decrypt WITH client's cooperation
(needs PC from certificate)
```

---

### Security Benefits Summary

| Feature | Simple Vault | ECDH Vault |
|---------|-------------|-----------|
| **Vault sees plaintext** | ❌ Yes | ✅ No |
| **Client controls keys** | ❌ No | ✅ Yes |
| **Vault breach impact** | ❌ All data exposed | ✅ Data stays encrypted |
| **Insider threat** | ❌ Employees can access | ✅ Cannot access without client key |
| **Compliance (PCI-DSS, GDPR)** | ❌ Difficult | ✅ Easier |
| **Multi-tenant security** | ❌ Shared risk | ✅ Isolated per tenant |
| **Perfect forward secrecy** | ❌ No | ✅ Yes (with ephemeral keys) |

---

## Part 6: Real-World Implementation

Let's walk through a complete real-world example: credit card tokenization for e-commerce.

### The Scenario

**Players:**
1. **E-commerce Application** (Client) - Your online store
2. **Vault Service** - Tokenization service
3. **Payment Processor** (Bearer) - Stripe, PayPal, etc.

**Goal:** Store credit card securely, process payments later

---

### Implementation: Step-by-Step

#### Step 1: Initial Setup

```java
// E-commerce application startup
public class PaymentService {
    private final VaultClient vaultClient;
    private final KeyPairProvider keyProvider;
    
    public void initialize() {
        // Generate or load client's key pair
        PrivateKey clientPrivate = keyProvider.getPrivateKey();
        PublicKey clientPublic = keyProvider.getPublicKey();
        X509Certificate clientCert = keyProvider.getCertificate();
        
        // Get vault's public key
        PublicKeyResponse vaultKey = vaultClient.getPublicKey();
        // Returns: {publicKey: "PV_base64", keyID: "vault-001"}
        
        // Get payment processor's public key from registry
        String bearerPublicKey = keyRegistry.getKey("stripe-processor");
    }
}
```

#### Step 2: Customer Checkout (Token Generation)

```java
public class CheckoutController {
    
    @PostMapping("/checkout")
    public CheckoutResponse checkout(@RequestBody CheckoutRequest request) {
        // 1. Customer submits credit card
        String creditCard = request.getCreditCardNumber();
        // "4532-1234-5678-9010"
        
        // 2. Get vault's public key
        PublicKeyResponse vaultKey = vaultClient.getPublicKey();
        
        // 3. Get payment processor's public key
        String bearerPublicKey = keyRegistry.getKey("stripe");
        
        // 4. Generate token
        Token token = tokenService.generateToken(
            vaultKey,
            creditCard,
            bearerPublicKey,
            tenantId
        );
        
        // 5. Store token (NOT credit card!) in database
        Order order = new Order();
        order.setId(UUID.randomUUID().toString());
        order.setCustomerId(request.getCustomerId());
        order.setAmount(request.getAmount());
        order.setPaymentToken(token.getJws());  // Store JWS
        orderRepository.save(order);
        
        // 6. Send token to vault for storage
        String tokenId = vaultClient.storeToken(token);
        order.setVaultTokenId(tokenId);
        orderRepository.save(order);
        
        // 7. FORGET the credit card number!
        creditCard = null;  // Now impossible to access original card
        
        return new CheckoutResponse(order.getId(), "Order placed successfully");
    }
}
```

#### Step 3: Token Generation Implementation

```java
@Service
public class TokenServiceImpl implements TokenService {
    
    @Override
    public CompletionStage<Token> generateToken(
        PublicKeyResponse vaultPublicKey,
        String data,
        String bearerPublicKey,
        Long tenantId
    ) {
        // Validate inputs
        validateInputs(bearerPublicKey, data, tenantId);
        
        Token token = new Token();
        
        // Attach client's certificate chain
        token.setSourceCertificate(
            sourceKeyPairProvider.getCertificateChain(tenantId)
        );
        
        // Generate random IV for AES-GCM
        byte[] iv = CipherUtils.generateIVForAESGCM();
        // Result: [a3, f9, c2, d1, 7e, 4b, 8f, 2a, 5c, 6d, 1e, 9b]
        
        // ECDH Key Agreement
        SecretKey secretKey = CipherUtils.generateECDHSecretKeyWithSha256(
            sourceKeyPairProvider.getPrivateKey(tenantId),  // Client's Kc
            ClientKeyPair.getECPublicKeyFromBytes(
                Base64.getDecoder().decode(vaultPublicKey.getPublicKey())
            )  // Vault's PV
        );
        // Result: 32-byte AES key
        
        // Encrypt data with AES-256-GCM
        byte[] encryptedBytes = CipherUtils.encryptDataAESGCM(
            data.getBytes(),      // "4532-1234-5678-9010"
            secretKey,             // From ECDH
            iv                     // Random IV
        );
        String encryptedDataBase64 = Base64.getEncoder()
            .encodeToString(encryptedBytes);
        token.setEncryptedBlockOfData(encryptedDataBase64);
        
        // Build metadata context
        DataContext dataContext = buildDataContext(
            encryptedDataBase64,
            iv,
            vaultPublicKey.getKeyID(),
            bearerPublicKey  // Payment processor's public key
        );
        
        // Sign the context with JWS (ES256)
        try {
            String jws = generateJWS(
                sourceKeyPairProvider.getPrivateKey(tenantId),
                objectMapper.writeValueAsString(dataContext),
                vaultPublicKey.getKeyID()
            );
            token.setJws(jws);
        } catch (JsonProcessingException e) {
            throw new CryptoException(ErrorCode.ERR_CRYPTO_0014, e);
        }
        
        return CompletableFuture.completedFuture(token);
    }
    
    private DataContext buildDataContext(
        String encryptedDataBase64,
        byte[] iv,
        String vaultKeyId,
        String bearerPublicKey
    ) {
        DataContext context = new DataContext();
        context.setVersion("1.0");
        context.setShaEncryptedBlockOfData(computeSHA256(encryptedDataBase64));
        
        DataContext.PayloadMetadata metadata = new DataContext.PayloadMetadata();
        metadata.setAlgorithm("AES-256-GCM");
        metadata.setIv(Base64.getEncoder().encodeToString(iv));
        metadata.setVaultKeyID(vaultKeyId);
        metadata.setBearerPublicKey(bearerPublicKey);
        
        context.setPayloadMetadata(metadata);
        return context;
    }
    
    private String generateJWS(PrivateKey privateKey, String payload, String keyId) {
        try {
            JWSSigner signer = new ECDSASigner((ECPrivateKey) privateKey);
            JWSObject jwsObject = new JWSObject(
                new JWSHeader.Builder(JWSAlgorithm.ES256)
                    .keyID(keyId)
                    .build(),
                new Payload(payload)
            );
            jwsObject.sign(signer);
            return jwsObject.serialize();
        } catch (JOSEException e) {
            throw new CryptoException(ErrorCode.ERR_CRYPTO_0015, e);
        }
    }
    
    private String computeSHA256(String dataBase64) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(Base64.getDecoder().decode(dataBase64));
            return Base64.getEncoder().encodeToString(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new CryptoException(ErrorCode.ERR_CRYPTO_0006, e);
        }
    }
}
```

#### Step 4: Payment Processing (Token Decryption)

```java
public class PaymentController {
    
    @PostMapping("/process-payment")
    public PaymentResponse processPayment(@RequestBody PaymentRequest request) {
        // 1. Retrieve order
        Order order = orderRepository.findById(request.getOrderId())
            .orElseThrow();
        
        // 2. Request decryption from vault
        DecryptResponse decryptResponse = vaultClient.requestDecryption(
            order.getVaultTokenId(),
            "stripe-processor"  // Bearer identifier
        );
        
        // 3. Decrypt the token
        String creditCard = tokenService.decryptToken(
            decryptResponse,
            tenantId
        ).toCompletableFuture().join();
        
        // 4. Process payment with payment processor
        PaymentResult result = stripeClient.charge(
            creditCard,
            order.getAmount(),
            order.getCurrency()
        );
        
        // 5. Clear credit card from memory
        creditCard = null;
        
        // 6. Update order status
        order.setPaymentStatus(result.getStatus());
        order.setTransactionId(result.getTransactionId());
        orderRepository.save(order);
        
        return new PaymentResponse(result);
    }
}
```

#### Step 5: Token Decryption Implementation

```java
@Service
public class TokenServiceImpl implements TokenService {
    
    @Override
    public CompletionStage<String> decryptToken(
        DecryptResponse decryptResponse,
        Long tenantId
    ) {
        // Validate inputs
        validateDecryptResponse(decryptResponse);
        
        try {
            // Extract client's public key from certificate
            List<X509Certificate> certificateChain = CertificateUtils
                .parseCertificateChain(decryptResponse.getPublicKeyCertificate());
            PublicKey clientPublicKey = CertificateUtils
                .extractPublicKeyFromLeafCertificate(certificateChain);
            
            // ECDH Key Agreement (reverse direction)
            SecretKey secretKey = CipherUtils.generateECDHSecretKeyWithSha256(
                sourceKeyPairProvider.getPrivateKey(tenantId),  // Vault's Kv
                clientPublicKey                                  // Client's PC
            );
            // Result: SAME 32-byte AES key as client computed!
            
            // Decrypt the data using AES-GCM
            byte[] encryptedData = Base64.getDecoder()
                .decode(decryptResponse.getEncryptedBlockOfData());
            byte[] iv = Base64.getDecoder()
                .decode(decryptResponse.getMetadata().getIv());
            
            byte[] decryptedBytes = CipherUtils.decryptDataAESGCM(
                encryptedData,
                secretKey,
                iv
            );
            
            return CompletableFuture.completedFuture(new String(decryptedBytes));
            
        } catch (Exception e) {
            throw new CryptoException(
                ErrorCode.ERR_CRYPTO_0009,
                "Failed to decrypt token using ECDH",
                e
            );
        }
    }
    
    private void validateDecryptResponse(DecryptResponse decryptResponse) {
        if (decryptResponse.getEncryptedBlockOfData() == null) {
            throw new CryptoException(
                ErrorCode.ERR_CRYPTO_0023,
                "Encrypted block of data is null"
            );
        }
        if (decryptResponse.getPublicKeyCertificate() == null) {
            throw new CryptoException(
                ErrorCode.ERR_CRYPTO_0024,
                "Public key certificate is null"
            );
        }
        if (decryptResponse.getMetadata() == null || 
            decryptResponse.getMetadata().getIv() == null) {
            throw new CryptoException(
                ErrorCode.ERR_CRYPTO_0025,
                "Metadata or IV is null"
            );
        }
    }
}
```

---

### Complete Data Flow Visualization

```
TIME: T0 - Customer Checkout
═══════════════════════════════════════════════════════════════════

┌──────────────┐
│   CUSTOMER   │
└──────────────┘
       │
       │ Enters credit card: "4532-1234-5678-9010"
       ↓
┌──────────────┐
│  E-COMMERCE  │
│     APP      │
└──────────────┘
       │
       │ 1. Get vault public key (PV)
       │ 2. Get bearer public key (PB)
       │ 3. Generate Token:
       │    - IV = random
       │    - SharedSecret = ECDH(Kc, PV)
       │    - Encrypted = AES-GCM(card, SharedSecret, IV)
       │    - JWS = ES256-Sign(metadata, Kc)
       │
       ↓
┌──────────────┐
│   DATABASE   │
│              │
│ Order:       │
│ - tokenId    │
│ - amount     │
│ - status     │
└──────────────┘
       │
       │ Token also sent to vault
       ↓
┌──────────────┐
│    VAULT     │
│              │
│ Stores:      │
│ - encrypted  │
│ - JWS        │
│ - cert       │
└──────────────┘

Credit card "4532-1234-5678-9010" is now FORGOTTEN ✅
Only encrypted token exists

═══════════════════════════════════════════════════════════════════
TIME: T1 - Payment Processing (Later)
═══════════════════════════════════════════════════════════════════

┌──────────────┐
│  E-COMMERCE  │
│     APP      │
└──────────────┘
       │
       │ Need to process payment for order
       │
       ↓
┌──────────────┐
│    VAULT     │
└──────────────┘
       │
       │ Request decryption with tokenId
       │
       ↓
┌──────────────┐
│    VAULT     │
│              │
│ 1. Extract PC from certificate
│ 2. SharedSecret = ECDH(Kv, PC)  ← SAME secret!
│ 3. Plaintext = AES-GCM-Decrypt(encrypted, SharedSecret, IV)
│
│ Returns: "4532-1234-5678-9010"
└──────────────┘
       │
       ↓
┌──────────────┐
│  E-COMMERCE  │
│     APP      │
└──────────────┘
       │
       │ Send to payment processor
       │
       ↓
┌──────────────┐
│   STRIPE     │
│   (Bearer)   │
└──────────────┘
       │
       │ Charge credit card
       │
       ↓
    SUCCESS ✅
```

---

## Conclusion: When to Use Each Approach

### Decision Matrix

| Scenario | Recommended Approach | Reason |
|----------|---------------------|--------|
| **Simple internal system** | Vault-managed encryption | Simpler, vault is trusted |
| **PCI-DSS compliance required** | ECDH + zero-knowledge | Client-side encryption mandatory |
| **Sensitive PII (healthcare, finance)** | ECDH + zero-knowledge | Regulatory requirements |
| **Multi-tenant SaaS** | ECDH + zero-knowledge | Tenant isolation critical |
| **High-value targets** | ECDH + zero-knowledge | Extra security layer |
| **Low-sensitivity data** | Vault-managed encryption | Cost/complexity not justified |
| **Legacy system migration** | Vault-managed encryption | Easier integration |

---

### Key Takeaways

1. **IV (Initialization Vector)**
   - Makes same plaintext produce different ciphertext
   - Must be unique and random
   - NOT secret, transmitted with ciphertext
   - Critical for AES-GCM security

2. **ECDH (Key Agreement)**
   - Two parties derive same secret without transmitting it
   - Based on elliptic curve mathematics
   - Much faster than RSA with smaller keys
   - Enables zero-knowledge architecture

3. **Digital Signatures (ES256/RS256)**
   - Proves authenticity (who created it)
   - Proves integrity (not tampered)
   - Does NOT provide confidentiality
   - Use ES256 (ECDSA) for modern systems

4. **Why ECDH Instead of Simple Vault**
   - Zero-knowledge: vault never sees plaintext
   - Client controls keys
   - Better compliance posture
   - Protection against insider threats
   - Vault breach doesn't expose data

5. **Bearer Public Key**
   - Stored as metadata, not used for initial encryption
   - Indicates who is authorized to access
   - Used when vault re-encrypts for bearer
   - Audit trail and access control

---

### Modern Cryptography Stack

```
┌─────────────────────────────────────────────────────────────┐
│                  RECOMMENDED STACK                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Key Agreement:    ECDH (Elliptic Curve Diffie-Hellman)   │
│  Curve:            P-256 (secp256r1) or Ed25519            │
│  Symmetric Cipher: AES-256-GCM                              │
│  Signatures:       ES256 (ECDSA with SHA-256)              │
│  Hashing:          SHA-256                                  │
│  Random:           SecureRandom (crypto-grade)              │
│                                                             │
│  Avoid:            RSA for encryption (legacy, slow)        │
│                    MD5, SHA-1 (broken)                      │
│                    ECB mode (insecure)                      │
│                    Predictable IVs (vulnerable)             │
└─────────────────────────────────────────────────────────────┘
```

---

### Further Reading

- [NIST SP 800-56A: Recommendation for Pair-Wise Key Establishment](https://csrc.nist.gov/publications/detail/sp/800-56a/rev-3/final)
- [RFC 7748: Elliptic Curves for Security](https://tools.ietf.org/html/rfc7748)
- [RFC 7519: JSON Web Token (JWT)](https://tools.ietf.org/html/rfc7519)
- [RFC 7515: JSON Web Signature (JWS)](https://tools.ietf.org/html/rfc7515)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

---

## About This Implementation

This article is based on a real production vault service implementation used for payment card tokenization. The architecture demonstrates industry best practices for:
- Zero-knowledge data storage
- PCI-DSS compliance
- Multi-tenant security
- Modern cryptographic standards

If you're building similar systems, consider this architecture as a starting point and adapt it to your specific security requirements and compliance needs.

---

**Questions or feedback?** Feel free to reach out or leave a comment below!