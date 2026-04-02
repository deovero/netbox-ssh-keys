from netbox.plugins import PluginConfig


class NetBoxSSHKeysConfig(PluginConfig):
    name = 'netbox_ssh_keys'
    verbose_name = 'SSH Keys'
    description = 'Manage SSH public keys as first-class NetBox objects'
    version = '0.1.5'
    author = 'Deovero'
    author_email = ''
    base_url = 'ssh-keys'
    min_version = '4.2.0'
    default_settings = {}
    graphql_schema = 'graphql.schema.schema'


config = NetBoxSSHKeysConfig
