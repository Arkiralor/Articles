# Generated by Django 4.1.1 on 2022-10-02 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_alter_useraccount_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='password',
            field=models.CharField(max_length=512),
        ),
    ]
