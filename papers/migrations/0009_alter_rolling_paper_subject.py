# Generated by Django 4.2.7 on 2023-11-23 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0008_alter_rolling_paper_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolling_paper',
            name='subject',
            field=models.CharField(default='Untitled', max_length=50),
        ),
    ]