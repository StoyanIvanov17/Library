document.addEventListener("DOMContentLoaded", function() {
    const deleteModal = document.getElementById("delete-modal");
    const deleteBtn = document.getElementById("delete-item-btn");
    const closeDeleteBtns = document.getElementsByClassName("close-btn");
    const cancelDeleteBtn = document.getElementById("cancel-delete-btn");
    const confirmDeleteBtn = document.getElementById("confirm-delete-btn");

    function disableScrolling() {
        document.body.style.overflow = "hidden";
    }

    function enableScrolling() {
        document.body.style.overflow = "auto";
    }

    function openModal(modalElement) {
        modalElement.style.display = "block";
        disableScrolling();
    }

    function closeModal(modalElement) {
        modalElement.style.display = "none";
        enableScrolling();
    }

    deleteBtn.onclick = function (event) {
        event.preventDefault();
        openModal(deleteModal);
    }

    for (let closeBtn of closeDeleteBtns) {
        closeBtn.onclick = function () {
            closeModal(deleteModal);
        }
    }

    cancelDeleteBtn.onclick = function () {
        closeModal(deleteModal);
    }

    confirmDeleteBtn.onclick = function () {
        const csrfToken = confirmDeleteBtn.getAttribute('data-csrf-token');
        const itemId = confirmDeleteBtn.getAttribute('data-item-id');
        const itemSlug = confirmDeleteBtn.getAttribute('data-item-slug');
        const redirectUrl = "/collections/display_items/";

        fetch(`/collections/${itemId}/${itemSlug}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
            .then(response => {
                if (response.ok) {
                    window.location.href = redirectUrl;
                } else {
                    console.error('Error during deletion');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    window.onclick = function (event) {
        if (event.target === deleteModal) {
            closeModal(deleteModal);
        }
    };
});