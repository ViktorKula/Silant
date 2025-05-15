from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email')

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('machine_serial_number', 'model_of_equipment', 'client', 'service_company')
    search_fields = ('machine_serial_number', 'model_of_equipment__title')
    list_filter = ('service_company',)

    def get_queryset(self, request):
        """Выделяем релевантные данные для каждой учётки"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'service':
            # Фильтруем машины по сервисной компании
            return qs.filter(service_company__user=request.user)
        if request.user.role == 'manager':
            # Менеджер видит все машины
            return qs
        return qs.filter(client__user=request.user)

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('machine', 'type_of_maintenance', 'date_of_maintenance', 'service_company')
    search_fields = ('machine__machine_serial_number', 'type_of_maintenance__title')
    list_filter = ('service_company',)

    def get_queryset(self, request):
        """Выделяем релевантные данные для каждой учётки"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'service':
            # Фильтруем ТО по сервисной компании
            return qs.filter(service_company__user=request.user)
        if request.user.role == 'manager':
            # Менеджер видит все ТО
            return qs
        return qs.filter(machine__client__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Фильтруем машины для выбора в форме"""
        if db_field.name == "machine":
            if request.user.is_superuser:
                return super().formfield_for_foreignkey(db_field, request, **kwargs)
            if request.user.role == 'service':
                # Ограничиваем выбор машин только для текущей сервисной компании
                kwargs["queryset"] = Machine.objects.filter(service_company__user=request.user)
            elif request.user.role == 'manager':
                # Менеджер видит все машины
                kwargs["queryset"] = Machine.objects.all()
            else:
                # Ограничиваем выбор машин только для текущего клиента
                kwargs["queryset"] = Machine.objects.filter(client__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Complaints)
class ComplaintsAdmin(admin.ModelAdmin):
    list_display = ('machine', 'date_of_refusal', 'failure_node', 'service_company')
    search_fields = ('machine__machine_serial_number', 'failure_node__title')
    list_filter = ('service_company',)

    def get_queryset(self, request):
        """Выделяем релевантные данные для каждой учётки"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'service':
            # Фильтруем рекламации по сервисной компании
            return qs.filter(service_company__user=request.user)
        if request.user.role == 'manager':
            # Менеджер видит все рекламации
            return qs
        return qs.filter(machine__client__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Фильтруем машины для выбора в форме"""
        if db_field.name == "machine":
            if request.user.is_superuser:
                return super().formfield_for_foreignkey(db_field, request, **kwargs)
            if request.user.role == 'service':
                # Ограничиваем выбор машин только для текущей сервисной компании
                kwargs["queryset"] = Machine.objects.filter(service_company__user=request.user)
            elif request.user.role == 'manager':
                # Менеджер видит все машины
                kwargs["queryset"] = Machine.objects.all()
            else:
                # Ограничиваем выбор машин только для текущего клиента
                kwargs["queryset"] = Machine.objects.filter(client__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'user')
    search_fields = ('name',)

@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

@admin.register(EngineModel)
class EngineModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

@admin.register(TransmissionModel)
class TransmissionModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

@admin.register(DrivingBridgeModel)
class DrivingBridgeModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

@admin.register(ControlledBridgeModel)
class ControlledBridgeModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

@admin.register(ServiceCompany)
class ServiceCompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user')
    search_fields = ('title',)

@admin.register(MaintenanceType)
class MaintenanceTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

@admin.register(FailureNode)
class FailureNodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

@admin.register(RecoveryMethod)
class RecoveryMethodAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)