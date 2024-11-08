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

    // Open delete modal
    deleteBtn.onclick = function (event) {
        event.preventDefault();
        openModal(deleteModal);
    }

    // Close modals with close buttons
    for (let closeBtn of closeDeleteBtns) {
        closeBtn.onclick = function () {
            closeModal(deleteModal);
        }
    }

    // Cancel button closes the modal
    cancelDeleteBtn.onclick = function () {
        closeModal(deleteModal);
    }

    // Confirm delete action
    confirmDeleteBtn.onclick = function () {
        const csrfToken = confirmDeleteBtn.getAttribute('data-csrf-token');  // Get CSRF token
        const itemId = confirmDeleteBtn.getAttribute('data-item-id'); // Get item ID
        const itemSlug = confirmDeleteBtn.getAttribute('data-item-slug'); // Get item slug
        const redirectUrl = "/collections/display_items/";

        fetch(`/collections/${itemId}/${itemSlug}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
            .then(response => {
                if (response.ok) {
                    window.location.href = redirectUrl; // Redirect after successful deletion
                } else {
                    console.error('Error during deletion');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Close modal when clicking outside
    window.onclick = function (event) {
        if (event.target === deleteModal) {
            closeModal(deleteModal);
        }
    };
});