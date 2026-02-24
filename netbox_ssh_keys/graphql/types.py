import strawberry
import strawberry_django

from netbox.graphql.types import NetBoxObjectType

from .. import models


@strawberry_django.type(models.SSHKey, fields='__all__')
class SSHKeyType(NetBoxObjectType):

    @strawberry.field(description='Full authorized_keys line')
    def authorized_keys_line(self) -> str:
        return f'{self.key_type} {self.public_key} {self.name}'
