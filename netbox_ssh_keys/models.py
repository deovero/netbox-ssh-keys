from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel

from .choices import SSHKeyTypeChoices
from .utils import calculate_fingerprint


class SSHKey(NetBoxModel):
    """An SSH public key managed as a first-class NetBox object."""

    name = models.CharField(
        max_length=256,
        unique=True,
        help_text='A unique friendly name for this key',
    )
    key_type = models.CharField(
        max_length=64,
        choices=SSHKeyTypeChoices,
        help_text='SSH key algorithm type',
    )
    public_key = models.CharField(
        max_length=1023,
        help_text='Base64-encoded public key material (without type prefix or comment)',
    )
    fingerprint = models.CharField(
        max_length=128,
        unique=True,
        editable=False,
        help_text='SHA256 fingerprint (auto-calculated)',
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='ssh_keys',
        blank=True,
        null=True,
    )
    description = models.CharField(
        max_length=200,
        blank=True,
    )

    clone_fields = ('key_type', 'tenant')

    class Meta:
        ordering = ['name']
        verbose_name = 'SSH key'
        verbose_name_plural = 'SSH keys'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_ssh_keys:sshkey', args=[self.pk])

    def clean(self):
        super().clean()
        if self.public_key:
            self.fingerprint = calculate_fingerprint(self.public_key)

    def save(self, *args, **kwargs):
        if self.public_key:
            self.fingerprint = calculate_fingerprint(self.public_key)
        super().save(*args, **kwargs)

    @property
    def authorized_keys_line(self):
        """Return the key formatted as an authorized_keys line, using name as comment."""
        return f'{self.key_type} {self.public_key} {self.name}'

