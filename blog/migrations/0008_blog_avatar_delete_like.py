# Generated by Django 5.1.3 on 2025-01-08 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_blog_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='avatar',
            field=models.ImageField(default='default.jpg', upload_to='profile_images'),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
