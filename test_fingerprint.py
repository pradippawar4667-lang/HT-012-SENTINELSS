from biometric_project import FingerprintAuth

# Object create
fp = FingerprintAuth()

print("1) VERIFY BEFORE TRAIN")
print(fp.verify())

print("\n2) TRAINING")
print(fp.train())

print("\n3) VERIFY AFTER TRAIN")
print(fp.verify())
