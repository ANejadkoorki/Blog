# Generated by Django 3.2.5 on 2021-07-14 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0007_alter_category_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'permissions': [], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]