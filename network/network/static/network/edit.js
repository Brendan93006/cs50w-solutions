document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("click", (e) => {
        const edit = e.target.closest(".edit"); 
        
        if (!edit) return;

        e.preventDefault();

        const postId = edit.dataset.postId;

        const editorContainer = document.querySelector(`#text-editor-${postId}`);

        if (editorContainer.querySelector("textarea")) return;

        edit.style.display = "none";

        let textEditor = document.createElement("textarea");

        let saveButton = document.createElement("button");

        saveButton.textContent = "Save";
        
        textEditor.value = document.querySelector(`#content-${postId}`).textContent;

        editorContainer.append(textEditor, saveButton);

        saveButton.addEventListener("click", () => {

            const content = textEditor.value;
            
            edit.style.display = "block";

            textEditor.remove();

            saveButton.remove();

            fetch(`/${postId}/edit/`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    content: content
                })
            })
            .then(res => res.json())
            .then(data => {
                document.querySelector(`#content-${postId}`).textContent = content;
            })
            .catch(() => {
                alert("Save failed");
            });
        });
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