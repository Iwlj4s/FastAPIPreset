from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""
Password hashing and verification utilities.
Uses bcrypt for secure password handling.
"""

def hash_password(plain_password: str):
    """
    Hash plain text password using bcrypt.
    
    :param plain_password: Original password text
    :return: Hashed password string
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str):
    """
    Verify plain password against hashed password.
    
    :param plain_password: Password to verify
    :param hashed_password: Stored hashed password
    :return: Boolean indicating password match
    """
    return pwd_context.verify(plain_password, hashed_password)