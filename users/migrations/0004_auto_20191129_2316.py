# Generated by Django 2.2.5 on 2019-11-29 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20191129_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='currency',
            field=models.CharField(blank=True, choices=[('usd', 'USD'), ('krw', 'KRW')], max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superhost',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('en', 'English'), ('kr', 'Korean')], max_length=2, null=True),
        ),
    ]