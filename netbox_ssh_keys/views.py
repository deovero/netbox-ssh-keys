from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from netbox.views import generic
from utilities.views import register_model_view

from .filtersets import SSHKeyFilterSet
from .forms import (
    SSHKeyBulkAuthorizedKeysForm,
    SSHKeyBulkEditForm,
    SSHKeyFilterForm,
    SSHKeyForm,
    SSHKeyImportForm,
)
from .models import SSHKey
from .tables import SSHKeyTable
from .utils import parse_ssh_public_key


# ---------------------------------------------------------------------------
# SSHKey views
# ---------------------------------------------------------------------------

@register_model_view(SSHKey, 'list', path='', detail=False)
class SSHKeyListView(generic.ObjectListView):
    queryset = SSHKey.objects.all()
    table = SSHKeyTable
    filterset = SSHKeyFilterSet
    filterset_form = SSHKeyFilterForm


@register_model_view(SSHKey)
class SSHKeyView(generic.ObjectView):
    queryset = SSHKey.objects.all()




@register_model_view(SSHKey, 'add', detail=False)
@register_model_view(SSHKey, 'edit')
class SSHKeyEditView(generic.ObjectEditView):
    queryset = SSHKey.objects.all()
    form = SSHKeyForm
    template_name = 'netbox_ssh_keys/sshkey_edit.html'


@register_model_view(SSHKey, 'delete')
class SSHKeyDeleteView(generic.ObjectDeleteView):
    queryset = SSHKey.objects.all()


@register_model_view(SSHKey, 'bulk_edit', path='edit', detail=False)
class SSHKeyBulkEditView(generic.BulkEditView):
    queryset = SSHKey.objects.all()
    filterset = SSHKeyFilterSet
    table = SSHKeyTable
    form = SSHKeyBulkEditForm


@register_model_view(SSHKey, 'bulk_delete', path='delete', detail=False)
class SSHKeyBulkDeleteView(generic.BulkDeleteView):
    queryset = SSHKey.objects.all()
    filterset = SSHKeyFilterSet
    table = SSHKeyTable


@register_model_view(SSHKey, 'bulk_import', path='import', detail=False)
class SSHKeyBulkImportView(generic.BulkImportView):
    queryset = SSHKey.objects.all()
    model_form = SSHKeyImportForm
    table = SSHKeyTable


# ---------------------------------------------------------------------------
# Bulk authorized_keys import (custom view)
# ---------------------------------------------------------------------------

@register_model_view(SSHKey, 'bulk_authorized_keys', path='import/authorized-keys', detail=False)
class SSHKeyBulkAuthorizedKeysView(View):
    """Import SSH keys from pasted authorized_keys content."""

    template_name = 'netbox_ssh_keys/sshkey_bulk_authorized_keys.html'

    def get(self, request):
        form = SSHKeyBulkAuthorizedKeysForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SSHKeyBulkAuthorizedKeysForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        tenant = form.cleaned_data.get('tenant')
        lines = form.cleaned_data['authorized_keys'].splitlines()
        created = []
        errors = []

        for i, line in enumerate(lines, 1):
            try:
                parsed = parse_ssh_public_key(line)
                if parsed is None:
                    continue  # skip blanks / comments

                name = parsed['comment'] or f'imported-key-{i}'
                key = SSHKey(
                    name=name,
                    key_type=parsed['key_type'],
                    public_key=parsed['public_key'],
                    tenant=tenant,
                )
                key.full_clean()
                key.save()
                created.append(key)
            except Exception as exc:
                errors.append(f'Line {i}: {exc}')

        if created:
            messages.success(request, f'Successfully imported {len(created)} SSH key(s).')
        if errors:
            for error in errors:
                messages.warning(request, error)

        if created and not errors:
            return redirect('plugins:netbox_ssh_keys:sshkey_list')

        return render(request, self.template_name, {'form': form})
