# Generated by Django 4.2.6 on 2024-03-27 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0004_msgupdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msgupdate',
            name='msg',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
