document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('.log_reg_form');
    const modal = document.getElementById('verificationModal');
    const closeModalButton = document.getElementById('closeModal');

    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    modal.style.display = 'block';
                    modal.querySelector('.verification-modal-content p').innerText = data.message;
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    if (closeModalButton) {
        closeModalButton.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }
});
