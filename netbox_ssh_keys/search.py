from netbox.search import SearchIndex, register_search

from .models import SSHKey


@register_search
class SSHKeyIndex(SearchIndex):
    model = SSHKey
    fields = (
        ('name', 100),
        ('fingerprint', 80),
        ('public_key', 60),
        ('description', 50),
    )
