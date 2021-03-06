# Generated by Django 3.0.6 on 2020-06-27 13:30

import config.storage_backends
import config.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0007_auto_20200620_0128'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='이름')),
                ('image', models.FileField(default='default_team.jpg', storage=config.storage_backends.PublicMediaStorage(), upload_to=config.utils.s3_test_image_upload_to, verbose_name='이미지')),
            ],
        ),
        migrations.AlterField(
            model_name='team',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
    ]
