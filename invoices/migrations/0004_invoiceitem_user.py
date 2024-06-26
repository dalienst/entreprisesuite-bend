# Generated by Django 5.0.6 on 2024-06-13 08:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_alter_invoice_total_amount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='user',
            field=models.ForeignKey(default='cee680d3-08f1-4577-9be1-41c431ab4310', on_delete=django.db.models.deletion.CASCADE, related_name='invoice_item', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
