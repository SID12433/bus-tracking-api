# Generated by Django 4.2.5 on 2024-03-15 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapi', '0015_alter_busstopdetail_busstop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busstopdetail',
            name='busstop',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='adminapi.busroutestops'),
        ),
    ]
