import hashlib as h
import json 


def hashblock(req):
    """
    This function takes a request object as input and returns a hash of the request object as a string.

    Parameters:
        req (dict): The request object to be hashed.

    Returns:
        str: The hash of the request object as a string.

    """
    encoded_block = json.dumps(req, sort_keys = True).encode()
    block_encryption =h.sha256() 
    block_encryption.update((encoded_block)) 
    return block_encryption.hexdigest()
