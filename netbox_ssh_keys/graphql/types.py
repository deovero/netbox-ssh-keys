from typing import Annotated, TYPE_CHECKING

import strawberry
import strawberry_django

from netbox.graphql.types import NetBoxObjectType

from .. import models
from .filters import SSHKeyFilter

if TYPE_CHECKING:
    from tenancy.graphql.types import TenantType

__all__ = (
    'SSHKeyType',
)


@strawberry_django.type(
    models.SSHKey,
    fields='__all__',
    filters=SSHKeyFilter,
    pagination=True,
)
class SSHKeyType(NetBoxObjectType):
    tenant: Annotated['TenantType', strawberry.lazy('tenancy.graphql.types')] | None

    @strawberry.field(description='Full authorized_keys line')
    def authorized_keys_line(self) -> str:
        return f'{self.key_type} {self.public_key} {self.name}'
