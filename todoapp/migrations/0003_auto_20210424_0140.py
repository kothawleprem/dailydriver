# Generated by Django 3.1.7 on 2021-04-23 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='category',
            field=models.CharField(choices=[('General', 'General'), ('Sports', 'Sports')], default='General', max_length=25),
        ),
    ]
