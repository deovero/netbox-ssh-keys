from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer

from ..models import SSHKey


class SSHKeySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_ssh_keys-api:sshkey-detail',
    )
    authorized_keys_line = serializers.CharField(read_only=True)

    class Meta:
        model = SSHKey
        fields = [
            'id', 'url', 'display', 'name', 'key_type', 'public_key',
            'fingerprint', 'tenant', 'description',
            'authorized_keys_line',
            'tags', 'custom_fields', 'created', 'last_updated',
        ]
        brief_fields = ['id', 'url', 'display', 'name', 'public_key', 'fingerprint', 'key_type']
