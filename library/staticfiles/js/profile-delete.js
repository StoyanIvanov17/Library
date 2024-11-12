document.addEventListener("DOMContentLoaded", function() {
    const deleteButton = document.getElementById("profile-delete-link");
    const modal = document.getElementById("profile-deletion-modal");
    const closeModal = document.querySelector(".profile-deletion-close");
    const cancelDelete = document.querySelector(".profile-deletion-cancel");

    function disableScroll() {
        document.body.style.overflow = "hidden";
    }

    function enableScroll() {
        document.body.style.overflow = "auto";
    }

    deleteButton.addEventListener("click", function(event) {
        event.preventDefault();
        modal.style.display = "block";
        disableScroll();
    });

    closeModal.onclick = function() {
        modal.style.display = "none";
        enableScroll();
    };

    cancelDelete.onclick = function() {
        modal.style.display = "none";
        enableScroll();
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
            enableScroll();
        }
    };
});
