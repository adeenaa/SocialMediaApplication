# Generated by Django 5.2 on 2025-05-03 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(default='/profilepics/default.jpg', upload_to='profilepics'),
        ),
    ]
