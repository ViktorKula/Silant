from django import forms
from .models import (
    Maintenance,
    Complaint,
    Machine,
)


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = [
            "maintenance_type",
            "maintenance_date",
            "operating_time",
            "work_order_number",
            "work_order_date",
            "the_organization_that_carried_out_the_maintenance",
            "machine",
            "service_company",
        ]
        widgets = {
            "maintenance_date": forms.DateInput(attrs={"type": "date"}),
            "work_order_date": forms.DateInput(attrs={"type": "date"}),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            "date_of_refusal",
            "operating_time",
            "failure_node",
            "description_of_failure",
            "recovery_method",
            "parts_used",
            "recovery_date",
            "equipment_downtime",
            "machine",
            "service_company",
        ]
        widgets = {
            "date_of_refusal": forms.DateInput(attrs={"type": "date"}),
            "recovery_date": forms.DateInput(attrs={"type": "date"}),
        }


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = [
            'serial_number_of_machine',
            'model_of_equipment',
            'model_of_engine',
            'serial_number_of_engine',
            'transmission_model',
            'serial_number_of_transmission',
            'drive_axle_model',
            'serial_number_of_drive_axle',
            'steering_axle_model',
            'serial_number_of_steering_axle',
            'supply_contract_number_and_date',
            'date_shipped_from_factory',
            'recipient',
            'delivery_address',
            'equipment',
            'client',
            'service_company',
        ]
        widgets = {
            'date_shipped_from_factory': forms.DateInput(attrs={'type': 'date'}),
        }