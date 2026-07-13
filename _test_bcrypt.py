import bcrypt

# Reproduce passlib's detect_wrap_bug exact scenario
secret = (b"0123456789" * 26)[:255]
print("secret length:", len(secret))

bug_hash = b"$2a$04$R1lJ2gkNaoPGdafE.H.16.nVyh2niHsGJhayOHLMiXlI45o8/DU.6"
print("bug_hash:", bug_hash)

try:
    result = bcrypt.hashpw(secret, bug_hash)
    print("OK:", result)
except Exception as e:
    print("FAIL:", type(e).__name__, ":", e)

correct_hash = b"$2a$04$R1lJ2gkNaoPGdafE.H.16.1MKHPvmKwryeulRe225LKProWYwt9Oi"
try:
    result2 = bcrypt.hashpw(secret, correct_hash)
    print("Correct OK:", result2)
except Exception as e:
    print("Correct FAIL:", type(e).__name__, ":", e)
