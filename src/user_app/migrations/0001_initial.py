# Generated by Django 4.1.1 on 2022-10-02 12:03

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import re
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=16, unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=16, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=32, null=True)),
                ('last_name', models.CharField(blank=True, max_length=16, null=True)),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator(code='400', message='Please enter a valid email address.')])),
                ('password', models.CharField(max_length=16)),
                ('mobile', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(code='400', message='Please enter a phone number without the ISD code.', regex=re.compile('^([\\s.-])?(\\+\\d{1,2}\\s)?\\(?\\d{3}\\)?([\\s.-])?\\d{3}([\\s.-])?\\d{4}$/gm'))])),
                ('account_type', models.CharField(choices=[('Administrator', 'Administrator'), ('Staff', 'Staff'), ('User', 'User')], default='User', max_length=25)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User Account',
                'verbose_name_plural': 'User Accounts',
                'ordering': ('-date_joined', '-created'),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
