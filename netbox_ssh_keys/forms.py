import base64

from django import forms
from django.core.exceptions import ValidationError

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelForm,
    NetBoxModelImportForm,
)
from tenancy.models import Tenant
from utilities.forms.fields import DynamicModelChoiceField, TagFilterField
from utilities.forms.rendering import FieldSet

from .choices import SSHKeyTypeChoices
from .models import SSHKey


# ---------------------------------------------------------------------------
# SSHKey forms
# ---------------------------------------------------------------------------

class SSHKeyForm(NetBoxModelForm):
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
    )

    fieldsets = (
        FieldSet(
            'name', 'key_type', 'public_key',
            'tenant', 'description', 'tags',
            name='SSH Key',
        ),
    )

    class Meta:
        model = SSHKey
        fields = [
            'name', 'key_type', 'public_key',
            'tenant', 'description', 'tags',
        ]
        widgets = {
            'public_key': forms.Textarea(attrs={
                'rows': 3,
                'id': 'id_public_key',
            }),
        }

    def clean_public_key(self):
        """
        Accept either raw base64 key material or a full authorized_keys line.
        If a full line is provided, auto-extract key_type and name.
        Server-side fallback for the JS auto-parse.
        """
        value = self.cleaned_data['public_key'].strip()
        parts = value.split(None, 2)

        if len(parts) >= 2 and parts[0] in SSHKeyTypeChoices.values():
            # Full authorized_keys line pasted
            self._parsed_key_type = parts[0]
            self._parsed_name = parts[2] if len(parts) > 2 else ''
            value = parts[1]

        # Validate base64
        try:
            base64.b64decode(value, validate=True)
        except Exception:
            raise ValidationError('Invalid base64-encoded public key material.')
        return value

    def clean(self):
        super().clean()
        # Auto-fill key_type and name when parsed from a full key line
        if hasattr(self, '_parsed_key_type'):
            if not self.cleaned_data.get('key_type'):
                self.cleaned_data['key_type'] = self._parsed_key_type
        if hasattr(self, '_parsed_name'):
            if not self.cleaned_data.get('name'):
                self.cleaned_data['name'] = self._parsed_name
        return self.cleaned_data


class SSHKeyBulkEditForm(NetBoxModelBulkEditForm):
    tenant = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
    )
    description = forms.CharField(
        max_length=200,
        required=False,
    )

    model = SSHKey
    fieldsets = (
        FieldSet('tenant', 'description'),
    )
    nullable_fields = ('tenant', 'description')


class SSHKeyImportForm(NetBoxModelImportForm):
    tenant = forms.ModelChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name='name',
        required=False,
    )

    class Meta:
        model = SSHKey
        fields = ['name', 'key_type', 'public_key', 'tenant', 'description']


class SSHKeyFilterForm(NetBoxModelFilterSetForm):
    model = SSHKey
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('key_type', 'tenant_id', 'fingerprint', name='Filters'),
    )
    key_type = forms.MultipleChoiceField(
        choices=SSHKeyTypeChoices,
        required=False,
    )
    tenant_id = DynamicModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        label='Tenant',
    )
    fingerprint = forms.CharField(
        required=False,
    )
    tag = TagFilterField(model)


# ---------------------------------------------------------------------------
# Bulk authorized_keys import (custom form)
# ---------------------------------------------------------------------------

class SSHKeyBulkAuthorizedKeysForm(forms.Form):
    """Form for bulk-importing SSH keys from authorized_keys format."""

    authorized_keys = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 15,
            'placeholder': 'Paste authorized_keys content here\u2026',
        }),
        help_text='Paste one or more SSH public key lines. Lines starting with # are ignored.',
    )
    tenant = forms.ModelChoiceField(
        queryset=Tenant.objects.all(),
        required=False,
        help_text='Optionally assign all imported keys to a tenant.',
    )
