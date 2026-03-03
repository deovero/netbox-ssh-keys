from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenancy', '0001_initial'),
        ('netbox_ssh_keys', '0004_alter_sshkey_public_key'),
    ]

    operations = [
        # Drop global unique on name
        migrations.AlterField(
            model_name='sshkey',
            name='name',
            field=models.CharField(
                help_text='A friendly name for this key',
                max_length=256,
            ),
        ),
        # Drop global unique on fingerprint
        migrations.AlterField(
            model_name='sshkey',
            name='fingerprint',
            field=models.CharField(
                editable=False,
                help_text='SHA256 fingerprint (auto-calculated)',
                max_length=128,
            ),
        ),
        # Add unique_together: fingerprint + tenant
        migrations.AddConstraint(
            model_name='sshkey',
            constraint=models.UniqueConstraint(
                fields=['fingerprint', 'tenant'],
                name='unique_fingerprint_per_tenant',
            ),
        ),
    ]
