# Generated by Django 4.0.6 on 2022-07-25 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_post_exercisename'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='exercisename',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.category'),
            preserve_default=False,
        ),
    ]
