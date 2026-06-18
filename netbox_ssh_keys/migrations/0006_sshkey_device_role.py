import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0001_initial'),
        ('netbox_ssh_keys', '0005_unique_fingerprint_per_tenant'),
    ]

    operations = [
        migrations.AddField(
            model_name='sshkey',
            name='device_role',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='ssh_keys',
                to='dcim.devicerole',
            ),
        ),
        migrations.AddConstraint(
            model_name='sshkey',
            constraint=models.UniqueConstraint(
                fields=['fingerprint', 'device_role'],
                name='unique_fingerprint_per_device_role',
            ),
        ),
    ]
