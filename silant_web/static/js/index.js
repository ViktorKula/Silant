const complaintButton = document.getElementById('complaint-button');
const generalButton = document.getElementById('general-button');
const maintenanceButton = document.getElementById('maintenance-button');
const createMaintenanceButton = document.getElementById('create_maintenance');
const createComplaintButton = document.getElementById('create_complaint');
const createMachineButton = document.getElementById('create_machine');


if (complaintButton) {
    complaintButton.addEventListener('click', () => {
        window.location.href = '/complaints/';
    });
};

if (generalButton) {
    generalButton.addEventListener('click', () => {
        window.location.href = '/machines/';
    });
};

if (maintenanceButton) {
    maintenanceButton.addEventListener('click', () => {
        window.location.href = '/maintenances/';
    });
};

if (createMaintenanceButton) {
    createMaintenanceButton.addEventListener('click', () => {
        window.location.href = '/maintenances/create/';
    });
};

if (createComplaintButton) {
    createComplaintButton.addEventListener('click', () => {
        window.location.href = '/complaints/create/';
    });
};

if (createMachineButton) {
    createMachineButton.addEventListener('click', () => {
        window.location.href = '/machines/create/';
    });
};
