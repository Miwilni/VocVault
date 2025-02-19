import hashlib
def generate_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()
#hash1 = generate_hash("Hello World")
#hash2 = generate_hash("Hello World")
#print(hash1==hash2)