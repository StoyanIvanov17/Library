document.addEventListener("DOMContentLoaded", function () {
    const items = document.querySelectorAll('.profile-item');
    const events = document.querySelectorAll('.profile-event');
    const modal = document.getElementById('profile-modal');
    const closeBtn = document.querySelector('.profile-close');
    const modalImage = document.querySelector('.profile-modal-image');
    const modalTitle = document.querySelector('.profile-modal-title');
    const modalLink = document.querySelector('.profile-modal-link');

    function openModal(title, image, link) {
        modal.style.display = "flex";
        modalTitle.textContent = title;
        modalImage.src = image;
        modalLink.href = link;
        document.body.classList.add("no-scroll");
    }

    items.forEach(item => {
        item.addEventListener('click', function () {
            const [id, title, link, image] = item.dataset.item.split('|');
            openModal(title, image, link);
        });
    });

    events.forEach(event => {
        event.addEventListener('click', function () {
            const [id, title, link, image] = event.dataset.event.split('|');
            openModal(title, image, link);
        });
    });

    closeBtn.addEventListener('click', function () {
        modal.style.display = "none";
        document.body.classList.remove("no-scroll");
    });

    window.addEventListener('click', function (e) {
        if (e.target === modal) {
            modal.style.display = "none";
            document.body.classList.remove("no-scroll");
        }
    });
});
