from app.core.security import hash_password, verify_password


def test_hash_password_does_not_return_plaintext() -> None:
    password = "StrongPassword123!"

    encoded_hash = hash_password(password)

    assert encoded_hash != password
    assert encoded_hash.startswith("$argon2")


def test_verify_password_accepts_correct_password() -> None:
    password = "StrongPassword123!"
    encoded_hash = hash_password(password)

    assert verify_password(password, encoded_hash) is True


def test_verify_password_rejects_incorrect_password() -> None:
    encoded_hash = hash_password("StrongPassword123!")

    assert verify_password("WrongPassword123!", encoded_hash) is False
