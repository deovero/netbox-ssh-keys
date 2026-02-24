import strawberry
import strawberry_django

from . import types
from .filters import SSHKeyFilter


@strawberry.type(name='SSHKeysQuery')
class SSHKeysQuery:
    ssh_key: types.SSHKeyType = strawberry_django.field()
    ssh_key_list: list[types.SSHKeyType] = strawberry_django.field(filters=SSHKeyFilter, pagination=True)


schema = [SSHKeysQuery]
