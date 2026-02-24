import base64
import hashlib


# All recognized SSH public key algorithm identifiers
VALID_KEY_TYPES = {
    'ssh-rsa',
    'ssh-ed25519',
    'ecdsa-sha2-nistp256',
    'ecdsa-sha2-nistp384',
    'ecdsa-sha2-nistp521',
    'sk-ssh-ed25519@openssh.com',
    'sk-ecdsa-sha2-nistp256@openssh.com',
    'ssh-dss',
}


def parse_ssh_public_key(line):
    """
    Parse an authorized_keys line into its components.

    Returns a dict with 'key_type', 'public_key', and 'comment' keys,
    or None if the line is empty or a comment.

    Raises ValueError if the line cannot be parsed.
    """
    line = line.strip()
    if not line or line.startswith('#'):
        return None

    parts = line.split(None, 2)
    if len(parts) < 2:
        raise ValueError(f'Invalid SSH public key format: {line[:80]}')

    key_type = parts[0]
    public_key = parts[1]
    comment = parts[2] if len(parts) > 2 else ''

    if key_type not in VALID_KEY_TYPES:
        raise ValueError(f'Unknown SSH key type: {key_type}')

    try:
        base64.b64decode(public_key, validate=True)
    except Exception:
        raise ValueError('Invalid base64-encoded public key material')

    return {
        'key_type': key_type,
        'public_key': public_key,
        'comment': comment,
    }


def calculate_fingerprint(public_key_b64):
    """
    Calculate the SHA256 fingerprint of a base64-encoded SSH public key.

    Returns a string in the format ``SHA256:<base64_hash>`` (matching
    ``ssh-keygen -l`` output).
    """
    key_bytes = base64.b64decode(public_key_b64)
    digest = hashlib.sha256(key_bytes).digest()
    fingerprint_b64 = base64.b64encode(digest).rstrip(b'=').decode('ascii')
    return f'SHA256:{fingerprint_b64}'
