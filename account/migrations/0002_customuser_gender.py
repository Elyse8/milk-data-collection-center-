# Generated by Django 4.1.13 on 2024-05-31 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(default='Male', max_length=50),
            preserve_default=False,
        ),
    ]
