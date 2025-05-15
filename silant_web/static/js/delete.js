function showDeleteModal(deleteUrl, itemName, csrfToken) {
    document.getElementById("item-name").textContent = `Вы действительно хотите удалить "${itemName}"?`;
    document.getElementById("delete-modal").style.display = "block";

    document.getElementById("confirm-delete").addEventListener("click", () => {
        fetch(deleteUrl, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error("Ошибка при удалении:", error);
            alert("Произошла ошибка при попытке удаления");
        });
    });

    document.getElementById("cancel-delete").addEventListener("click", () => {
        document.getElementById("delete-modal").style.display = "none";
    });

    document.getElementById('close-button-modal-delete').addEventListener("click", () => {
        document.getElementById("delete-modal").style.display = "none";
    });
}

document.querySelectorAll(".delete-machine-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const machineId = btn.dataset.machineId;
        const machineName = btn.closest("tr").querySelector("td:nth-child(1)").textContent.trim();
        const csrfToken = btn.dataset.machineToken;
        showDeleteModal(`/machines/delete/${machineId}/`, machineName, csrfToken);
    });
});

document.querySelectorAll(".delete-maintenance-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const maintenanceId = btn.dataset.maintenanceId;
        const maintenanceName = btn.closest("tr").querySelector("td:nth-child(1)").textContent.trim();
        const csrfToken = btn.dataset.maintenanceToken;
        showDeleteModal(`/maintenances/delete/${maintenanceId}/`, maintenanceName, csrfToken);
    });
})

document.querySelectorAll(".delete-complaint-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const complaintId = btn.dataset.complaintId;
        const complaintName = btn.closest("tr").querySelector("td:nth-child(1)").textContent.trim();
        const csrfToken = btn.dataset.complaintToken;
        showDeleteModal(`/complaints/delete/${complaintId}/`, complaintName, csrfToken);
    });
})