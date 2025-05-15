from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from .forms import SearchForm
from .models import *
# import logging
#
# logger = logging.getLogger(__name__)


def main_view(request):
    """Возвращаем данные каждой таблицы в зависимости от роли пользователя"""
    client_name = None
    service_company_name = None
    machines = []
    maintenances = []
    complaints = []

    # Преобразование строковых дат в объекты datetime
    for machine in machines:
        machine.date_of_shipment = datetime.strptime(machine.date_of_shipment, '%b. %d, %Y, %I:%M %p')

    for maintenance in maintenances:
        maintenance.date_of_maintenance = datetime.strptime(maintenance.date_of_maintenance, '%b. %d, %Y, %I:%M %p')

    for complaint in complaints:
        complaint.date_of_refusal = datetime.strptime(complaint.date_of_refusal, '%b. %d, %Y, %I:%M %p')

    if request.user.is_authenticated:
        if request.user.role == 'manager':
            machines = Machine.objects.all()  # Менеджер видит все машины
            maintenances = Maintenance.objects.all()
            complaints = Complaints.objects.all()
        elif request.user.role == 'client':
            client = request.user.client
            machines = Machine.objects.filter(client=client)  # Клиент видит свои машины
            maintenances = Maintenance.objects.filter(machine__client=client)
            complaints = Complaints.objects.filter(machine__client=client)
            client_name = client.name  # Получаем имя клиента
        elif request.user.role == 'service':
            if hasattr(request.user, 'servicecompany'):
                service_company = request.user.servicecompany
                machines = Machine.objects.filter(service_company=service_company)  # Сервисная организация видит свои машины
                maintenances = Maintenance.objects.filter(service_company=service_company)
                complaints = Complaints.objects.filter(service_company=service_company)
                service_company_name = service_company.title  # Получаем название сервисной компании

    context = {
        'machines': machines,
        'maintenances': maintenances,
        'complaints': complaints,
        'client_name': client_name,
        'service_company_name': service_company_name,
        'request': request,
    }

    return render(request, '../templates/app/main.html', context)

def about_machine(request, machine_id):
    """Отображение деталей конкретной машины"""
    try:
        machine = Machine.objects.get(id=machine_id)
        maintenances = Maintenance.objects.filter(machine=machine)  # Получаем данные о ТО для этой машины
        complaints = Complaints.objects.filter(machine=machine)  # Получаем данные о рекламациях для этой машины

        # Преобразование строковых дат в объекты datetime, если они еще не являются таковыми
        if isinstance(machine.date_of_shipment, str):
            machine.date_of_shipment = datetime.strptime(machine.date_of_shipment, '%b. %d, %Y, %I:%M %p')

        for maintenance in maintenances:
            if isinstance(maintenance.date_of_maintenance, str):
                maintenance.date_of_maintenance = datetime.strptime(maintenance.date_of_maintenance,
                                                                    '%b. %d, %Y, %I:%M %p')

        for complaint in complaints:
            if isinstance(complaint.date_of_refusal, str):
                complaint.date_of_refusal = datetime.strptime(complaint.date_of_refusal, '%b. %d, %Y, %I:%M %p')

    except Machine.DoesNotExist:
        return render(request, '../templates/app/404.html')  # Страница 404, если машина не найдена

    context = {
        'machine': machine,
        'maintenances': maintenances,
        'complaints': complaints,
    }

    return render(request, '../templates/app/about_machine.html', context)

def index_view(request):
    """Страница для клиента (неавторизованный пользователь)"""
    form = SearchForm()
    results = []

    # Проверяем, был ли запрос методом GET
    if request.method == 'GET':
        form = SearchForm(request.GET)
        # Проверяем, была ли форма отправлена и валидна
        if form.is_valid():
            query = form.cleaned_data['query']
            # Выполняем поиск в базе данных только если форма валидна
            results = Machine.objects.filter(machine_serial_number__icontains=query)

    # Сортировка по умолчанию
    if results:
        results = results.order_by('date_of_shipment')  # Сортировка по дате отгрузки

    # Обработка авторизации
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})  # Успешная авторизация
        else:
            return JsonResponse({'success': False, 'message': 'Неверный логин или пароль.'}, status=400)

    return render(request, '../templates/app/index.html', {
        'form': form,
        'results': results,
        'user': request.user,
    })

def logout_view(request):
    """Выход из системы"""
    logout(request)
    return redirect('index')


def get_description(request):
    """Получение описания модели по типу и ID"""
    model_type = request.GET.get('model_type')
    model_id = request.GET.get('model_id')
    description = ""

    model_mapping = {
        "equipment": EquipmentModel,
        "engine": EngineModel,
        "transmission": TransmissionModel,
        "driving_bridge": DrivingBridgeModel,
        "controlled_bridge": ControlledBridgeModel,
        "maintenance_type": MaintenanceType,
        "failure_node": FailureNode,
        "recovery_method": RecoveryMethod,
        "service_company": ServiceCompany,
    }

    if model_type in model_mapping:
        try:
            model = model_mapping[model_type].objects.get(id=model_id)
            description = model.description
        except model_mapping[model_type].DoesNotExist:
            description = "Описание не найдено."

    return JsonResponse({'description': description})