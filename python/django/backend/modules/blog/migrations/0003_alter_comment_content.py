# Generated by Django 4.2.11 on 2024-06-25 08:37

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_article_full_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Текст комментария'),
        ),
    ]