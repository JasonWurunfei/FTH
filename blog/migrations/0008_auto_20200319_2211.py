# Generated by Django 3.0.3 on 2020-03-19 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200319_2202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogseries',
            name='blogs',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='series',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.BlogSeries'),
        ),
    ]
