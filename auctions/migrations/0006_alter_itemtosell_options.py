# Generated by Django 3.2.7 on 2021-10-20 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_itemtosell_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemtosell',
            options={'ordering': ['title']},
        ),
    ]
