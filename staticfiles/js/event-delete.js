document.addEventListener("DOMContentLoaded", function() {
    const deleteModal = document.getElementById("delete-modal");
    const deleteBtn = document.getElementById("delete-item-btn");
    const closeDeleteBtns = document.getElementsByClassName("close-btn");
    const cancelDeleteBtn = document.getElementById("cancel-delete-btn");
    const confirmDeleteBtn = document.getElementById("confirm-delete-btn");
    // Disable scrolling when modal is open
    function disableScrolling() {
        document.body.style.overflow = "hidden";
    }

    // Enable scrolling when modal is closed
    function enableScrolling() {
        document.body.style.overflow = "auto";
    }

    // Open modal
    function openModal(modalElement) {
        modalElement.style.display = "block";
        disableScrolling();
    }

    // Close modal
    function closeModal(modalElement) {
        modalElement.style.display = "none";
        enableScrolling();
    }

    // Open the delete modal when the delete button is clicked
    deleteBtn.onclick = function(event) {
        event.preventDefault();
        openModal(deleteModal);
    };

    // Close modal when clicking the close button
    for (let closeBtn of closeDeleteBtns) {
        closeBtn.onclick = function() {
            closeModal(deleteModal);
        };
    }

    // Close modal when clicking the cancel button
    cancelDeleteBtn.onclick = function() {
        closeModal(deleteModal);
    };

    // Confirm the deletion and send the request
    confirmDeleteBtn.onclick = function() {
        const csrfToken = confirmDeleteBtn.getAttribute('data-csrf-token');  // Get CSRF token
        const itemId = confirmDeleteBtn.getAttribute('data-item-id'); // Get item ID
        const itemSlug = confirmDeleteBtn.getAttribute('data-item-slug'); // Get item slug
        const redirectUrl = "/events/display_events/";

        // Send the deletion request using fetch
        fetch(`/events/${itemId}/${itemSlug}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,  // Include CSRF token in the headers
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                item_id: itemId,
            })
        })
        .then(response => {
            if (response.ok) {
                window.location.href = redirectUrl;  // Redirect after successful deletion
            } else {
                console.error('Error during deletion');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

        closeModal(deleteModal);  // Close the modal after confirming
    };

    // Close modal when clicking outside of it
    window.onclick = function(event) {
        if (event.target === deleteModal) {
            closeModal(deleteModal);
        }
    };
});
