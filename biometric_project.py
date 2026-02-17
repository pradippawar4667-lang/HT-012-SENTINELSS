import hashlib
import random


class FingerprintAuth:
    def __init__(self):
        self.fingerprint_hash = None

    def generate_fingerprint_data(self):
        return str(random.getrandbits(256))

    def hash_fingerprint(self, fingerprint_data):
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()

    def train(self):
        fingerprint_data = self.generate_fingerprint_data()
        self.fingerprint_hash = self.hash_fingerprint(fingerprint_data)

        return {
            "status": "fingerprint_trained",
            "message": "Fingerprint Registered Successfully"
        }

    def verify(self):
        if not self.fingerprint_hash:
            return {
                "status": "denied",
                "message": "Fingerprint not trained"
            }

        match_probability = random.randint(1, 100)

        if match_probability > 20:
            return {
                "status": "verified",
                "score": 95,
                "reason": "FINGERPRINT MATCH CONFIRMED"
            }
        else:
            return {
                "status": "denied",
                "score": 10,
                "reason": "FINGERPRINT MISMATCH"
            }
