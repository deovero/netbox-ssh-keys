from utilities.choices import ChoiceSet


class SSHKeyTypeChoices(ChoiceSet):
    """SSH public key algorithm types."""

    key = 'SSHKey.key_type'

    TYPE_RSA = 'ssh-rsa'
    TYPE_ED25519 = 'ssh-ed25519'
    TYPE_ECDSA_P256 = 'ecdsa-sha2-nistp256'
    TYPE_ECDSA_P384 = 'ecdsa-sha2-nistp384'
    TYPE_ECDSA_P521 = 'ecdsa-sha2-nistp521'
    TYPE_SK_ED25519 = 'sk-ssh-ed25519@openssh.com'
    TYPE_SK_ECDSA = 'sk-ecdsa-sha2-nistp256@openssh.com'

    CHOICES = [
        (TYPE_RSA, 'RSA'),
        (TYPE_ED25519, 'Ed25519'),
        (TYPE_ECDSA_P256, 'ECDSA (nistp256)'),
        (TYPE_ECDSA_P384, 'ECDSA (nistp384)'),
        (TYPE_ECDSA_P521, 'ECDSA (nistp521)'),
        (TYPE_SK_ED25519, 'Ed25519-SK'),
        (TYPE_SK_ECDSA, 'ECDSA-SK'),
    ]
