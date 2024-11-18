# Generated by Django 4.1.13 on 2024-05-31 21:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customuser_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Milk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=250)),
                ('price', models.CharField(max_length=50)),
                ('date1', models.DateTimeField(auto_now_add=True)),
                ('customuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
