document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".heart").forEach(heart => {
        const postId = heart.dataset.postId;

        heart.addEventListener("click", (e) => {
            e.preventDefault();

            fetch(`/${postId}/like/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(res => res.json())
            .then(data => {
                document.querySelector(`#likes-${postId}`).textContent = data.like_count;

                if (data.like) {

                    heart.innerHTML = "&#9829;";

                    heart.classList.add("filled");

                } else {

                    heart.innerHTML = "&#9825;";

                    heart.classList.remove("filled");

                }

            })
            .catch(() => {
                alert("Login required: Like failed");
            });
        })
    })
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