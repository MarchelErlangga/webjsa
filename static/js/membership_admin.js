// add hovered class to selected list item
let list = document.querySelectorAll(".navigation li");

function activeLink() {
    list.forEach((item) => {
        item.classList.remove("hovered");
    });
    this.classList.add("hovered");
}

list.forEach((item) => {
    item.addEventListener("mouseenter", activeLink);
    item.addEventListener("mouseleave", () => {
        item.classList.remove("hovered");
    });
});

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
    navigation.classList.toggle("active");
    main.classList.toggle("active");
};

// add user
const modal = document.getElementById('addMembershipModal');
const addButton = document.querySelector('.cardHeader ion-icon');
const closeButton = document.querySelector('.close');

// Show modal
addButton.addEventListener('click', () => {
    modal.style.display = 'block';
});

// Hide modal
closeButton.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Hide modal when clicking outside the modal content
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

// Ambil semua tombol "Edit" dari tabel
const editButtons = document.querySelectorAll('.status.biru.tombol');

// Ambil modal dan elemen input di dalamnya
const editMembershipModal = document.getElementById('editMembershipModal');
const editNameInput = document.getElementById('editName');
const editPhoneInput = document.getElementById('editPhone');
const editMasaBerlakuInput = document.getElementById('editMasaBerlaku');
const editStatusPembayaranInput = document.getElementById('editStatusPembayaran');
const closeModal = editMembershipModal.querySelector('.close');

// Tambahkan event untuk membuka modal dan mengisi data
editButtons.forEach(button => {
    button.addEventListener('click', function () {
        const row = this.closest('tr'); // Dapatkan baris yang terkait
        const name = row.cells[0].textContent; // Ambil teks di kolom "Nama"
        const phone = row.cells[1].textContent; // Ambil teks di kolom "No_Telp"
        const email = row.cells[2].textContent;  // Ambil email dari kolom ketiga
        const masaBerlaku = row.cells[3].textContent; // Ambil teks di kolom "Paket"
        const status = row.cells[5].textContent; // Ambil teks di kolom "Status"

        // Isi input modal dengan data
        editNameInput.value = name;
        editPhoneInput.value = phone;
        document.getElementById('editEmail').value = email;  // Set email

        // editMasaBerlakuInput.value = masaBerlaku;
        // editStatusInput.value = status;

        // Set masa berlaku dropdown berdasarkan data masa berlaku
        $('#editMasaBerlaku').val(masaBerlaku.toLowerCase()); // Set nilai masa berlaku dropdown

        // Set status dropdown berdasarkan data status
        $('#editStatusPembayaran').val(status.toLowerCase()); // Set nilai status dropdown

        // Tampilkan modal
        editMembershipModal.style.display = 'block';
    });
});

$(document).ready(function () {
    // Event handler untuk tombol close
    $('.close').on('click', function () {
        console.log('Tombol close diklik');
        $('#editMembershipModal').hide();
    });

    // Tutup modal ketika area luar modal diklik
    $(window).on('click', function (event) {
        if (event.target.id === 'editMembershipModal') {
            $('#editMembershipModal').hide();
        }
    });

    // Form submit
    $('#editMembershipForm').on('submit', function (event) {
        event.preventDefault(); // Mencegah pengiriman form default

        const fullName = $('#editName').val();
        const phone = $('#editPhone').val();
        const email = $('#editEmail').val();
        const membershipPlan = $('#editMasaBerlaku').val();
        const status = $('#editStatusPembayaran').val();

        // AJAX request
        $.ajax({
            type: 'POST',
            url: '/api/edit_membership',
            data: {
                full_name: fullName,
                phone: phone,
                email: email,
                membership_plan: membershipPlan,
                status: status
            },
            success: function (response) {
                if (response.result === 'success') {
                    // Alert standar
                    alert('Membership berhasil diperbarui');

                    // Tutup modal edit
                    $('#editMembershipModal').modal('hide');

                    // Pilih metode refresh sesuai kebutuhan Anda:

                    // Opsi 1: Reload seluruh halaman
                    location.reload();

                    // Opsi 2: Reload tabel (jika menggunakan DataTables)
                    // $('#membershipTable').DataTable().ajax.reload();

                    // Logging tambahan
                    if (response.membership_updated) {
                        console.log('Data membership diperbarui');
                    }
                    if (response.user_updated) {
                        console.log('Email user diperbarui');
                    }
                    if (!response.user_updated) {
                        console.log('User tidak ditemukan untuk diupdate');
                    }
                } else {
                    // Alert error
                    alert(response.msg);
                }
            },
            error: function () {
                // Alert error koneksi
                alert('Terjadi kesalahan saat memperbarui membership');
            }
        });
    });
});

// tambah membership

$('#addMembershipModal').on('submit', function (event) {
    event.preventDefault(); // Hindari reload halaman

    const name = $('#name').val();
    const phone = $('#phone').val();
    const email = $('#email').val();  // Tambahkan email
    const masaBerlaku = $('#masaBerlaku').val();
    const status = $('#statusPembayaran').val();

    // Validasi input
    if (!name || !phone || !masaBerlaku || !status) {
        alert('Semua field harus diisi!');
        return;
    }

    // Set masa berlaku dan status dropdown
    $('#masaBerlaku').val(masaBerlaku.toLowerCase());
    $('#statusPembayaran').val(status.toLowerCase());

    // Menonaktifkan tombol submit
    $('#submitButton').prop('disabled', true);

    $.ajax({
        url: '/api/add_membership',
        type: 'POST',
        data: {
            'full_name': name,
            'email': email,  // Kirim email
            'phone': phone,
            'membership_plan': masaBerlaku,
            'status': status
        },
        success: function (response) {
            alert(response.msg); // Tampilkan pesan
            if (response.result === 'success') {
                location.reload(); // Reload halaman
            }
        },
        error: function (xhr, status, error) {
            alert('Terjadi kesalahan: ' + error);
        }
    });
});
// Delete User Modal
const deleteUserModal = document.getElementById('deleteUserModal');
const confirmDeleteButton = document.getElementById('confirmDelete');
const cancelDeleteButton = document.getElementById('cancelDelete');

// Function to confirm delete
function confirmDelete(fullName) {
    deleteUserModal.style.display = 'block'; // Show modal


    // Confirm delete action
    confirmDeleteButton.onclick = function () {
        $.ajax({
            url: '/api/delete_membership',
            type: 'POST',
            data: { 'full_name': fullName },
            success: function (data) {
                alert(data.msg);  // Tampilkan pesan
                if (data.result === 'success') {
                    location.reload();  // Reload halaman untuk memperbarui daftar
                }
            },
            error: function (xhr, status, error) {
                alert('Terjadi kesalahan: ' + error); // Tampilkan pesan kesalahan
            }
        });
    };
}

// Close modal when cancel button is clicked
cancelDeleteButton.addEventListener('click', () => {
    deleteUserModal.style.display = 'none';
});

// Close modal when 'x' is clicked
deleteUserModal.querySelector('.close').addEventListener('click', () => {
    deleteUserModal.style.display = 'none';
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


