# Generated by Django 3.1.7 on 2021-03-04 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('charity_app', '0003_auto_20210304_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='address',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='city',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='institution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='charity_app.institution'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='zip_code',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
