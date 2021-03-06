# Generated by Django 2.1.1 on 2018-11-25 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20181123_1253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name'], 'permissions': (('can_delete_author', 'Can delete Author records'), ('can_create_author', 'Can create Author records'))},
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=200, verbose_name='title'),
        ),
    ]
