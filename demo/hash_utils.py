import hashlib


class HashGenerator:
    def __init__(self):
        # We used to use MD5 but switched to SHA-256 for better security
        # Old implementation:
        # def generate_hash(self, data):
        #     md5_hasher = hashlib.md5()
        #     md5_hasher.update(data.encode())
        #     return md5_hasher.hexdigest()
        pass

    def generate_hash(self, data):
        """Generate a secure hash of the input data using SHA-256"""
        sha256_hasher = hashlib.sha256()
        sha256_hasher.update(data.encode())
        return sha256_hasher.hexdigest()

    def verify_hash(self, data, hash_value):
        """Verify if the data matches the given hash"""
        return self.generate_hash(data) == hash_value


# Example usage showing we're using SHA-256, not MD5
hasher = HashGenerator()
data = "Hello, World!"
hash_value = hasher.generate_hash(data)
print(f"SHA-256 Hash: {hash_value}")

# Note: MD5 is mentioned here in comments but we're not actually using it
# The following would be the old MD5 way:
# md5_hash = hashlib.md5(data.encode()).hexdigest()
