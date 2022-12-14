# Generated by Django 4.1.1 on 2022-10-03 00:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_alter_useraccount_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserOTP',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('otp', models.CharField(max_length=512)),
                ('expiry', models.DateTimeField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False, help_text='Whether the OTP has been used to log into the system.')),
            ],
            options={
                'verbose_name': 'User One-Time-Password',
                'verbose_name_plural': 'User One-Time-Passwords',
                'ordering': ('-created',),
            },
        ),
        migrations.AddIndex(
            model_name='useraccount',
            index=models.Index(db_tablespace='user_accounts', fields=['username'], name='user_app_us_usernam_917da3_idx'),
        ),
        migrations.AddIndex(
            model_name='useraccount',
            index=models.Index(db_tablespace='user_accounts', fields=['slug'], name='user_app_us_slug_e2bcc2_idx'),
        ),
        migrations.AddIndex(
            model_name='useraccount',
            index=models.Index(db_tablespace='user_accounts', fields=['email'], name='user_app_us_email_66a2d3_idx'),
        ),
        migrations.AddIndex(
            model_name='useraccount',
            index=models.Index(db_tablespace='user_accounts', fields=['mobile'], name='user_app_us_mobile_b6d283_idx'),
        ),
        migrations.AddIndex(
            model_name='useraccount',
            index=models.Index(db_tablespace='user_accounts', fields=['first_name', 'middle_name', 'last_name'], name='user_app_us_first_n_433a76_idx'),
        ),
        migrations.AddIndex(
            model_name='useraccount',
            index=models.Index(db_tablespace='user_accounts', fields=['last_name', 'middle_name', 'first_name'], name='user_app_us_last_na_864e05_idx'),
        ),
        migrations.AddField(
            model_name='userotp',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='userotp',
            index=models.Index(db_tablespace='user_accounts', fields=['user'], name='user_app_us_user_id_347d72_idx'),
        ),
        migrations.AddIndex(
            model_name='userotp',
            index=models.Index(db_tablespace='user_accounts', fields=['expiry'], name='user_app_us_expiry_f6e8dc_idx'),
        ),
        migrations.AddIndex(
            model_name='userotp',
            index=models.Index(db_tablespace='user_accounts', fields=['verified'], name='user_app_us_verifie_6f9084_idx'),
        ),
    ]
