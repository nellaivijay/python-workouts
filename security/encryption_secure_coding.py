"""
Security - Encryption, Secure Coding, and Authentication Examples
"""

import hashlib
import secrets
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import warnings
warnings.filterwarnings('ignore')


# Encryption Examples
def symmetric_encryption_example():
    """Demonstrate symmetric encryption with Fernet"""
    print("Symmetric Encryption (Fernet):")
    
    # Generate key
    key = Fernet.generate_key()
    fernet = Fernet(key)
    
    # Encrypt message
    message = "This is a secret message"
    encrypted = fernet.encrypt(message.encode())
    print(f"  Original: {message}")
    print(f"  Encrypted: {encrypted}")
    
    # Decrypt message
    decrypted = fernet.decrypt(encrypted).decode()
    print(f"  Decrypted: {decrypted}")


def hash_examples():
    """Demonstrate various hashing algorithms"""
    print("\nHashing Examples:")
    
    message = "Secure password"
    
    # MD5 (not recommended for security)
    md5_hash = hashlib.md5(message.encode()).hexdigest()
    print(f"  MD5: {md5_hash}")
    
    # SHA-256 (recommended)
    sha256_hash = hashlib.sha256(message.encode()).hexdigest()
    print(f"  SHA-256: {sha256_hash}")
    
    # SHA-512
    sha512_hash = hashlib.sha512(message.encode()).hexdigest()
    print(f"  SHA-512: {sha512_hash}")


def password_hashing_example():
    """Demonstrate secure password hashing with salt"""
    print("\nSecure Password Hashing:")
    
    password = "my_secure_password"
    
    # Generate salt
    salt = secrets.token_hex(16)
    print(f"  Salt: {salt}")
    
    # Hash password with salt
    salted_password = password + salt
    hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
    print(f"  Hashed password: {hashed_password}")
    
    # Verify password
    def verify_password(input_password, stored_hash, salt):
        salted_input = input_password + salt
        input_hash = hashlib.sha256(salted_input.encode()).hexdigest()
        return input_hash == stored_hash
    
    is_valid = verify_password(password, hashed_password, salt)
    print(f"  Password verification: {is_valid}")


def key_derivation_example():
    """Demonstrate key derivation from password"""
    print("\nKey Derivation (PBKDF2):")
    
    password = b"my_secure_password"
    salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password))
    print(f"  Derived key: {key}")


# Secure Coding Examples
def secure_random_example():
    """Demonstrate secure random number generation"""
    print("\nSecure Random Generation:")
    
    # Cryptographically secure random bytes
    secure_bytes = secrets.token_bytes(16)
    print(f"  Secure bytes: {secure_bytes.hex()}")
    
    # Secure random token
    secure_token = secrets.token_urlsafe(16)
    print(f"  Secure token: {secure_token}")
    
    # Secure random number within range
    secure_number = secrets.randbelow(100)
    print(f"  Secure number (0-99): {secure_number}")


def input_validation_example():
    """Demonstrate input validation"""
    print("\nInput Validation:")
    
    def validate_email(email: str) -> bool:
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(password: str) -> tuple:
        """Password strength validation"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not any(c.isupper() for c in password):
            return False, "Password must contain uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Password must contain lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain digit"
        return True, "Password is valid"
    
    # Test email validation
    emails = ["valid@example.com", "invalid-email", "test@test"]
    for email in emails:
        is_valid = validate_email(email)
        print(f"  {email}: {'Valid' if is_valid else 'Invalid'}")
    
    # Test password validation
    passwords = ["weak", "StrongPass123", "nouppercase123"]
    for password in passwords:
        is_valid, message = validate_password(password)
        print(f"  '{password}': {message}")


def sql_injection_prevention():
    """Demonstrate SQL injection prevention"""
    print("\nSQL Injection Prevention:")
    
    # Vulnerable example (DON'T DO THIS)
    def vulnerable_query(user_input):
        return f"SELECT * FROM users WHERE name = '{user_input}'"
    
    # Secure example with parameterized queries
    def secure_query(user_input):
        return "SELECT * FROM users WHERE name = ?", (user_input,)
    
    malicious_input = "admin' OR '1'='1"
    
    print(f"  Vulnerable query: {vulnerable_query(malicious_input)}")
    print(f"  Secure query: {secure_query(malicious_input)}")


# Authentication Examples
class SimpleAuth:
    """Simple authentication system"""
    
    def __init__(self):
        self.users = {}
        self.sessions = {}
    
    def register(self, username: str, password: str):
        """Register a new user"""
        if username in self.users:
            return False, "Username already exists"
        
        # Hash password with salt
        salt = secrets.token_hex(16)
        salted_password = password + salt
        hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        
        self.users[username] = {
            'salt': salt,
            'hashed_password': hashed_password
        }
        return True, "User registered successfully"
    
    def login(self, username: str, password: str):
        """Authenticate user"""
        if username not in self.users:
            return False, "User not found"
        
        user_data = self.users[username]
        salted_password = password + user_data['salt']
        input_hash = hashlib.sha256(salted_password.encode()).hexdigest()
        
        if input_hash == user_data['hashed_password']:
            # Create session token
            session_token = secrets.token_urlsafe(32)
            self.sessions[session_token] = username
            return True, session_token
        else:
            return False, "Invalid password"
    
    def verify_session(self, session_token: str):
        """Verify session token"""
        return self.sessions.get(session_token) is not None


def authentication_example():
    """Demonstrate authentication system"""
    print("\nAuthentication System:")
    
    auth = SimpleAuth()
    
    # Register users
    success, message = auth.register("alice", "SecurePass123")
    print(f"  Register alice: {message}")
    
    success, message = auth.register("bob", "AnotherSecure456")
    print(f"  Register bob: {message}")
    
    # Login attempts
    success, result = auth.login("alice", "SecurePass123")
    print(f"  Login alice (correct): {result if success else message}")
    
    success, message = auth.login("alice", "wrongpassword")
    print(f"  Login alice (wrong): {message}")
    
    success, result = auth.login("charlie", "password")
    print(f"  Login charlie (nonexistent): {message}")


def xss_prevention():
    """Demonstrate XSS prevention"""
    print("\nXSS Prevention:")
    
    import html
    
    user_input = "<script>alert('XSS')</script>"
    
    # Unsafe (vulnerable to XSS)
    unsafe_output = f"<div>{user_input}</div>"
    print(f"  Unsafe: {unsafe_output}")
    
    # Safe (escaped)
    safe_output = f"<div>{html.escape(user_input)}</div>"
    print(f"  Safe: {safe_output}")


def main():
    """Main function to demonstrate security concepts"""
    print("Security Examples")
    print("=" * 50)
    
    # Encryption examples
    symmetric_encryption_example()
    hash_examples()
    password_hashing_example()
    key_derivation_example()
    
    # Secure coding examples
    secure_random_example()
    input_validation_example()
    sql_injection_prevention()
    xss_prevention()
    
    # Authentication examples
    authentication_example()
    
    print("\n" + "=" * 50)
    print("Security Key Concepts:")
    print("✓ Encryption: Protect sensitive data at rest")
    print("✓ Hashing: Verify data integrity, password storage")
    print("✓ Salting: Prevent rainbow table attacks")
    print("✓ Key Derivation: Generate keys from passwords")
    print("✓ Secure Random: Cryptographically secure randomness")
    print("✓ Input Validation: Prevent injection attacks")
    print("✓ Authentication: Secure user login systems")
    print("✓ XSS Prevention: Escape user-generated content")
    print("\nBest Practices:")
    print("• Never store passwords in plain text")
    print("• Always use parameterized queries")
    print("• Validate and sanitize all user input")
    print("• Use HTTPS for data transmission")
    print("• Keep security libraries updated")
    print("\nTo run this script:")
    print("pip install cryptography")


if __name__ == "__main__":
    main()