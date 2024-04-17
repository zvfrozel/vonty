# Generated by Django 5.0.4 on 2024-04-17 14:23

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vonty_app', '0004_alter_tag_desc'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='is_filter',
        ),
        migrations.AddField(
            model_name='tag',
            name='use_filter',
            field=models.BooleanField(default=True, help_text='Specifies whether users should use this tag to filter problems. Uncheck this for tags that are purely meant to be used as umbrella parent tags and not as filters.'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='aops_url',
            field=models.URLField(blank=True, help_text='A link to the problem on AOPS, if it exists. '),
        ),
        migrations.AlterField(
            model_name='problem',
            name='desc',
            field=models.CharField(help_text='A short one-line description of the problem statement. e.g. Fiendish inequality', max_length=100),
        ),
        migrations.AlterField(
            model_name='problem',
            name='git_url',
            field=models.URLField(blank=True, help_text='Read-only link to pull the problem via git. See LINK TO GIT PULL DOCUMENTATION.'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='hardness',
            field=models.PositiveIntegerField(blank=True, help_text='Hardness of the problem according to the MOHS scale. The rating can range from 0 to 60, and can be left blank if the problem is considered not-rateable. See https://web.evanchen.cc/upload/MOHS-hardness.pdf for more information.', null=True, validators=[django.core.validators.MaxValueValidator(60, 'MOHS rating cannot exceed 60'), django.core.validators.StepValueValidator(5, 'MOHS rating must be a multiple of 5')]),
        ),
        migrations.AlterField(
            model_name='problem',
            name='proposer',
            field=models.ForeignKey(blank=True, help_text='The author, if they are a member of this database. Use this in problems you have proposed yourself, for example.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='problem',
            name='source',
            field=models.CharField(blank=True, help_text='Problem source. This must be either blank or unique. e.g. IMO 2023/6', max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='parent',
            field=models.ForeignKey(help_text='The parent tag that this tag comes under. Filtering by the parent tag filters by this tag too. If this field is blank, the is_filter option must be unchecked.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='vonty_app.tag'),
        ),
    ]