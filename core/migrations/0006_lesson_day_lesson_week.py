# Generated by Django 5.1.3 on 2024-12-02 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_learningresource_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='day',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='lesson',
            name='week',
            field=models.IntegerField(default=1),
        ),
    ]
