# Generated by Django 4.0.2 on 2022-03-02 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wGOA', '0002_remove_cpc_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpc',
            name='Time',
            field=models.CharField(default=1234567890, max_length=100),
            preserve_default=False,
        ),
    ]
