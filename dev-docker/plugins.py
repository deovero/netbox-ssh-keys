# Extra NetBox configuration loaded from /etc/netbox/config/.
# Enables the netbox-ssh-keys plugin in the test stack.
PLUGINS = [
    'netbox_ssh_keys',
]

PLUGINS_CONFIG = {
    'netbox_ssh_keys': {},
}
