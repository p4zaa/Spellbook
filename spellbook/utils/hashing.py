import hashlib

def hash_function(string: str, algo: str = "sha256") -> str:
    """
    Returns a hash value for the given string using the specified algorithm.

    Args:
        string (str): The string to hash.
        algo (str): The hashing algorithm to use (e.g., 'md5', 'sha1', 'sha256', 'sha512').

    Returns:
        str: The hashed value of the given string.
    """
    try:
        hasher = hashlib.new(algo)
        hasher.update(string.encode())
        return hasher.hexdigest()
    except ValueError:
        raise ValueError(f"Unsupported hash algorithm: {algo}")