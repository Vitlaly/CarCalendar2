# Generated by Django 3.2.9 on 2022-03-11 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20220311_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
