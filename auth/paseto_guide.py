import os
from datetime import datetime, timedelta, timezone
from pyseto import Pyseto, Key, Token

"""
PASETO (Platform-Agnostic Security Tokens) Guide
----------------------------------------------
PASETO is a more secure alternative to JWT. It eliminates "algorithm: none" 
vulnerabilities and provides safe defaults.

Version: v4 (Recommended)
Purpose: local (symmetric) or public (asymmetric)

Installation:
    pip install pyseto
"""

# --- 1. SYMMETRIC ENCRYPTION (v4.local) ---
# Use this when the same server issues and validates the token.
def demo_symmetric():
    print("--- Symmetric (v4.local) Demo ---")
    
    # Generate or load a 32-byte key
    # In production, store this in an environment variable
    secret_key = os.urandom(32) 
    key = Key.new(version=4, purpose="local", key=secret_key)
    
    # Payload (Claims)
    payload = {
        "sub": "user_123",
        "name": "Nabin Hamal",
        "iat": datetime.now(timezone.utc).isoformat(),
        "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
    }
    
    # 1. Issue Token
    token = Pyseto.encode(key, payload)
    print(f"Issued Token: {token.decode()[:40]}...")
    
    # 2. Verify and Decode
    decoded = Pyseto.decode(key, token)
    print(f"Decoded Payload: {decoded.payload}")
    print("\n")

# --- 2. ASYMMETRIC SIGNATURES (v4.public) ---
# Use this when one server issues (Private Key) and others validate (Public Key).
def demo_asymmetric():
    print("--- Asymmetric (v4.public) Demo ---")
    
    # Generate Ed25519 Key Pair
    # In production, use file-based keys (PEM/DER)
    from cryptography.hazmat.primitives.asymmetric import ed25519
    priv_key_obj = ed25519.Ed25519PrivateKey.generate()
    pub_key_obj = priv_key_obj.public_key()
    
    # Wrap in Pyseto Key objects
    signing_key = Key.from_asymmetric_key(priv_key_obj)
    verifying_key = Key.from_asymmetric_key(pub_key_obj)
    
    # Payload
    payload = {
        "sub": "admin_456",
        "role": "admin",
        "iat": datetime.now(timezone.utc).isoformat(),
    }
    
    # 1. Sign Token
    token = Pyseto.encode(signing_key, payload)
    print(f"Signed Token: {token.decode()[:40]}...")
    
    # 2. Verify Signature
    decoded = Pyseto.decode(verifying_key, token)
    print(f"Verified Payload: {decoded.payload}")
    print("\n")

if __name__ == "__main__":
    try:
        demo_symmetric()
        demo_asymmetric()
    except ImportError:
        print("Error: 'pyseto' not found. Please run 'pip install pyseto'")
    except Exception as e:
        print(f"An error occurred: {e}")
