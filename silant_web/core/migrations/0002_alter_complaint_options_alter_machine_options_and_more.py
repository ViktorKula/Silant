# Generated by Django 5.0.7 on 2025-05-06 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='complaint',
            options={'ordering': ['-date_of_refusal']},
        ),
        migrations.AlterModelOptions(
            name='machine',
            options={'ordering': ['-date_shipped_from_factory']},
        ),
        migrations.AlterModelOptions(
            name='maintenance',
            options={'ordering': ['-maintenance_date']},
        ),
        migrations.AlterField(
            model_name='complaint',
            name='date_of_refusal',
            field=models.DateField(null=True, verbose_name='Дата отказа'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='description_of_failure',
            field=models.CharField(max_length=255, verbose_name='Описание отказа'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='equipment_downtime',
            field=models.IntegerField(verbose_name='Время простоя'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='failure_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.failurenode', verbose_name='Узел отказа'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.machine', verbose_name='Машина'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='operating_time',
            field=models.IntegerField(verbose_name='Наработка, м/час'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='parts_used',
            field=models.CharField(max_length=255, verbose_name='Использованные запчасти'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='recovery_date',
            field=models.DateField(null=True, verbose_name='Дата восстановления отказа'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='recovery_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.recoverymethod', verbose_name='Способ восстановления отказа'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='service_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.servicecompany', verbose_name='Сервисная компания'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.machine', verbose_name='Машина'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='maintenance_date',
            field=models.DateField(null=True, verbose_name='Дата проведения ТО'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='maintenance_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.maintenancetype', verbose_name='Вид ТО'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='operating_time',
            field=models.IntegerField(verbose_name='Наработка, м/час'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='service_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.servicecompany', verbose_name='Сервисная компания'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='the_organization_that_carried_out_the_maintenance',
            field=models.CharField(max_length=255, verbose_name='Организация, проводившая ТО'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='work_order_date',
            field=models.DateField(null=True, verbose_name='Дата заказ-наряда'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='work_order_number',
            field=models.CharField(max_length=255, verbose_name='№ заказ-наряда'),
        ),
    ]
