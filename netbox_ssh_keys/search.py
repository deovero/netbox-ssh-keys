from netbox.search import SearchIndex, register_search

from .models import SSHKey


@register_search
class SSHKeyIndex(SearchIndex):
    model = SSHKey
    fields = (
        ('name', 100),
        ('fingerprint', 80),
        ('authorized_keys_line', 60),
        ('description', 50),
    )
