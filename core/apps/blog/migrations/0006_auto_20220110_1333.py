# Generated by Django 3.2.6 on 2022-01-10 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20220110_1315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('date_created',), 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(default='article-default.jpg', upload_to='articles-images'),
        ),
    ]
