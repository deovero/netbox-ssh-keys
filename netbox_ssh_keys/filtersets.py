import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet
from tenancy.models import Tenant

from .choices import SSHKeyTypeChoices
from .models import SSHKey


class SSHKeyFilterSet(NetBoxModelFilterSet):
    key_type = django_filters.MultipleChoiceFilter(
        choices=SSHKeyTypeChoices,
    )
    fingerprint = django_filters.CharFilter(
        lookup_expr='exact',
    )
    tenant_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Tenant.objects.all(),
        label='Tenant (ID)',
    )
    tenant = django_filters.ModelMultipleChoiceFilter(
        field_name='tenant__slug',
        queryset=Tenant.objects.all(),
        to_field_name='slug',
        label='Tenant (slug)',
    )

    class Meta:
        model = SSHKey
        fields = ['id', 'name', 'key_type', 'fingerprint', 'tenant_id']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(fingerprint__icontains=value)
            | Q(description__icontains=value)
        )
