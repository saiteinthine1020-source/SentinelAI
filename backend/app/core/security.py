from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plaintext password using the configured secure algorithm."""

    return password_hash.hash(password)


def verify_password(password: str, encoded_hash: str) -> bool:
    """Verify a plaintext password against an encoded password hash."""

    return password_hash.verify(password, encoded_hash)
