# Generated by Django 5.0.7 on 2024-08-27 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dsaSLN', '0006_dsapayout'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dsapayout',
            old_name='con',
            new_name='payouts',
        ),
    ]
