# Generated by Django 3.0.10 on 2020-09-26 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterUserConfig',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('is_deleted', models.BooleanField(db_index=True, default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('oauth_token', models.CharField(max_length=200, verbose_name='Oauth Token')),
                ('oauth_token_secret', models.CharField(max_length=200, verbose_name='Oauth Token Secret')),
                ('access_token', models.CharField(blank=True, max_length=200, null=True, verbose_name='Access Token')),
                ('access_token_secret', models.CharField(blank=True, max_length=200, null=True, verbose_name='Access Token Secret')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]