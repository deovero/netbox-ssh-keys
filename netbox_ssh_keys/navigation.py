from netbox.plugins import PluginMenu, PluginMenuButton, PluginMenuItem

menu = PluginMenu(
    label='SSH Keys',
    groups=(
        ('SSH Keys', (
            PluginMenuItem(
                link='plugins:netbox_ssh_keys:sshkey_list',
                link_text='SSH Keys',
                buttons=(
                    PluginMenuButton(
                        link='plugins:netbox_ssh_keys:sshkey_add',
                        title='Add',
                        icon_class='mdi mdi-plus-thick',
                    ),
                    PluginMenuButton(
                        link='plugins:netbox_ssh_keys:sshkey_bulk_authorized_keys',
                        title='Import',
                        icon_class='mdi mdi-upload',
                    ),
                ),
            ),
        )),
    ),
    icon_class='mdi mdi-key-chain',
)
