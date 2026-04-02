from netbox.plugins import PluginMenuButton, PluginMenuItem

menu_items = (
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
)
