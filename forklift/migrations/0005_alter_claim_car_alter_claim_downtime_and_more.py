# Generated by Django 4.1.3 on 2023-07-13 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forklift', '0004_alter_forklift_end_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forklift.forklift', verbose_name='Зав. № машины'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='downtime',
            field=models.IntegerField(default=0, verbose_name='Время простоя техники'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='operating',
            field=models.PositiveIntegerField(default=0, verbose_name='Наработка, м/час'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='order_description',
            field=models.TextField(verbose_name='Описание отказа'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='order_note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forklift.naturerefusal', verbose_name='Узел отказа'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='orders_date',
            field=models.DateField(verbose_name='Дата отказа'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='recovery_date',
            field=models.DateField(verbose_name='Дата восстановления'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='recovery_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forklift.recoverymethod', verbose_name='Способ восстановления'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='service_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forklift.service_company', verbose_name='Сервисная компания'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='used_spare_parts',
            field=models.TextField(verbose_name='Используемые запасные части'),
        ),
        migrations.AlterField(
            model_name='to',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forklift.forklift', verbose_name='Зав. № машины'),
        ),
        migrations.AlterField(
            model_name='to',
            name='date',
            field=models.DateField(verbose_name='Дата проведения ТО'),
        ),
        migrations.AlterField(
            model_name='to',
            name='operating',
            field=models.PositiveIntegerField(default=0, verbose_name='Наработка, м/час'),
        ),
        migrations.AlterField(
            model_name='to',
            name='orders_date',
            field=models.DateField(verbose_name='дата заказ-наряда'),
        ),
        migrations.AlterField(
            model_name='to',
            name='orders_number',
            field=models.CharField(max_length=32, verbose_name='№ заказ-наряда'),
        ),
        migrations.AlterField(
            model_name='to',
            name='organization',
            field=models.CharField(max_length=32, verbose_name='Организация, проводившая ТО'),
        ),
        migrations.AlterField(
            model_name='to',
            name='service_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forklift.service_company', verbose_name='Сервисная компания'),
        ),
        migrations.AlterField(
            model_name='to',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forklift.typeto', verbose_name='Вид Тo'),
        ),
    ]
