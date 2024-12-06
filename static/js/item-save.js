document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('save-item-btn').addEventListener('click', function (event) {
        const itemId = this.getAttribute('data-item-id');
        const itemSlug = this.getAttribute('data-item-slug');
        const csrfToken = this.getAttribute('data-csrf-token');
        const saveText = this.querySelector('.save-text');

        fetch(`/collections/${itemId}/${itemSlug}/save_item/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({item_id: itemId})
        })
            .then(response => response.json())
            .then(data => {
                if (data.favorited) {
                    saveText.innerHTML = 'ALREADY SAVED';
                } else {
                    saveText.innerHTML = 'SAVE TO PROFILE';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});