from netbox.api.viewsets import NetBoxModelViewSet

from ..filtersets import SSHKeyFilterSet
from ..models import SSHKey
from .serializers import SSHKeySerializer


class SSHKeyViewSet(NetBoxModelViewSet):
    queryset = SSHKey.objects.prefetch_related('tenant', 'tags')
    serializer_class = SSHKeySerializer
    filterset_class = SSHKeyFilterSet
