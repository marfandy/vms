# Generated by Django 4.2 on 2024-05-06 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_purchaseorder_quality_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='issue_order',
            field=models.CharField(max_length=225, null=True),
        ),
    ]