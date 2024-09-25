import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
import base64

def extract_public_key(private_key_pem):
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem.decode()

def verify_token_manually(token, public_key_pem):
    header, payload, signature = token.split('.')
    message = f"{header}.{payload}"
    
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode(),
        backend=default_backend()
    )
    
    try:
        public_key.verify(
            base64.urlsafe_b64decode(signature + "=="),
            message.encode(),
            ec.ECDSA(ec.SHA256())
        )
        return True
    except:
        return False

private_key_pem = """-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIMN6kbeP011DGZ/N0mbEToX2vFSlw4cf+yK8DTO7VGOSoAoGCCqGSM49
AwEHoUQDQgAEQMQcwI7nmmWmBRdrm+9geMDk9AFh0yiXINhDYl9Zhy4GbGLeinMa
iDLY6aQZLlQxk5vSG0WVB6NvA3mQAAGW0w==
-----END EC PRIVATE KEY-----"""

token = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2aXNpdG9ySWQiOiJ0ZXN0eSIsInNpdGVJZCI6IjQ0NzAyOGZjLThmMDUtNGNhNS05MmY4LWIxYzdiYjFlMjkyZiIsImxvb2t1cF9pZCI6InRlc3R5IiwiZW1haWwiOiJ0ZXN0eUBtYWlsaW5hdG9yLmNvbSIsImV4cCI6MTcyNzE3MDY1OCwiaWF0IjoxNzI3MTcwMzU4fQ.Q61mzwBpnLUHcdZrN0xviuNQekWJyalQuAPdLKyX0qsDfCNcmMDDzsyDVWDQx0wqrhLsmeONEW1LpohTVhYUCg"

public_key_pem = extract_public_key(private_key_pem)
print("Public Key (SPKI format):")
print(public_key_pem)

print("\nVerifying token using PyJWT:")
try:
    decoded = jwt.decode(token, public_key_pem, algorithms=['ES256'])
    print("Token is valid!")
    print("Payload:", decoded)
except jwt.ExpiredSignatureError:
    print("Token has expired")
except jwt.InvalidSignatureError:
    print("Invalid signature")
except Exception as e:
    print("Error:", str(e))

print("\nVerifying token manually:")
if verify_token_manually(token, public_key_pem):
    print("Token signature is valid!")
else:
    print("Token signature is invalid!")

# Print token parts for inspection
print("\nToken parts:")
header, payload, signature = token.split('.')
print("Header:", base64.urlsafe_b64decode(header + "==").decode())
print("Payload:", base64.urlsafe_b64decode(payload + "==").decode())