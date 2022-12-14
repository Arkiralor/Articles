# Generated by Django 4.1.1 on 2022-10-02 12:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SampleModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=16)),
                ('char_field', models.CharField(blank=True, max_length=128, null=True)),
                ('decimal_field', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('integer_field', models.PositiveIntegerField(blank=True, null=True)),
                ('boolean_field', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Sample Object',
                'verbose_name_plural': 'Sample Objects',
                'ordering': ('name', '-created'),
                'unique_together': {('name', 'char_field', 'decimal_field', 'integer_field', 'boolean_field')},
            },
        ),
    ]
