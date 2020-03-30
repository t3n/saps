# Generated by Django 3.0.3 on 2020-03-13 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FunctionKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fkey1', models.CharField(max_length=25)),
                ('phone', models.ForeignObject(from_fields=['phone_type', 'mac_address'], on_delete=django.db.models.deletion.CASCADE, to='snom.Phone', to_fields=['phone_type', 'mac_address'])),
            ],
        ),
    ]
