import hashlib
import bcrypt

def generate_normal_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def generate_secure_hash(data: str) -> str:
    return bcrypt.hashpw(data.encode(), bcrypt.gensalt()).decode()

def verify_secure_hash(input_data, stored_hash):
    return bcrypt.checkpw(input_data.encode(), stored_hash.encode())