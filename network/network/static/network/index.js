document.addEventListener("DOMContentLoaded", () => {
    let followButton = document.querySelector("#follow, #unfollow");

    if (!followButton) {
        return;
    }
    
    followButton.addEventListener("click", (e) => {
        e.preventDefault();

        const username = followButton.dataset.username;

        fetch(`/profile/${username}/follow/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(res => res.json())
        .then(data => {
            document.querySelector("#followers-count").textContent = `Followers: ${data.followers_count}`;

            if (followButton.id === "follow") {
                followButton.id = "unfollow";
                followButton.textContent = "Unfollow";
                followButton.classList.replace("btn-primary", "btn-secondary");
            } 
            else if (followButton.id === "unfollow") {
                followButton.id = "follow";
                followButton.textContent = "Follow";
                followButton.classList.replace("btn-secondary", "btn-primary");
            }
        })
        .catch(err => console.error(err));
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
