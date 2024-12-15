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
const modal = document.getElementById('addUserModal');
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

// Handle Add User Form Submission
const addUserForm = document.getElementById('addUserForm');
addUserForm.addEventListener('submit', (e) => {
  e.preventDefault(); // Prevent default form submission

  const name = document.getElementById('name').value;
  const password = document.getElementById('password').value;
  const email = document.getElementById('email').value;
  const noTelp = document.getElementById('no_telp').value;

  $.ajax({
    type: 'POST',
    url: '/api/create_user', // Ensure this URL matches your Flask route
    data: {
      username_give: name,
      password_give: password,
      email_give: email,
      no_telp_give: noTelp
    },
    success: function (response) {
      if (response.result === 'success') {
        alert(response.msg);
        window.location.reload(); // Reload to see the new user
      } else {
        alert(response.msg);
      }
    },
    error: function (xhr, status, error) {
      alert('An error occurred: ' + error);
    }
  });
});

// Ambil semua tombol "Edit" dari tabel
const editButtons = document.querySelectorAll('.status.biru.tombol');

// Ambil modal dan elemen input di dalamnya
const editUserModal = document.getElementById('editUser Modal');
const editNameInput = document.getElementById('editName');
const editEmailInput = document.getElementById('editEmail');
const editPasswordInput = document.getElementById('editPassword'); // Add this line
const editNoTelpInput = document.getElementById('editNoTelp'); // Add this line
const closeModal = editUserModal.querySelector('.close');

// Tambahkan event untuk membuka modal dan mengisi data
editButtons.forEach(button => {
  button.addEventListener('click', function () {
    const row = this.closest('tr'); // Dapatkan baris yang terkait
    const name = row.cells[0].textContent; // Ambil teks di kolom "Nama"
    const email = row.cells[2].textContent; // Ambil teks di kolom "Email"
    const password = row.cells[1].textContent; // Ambil teks di kolom "Password"
    const noTelp = row.cells[3].textContent; // Ambil teks di kolom "No Telephone"

    // Isi input modal dengan data
    editNameInput.value = name;
    editEmailInput.value = email;
    editPasswordInput.value = password; // Add this line
    editNoTelpInput.value = noTelp; // Add this line

    // Tampilkan modal
    editUserModal.style.display = 'block';
  });
});

// Tambahkan event untuk menutup modal
closeModal.addEventListener('click', () => {
  editUserModal.style.display = 'none';
});

// Tutup modal ketika area luar modal diklik
window.addEventListener('click', event => {
  if (event.target === editUserModal) {
    editUserModal.style.display = 'none';
  }
});

// Delete User Modal
const deleteUserModal = document.getElementById('deleteUserModal');
const confirmDelete = document.getElementById('confirmDelete');
const cancelDelete = document.getElementById('cancelDelete');
let currentUserEmail = null;
let currentRow = null;

document.querySelectorAll('.status.merah').forEach(button => {
  button.addEventListener('click', () => {
    const row = button.closest('tr'); // Ganti this dengan button
    currentUserEmail = row.querySelector('td:nth-child(3)').textContent; // Ambil email dari kolom ketiga
    currentRow = row; // Simpan referensi baris
    deleteUserModal.style.display = 'block';
  });
});

// Close modal when cancel button is clicked
cancelDelete.addEventListener('click', () => {
  deleteUserModal.style.display = 'none';
});

// Close modal when 'x' is clicked
deleteUserModal.querySelector('.close').addEventListener('click', () => {
  deleteUserModal.style.display = 'none';
});

confirmDelete.addEventListener('click', () => {
  if (currentUserEmail) {
  $.ajax({
    url: '/api/delete_user',
    type: 'POST',
    data: {
      email_give: currentUserEmail
    },
    success: function (response) {
      if (response.result === 'success') {
        // Hapus baris dari tabel
        if (currentRow) {
          currentRow.remove();
        }
          // Tutup modal
          deleteUserModal.style.display = 'none';
        // Tampilkan pesan sukses
        Swal.fire({
          icon: 'success',
          title: 'Berhasil!',
          text: 'User  berhasil dihapus.'
        });
      } else {
        Swal.fire({
          icon: 'error',
          title: 'Gagal',
          text: response.msg || 'Gagal menghapus user'
        });
      }
    },
    error: function (xhr, status, error) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Terjadi kesalahan: ' + error
      });
    }
  });
}
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




