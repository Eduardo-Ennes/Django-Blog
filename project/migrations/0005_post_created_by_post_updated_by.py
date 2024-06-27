# Generated by Django 5.0.4 on 2024-06-18 19:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_alter_page_is_published_post'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='page_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='page_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]