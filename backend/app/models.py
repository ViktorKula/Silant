from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Пользователь (расширение модели)"""
    ROLE_CHOICES = [
        ('guest', 'Гость'),
        ('client', 'Клиент'),
        ('service', 'Сервисная организация'),
        ('manager', 'Менеджер'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Machine(models.Model):
    """Машина"""
    machine_serial_number = models.CharField(max_length=120, verbose_name='Заводской номер машины')
    model_of_equipment = models.ForeignKey('EquipmentModel', verbose_name='Модель техники', on_delete=models.CASCADE)
    engine_model = models.ForeignKey('EngineModel', verbose_name='Модель двигателя', on_delete=models.CASCADE)
    engine_serial_number = models.CharField(max_length=120, verbose_name='Заводской номер двигателя')
    transmission_model = models.ForeignKey('TransmissionModel', verbose_name='Модель трансмиссии', on_delete=models.CASCADE)
    transmission_serial_number = models.CharField(max_length=120, verbose_name='Заводской номер трансмиссии')
    model_of_the_drivig_bridge = models.ForeignKey('DrivingBridgeModel', verbose_name='Модель ведущего моста', on_delete=models.CASCADE)
    driving_bridge_serial_number = models.CharField(max_length=120, verbose_name='Заводской номер ведущего моста')
    model_of_a_controlled_bridge = models.ForeignKey('ControlledBridgeModel', verbose_name='Модель управляемого моста', on_delete=models.CASCADE)
    controlled_bridge_serial_number = models.CharField(max_length=120, verbose_name='Заводской номер управляемого моста')
    supply_contract = models.CharField(max_length=120, verbose_name='Договор поставки', blank=True, null=True)
    date_of_shipment = models.DateTimeField(verbose_name='Дата отгрузки с завода', blank=True, null=True)
    consignee = models.CharField(max_length=120, verbose_name='Грузополучатель', blank=True, null=True)
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес поставки', blank=True, null=True)
    equipment = models.CharField(max_length=255, verbose_name='Комплектация', blank=True, null=True)
    client = models.ForeignKey('Client', verbose_name='Клиент', related_name='machines', blank=True, null=True, on_delete=models.CASCADE)
    service_company = models.ForeignKey('ServiceCompany', verbose_name='Сервисная компания', on_delete=models.CASCADE)

    def __str__(self):
        return f'Машина {self.machine_serial_number}'

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'


class Maintenance(models.Model):
    """Техническое обслуживание"""
    machine = models.ForeignKey('Machine', verbose_name='Машина', on_delete=models.CASCADE)
    type_of_maintenance = models.ForeignKey('MaintenanceType', verbose_name='Вид ТО', on_delete=models.CASCADE)
    date_of_maintenance = models.DateTimeField(verbose_name='Дата проведения ТО')
    maintenance_development = models.IntegerField(verbose_name='Наработка')
    order_number = models.CharField(max_length=100, verbose_name='Номер заказ-наряда')
    order_date = models.DateTimeField(verbose_name='Дата заказ-наряда')
    service_company = models.ForeignKey('ServiceCompany', verbose_name='Сервисная компания', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.machine.machine_serial_number} - {self.type_of_maintenance.title}'

    class Meta:
        verbose_name = 'Техническое обслуживание'
        verbose_name_plural = 'Техническое обслуживание'


class Complaints(models.Model):
    """Рекламации"""
    machine = models.ForeignKey('Machine', verbose_name='Машина', on_delete=models.CASCADE)
    date_of_refusal = models.DateTimeField(max_length=120, verbose_name='Дата отказа') # в ТЗ textfield!!!
    complaints_development = models.IntegerField(verbose_name='Наработка')
    failure_node = models.ForeignKey('FailureNode', verbose_name='Узел отказа', on_delete=models.CASCADE)
    description_of_the_failure = models.TextField(verbose_name='Описание отказа')
    recovery_method = models.ForeignKey('RecoveryMethod', verbose_name='Способ восстановления', on_delete=models.CASCADE)
    used_spare_parts = models.TextField(verbose_name='Используемые запасные части', blank=True, null=True)
    date_of_restoration = models.DateTimeField(verbose_name='Дата восстановления') # возможно нужно dateTimeField
    machine_downtime = models.TextField(verbose_name='Время простоя техники') # возможно нужно dateTimeField или IntegerField
    service_company = models.ForeignKey('ServiceCompany', verbose_name='Сервисная компания', on_delete=models.CASCADE)
    # service_company = models.TextField(verbose_name='Сервисная компания') # так указано в ТЗ, но странно


    def save(self, *args, **kwargs):
        """Высчитываем время простоя техники"""
        if self.date_of_restoration and self.date_of_refusal:
            self.machine_downtime = (self.date_of_restoration - self.date_of_refusal).days
        else:
            self.machine_downtime = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.machine.machine_serial_number} - {self.failure_node.title}'

    class Meta:
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'


class Client(models.Model):
    """Клиент"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, verbose_name='Имя')
    address = models.CharField(max_length=255, verbose_name='Адрес', default='Не указан')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

class EquipmentModel(models.Model):
    """Модель техники"""
    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.CharField(max_length=120, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель техники'
        verbose_name_plural = 'Модели техники'

class EngineModel(models.Model):
    """Модель двигателя"""
    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.CharField(max_length=120, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель двигателя'
        verbose_name_plural = 'Модели двигателей'

class TransmissionModel(models.Model):
    """Модель трансмиссии"""
    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.CharField(max_length=120, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель трансмиссии'
        verbose_name_plural = 'Модели трансмиссий'

class DrivingBridgeModel(models.Model):
    """Модель ведущего моста"""
    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.CharField(max_length=120, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель ведущего моста'
        verbose_name_plural = 'Модели ведущего моста'

class ControlledBridgeModel(models.Model):
    """Модель управляемого моста"""
    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.CharField(max_length=120, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель управляемого моста'
        verbose_name_plural = 'Модели управляемого моста'

class ServiceCompany(models.Model):
    """Сервисная компания"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.CharField(max_length=120, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сервисная компания'
        verbose_name_plural = 'Сервисные компании'

class MaintenanceType(models.Model):
    """Вид ТО"""
    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.CharField(max_length=120, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вид ТО'
        verbose_name_plural = 'Виды ТО'

class FailureNode(models.Model):
    """Узел отказа"""
    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.CharField(max_length=120, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Узел отказа'
        verbose_name_plural = 'Узлы отказа'

class RecoveryMethod(models.Model):
    """Способ восстановления"""
    title = models.CharField(max_length=120, verbose_name='Название')
    description = models.CharField(max_length=120, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Способ восстановления'
        verbose_name_plural = 'Способы восстановления'