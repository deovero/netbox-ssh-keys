import django_tables2 as tables

from netbox.tables import NetBoxTable, columns

from .models import SSHKey


class SSHKeyTable(NetBoxTable):
    name = tables.Column(linkify=True)
    key_type = tables.Column(verbose_name='Type')
    fingerprint = tables.Column()
    tenant = tables.Column(linkify=True)
    tags = columns.TagColumn(url_name='plugins:netbox_ssh_keys:sshkey_list')

    class Meta(NetBoxTable.Meta):
        model = SSHKey
        fields = (
            'pk', 'id', 'name', 'key_type', 'fingerprint',
            'tenant', 'description', 'tags', 'created', 'last_updated',
        )
        default_columns = ('name', 'key_type', 'fingerprint', 'tenant', 'tags')
