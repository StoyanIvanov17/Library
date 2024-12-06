document.addEventListener("DOMContentLoaded", function() {
    const sampleModal = document.getElementById("sample-modal");
    const openSampleBtn = document.getElementById("open-sample-btn");
    const sampleTextContainer = document.getElementById("sample-text-container");
    const pageSize = 500;
    let pages = [];
    let currentPage = 0;

    const sampleText = openSampleBtn.getAttribute("data-sample-text");

    function paginateSampleText(text, pageSize) {
        let words = text.split(' ');
        let pagesArray = [];
        let currentPageText = '';

        words.forEach(word => {
            if ((currentPageText + word + ' ').length > pageSize) {
                pagesArray.push(currentPageText.trim());
                currentPageText = word + ' ';
            } else {
                currentPageText += word + ' ';
            }
        });

        if (currentPageText.trim().length > 0) {
            pagesArray.push(currentPageText.trim());
        }

        return pagesArray;
    }

    function updateSampleText() {
        sampleTextContainer.innerHTML = `<p>${pages[currentPage]}</p>`;
        document.getElementById("current-page").textContent = `Page ${currentPage + 1} of ${pages.length}`;
        document.getElementById("prev-page-btn").disabled = currentPage === 0;
        document.getElementById("next-page-btn").disabled = currentPage === pages.length - 1;
    }

    function openSampleModal(event) {
        event.preventDefault();
        pages = paginateSampleText(sampleText, pageSize);
        currentPage = 0;
        updateSampleText();
        openModal(sampleModal);
    }

    document.getElementById("prev-page-btn").addEventListener("click", function() {
        if (currentPage > 0) {
            currentPage--;
            updateSampleText();
        }
    });

    document.getElementById("next-page-btn").addEventListener("click", function() {
        if (currentPage < pages.length - 1) {
            currentPage++;
            updateSampleText();
        }
    });

    openSampleBtn.addEventListener("click", openSampleModal);

    const closeBtn = document.querySelector(".close-btn");

    closeBtn.onclick = function() {
    sampleModal.style.display = "none";
    document.body.classList.remove("no-scroll");
    document.getElementById("delete-modal").style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target === sampleModal) {
            sampleModal.style.display = "none";
            document.body.classList.remove("no-scroll");
        }
    };
});

function openModal(modal) {
    modal.style.display = "block";
    document.body.classList.add("no-scroll");
}