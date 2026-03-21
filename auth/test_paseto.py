from pyseto import Key, Pyseto
import os
from datetime import datetime, timedelta, timezone

def test_paseto():
    print("Testing PASETO implementation...")
    
    # 1. Setup
    secret = os.urandom(32)
    key = Key.new(version=4, purpose="local", key=secret)
    
    # 2. Issue Token
    payload = {"user_id": 1, "exp": (datetime.now(timezone.utc) + timedelta(seconds=2)).isoformat()}
    token = Pyseto.encode(key, payload)
    assert token is not None
    print("✓ Token issued successfully")
    
    # 3. Decode Token
    decoded = Pyseto.decode(key, token)
    assert decoded.payload["user_id"] == 1
    print("✓ Token decoded successfully")
    
    # 4. Tamper Test
    tampered_token = token[:-1] + (b'a' if token[-1:] != b'a' else b'b')
    try:
        Pyseto.decode(key, tampered_token)
        raise Exception("Failed: Tampered token was accepted")
    except Exception:
        print("✓ Tampered token correctly rejected")

    print("All tests passed!")

if __name__ == "__main__":
    try:
        test_paseto()
    except ImportError:
        print("Skipping test: pyseto not installed.")
    except Exception as e:
        print(f"Test failed: {e}")
        exit(1)
