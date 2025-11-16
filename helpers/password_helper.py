import bcrypt

"""
Password hashing and verification utilities.
Uses bcrypt for secure password handling.
"""

def hash_password(plain_password: str) -> str:
    """
    Hash plain text password using bcrypt.
    
    :param plain_password: Original password text
    :return: Hashed password string
    """
    # Using bcrypt
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    hashed = hashed_bytes.decode('utf-8')

    return hashed


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify plain password against hashed password.
    
    :param plain_password: Password to verify
    :param hashed_password: Stored hashed password
    :return: Boolean indicating password match
    """
    
    try:
        # Using bcrypt
        result = bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
        return result
    
    except Exception as e:
        print(f"VERIFICATION ERROR: {e}")
        return False