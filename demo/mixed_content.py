import hashlib
from dataclasses import dataclass

# This file contains both real crypto usage and potential false positives


@dataclass
class FortunaWheel:
    """A wheel of fortune game implementation"""

    segments: list
    current_position: int = 0

    def spin(self):
        """Spin the wheel of fortune"""
        import random

        self.current_position = random.randint(0, len(self.segments) - 1)
        return f"Fortuna's wheel lands on: {self.segments[self.current_position]}"


def calculate_hash(data):
    """Real crypto usage: Calculate SHA-256 hash"""
    # Note: We have an MD5 implementation but it's commented out for security reasons
    # md5_hash = hashlib.md5(data.encode()).hexdigest()

    # Using SHA-256 instead
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    return sha256.hexdigest()


# Game implementation using Fortuna theme (false positive)
wheel = FortunaWheel(
    ["Double Fortune", "Triple Luck", "Fortune's Favor", "Lady Fortuna's Blessing"]
)


# Real crypto usage mixed with game mechanics
def secure_spin(player_id):
    """Spin the wheel and record the result with a secure hash"""
    result = wheel.spin()
    # Hash the result for verification
    result_hash = calculate_hash(f"{player_id}:{result}")
    return {"result": result, "verification_hash": result_hash}


# Example usage
print("Welcome to Fortuna's Wheel of Fortune!")
result = secure_spin("player123")
print(f"Spin result: {result['result']}")
print(f"Verification hash: {result['verification_hash']}")
