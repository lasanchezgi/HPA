from src.infrastructure.security.password_hasher import PasswordHasher


def test_hash_returns_different_string_than_plain():
    hasher = PasswordHasher()
    hashed = hasher.hash("mypassword")
    assert hashed != "mypassword"


def test_verify_correct_password_returns_true():
    hasher = PasswordHasher()
    hashed = hasher.hash("correcthorse")
    assert hasher.verify("correcthorse", hashed) is True


def test_verify_wrong_password_returns_false():
    hasher = PasswordHasher()
    hashed = hasher.hash("correcthorse")
    assert hasher.verify("wrongpassword", hashed) is False


def test_two_hashes_of_same_password_are_different():
    hasher = PasswordHasher()
    h1 = hasher.hash("samepassword")
    h2 = hasher.hash("samepassword")
    assert h1 != h2
