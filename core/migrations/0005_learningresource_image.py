# Generated by Django 5.1.3 on 2024-12-02 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningresource',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='learning_resources/'),
        ),
    ]
