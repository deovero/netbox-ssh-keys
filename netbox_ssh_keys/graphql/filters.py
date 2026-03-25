from typing import Annotated, TYPE_CHECKING

import strawberry
import strawberry_django
from strawberry import ID
from strawberry_django import StrFilterLookup

from netbox.graphql.filters import NetBoxModelFilter

from netbox_ssh_keys import models

if TYPE_CHECKING:
    from tenancy.graphql.filters import TenantFilter

__all__ = (
    'SSHKeyFilter',
)


@strawberry_django.filter_type(models.SSHKey, lookups=True)
class SSHKeyFilter(NetBoxModelFilter):
    name: StrFilterLookup | None = strawberry_django.filter_field()
    key_type: StrFilterLookup | None = strawberry_django.filter_field()
    public_key: StrFilterLookup | None = strawberry_django.filter_field()
    fingerprint: StrFilterLookup | None = strawberry_django.filter_field()
    tenant: Annotated['TenantFilter', strawberry.lazy('tenancy.graphql.filters')] | None = (
        strawberry_django.filter_field()
    )
    tenant_id: ID | None = strawberry_django.filter_field()
