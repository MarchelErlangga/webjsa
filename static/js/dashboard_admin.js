function showPaymentProof(imageSrc) {
    var modalHtml = `
        <div id="paymentProofModal" class="payment-proof-modal">
            <div class="modal-overlay"></div>
            <div class="modal-container">
                <div class="modal-header">
                    <h3>Bukti Pembayaran</h3>
                    <button class="close-btn" onclick="closePaymentProofModal()">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="image-container">
                        <img src="${imageSrc}" alt="Bukti Pembayaran" class="payment-proof-image">
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="close-modal-btn" onclick="closePaymentProofModal()">Tutup</button>
                    <a href="${imageSrc}" download class="download-btn">
                        Download
                    </a>
                </div>
            </div>
        </div>
    `;

    $('body').append(modalHtml);

    // Tambahkan event listener untuk menutup modal saat klik di luar
    $('#paymentProofModal .modal-overlay').on('click', closePaymentProofModal);

    // Tambahkan event listener untuk tombol Escape
    $(document).on('keydown', function (e) {
        if (e.key === "Escape") {
            closePaymentProofModal();
        }
    });
}

function closePaymentProofModal() {
    // Hapus event listener sebelum menghapus modal
    $(document).off('keydown');
    $('#paymentProofModal').remove();
}

$(document).ready(function () {
    // Otomatis hilangkan alert setelah 5 detik
    setTimeout(function () {
        $('.alert').alert('close');
    }, 5000);
});





// Get modal elements
const signOutModal = document.getElementById('signOutModal');
const signOutLink = document.querySelector('.navigation li:last-child a');
const closeSignOutModal = document.querySelector('#signOutModal .close');
const confirmSignOut = document.getElementById('confirmSignOut');
const cancelSignOut = document.getElementById('cancelSignOut');

// Show modal when Sign Out is clicked
signOutLink.addEventListener('click', (e) => {
    e.preventDefault(); // Prevent default link behavior
    signOutModal.style.display = 'block';
});

// Close modal when X or Cancel is clicked
closeSignOutModal.addEventListener('click', () => {
    signOutModal.style.display = 'none';
});
cancelSignOut.addEventListener('click', () => {
    signOutModal.style.display = 'none';
});

// Handle confirmation
confirmSignOut.addEventListener('click', () => {
    // Redirect to the sign-out action or perform a logout
    window.location.href = '/logout'; // Replace with your logout URL
});

// Close modal when clicking outside of it
window.addEventListener('click', (e) => {
    if (e.target === signOutModal) {
        signOutModal.style.display = 'none';
    }
});
