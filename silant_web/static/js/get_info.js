const currentUrl = window.location.href;

function showSummaryModal(summaryUrl) {
    document.getElementById("summary-modal").style.display = "block";
    fetch(summaryUrl).then(response => response.json()).then(data => {
        if (data) {
            document.getElementById("object-name").innerHTML = data.name;
            document.getElementById("object-description").innerHTML = data.description;
        } else {
            alert("Произошла ошибка при получении информации");
        }
    })

    document.getElementById("close-modal").addEventListener("click", () => {
        document.getElementById("summary-modal").style.display = "none";
    });

    document.getElementById('close-button-modal-info').addEventListener("click", () => {
        document.getElementById("summary-modal").style.display = "none";
    });
}

const buttonInit = (button, includePath, urlPath) => {
    if (currentUrl.includes(includePath)) {
        let summaryUrl = `${urlPath}${button.dataset.objectId}`;
        showSummaryModal(summaryUrl);
    } else {
        let summaryUrl = `${includePath}${urlPath}${button.dataset.objectId}`;
        showSummaryModal(summaryUrl);
    }
}

document.querySelectorAll(".model-of-equipment").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'machines/', 'equipment_model_info/'));
})

document.querySelectorAll(".model-of-engine").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'machines/', 'engine_model_info/'));
})

document.querySelectorAll(".model-of-transmission").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'machines/', 'transmission_model_info/'));
})

document.querySelectorAll(".model-of-drive-axle").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'machines/', 'drive_axle_model_info/'));
})

document.querySelectorAll(".model-of-steering-axle").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'machines/', 'steering_axle_model_info/'));
})

document.querySelectorAll(".client-info").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'machines/', 'client_info/'));
})

document.querySelectorAll(".service-company-info").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'machines/', 'service_company_info/'));
})

document.querySelectorAll(".service-company-maintenance-info").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'maintenances/', 'service_company_maintenance_info/'));
})

document.querySelectorAll(".maintenance-type-info").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'maintenances/', 'maintenance_type_info/'));
})

document.querySelectorAll(".organization-info").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'maintenances/', 'the_organization_that_carried_out_the_maintenance_info/'));
})

document.querySelectorAll(".failure-node-info").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'complaints/', 'failure_node_info/'));
})

document.querySelectorAll(".recovery-method-info").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'complaints/', 'recovery_method_info/'));
})

document.querySelectorAll(".service-company-complaint-info").forEach(button => {
    button.addEventListener("click", () => buttonInit(button, 'complaints/', 'service_company_complaint_info/'));
})