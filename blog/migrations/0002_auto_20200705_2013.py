# Generated by Django 2.2.7 on 2020-07-05 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setting',
            name='engilsh_title',
        ),
        migrations.RemoveField(
            model_name='setting',
            name='persian_title',
        ),
        migrations.AddField(
            model_name='setting',
            name='title',
            field=models.CharField(default='FaraPy', max_length=200, verbose_name='عنوان'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.IntegerField(choices=[(1, 'تائید شد'), (0, 'تائید نشده')], default=0, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='status',
            field=models.IntegerField(choices=[(0, 'منوی اصلی'), (1, 'منوی فرعی')], default=0, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='address',
            field=models.CharField(max_length=200, null=True, verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='api',
            field=models.CharField(max_length=200, null=True, verbose_name='api kavenegar'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='city',
            field=models.CharField(default='tehran', max_length=200, null=True, verbose_name='شهر'),
        ),
        migrations.AlterField(
            model_name='setting',
            name='tel_no',
            field=models.IntegerField(null=True, verbose_name='شماره تماس'),
        ),
        migrations.AlterField(
            model_name='submenu',
            name='status',
            field=models.IntegerField(choices=[(0, 'دسته بندی'), (1, 'ادرس'), (2, 'صفحه')], default=0, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='task_manegar',
            name='status',
            field=models.IntegerField(choices=[(3, 'انجام شده'), (0, 'در حال انجام'), (1, 'برای آینده')], default=0, verbose_name='وضعیت'),
        ),
    ]
