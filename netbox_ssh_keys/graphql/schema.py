import strawberry
import strawberry_django

from .. import models
from . import types
from .filters import SSHKeyFilter


@strawberry.type(name='SSHKeysQuery')
class SSHKeysQuery:
    ssh_key: types.SSHKeyType = strawberry_django.field()
    ssh_key_list: list[types.SSHKeyType] = strawberry_django.field(filters=SSHKeyFilter, pagination=True)

    @strawberry.field(description='Flat list of authorized_keys-formatted lines')
    def ssh_key_authorized_keys_lines(self, tenant_slug: str | None = None) -> list[str]:
        queryset = models.SSHKey.objects.all().order_by('name')
        if tenant_slug:
            queryset = queryset.filter(tenant__slug=tenant_slug)
        return [ssh_key.authorized_keys_line for ssh_key in queryset]


schema = [SSHKeysQuery]
