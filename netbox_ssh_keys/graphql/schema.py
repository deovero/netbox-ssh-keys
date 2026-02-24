import strawberry
import strawberry_django

from . import types


@strawberry.type(name='SSHKeysQuery')
class SSHKeysQuery:
    ssh_key: types.SSHKeyType = strawberry_django.field()
    ssh_key_list: list[types.SSHKeyType] = strawberry_django.field()


schema = [SSHKeysQuery]
