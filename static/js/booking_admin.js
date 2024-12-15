
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
const modal = document.getElementById('addBookingModal');
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
const editBookingModal = document.getElementById('editBookingModal');
const editNameInput = document.getElementById('editName');
const editlapanganInput = document.getElementById('editLapangan');
const editTanggalInput = document.getElementById('editTanggal');
const editJamInput = document.getElementById('editJam');
const editDurasiInput = document.getElementById('editDurasi');
const editStatusInput = document.getElementById('editStatus');
const closeModal = editBookingModal.querySelector('.close');

// Tambahkan event untuk membuka modal dan mengisi data
editButtons.forEach(button => {
    button.addEventListener('click', function () {
        const row = this.closest('tr'); // Dapatkan baris yang terkait
        const name = row.cells[0].textContent; // Ambil teks di kolom "Nama"
        const lapangan = row.cells[1].textContent; // Ambil teks di kolom "Lapangan"
        const tanggal = row.cells[2].textContent; // Ambil teks di kolom "Tanggal"
        const jam = row.cells[3].textContent; // Ambil teks di kolom "Jam"
        const durasiString = row.cells[4].textContent; // Ambil teks di kolom "Durasi"
        const status = row.cells[5].textContent; // Ambil teks di kolom "Status"

        // Isi input modal dengan data
        editNameInput.value = name;
        editlapanganInput.value = lapangan;
        editStatusInput.value = status;

        // Konversi durasi dengan presisi tinggi
        const durasi = durasiString.match(/\d+/)[0];

        // Reset dropdown durasi terlebih dahulu
        editDurasiInput.querySelectorAll('option').forEach(option => {
            option.selected = option.value === durasi;
        });

        // Konversi dan set jam
        const jamParts = jam.split(' - ');
        const jamAwal = jamParts[0].replace('.00', '').trim();

        // Reset dropdown jam
        editJamInput.querySelectorAll('option').forEach(option => {
            option.selected = option.value === jamAwal;
        });

        // Format tanggal
        const formattedDate = formatDateToInput(tanggal);
        editTanggalInput.value = formattedDate;

        // Tampilkan modal
        editBookingModal.style.display = 'block';
    });
});

// Fungsi untuk mengubah format tanggal
function formatDateToInput(dateString) {
    // Misalkan format input adalah DD/MM/YYYY
    const parts = dateString.split('/');

    // Pastikan format output YYYY-MM-DD
    if (parts.length === 3) {
        return `${parts[2]}-${parts[1]}-${parts[0]}`;
    }

    return dateString; // Kembalikan asli jika format tidak sesuai
}
// Ambil elemen form dari modal edit
const editBookingForm = document.getElementById('editBookingForm'); // Pastikan ID form sesuai

// Tambahkan event listener untuk form submit
editBookingForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Mencegah reload halaman

    // Ambil data dari input
    const formData = new FormData(editBookingForm);

    // Kirim data menggunakan fetch API
    fetch('/api/edit_booking', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            alert(data.msg); // Tampilkan pesan
            if (data.result === 'success') {
                location.reload(); // Muat ulang halaman jika berhasil
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Terjadi kesalahan saat mengedit booking.'); // Tampilkan pesan kesalahan
        });
});

function formatJamToInput(jamString) {
    // Pecah string jam menjadi array
    const jamParts = jamString.split(' - ');

    // Ambil jam awal dan hapus ".00"
    const jamAwal = jamParts[0].replace('.00', '');

    // Konversi ke integer
    return parseInt(jamAwal);
}


// Fungsi untuk mengubah format tanggal
function formatDateToInput(dateString) {
    const parts = dateString.split('/'); // Misalnya, jika formatnya DD/MM/YYYY
    return `${parts[2]}-${parts[1]}-${parts[0]}`; // Mengubah ke format YYYY-MM-DD
}

// Tambahkan event untuk menutup modal
closeModal.addEventListener('click', () => {
    editBookingModal.style.display = 'none';
});

// Tutup modal ketika area luar modal diklik
window.addEventListener('click', event => {
    if (event.target === editBookingModal) {
        editBookingModal.style.display = 'none';
    }
});
// Fungsi untuk konfirmasi penghapusan
let bookingToDelete = ''; // Variabel untuk menyimpan nama booking yang akan dihapus

function confirmDelete(nama) {
    console.log("Confirm delete called for:", nama); // Debugging
    const modal = document.getElementById('deleteUser Modal'); // Pastikan ID modal sesuai
    const confirmButton = document.getElementById('confirmDelete');

    // Tampilkan modal konfirmasi
    modal.style.display = 'block';

    // Ketika tombol konfirmasi di klik
    confirmButton.onclick = function () {
        console.log("Delete confirmed for:", nama); // Debugging
        fetch('/api/delete_booking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'nama_give=' + encodeURIComponent(nama) // Kirim nama booking yang akan dihapus
        })
            .then(response => response.json())
            .then(data => {
                alert(data.msg); // Tampilkan pesan
                modal.style.display = 'none'; // Sembunyikan modal
                location.reload(); // Muat ulang halaman untuk memperbarui daftar
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Terjadi kesalahan saat menghapus booking.'); // Tampilkan pesan kesalahan
            });
    };

    // Menutup modal jika tombol cancel di klik
    document.getElementById('cancelDelete').onclick = function () {
        modal.style.display = 'none'; // Sembunyikan modal
    };
}

// Tutup modal ketika area luar modal diklik
window.addEventListener('click', event => {
    const deleteModal = document.getElementById('deleteUser  Modal');
    if (event.target === deleteModal) {
        deleteModal.style.display = 'none'; // Sembunyikan modal
    }
});


function showPaymentProof(imageSrc) {
    var modalHtml = `
        <div id="paymentProofModal" class="payment-proof-modal">
            <div class="modal-overlay" onclick="closePaymentProofModal()"></div>
            <div class="modal-container">
                <div class="modal-header">
                    <h3>Bukti Pembayaran</h3>
                    <button class="close-btn" onclick="closePaymentProofModal()">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="image-container">
                        <img src="${imageSrc}" alt="Bukti Pembayaran" class="payment-proof-image">
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="close-modal-btn" onclick="closePaymentProofModal()">Tutup</button>
                    <a href="${imageSrc}" download class="download-btn">Download</a>
                </div>
            </div>
        </div>
    `;

    // Menambahkan modal ke body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function closePaymentProofModal() {
    const modal = document.getElementById('paymentProofModal');
    if (modal) {
        modal.remove(); // Menghapus modal dari DOM
    }
}

function showJadwalModal(nama, lapangan, tanggal, jam, durasi, status) {
    // Set values in modal
    document.getElementById('modalNama').textContent = nama;
    document.getElementById('modalLapangan').textContent = 'Lapangan ' + lapangan;
    document.getElementById('modalTanggal').textContent = tanggal;
    document.getElementById('modalJam').textContent = jam + '.00';
    document.getElementById('modalDurasi').textContent = durasi + ' Jam';

    // Set status with appropriate class
    const statusElement = document.getElementById('modalStatus');
    statusElement.textContent = status;
    statusElement.className = 'detail-value status-badge status-' + status;

    // Show modal
    document.getElementById('jadwalDetailModal').style.display = 'block';
}

function closeJadwalModal() {
    document.getElementById('jadwalDetailModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function (event) {
    const modal = document.getElementById('jadwalDetailModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Optional: JavaScript untuk toggle dropdown jika diperlukan
document.addEventListener('DOMContentLoaded', function () {
    const dropdownBtn = document.querySelector('.dropbtn');
    const dropdownContent = document.querySelector('.dropdown-content');

    dropdownBtn.addEventListener('click', function () {
        dropdownContent.style.display =
            dropdownContent.style.display === 'block' ? 'none' : 'block';
    });

    // Tutup dropdown jika diklik di luar
    window.addEventListener('click', function (event) {
        if (!event.target.matches('.dropbtn') &&
            !event.target.closest('.dropdown')) {
            dropdownContent.style.display = 'none';
        }
    });
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
    window.location.href = '/login'; // Replace with your logout URL
});

// Close modal when clicking outside of it
window.addEventListener('click', (e) => {
    if (e.target === signOutModal) {
        signOutModal.style.display = 'none';
    }
});