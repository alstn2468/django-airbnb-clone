# Generated by Django 2.2.10 on 2020-03-13 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200313_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_secret',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
    ]