---
layout: blog-post
title: "Envelope encryption with vault"
excerpt: "Envelope encryption with vault"
disqus_id: /2026/10/01/envelope-encryption-with-vault/
tags:
    - Vault
---

> **Disclaimer**: This blog article has been generated with the assistance of AI. While the content is AI-generated, the software itself and the ideas behind it are the result of real development work and genuine user needs.


## The Problem

Encrypting data directly with a master key stored in an HSM or KMS creates three issues:

1. **Performance**: Every encryption operation requires a network call to the HSM/KMS
2. **Key rotation**: Rotating the master key means re-encrypting all data
3. **Blast radius**: Compromised master key exposes all encrypted data

Envelope encryption solves these problems by introducing a two-tier key hierarchy.

## How Envelope Encryption Works

Data is encrypted with a Data Encryption Key (DEK), then the DEK is encrypted with a master Key Encryption Key (KEK).

```
┌─────────────────┐
│   Your Data     │
└────────┬────────┘
         │ Encrypted with
         ▼
┌─────────────────┐
│  Data Key (DEK) │  ← Generated per encryption operation
└────────┬────────┘
         │ Encrypted with
         ▼
┌─────────────────┐
│ Master Key (KEK)│  ← Lives in Vault/HSM
└─────────────────┘
```

The ciphertext contains both the encrypted data and the encrypted DEK bundled together.

### Setting Up Vault Transit Engine

```bash
# Enable Transit engine
vault secrets enable transit

# Create an encryption key
vault write -f transit/keys/customer-data
```

### Encryption Process

Encrypt data with Vault:

```bash
vault write transit/encrypt/customer-data \
  plaintext=$(echo "SSN: 123-45-6789" | base64)
```

Vault internally:
1. Generates a unique DEK (256-bit AES key)
2. Encrypts data with DEK using AES-256-GCM
3. Encrypts DEK with master key
4. Returns bundled ciphertext

Response:

```
vault:v1:8SDd3WHDOjf7mq69CylmKFRZnViXf4...
```

Format:
- `vault:` - Identifier
- `v1:` - Key version
- Encrypted data + encrypted DEK

### Decryption Process

```bash
vault write transit/decrypt/customer-data \
  ciphertext="vault:v1:8SDd3WHDOjf7mq69CylmKFRZnViXf4..."
```

Vault:
1. Extracts encrypted DEK from ciphertext
2. Decrypts DEK with master key
3. Decrypts data with DEK
4. Returns plaintext
5. Discards DEK

## Key Rotation

Rotate the master key:

```bash
vault write -f transit/keys/customer-data/rotate
```

No data re-encryption needed. The data remains encrypted with the same DEKs. Only the DEK wrappers need updating.

Rewrap ciphertext with new key version:

```bash
vault write transit/rewrap/customer-data \
  ciphertext="vault:v1:8SDd3WHDOjf7mq69CylmKFRZnViXf4..."
```

Result:

```
vault:v2:9TEe4XIEPkg8nr70DzmmlGSaOwhYg5...
```

Version changed from `v1` to `v2`. The underlying data wasn't touched—only the DEK wrapper was re-encrypted.

## Example: Database Field Encryption

```python
import hvac
import base64

client = hvac.Client(url='http://localhost:8200')
client.token = 'your-vault-token'

def encrypt_ssn(ssn):
    plaintext_b64 = base64.b64encode(ssn.encode()).decode()
    
    response = client.secrets.transit.encrypt_data(
        name='customer-data',
        plaintext=plaintext_b64
    )
    
    return response['data']['ciphertext']

def decrypt_ssn(ciphertext):
    response = client.secrets.transit.decrypt_data(
        name='customer-data',
        ciphertext=ciphertext
    )
    
    plaintext = base64.b64decode(response['data']['plaintext']).decode()
    return plaintext

# Usage
encrypted = encrypt_ssn("123-45-6789")
# Store in DB: vault:v1:8SDd3WHDOjf7...

original = decrypt_ssn(encrypted)
# Returns: "123-45-6789"
```

## Batch Operations

Encrypt multiple values in one API call:

```bash
vault write transit/encrypt/customer-data/batch \
  batch_input='[
    {"plaintext": "'"$(echo 'SSN: 123-45-6789' | base64)"'"},
    {"plaintext": "'"$(echo 'SSN: 987-65-4321' | base64)"'"}
  ]'
```

## Convergent Encryption

Enable convergent mode for deterministic encryption (same plaintext → same ciphertext):

```bash
vault write transit/keys/dedup-data \
  convergent_encryption=true \
  derived=true
```

Encrypt with context:

```bash
vault write transit/encrypt/dedup-data \
  plaintext=$(echo "duplicate-data" | base64) \
  context=$(echo "user-123" | base64)
```

Same plaintext with same context always produces the same ciphertext, enabling deduplication.

## Key Configuration Options

View key configuration:

```bash
vault read transit/keys/customer-data
```

Configure key parameters:

```bash
# Prevent old versions from being used for decryption
vault write transit/keys/customer-data/config \
  min_decryption_version=2

# Prevent old versions from being used for encryption
vault write transit/keys/customer-data/config \
  min_encryption_version=3

# Allow key deletion (disabled by default)
vault write transit/keys/customer-data/config \
  deletion_allowed=true
```

## Performance Comparison

**Direct master key encryption:**
- 1GB file encrypted via HSM: ~1000s of API calls
- Slow, expensive
- Key rotation: re-encrypt all data

**Envelope encryption:**
- 1GB file encrypted locally with DEK: fast
- Encrypt DEK via Vault: 1 API call
- Key rotation: rewrap DEKs only (no data re-encryption)

## Key Operations Reference

```bash
# Create key
vault write -f transit/keys/mykey

# Encrypt
vault write transit/encrypt/mykey plaintext=$(echo "data" | base64)

# Decrypt
vault write transit/decrypt/mykey ciphertext="vault:v1:..."

# Rotate key
vault write -f transit/keys/mykey/rotate

# Rewrap with latest key version
vault write transit/rewrap/mykey ciphertext="vault:v1:..."

# Read key info
vault read transit/keys/mykey

# Delete key (if deletion_allowed=true)
vault delete transit/keys/mykey

# List all keys
vault list transit/keys
```

## References

- [Vault Transit Engine Docs](https://developer.hashicorp.com/vault/docs/secrets/transit)
- [Encryption as a Service Tutorial](https://developer.hashicorp.com/vault/tutorials/encryption-as-a-service)
- [Transit API Reference](https://developer.hashicorp.com/vault/api-docs/secret/transit)