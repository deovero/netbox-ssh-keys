from typing import Annotated, TYPE_CHECKING

import strawberry
import strawberry_django
from strawberry import ID
from strawberry_django import FilterLookup

from netbox.graphql.filters import NetBoxModelFilter

from netbox_ssh_keys import models

if TYPE_CHECKING:
    from tenancy.graphql.filters import TenantFilter

__all__ = (
    'SSHKeyFilter',
)


@strawberry_django.filter_type(models.SSHKey, lookups=True)
class SSHKeyFilter(NetBoxModelFilter):
    name: FilterLookup[str] | None = strawberry_django.filter_field()
    key_type: FilterLookup[str] | None = strawberry_django.filter_field()
    public_key: FilterLookup[str] | None = strawberry_django.filter_field()
    fingerprint: FilterLookup[str] | None = strawberry_django.filter_field()
    tenant: Annotated['TenantFilter', strawberry.lazy('tenancy.graphql.filters')] | None = (
        strawberry_django.filter_field()
    )
    tenant_id: ID | None = strawberry_django.filter_field()
