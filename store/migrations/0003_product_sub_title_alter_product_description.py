# Generated by Django 5.0.4 on 2024-04-06 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_category_options_product_is_sale_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sub_title',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, default='', max_length=600, null=True),
        ),
    ]
