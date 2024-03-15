import hashlib

def sha1_digest_bytes(data) -> str:
    return hashlib.sha1(data).hexdigest()

def sha1_digest_file(filepath) -> str:
    with open(filepath, "rb") as opened_file:
        return sha1_digest_bytes(opened_file.read())