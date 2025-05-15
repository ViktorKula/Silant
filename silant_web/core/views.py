from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseNotAllowed

from django.views.generic import (
    CreateView,
    UpdateView,
)

from .models import (
    Machine,
    Client,
    Maintenance,
    EquipmentModel,
    EngineModel,
    TransmissionModel,
    DriveAxleModel,
    SteeringAxleModel,
    ServiceCompany,
    MaintenanceType,
    FailureNode,
    RecoveryMethod,
    Complaint,
    TheOrganizationThatCarriedOutTheMaintenance,
)

from .forms import (
    MaintenanceForm,
    ComplaintForm,
    MachineForm,
)


from .filters import (
    MachineFilter,
    MaintenanceFilter,
    ComplaintFilter,
)

# Create your views here.


def unauthorized_index(request):
    if request.user.is_authenticated:
        return redirect("machine_list")

    if request.method == "POST":
        serial_number = request.POST.get("serial_number")
        machine = (
            Machine.objects.filter(serial_number_of_machine=serial_number)
            .values(
                "serial_number_of_machine",
                "model_of_equipment",
                "model_of_engine",
                "serial_number_of_engine",
                "transmission_model",
                "serial_number_of_transmission",
                "drive_axle_model",
                "serial_number_of_drive_axle",
                "steering_axle_model",
                "serial_number_of_steering_axle",
            )
            .first()
        )

        model_of_equipment_name = (
            EquipmentModel.objects.filter(id=machine["model_of_equipment"])
            .values("id", "name")
            .first()
        )

        model_of_engine_name = (
            EngineModel.objects.filter(id=machine["model_of_engine"])
            .values("id", "name")
            .first()
        )

        model_of_transmission_name = (
            TransmissionModel.objects.filter(id=machine["transmission_model"])
            .values("id", "name")
            .first()
        )

        model_of_drive_axle_name = (
            DriveAxleModel.objects.filter(id=machine["drive_axle_model"])
            .values("id", "name")
            .first()
        )

        model_of_steering_axle_name = (
            SteeringAxleModel.objects.filter(id=machine["steering_axle_model"])
            .values("id", "name")
            .first()
        )

        if (
            machine
            and model_of_equipment_name
            and model_of_engine_name
            and model_of_transmission_name
            and model_of_drive_axle_name
            and model_of_steering_axle_name
        ):
            return render(
                request,
                "main/index.html",
                {
                    "machine": machine,
                    "model_of_equipment_name": model_of_equipment_name["name"],
                    "model_of_equipment_id": model_of_equipment_name["id"],
                    "model_of_engine_name": model_of_engine_name["name"],
                    "model_of_engine_id": model_of_engine_name["id"],
                    "model_of_transmission_name": model_of_transmission_name["name"],
                    "model_of_transmission_id": model_of_transmission_name["id"],
                    "model_of_drive_axle_name": model_of_drive_axle_name["name"],
                    "model_of_drive_axle_id": model_of_drive_axle_name["id"],
                    "model_of_steering_axle_name": model_of_steering_axle_name["name"],
                    "model_of_steering_axle_id": model_of_steering_axle_name["id"],
                },
            )
        else:
            return render(request, "main/index.html", {"error_message": "Not found"})
    return render(request, "main/index.html")


@login_required
@permission_required("core.view_machine", raise_exception=True)
def machine_list(request):
    user_id = request.user.id
    can_add_machine = request.user.has_perm("core.add_machine")
    can_update_machine = request.user.has_perm("core.change_machine")
    can_delete_machine = request.user.has_perm("core.delete_machine")
    client = None
    username = request.user.first_name

    try:
        client = Client.objects.get(user_id=user_id)
    except Client.DoesNotExist:
        try:
            service_company = ServiceCompany.objects.get(user_id=user_id)
        except ServiceCompany.DoesNotExist:
            client = username
            machines = Machine.objects.all()
            machine_filter = MachineFilter(request.GET, queryset=machines)

            return render(
                request,
                "machine/machine_list.html",
                {
                    "machines": machines,
                    "filter": machine_filter,
                    "can_add_machine": can_add_machine,
                    "can_update_machine": can_update_machine,
                    "can_delete_machine": can_delete_machine,
                    "client": client,
                    "username": username,
                },
            )
        client = username
        machines = Machine.objects.filter(service_company_id=service_company.id)
        machine_filter = MachineFilter(request.GET, queryset=machines)

        return render(
            request,
            "machine/machine_list.html",
            {
                "machines": machines,
                "filter": machine_filter,
                "can_add_machine": can_add_machine,
                "can_update_machine": can_update_machine,
                "can_delete_machine": can_delete_machine,
                "client": client,
                "username": username,
            },
        )

    machines = Machine.objects.filter(client=client)
    machine_filter = MachineFilter(request.GET, queryset=machines)

    return render(
        request,
        "machine/machine_list.html",
        {
            "machines": machines,
            "client": client,
            "filter": machine_filter,
            "can_add_machine": can_add_machine,
            "can_update_machine": can_update_machine,
            "can_delete_machine": can_delete_machine,
        },
    )


@login_required
@permission_required("core.delete_machine", raise_exception=True)
def machine_delete(request, machine_id):
    if request.method == "DELETE":
        try:
            machine = Machine.objects.get(id=machine_id)
            if request.user.has_perm("core.delete_machine"):
                machine.delete()
                return JsonResponse({"success": True})
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Недостаточно прав для удаления машины.",
                    },
                    status=403,
                )
        except Machine.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Машина не найдена."}, status=404
            )
    return HttpResponseNotAllowed(["DELETE"])


@login_required
@permission_required("core.view_machine", raise_exception=True)
@permission_required("core.view_maintenance", raise_exception=True)
def machine_detail(request, machine_id):
    client = None
    username = request.user.first_name

    try:
        machine = Machine.objects.get(id=machine_id)
    except Machine.DoesNotExist:
        return redirect("machine_list")

    try:
        client = Client.objects.get(user_id=request.user.id)
    except Client.DoesNotExist:
        client = username

    maintenances = Maintenance.objects.filter(machine_id=machine_id)
    maintenances_filter = MaintenanceFilter(request.GET, queryset=maintenances)

    return render(
        request,
        "machine/machine_detail.html",
        {
            "machine": machine,
            "maintenances": maintenances,
            "username": username,
            "client": client,
            "filter": maintenances_filter,
        },
    )


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("core.add_machine", raise_exception=True), name="dispatch"
)
class MachineCreateView(CreateView):
    form_class = MachineForm
    model = Machine
    template_name = "machine/machine_create.html"
    success_url = "/machines/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.first_name
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("core.change_machine", raise_exception=True), name="dispatch"
)
class MachineUpdateView(UpdateView):
    form_class = MachineForm
    model = Machine
    template_name = "machine/machine_create.html"
    success_url = "/machines/"


@login_required
@permission_required("core.view_maintenance", raise_exception=True)
def maintenance_list(request):
    client = None
    username = request.user.first_name
    service_company = None

    can_add_maintenances = request.user.has_perm("core.add_maintenance")
    can_update_maintenance = request.user.has_perm("core.change_maintenance")
    can_delete_maintenance = request.user.has_perm("core.delete_maintenance")

    try:
        client = Client.objects.get(user_id=request.user.id)
    except Client.DoesNotExist:
        try:
            service_company = ServiceCompany.objects.get(user_id=request.user.id)
        except ServiceCompany.DoesNotExist:
            maintenances = Maintenance.objects.all()
            maintenances_filter = MaintenanceFilter(request.GET, queryset=maintenances)

            return render(
                request,
                "maintenance/maintenance_list.html",
                {
                    "maintenances": maintenances,
                    "filter": maintenances_filter,
                    "can_add_maintenance": can_add_maintenances,
                    "can_update_maintenance": can_update_maintenance,
                    "can_delete_maintenance": can_delete_maintenance,
                    "username": username,
                    "client": client,
                },
            )

        client = username
        maintenances = Maintenance.objects.filter(service_company_id=service_company.id)
        maintenances_filter = MaintenanceFilter(request.GET, queryset=maintenances)

        return render(
            request,
            "maintenance/maintenance_list.html",
            {
                "maintenances": maintenances,
                "filter": maintenances_filter,
                "can_add_maintenance": can_add_maintenances,
                "can_update_maintenance": can_update_maintenance,
                "can_delete_maintenance": can_delete_maintenance,
                "username": username,
                "client": client,
            },
        )
    client_machines = Machine.objects.filter(client=client)
    maintenances = Maintenance.objects.filter(machine__in=client_machines)
    maintenances_filter = MaintenanceFilter(request.GET, queryset=maintenances)

    return render(
        request,
        "maintenance/maintenance_list.html",
        {
            "maintenances": maintenances,
            "client": client,
            "filter": maintenances_filter,
            "can_add_maintenance": can_add_maintenances,
            "can_update_maintenance": can_update_maintenance,
            "can_delete_maintenance": can_delete_maintenance,
        },
    )


@login_required
@permission_required("core.delete_maintenance", raise_exception=True)
def maintenance_delete(request, maintenance_id):
    if request.method == "DELETE":
        try:
            maintenance = Maintenance.objects.get(id=maintenance_id)
            if request.user.has_perm("core.delete_maintenance"):
                maintenance.delete()
                return JsonResponse({"success": True})
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Не хватает прав для удаления обслуживания",
                    },
                    status=403,
                )
        except Maintenance.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Обслуживание не найдено"}, status=404
            )
    return HttpResponseNotAllowed(["DELETE"])


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("core.add_maintenance", raise_exception=True), name="dispatch"
)
class MaintenanceCreateView(CreateView):
    form_class = MaintenanceForm
    model = Maintenance
    template_name = "maintenance/maintenance_create.html"
    success_url = "/maintenances/"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        try:
            client = Client.objects.get(user=self.request.user)

            form.fields["machine"].queryset = Machine.objects.filter(client=client)
        except Client.DoesNotExist:
            pass

        try:
            service_company = ServiceCompany.objects.get(user=self.request.user)
            form.fields["service_company"].queryset = ServiceCompany.objects.filter(id=service_company.id)
        except ServiceCompany.DoesNotExist:
            pass

        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.first_name
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("core.change_maintenance", raise_exception=True),
    name="dispatch",
)
class MaintenanceUpdateView(UpdateView):
    form_class = MaintenanceForm
    model = Maintenance
    template_name = "maintenance/maintenance_create.html"
    success_url = "/maintenances/"


@login_required
@permission_required("core.view_complaint", raise_exception=True)
def complaints_list(request):
    can_add_complaints = request.user.has_perm("core.add_complaint")
    can_update_complaints = request.user.has_perm("core.change_complaint")
    can_delete_complaints = request.user.has_perm("core.delete_complaint")
    client = None
    username = request.user.first_name

    try:
        client = Client.objects.get(user_id=request.user.id)
    except Client.DoesNotExist:
        try: 
            service_company = ServiceCompany.objects.get(user_id=request.user.id)
        except ServiceCompany.DoesNotExist:
            complaints = Complaint.objects.all()
            complaints_filter = ComplaintFilter(request.GET, queryset=complaints)

            return render(
                request,
                "complaints/complaints_list.html",
                {
                    "complaints": complaints,
                    "filter": complaints_filter,
                    "can_add_complaint": can_add_complaints,
                    "can_update_complaint": can_update_complaints,
                    "can_delete_complaint": can_delete_complaints,
                    "username": username,
                    "client": client,
                },
            )
        
        client = username
        complaints = Complaint.objects.filter(service_company_id=service_company.id)
        complaints_filter = ComplaintFilter(request.GET, queryset=complaints)

        return render(
            request,
            "complaints/complaints_list.html",
            {
                "complaints": complaints,
                "filter": complaints_filter,
                "can_add_complaint": can_add_complaints,
                "can_update_complaint": can_update_complaints,
                "can_delete_complaint": can_delete_complaints,
                "username": username,
                "client": client,
            },
        )
    client_machines = Machine.objects.filter(client=client)
    complaints = Complaint.objects.filter(machine__in=client_machines)
    complaints_filter = ComplaintFilter(request.GET, queryset=complaints)

    return render(
        request,
        "complaints/complaints_list.html",
        {
            "complaints": complaints,
            "client": client,
            "filter": complaints_filter,
            "can_add_complaint": can_add_complaints,
            "can_update_complaint": can_update_complaints,
            "can_delete_complaint": can_delete_complaints,
        },
    )


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("core.add_complaint", raise_exception=True), name="dispatch"
)
class ComplaintCreateView(CreateView):
    form_class = ComplaintForm
    model = Complaint
    template_name = "complaints/complaint_create.html"
    success_url = "/complaints/"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        try:
            service_company = ServiceCompany.objects.get(user=self.request.user)
            form.fields["service_company"].queryset = ServiceCompany.objects.filter(id=service_company.id)
        except ServiceCompany.DoesNotExist:
            pass

        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.first_name
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(
    permission_required("core.change_complaint", raise_exception=True),
    name="dispatch",
)
class ComplaintUpdateView(UpdateView):
    form_class = ComplaintForm
    model = Complaint
    template_name = "complaints/complaint_create.html"
    success_url = "/complaints/"

@login_required
@permission_required("core.delete_complaint", raise_exception=True)
def complaint_delete(request, complaint_id):
    if request.method == "DELETE":
        try:
            complaint = Complaint.objects.get(id=complaint_id)
            if request.user.has_perm("core.delete_complaint"):
                complaint.delete()
                return JsonResponse({"success": True})
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "Не хватает прав для удаления рекламации",
                    },
                    status=403,
                )
        except Complaint.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Рекламация не найдена"}, status=404
            )
    return HttpResponseNotAllowed(["DELETE"])

def equipment_model_info(request, equipment_model_id):
    if request.method == "GET":
        try:
            equipment_model_info = EquipmentModel.objects.get(id=equipment_model_id)
            data = {
                "name": equipment_model_info.name,
                "description": equipment_model_info.description
            }
            return JsonResponse(data)
        except EquipmentModel.DoesNotExist:
            return JsonResponse({"success": False, "error": "Модель не найдена"}, status=404)
    return HttpResponseNotAllowed(["GET"])


def engine_model_info(request, engine_model_id):
    if request.method == "GET":
        try:
            engine_model_info = EngineModel.objects.get(id=engine_model_id)
            data = {
                "name": engine_model_info.name,
                "description": engine_model_info.description
            }
            return JsonResponse(data)
        except EngineModel.DoesNotExist:
            return JsonResponse({"success": False, "error": "Модель не найдена"}, status=404)
    return HttpResponseNotAllowed(["GET"])


def transmission_model_info(request, transmission_model_id):
    if request.method == "GET":
        try:
            transmission_model_info = TransmissionModel.objects.get(id=transmission_model_id)
            data = {
                "name": transmission_model_info.name,
                "description": transmission_model_info.description
            }
            return JsonResponse(data)
        except EngineModel.DoesNotExist:
            return JsonResponse({"success": False, "error": "Модель не найдена"}, status=404)
    return HttpResponseNotAllowed(["GET"])


def drive_axle_model_info(request, drive_axle_model_id):
    if request.method == "GET":
        try:
            drive_axle_model_info = DriveAxleModel.objects.get(id=drive_axle_model_id)
            data = {
                "name": drive_axle_model_info.name,
                "description": drive_axle_model_info.description
            }
            return JsonResponse(data)
        except EngineModel.DoesNotExist:
            return JsonResponse({"success": False, "error": "Модель не найдена"}, status=404)
    return HttpResponseNotAllowed(["GET"])


def steering_axle_model_info(request, steering_axle_model_id):
    if request.method == "GET":
        try:
            steering_axle_model_info = SteeringAxleModel.objects.get(id=steering_axle_model_id)
            data = {
                "name": steering_axle_model_info.name,
                "description": steering_axle_model_info.description
            }
            return JsonResponse(data)
        except EngineModel.DoesNotExist:
            return JsonResponse({"success": False, "error": "Модель не найдена"}, status=404)
    return HttpResponseNotAllowed(["GET"])


def client_info(request, client_id):
    if request.method == "GET":
        try:
            client_info = Client.objects.get(id=client_id)
            data = {
                "name": client_info.name,
                "description": client_info.description
            }
            return JsonResponse(data)
        except Client.DoesNotExist:
            return JsonResponse({"success": False, "error": "Клиент не найден"}, status=404)
    return HttpResponseNotAllowed(["GET"])


def service_company_info(request, service_company_id):
    if request.method == "GET":
        try:
            service_company_info = ServiceCompany.objects.get(id=service_company_id)
            data = {
                "name": service_company_info.name,
                "description": service_company_info.description
            }
            return JsonResponse(data)
        except ServiceCompany.DoesNotExist:
            return JsonResponse({"success": False, "error": "Компания не найдена"}, status=404)
    return HttpResponseNotAllowed(["GET"])


def maintenance_type_info(request, maintenance_type_id):
    if request.method == "GET":
        try:
            maintenance_type_info = MaintenanceType.objects.get(id=maintenance_type_id)
            data = {
                "name": maintenance_type_info.name,
                "description": maintenance_type_info.description
            }
            return JsonResponse(data)
        except MaintenanceType.DoesNotExist:
            return JsonResponse({"success": False, "error": "Тип не найден"}, status=404)
    return HttpResponseNotAllowed(["GET"])


def failure_node_info(request, failure_node_id):
    if request.method == "GET":
        try:
            failure_node_info = FailureNode.objects.get(id=failure_node_id)
            data = {
                "name": failure_node_info.name,
                "description": failure_node_info.description
            }
            return JsonResponse(data)
        except FailureNode.DoesNotExist:
            return JsonResponse({"success": False, "error": "Узел не найден"}, status=404)
    return HttpResponseNotAllowed(["GET"])


def recovery_method_info(request, recovery_method_id):
    if request.method == "GET":
        try:
            recovery_method_info = RecoveryMethod.objects.get(id=recovery_method_id)
            data = {
                "name": recovery_method_info.name,
                "description": recovery_method_info.description
            }
            return JsonResponse(data)
        except RecoveryMethod.DoesNotExist:
            return JsonResponse({"success": False, "error": "Метод восстановления не найден"}, status=404)
    return HttpResponseNotAllowed(["GET"])

def the_organization_that_carried_out_the_maintenance_info(request, organization_id):
    if request.method == "GET":
        try:
            the_organization_that_carried_out_the_maintenance_info = TheOrganizationThatCarriedOutTheMaintenance.objects.get(id=organization_id)
            data = {
                "name": the_organization_that_carried_out_the_maintenance_info.name,
                "description": the_organization_that_carried_out_the_maintenance_info.description
            }
            return JsonResponse(data)
        except TheOrganizationThatCarriedOutTheMaintenance.DoesNotExist:
            return JsonResponse({"success": False, "error": "Организация не найдена"}, status=404)
    return HttpResponseNotAllowed(["GET"])