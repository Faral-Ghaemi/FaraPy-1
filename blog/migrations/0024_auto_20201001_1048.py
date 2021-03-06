# Generated by Django 2.2.7 on 2020-10-01 07:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_auto_20201001_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subtickets',
            name='title',
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.IntegerField(choices=[(1, 'Confirmed'), (0, 'Not confirmed')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='status',
            field=models.IntegerField(choices=[(1, 'Secondry Menu'), (0, 'Primary Menu')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='portable',
            name='sex',
            field=models.IntegerField(choices=[(1, 'Male'), (0, 'Female')], default=1, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='submenu',
            name='status',
            field=models.IntegerField(choices=[(0, 'Category'), (1, 'Address'), (2, 'Page')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='task_manegar',
            name='created_time',
            field=models.DateField(default=datetime.datetime(2020, 10, 1, 10, 48, 20, 897959), null=True, verbose_name='Start date'),
        ),
        migrations.AlterField(
            model_name='task_manegar',
            name='end_time',
            field=models.DateField(default=datetime.datetime(2020, 10, 1, 10, 48, 20, 897959), null=True, verbose_name='Finish date'),
        ),
        migrations.AlterField(
            model_name='task_manegar',
            name='status',
            field=models.IntegerField(choices=[(0, 'To Do'), (1, 'In progress'), (3, 'Done!')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Portable', verbose_name='User'),
        ),
    ]
