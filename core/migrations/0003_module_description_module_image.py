# Generated by Django 5.1.3 on 2024-12-01 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_learningresource_assignment_progress_quiz_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='module',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='modules/'),
        ),
    ]