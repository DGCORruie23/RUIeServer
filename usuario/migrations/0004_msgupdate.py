# Generated by Django 4.2.6 on 2024-03-27 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_rescatepunto_embarazo'),
    ]

    operations = [
        migrations.CreateModel(
            name='MsgUpdate',
            fields=[
                ('idMsg', models.AutoField(primary_key=True, serialize=False)),
                ('version', models.CharField(max_length=25)),
                ('msg', models.CharField(max_length=500)),
            ],
        ),
    ]
