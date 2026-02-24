from netbox.plugins import PluginTemplateExtension

from .models import SSHKey


class TenantSSHKeysPanel(PluginTemplateExtension):
    """Show SSH keys owned by this tenant on the Tenant detail page."""

    models = ['tenancy.tenant']

    def right_page(self):
        obj = self.context['object']
        ssh_keys = SSHKey.objects.filter(tenant=obj)
        return self.render(
            'netbox_ssh_keys/inc/tenant_ssh_keys.html',
            extra_context={'ssh_keys': ssh_keys},
        )


template_extensions = [
    TenantSSHKeysPanel,
]
