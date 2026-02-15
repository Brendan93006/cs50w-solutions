document.addEventListener("DOMContentLoaded", () => {

    document.addEventListener('click', (e) => {
        const deleteButton = e.target.closest(".delete-employee-btn");
        if (!deleteButton) return;
        e.preventDefault();

        const employeeId = deleteButton.dataset.employeeId;

        fetch(`/shifts/${employeeId}/delete/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(res => res.json())
        .then(data => {
            console.log(`deleted: ${data}`);
            const card = deleteButton.closest(".col-md-6, .col-lg-4, .col");
            if (card) card.remove();
        })
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}