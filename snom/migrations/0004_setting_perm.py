# Generated by Django 3.0.7 on 2020-07-02 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snom', '0003_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='perm',
            field=models.CharField(choices=[('', 'None'), ('R', 'Read'), ('RW', 'Read/Write')], default='', max_length=2),
        ),
    ]