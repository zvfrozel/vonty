# Generated by Django 5.0.4 on 2024-04-20 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vonty', '0004_tag_depth_tag_numchild_tag_path'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='tag',
            name='filter_implies_parent',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='parent',
        ),
    ]
