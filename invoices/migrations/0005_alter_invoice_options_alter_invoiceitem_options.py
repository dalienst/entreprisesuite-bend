# Generated by Django 5.0.6 on 2024-06-13 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_invoiceitem_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ['-created_at'], 'verbose_name': 'Invoice', 'verbose_name_plural': 'Invoices'},
        ),
        migrations.AlterModelOptions(
            name='invoiceitem',
            options={'ordering': ['-created_at'], 'verbose_name': 'Invoice Item', 'verbose_name_plural': 'Invoice Items'},
        ),
    ]
