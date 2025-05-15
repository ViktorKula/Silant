from rest_framework import serializers
from app.models import (
    Machine, Maintenance, Complaints,
    EquipmentModel, EngineModel, TransmissionModel,
    DrivingBridgeModel, ControlledBridgeModel,
    ServiceCompany, MaintenanceType, FailureNode, RecoveryMethod
)

class EquipmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentModel
        fields = ['id', 'title']  # Укажите необходимые поля

class EngineModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineModel
        fields = ['id', 'title']

class TransmissionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmissionModel
        fields = ['id', 'title']

class DrivingBridgeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrivingBridgeModel
        fields = ['id', 'title']

class ControlledBridgeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlledBridgeModel
        fields = ['id', 'title']

class ServiceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCompany
        fields = ['id', 'title']

class MaintenanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceType
        fields = ['id', 'title']

class FailureNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FailureNode
        fields = ['id', 'title']

class RecoveryMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecoveryMethod
        fields = ['id', 'title']

class MachineSerializer(serializers.ModelSerializer):
    model_of_equipment = EquipmentModelSerializer()
    engine_model = EngineModelSerializer()
    transmission_model = TransmissionModelSerializer()
    model_of_the_drivig_bridge = DrivingBridgeModelSerializer()
    model_of_a_controlled_bridge = ControlledBridgeModelSerializer()
    service_company = ServiceCompanySerializer()

    class Meta:
        model = Machine
        fields = [
            'id', 'machine_serial_number', 'model_of_equipment', 'engine_model',
            'engine_serial_number', 'transmission_model', 'transmission_serial_number',
            'model_of_the_drivig_bridge', 'driving_bridge_serial_number',
            'model_of_a_controlled_bridge', 'controlled_bridge_serial_number',
            'date_of_shipment', 'consignee', 'delivery_address', 'equipment', 'client', 'service_company'
        ]

class MaintenanceSerializer(serializers.ModelSerializer):
    machine = MachineSerializer()
    type_of_maintenance = MaintenanceTypeSerializer()
    service_company = ServiceCompanySerializer()

    class Meta:
        model = Maintenance
        fields = [
            'id', 'machine', 'type_of_maintenance', 'date_of_maintenance',
            'maintenance_development', 'order_number', 'order_date', 'service_company'
        ]

class ComplaintsSerializer(serializers.ModelSerializer):
    machine = MachineSerializer()
    failure_node = FailureNodeSerializer()
    recovery_method = RecoveryMethodSerializer()

    class Meta:
        model = Complaints
        fields = [
            'id', 'machine', 'date_of_refusal', 'complaints_development',
            'failure_node', 'description_of_the_failure', 'recovery_method',
            'used_spare_parts', 'date_of_restoration', 'machine_downtime', 'service_company'
        ]