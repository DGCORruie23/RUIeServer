# Generated by Django 4.2.6 on 2024-07-31 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0008_alter_rescatepunto_numpresuntosdelincuentes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rescatepunto',
            name='numFamilia',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
