document.addEventListener("DOMContentLoaded", function() {
    const scrollButton = document.getElementById('scroll-button');
    if (scrollButton) {
        scrollButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default behavior
            const target = document.getElementById('main-content');
            const headerOffset = 50; // Adjust based on navbar height
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: "smooth"
            });
        });
    }
});
