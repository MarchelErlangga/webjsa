from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, url_for, redirect, flash, session
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from functools import wraps


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)
app.secret_key = 'holaa'

client = MongoClient('mongodb://raimondabukit20:Gemer$12345@cluster0-shard-00-00.h4pla.mongodb.net:27017,cluster0-shard-00-01.h4pla.mongodb.net:27017,cluster0-shard-00-02.h4pla.mongodb.net:27017/?ssl=true&replicaSet=atlas-rwckp1-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
db = client.dbraimonda

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

#Tampilan halaman sebelum login
@app.route('/')
def main():
    return render_template('/public_page/homePage.html')

@app.route('/about_public')
def about_public():
    return render_template('/public_page/about.html')

@app.route('/booking_public')
def booking_public():
    flash('Untuk booking lapangan, silakan login terlebih dahulu.', 'warning')
    return redirect(url_for('login'))

@app.route('/facilities_public')
def facilities_public():
    return render_template('/public_page/facilities.html')

@app.route('/jadwal1_public')
def jadwal1_public():
    flash('Untuk melihat jadwal, silakan login terlebih dahulu.', 'warning')
    return redirect(url_for('login'))


@app.route('/jadwal2_public')
def jadwal2_public():
    flash('Untuk melihat jadwal, silakan login terlebih dahulu.', 'warning')
    return redirect(url_for('login'))

@app.route('/jadwal3_public')
def jadwal3_public():
    flash('Untuk melihat jadwal, silakan login terlebih dahulu.', 'warning')
    return redirect(url_for('login'))

@app.route('/membership_public')
def membership_public():
    return render_template('/public_page/membership.html')

@app.route('/api/create_membership')
def create_membership_public():
    flash('Untuk mendaftar membership, silakan login terlebih dahulu.', 'warning')
    return redirect(url_for('login'))

@app.route('/prabooking_public')
def prabooking_public():
    return render_template('/public_page/prabooking.html')

#<---------------------------------------------------------------------------------------------------------------------------->

@app.route('/home')
def home():
    # if 'user' in session:
    #     return render_template('home2.html')
    return render_template('home2.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile')
def profile():

    if 'user' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))
    
    # Ambil data pengguna dari database
    user_data = db.jsausers.find_one({'username': session['user']})
    if not user_data:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))
    
    # Cari membership untuk user ini berdasarkan email
    current_date = datetime.now()
    membership = db.payments.find_one({
        'email': user_data['email'],  # Gunakan email untuk mencari membership
        'end_date': {'$gt': current_date}  # Membership masih aktif
    })
    
    # Siapkan variabel membership
    membership_info = {
        'status': 'Tidak Aktif',
        'status_db': 'nonaktif',  # Tambahkan status dari database
        'plan': '-',
        'end_date': '-'
    }
    
    if membership:
        membership_info = {
            'status': 'Aktif',
            'status_db': membership.get('status', 'nonaktif'),  # Ambil status dari database
            'plan': membership.get('membership_plan', '-'),
            'end_date': membership.get('end_date', '-')
        }
    
    # Ambil data booking untuk user ini
    bookings = list(db.booking1s.find({'nama': user_data['username']})) + \
               list(db.booking2s.find({'nama': user_data['username']})) + \
               list(db.booking3s.find({'nama': user_data['username']}))
               
    
    for booking in bookings:
        if 'tanggal' in booking: 
            booking_date = booking['tanggal']
            if isinstance(booking_date, datetime):
                booking['tanggal'] = booking_date.strftime('%d/%m/%Y')  # Format menjadi DD/MM/YYYY

    if request.args.get('_anchor') == 'flash':
        flash_message = request.args.get('flash_message')
        flash_category = request.args.get('flash_category')
        if flash_message and flash_category:
            flash(flash_message, flash_category)
    
    return render_template('profile.html', 
        username=user_data['username'], 
        no_telp=user_data['no_telp'], 
        email=user_data['email'],
        membership=membership_info,
        bookings=bookings  
    )
    
@app.route('/logout')
def logout():
    # Hapus session pengguna
    session.clear()
    # Redirect ke halaman login
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Cek login sebagai admin
        admin = db["jsaadmins"].find_one({"username": username, "password": password})
        if admin:
            session['admin'] = username  # Set sesi untuk admin
            # flash('Login berhasil sebagai admin!', 'success')
            return redirect(url_for('admin_dashboard'))

        # Cek login sebagai user
        user = db["jsausers"].find_one({"username": username, "password": password})
        if user:
            session['user'] = username  # Set sesi untuk user
            flash('Login berhasil!', 'success')
            return redirect(url_for('home'))

        # Jika gagal login
        flash('Login gagal, username atau password salah.', 'danger')
        return redirect(url_for('login'))  # Redirect ke halaman login

    return render_template('login.html')

@app.route('/check_login_status')
def check_login_status():
    return jsonify({
        'is_logged_in': 'user' in session
    })

@app.route('/register')
def register():
    return render_template('register.html')
        
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session:
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))
    
    # Ambil data pengguna dari database
    user_data = db.jsausers.find_one({'username': session['user']})
    
    if request.method == 'POST':
        # new_username = request.form.get('username')
        no_telp = request.form.get('no_telp')
        
        # # Validasi input
        # if not new_username:
        #     flash('Username tidak boleh kosong.', 'danger')
        #     return render_template('edit_profile.html', user=user_data)
        
        # # Cek apakah username sudah ada
        # existing_user = db.jsausers.find_one({'username': new_username})
        # if existing_user and existing_user['username'] != session['user']:
        #     flash('Username sudah digunakan.', 'danger')
        #     return render_template('edit_profile.html', user=user_data)
        
        # # Update username di database
        # db.jsausers.update_one(
        #     {'username': session['user']},
        #     {'$set': {'username': new_username,'no_telp' : no_telp}}
        # )
        # Update username di database
        db.jsausers.update_one(
            {'username': session['user']},
            {'$set': {'no_telp' : no_telp}}
        )
        
        # # Update session username
        # session['user'] = new_username
        
        flash('Profil berhasil diperbarui.', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html', user=user_data)

@app.route('/facilities')
def facilites():
    return render_template('facilities.html')

@app.route('/membership')
def membership():
    # Inisialisasi membership dengan status default
    membership_info = {
        'status': 'Tidak Aktif',
        'plan': '-',
        'end_date': '-'
    }
    
    # Tangkap flash message dari parameter URL
    flash_message = request.args.get('flash_message')
    flash_category = request.args.get('flash_category')
    
    # Tampilkan flash message jika ada
    if flash_message and flash_category:
        flash(flash_message, flash_category)

    # Jika user sudah login, cek membership
    if 'user' in session:
        user_data = db.jsausers.find_one({'username': session['user']})
        
        if user_data:
            # Cari membership untuk user ini berdasarkan email
            current_date = datetime.now()
            membership = db.payments.find_one({
                'email': user_data['email'],
                'end_date': {'$gt': current_date}
            })
            
            # Update membership info jika ditemukan
            if membership:
                membership_info = {
                    'status': 'Aktif',
                    'plan': membership.get('membership_plan', '-'),
                    'end_date': membership.get('end_date', '-')
                }

    return render_template('membership.html', membership=membership_info)

@app.route('/check_membership_status', methods=['POST'])
def check_membership_status():
    data = request.get_json()
    email = data.get('email')

    # Jika tidak ada email, kembalikan error
    if not email:
        return jsonify({
            'status': 'Tidak Aktif',
            'plan': '-',
            'end_date': '-',
            'registered_email': None
        }), 400

    # Cari user berdasarkan email
    user = db.jsausers.find_one({'email': email})
    
    if not user:
        return jsonify({
            'status': 'Tidak Aktif',
            'plan': '-',
            'end_date': '-',
            'registered_email': None
        })

    # Cari membership berdasarkan email
    current_date = datetime.now()
    membership = db.payments.find_one({
        'email': email,
        'end_date': {'$gt': current_date},
        'status': {'$in': ['Menunggu', 'Terima']}  
    })

    if membership:
        return jsonify({
            'status': 'Aktif',
            'plan': membership.get('membership_plan', '-'),
            'end_date': membership.get('end_date', '-').strftime('%d %B %Y') if membership.get('end_date') else '-',
            'registered_email': email
        })
    else:
        return jsonify({
            'status': 'Tidak Aktif',
            'plan': '-',
            'end_date': '-',
            'registered_email': email
        })
        


@app.route('/api/add_membership', methods=['POST'])
def add_membership():
    name = request.form.get('full_name')
    phone = request.form.get('phone')
    email = request.form.get('email')  # Tambahkan email
    membership_plan = request.form.get('membership_plan')
    status = request.form.get('status')

    print(f"Received data: name={name}, phone={phone}, membership_plan={membership_plan}, status={status}")

    if not name or not phone or not membership_plan:
        return jsonify({'result': 'error', 'msg': 'Semua field harus diisi.'}), 400

    # Menentukan durasi untuk setiap paket
    membership_durations = {
        'basic': 30,    # 30 hari
        'standard': 60, # 60 hari
        'premium': 90   # 90 hari
    }

    # Menghitung tanggal akhir
    duration = membership_durations.get(membership_plan)
    if duration is None:
        return jsonify({'result': 'error', 'msg': 'Paket tidak valid.'}), 400

    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=duration)

    try:
        db.payments.insert_one({
            'full_name': name,
            'phone': phone,
            'email': email,  # Simpan email di database
            'membership_plan': membership_plan,
            'status': status,
            'start_date': start_date,  # Tambahkan start_date
            'end_date': end_date  # Menyimpan tanggal akhir
        })
        return jsonify({'result': 'success', 'msg': 'Membership berhasil ditambahkan.'})
    except Exception as e:
        return jsonify({'result': 'error', 'msg': str(e)}), 500
    
@app.route('/api/edit_membership', methods=['POST'])
def edit_membership():
    full_name = request.form.get('full_name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    membership_plan = request.form.get('membership_plan')
    status = request.form.get('status')

    # Validasi input
    if not full_name or not email:
        return jsonify({'result': 'error', 'msg': 'Nama dan Email harus diisi.'}), 400

    # Tentukan masa berlaku berdasarkan paket
    membership_durations = {
        'basic': 30,
        'standard': 90,
        'premium': 360
    }

    # Hitung tanggal awal dan akhir berdasarkan paket
    start_date = datetime.now()
    if membership_plan in membership_durations:
        duration_days = membership_durations[membership_plan]
        end_date = start_date + timedelta(days=duration_days)
    else:
        return jsonify({'result': 'error', 'msg': 'Paket membership tidak valid.'}), 400

    try:
        # Cari membership berdasarkan nama
        existing_membership = db.payments.find_one({'full_name': full_name})
        
        if existing_membership:
            # Update data membership
            result_membership = db.payments.update_one(
                {'email': email,},
                {'$set': {
                    'full_name': full_name,
                    'phone': phone,
                    'membership_plan': membership_plan,
                    'status': status,
                    'start_date': start_date,
                    'end_date': end_date
                }}
            )

            # Cari user berdasarkan email
            existing_user = db.jsausers.find_one({'email': existing_membership.get('email')})
            
            # Update email di user jika user ditemukan
            if existing_user:
                result_user = db.jsausers.update_one(
                    {'email': existing_user['email']},
                    {'$set': {
                        'email': email  # Update email
                    }}
                )

                if result_membership.modified_count > 0 or result_user.modified_count > 0:
                    return jsonify({
                        'result': 'success', 
                        'msg': 'Membership dan email berhasil diperbarui!',
                        'membership_updated': result_membership.modified_count > 0,
                        'user_updated': result_user.modified_count > 0
                    })
            else:
                # Jika user tidak ditemukan, kembalikan sukses untuk membership
                if result_membership.modified_count > 0:
                    return jsonify({
                        'result': 'success', 
                        'msg': 'Membership berhasil diperbarui, tetapi user tidak ditemukan!',
                        'membership_updated': True,
                        'user_updated': False
                    })

            return jsonify({'result': 'error', 'msg': 'Tidak ada perubahan yang dilakukan!'})
        else:
            return jsonify({'result': 'error', 'msg': 'Membership tidak ditemukan!'})
    
    except Exception as e:
        return jsonify({'result': 'error', 'msg': str(e)}), 500
    
@app.route('/api/delete_membership', methods=['POST'])
def delete_membership():
    full_name = request.form.get('full_name')  # Ambil nama lengkap dari permintaan
    
    # Cari dokumen membership untuk mendapatkan nama file bukti pembayaran
    membership = db.payments.find_one({'full_name': full_name})
    
    if membership:
        # Hapus file bukti pembayaran jika ada
        payment_proof = membership.get('payment_proof')
        if payment_proof:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], payment_proof)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"File {payment_proof} berhasil dihapus")
            except Exception as e:
                print(f"Gagal menghapus file: {e}")
        
        # Hapus dokumen dari database
        result = db.payments.delete_one({'full_name': full_name})

        # Cek jika ada yang berhasil dihapus
        if result.deleted_count > 0:
            return jsonify({'result': 'success', 'msg': 'Membership berhasil dihapus!'})
        else:
            return jsonify({'result': 'error', 'msg': 'Membership tidak ditemukan!'})
    
    return jsonify({'result': 'error', 'msg': 'Membership tidak ditemukan!'})

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Ambil data user yang sedang login
    user_data = db.jsausers.find_one({'username': session['user']})
    
    # Pastikan ini adalah metode POST
    if request.method == 'POST':
        try:
            # Ambil data dari form
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            membership_plan = request.form.get('membership_plan', 'basic')
            payment_method = request.form.get('payment_method')
            payment_proof = request.files.get('payment_proof')

            # Validasi input
            if not all([full_name, email, phone, payment_method]):
                flash('Semua field harus diisi.', 'danger')
                return redirect(url_for('checkout'))

            # Validasi metode pembayaran
            if payment_method not in ['bca_va', 'gopay', 'dana']:
                flash("Metode pembayaran tidak valid.", "danger")
                return redirect(url_for('checkout'))

            # Definisi durasi membership
            membership_duration = {
                'basic': 30,
                'standard': 90,
                'premium': 360
            }

            # Hitung durasi membership
            duration_days = membership_duration.get(membership_plan.lower(), 30)
            start_date = datetime.now()
            end_date = start_date + timedelta(days=duration_days)

            # Harga membership
            membership_prices = {
                'basic': 150000,
                'standard': 450000,
                'premium': 1200000
            }
            total_price = membership_prices.get(membership_plan.lower(), 150000)

            # Validasi dan simpan bukti pembayaran
            if payment_proof and allowed_file(payment_proof.filename):
                filename = secure_filename(payment_proof.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                payment_proof.save(file_path)

                # Simpan data pembayaran
                payment_doc = {
                    'username': session['user'],
                    'full_name': full_name,
                    'email': email,
                    'phone': phone,
                    'membership_plan': membership_plan,
                    'payment_method': payment_method,
                    'payment_proof': filename,
                    'total_price': total_price,
                    'status': 'Menunggu',
                    'start_date': start_date,
                    'end_date': end_date
                }

                db.payments.insert_one(payment_doc)

                # Redirect ke halaman membership dengan flash message
                return redirect(url_for('membership', 
                    flash_message='Pembayaran Anda telah berhasil diproses. Silakan periksa status keanggotaan Anda secara berkala melalui halaman profil.', 
                    flash_category='success'))
            else:
                flash('Bukti pembayaran tidak valid.', 'danger')
                return redirect(url_for('checkout'))

        except Exception as e:
            # Log error untuk debugging
            app.logger.error(f"Checkout error: {str(e)}")
            flash('Terjadi kesalahan. Silakan coba lagi.', 'danger')
            return redirect(url_for('checkout'))
    
    # Ini adalah metode GET, tampilkan halaman checkout
    return render_template('checkout.html', user=user_data)

@app.route('/payment')
def payment():
    user_data = db.jsausers.find_one({'username': session['user']})
        # Periksa membership aktif
    current_date = datetime.now()
    existing_membership = db.payments.find_one({
        'email': user_data['email'],
        'end_date': {'$gt': current_date},
        'status': {'$in': ['Menunggu', 'Terima']}
    })

    if existing_membership:
        return redirect(url_for('membership'))

    
        # Periksa login
    if 'user' not in session:
        flash('Silakan login terlebih dahulu.', 'danger')
        return redirect(url_for('login'))
    return render_template('ringkasan_order.html')

@app.route('/payment_booking')
def order_summary():
        # Periksa login
    if 'user' not in session:
        flash('Silakan login terlebih dahulu.', 'danger')
        return redirect(url_for('login'))
    return render_template('ringkasan_order_booking.html')

@app.route('/prabooking')
def prabooking():
    return render_template('prabooking.html')

@app.route('/booking')
def booking():
    # Periksa apakah user sudah login
    if 'user' not in session:
        # Simpan pesan flash untuk memberi tahu user
        flash('Silakan login terlebih dahulu ', 'danger')
        # Redirect ke halaman login
        return redirect(url_for('login'))
    
    # Jika sudah login, tampilkan halaman booking
    return render_template('booking.html')

@app.route('/checkout_booking', methods=['GET', 'POST'])
def checkout_booking():
    if request.method == 'POST':
        # Mengambil data dari form
        nama = request.form.get('nama')
        tanggal = request.form.get('tanggal')
        jam = request.form.get('jam')
        durasi = request.form.get('durasi')
        lapangan = request.form.get('lapangan')
        payment_method = request.form.get('payment_method')
        payment_proof = request.files.get('payment_proof')

        # Validasi: Pastikan semua field diisi
        if not all([nama, tanggal, jam, durasi, lapangan, payment_method, payment_proof]):
            flash('Semua field harus diisi.', 'error')
            return redirect(url_for('checkout_booking'))  # Kembali ke halaman checkout

        # Menyimpan bukti pembayaran
        if payment_proof and allowed_file(payment_proof.filename):
            filename = secure_filename(payment_proof.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            payment_proof.save(file_path)

            # Tentukan koleksi berdasarkan lapangan
            if lapangan == '1':
                collection_name = 'booking1s'
            elif lapangan == '2':
                collection_name = 'booking2s'
            elif lapangan == '3':
                collection_name = 'booking3s'
            else:
                flash('Lapangan tidak valid.', 'error')
                return redirect(url_for('checkout_booking'))
            

            # Simpan data ke koleksi yang sesuai
            booking_data = {
                'nama': nama,
                'tanggal': tanggal,
                'jam': jam,
                'durasi': durasi,
                'lapangan': lapangan,
                'payment_method': payment_method,
                'payment_proof': filename,
                'status' : 'Menunggu'
            }

            try:
                db[collection_name].insert_one(booking_data)  # Simpan data ke koleksi yang sesuai
                flash('Terima kasih telah melakukan pemesanan. Silakan tunggu konfirmasi dari admin dan periksa profile secara berkala!!', 'success')
                return redirect(url_for('prabooking'))  
            except Exception as e:
                flash('Terjadi kesalahan saat menyimpan data booking. Silakan coba lagi.', 'error')
                return redirect(url_for('checkout_booking'))

    # Jika metode GET, tampilkan halaman checkout
    return render_template('checkout_booking.html')  # Pastikan ini adalah nama template yang benar 

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            flash('Anda harus login sebagai admin', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@admin_required
def admin_dashboard():
    try:
        #Data Users
        users = list(db.jsausers.find({}, {"_id": False}))
        len_users = len(users)

        #Data Booking
        booking1s = list(db.booking1s.find({}, {"_id": False}))
        booking2s = list(db.booking2s.find({}, {"_id": False}))
        booking3s = list(db.booking3s.find({}, {"_id": False}))

        all_data = booking1s + booking2s + booking3s  # Menggabungkan semua data
        first_5_data = all_data[:5]
        status_to_count = "Booking"
        # Hitung jumlah booking dengan status tertentu
        count_by_status = sum(1 for booking in all_data if booking.get("status") == status_to_count)

        # Hitung jumlah membership aktif (dengan status 'accept')
        total_membership_aktif = db.payments.count_documents({
            'status': 'Terima'
        })
        
        # Ambil 5 membership terbaru (tanpa filter status)
        recent_memberships = list(
            db.payments.find()
            .sort([("start_date", -1)])  # Sorting secara descending berdasarkan start_date
            .limit(5)
        )
        
        # Debugging
        print(f"Total Membership Aktif: {total_membership_aktif}")
        print("Recent Memberships:")
        for membership in recent_memberships:
            print(f"Name: {membership.get('full_name')}, Status: {membership.get('status')}, Start Date: {membership.get('start_date')}")
        
    except Exception as e:
        print(f"Error dalam admin dashboard: {e}")
        total_membership_aktif = 0
        recent_memberships = []
    
    return render_template('dashboard_admin.html', 
                           total_membership_aktif=total_membership_aktif,
                           recent_memberships=recent_memberships,
                           jlh_booking = count_by_status,
                           jlh_users = len_users,
                           recent_bookings = first_5_data)


@app.route('/admin/user')
@admin_required
def admin_user():
    data = list(db.jsausers.find({}, {"_id": False}))
    return render_template('user_admin.html', users=data)

@app.route('/api/edit_user', methods=['POST'])
def edit_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    noTelp = request.form['no_telp']

    # Attempt to update the user
    result = db.jsausers.update_one(
        {"email": email},
        {"$set": {
            "username": name,
            "password": password,
            "no_telp": noTelp,
        }}
    )
    
    return redirect(url_for('admin_user'))  # Redirect back to the user admin page

@app.route('/admin/membership')
@admin_required
def admin_membership():
    memberships = db.payments.find()  # Ambil data dari database
    current_date = datetime.now()  # Mendapatkan tanggal saat ini
    return render_template('membership_admin.html', memberships=memberships, current_date=current_date)

@app.route('/admin/booking')
@admin_required
def admin_booking():
    booking1s = list(db.booking1s.find({}, {"_id": False}))
    booking2s = list(db.booking2s.find({}, {"_id": False}))
    booking3s = list(db.booking3s.find({}, {"_id": False}))

    all_data = booking1s + booking2s + booking3s  # Menggabungkan semua data

    return render_template('booking_admin.html', bookings=all_data)

@app.route('/admin/jadwal1')
@admin_required
def admin_jadwal1():
    collection = db["booking1s"]
    all_data = list(collection.find({}, {"_id" : False}))
    return render_template('jadwal1.html', data = all_data)

@app.route('/admin/jadwal2')
@admin_required
def admin_jadwal2():
    collection = db["booking2s"]
    all_data = list(collection.find({}, {"_id" : False}))
    return render_template('jadwal2.html', data = all_data)

@app.route('/admin/jadwal3')
@admin_required
def admin_jadwal3():
    collection = db["booking3s"]
    all_data = list(collection.find({}, {"_id" : False}))
    return render_template('jadwal3.html', data = all_data)



@app.route('/api/get_schedule')
def get_schedule():
    # Pastikan admin sudah login
    if 'admin' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    # Ambil semua booking dari koleksi yang berbeda
    booking1s = list(db.booking1s.find({}, {"_id": False}))
    booking2s = list(db.booking2s.find({}, {"_id": False}))
    booking3s = list(db.booking3s.find({}, {"_id": False}))

    # Gabungkan semua data booking
    all_bookings = booking1s + booking2s + booking3s
    
    # Konversi data
    schedule_data = []
    for booking in all_bookings:
        schedule_data.append({
            'lapangan': booking['lapangan'],
            'tanggal': booking['tanggal'],
            'jam': booking['jam'],
            'durasi': booking['durasi'],
            'status': booking['status']
        })

    return jsonify(schedule_data)

@app.route('/api/admin/create_boking', methods=['POST'])
def admin_createbooking():
    name = request.form['name']
    lapangan = request.form['lapangan']
    tanggal = request.form['tanggal']
    formatted_date = datetime.strptime(tanggal, "%Y-%m-%d").strftime("%m/%d/%Y")
    jam = request.form['jam']
    durasi = request.form['durasi']

    doc = {
        'nama' : name,
        'tanggal': formatted_date,  # Tambahkan tanggal ke dokumen
        'jam' : jam,
        'durasi' : durasi,
        'lapangan' : lapangan,
        'status' : 'Booking',
    }
    

    if(lapangan == "1"):
        db.booking1s.insert_one(doc)
    elif(lapangan == "2"):
        db.booking2s.insert_one(doc)
    else:
        db.booking3s.insert_one(doc)
    return redirect(url_for('admin_booking'))

@app.route('/api/edit_booking', methods=['POST'])
def edit_booking():
    name = request.form['name']
    new_lapangan = request.form['lapangan']
    new_tanggal = request.form['tanggal']
    formatted_date = datetime.strptime(new_tanggal, "%Y-%m-%d").strftime("%d/%m/%Y")
    new_jam = request.form['jam']
    new_durasi = request.form['durasi']
    new_status = request.form['status']

    if new_lapangan == "1":
        db.booking1s.update_one(
            {"nama": name},
            {"$set": {
                "tanggal": formatted_date,
                "jam": new_jam,
                "durasi": new_durasi,
                "status": new_status
            }}
        )
    elif new_lapangan == "2":
        db.booking2s.update_one(
            {"nama": name},
            {"$set": {
                "tanggal": formatted_date,
                "jam": new_jam,
                "durasi": new_durasi,
                "status": new_status
            }}
        )
    elif new_lapangan == "3":
        db.booking3s.update_one(
            {"nama": name},
            {"$set": {
                "tanggal": formatted_date,
                "jam": new_jam,
                "durasi": new_durasi,
                "status": new_status
            }}
        )
    else:
        return jsonify({'result': 'error', 'msg': 'Lapangan tidak valid!'})

    return jsonify({'result': 'success', 'msg': 'Booking berhasil diedit!'})

@app.route('/api/delete_booking', methods=['POST'])
def delete_booking():
    nama_receive = request.form.get('nama_give')
    
    # Cek dan hapus dari booking1s, booking2s, dan booking3s
    result1 = db.booking1s.delete_one({'nama': nama_receive})
    result2 = db.booking2s.delete_one({'nama': nama_receive})
    result3 = db.booking3s.delete_one({'nama': nama_receive})
    
    # Cek jika ada yang berhasil dihapus
    if result1.deleted_count > 0 or result2.deleted_count > 0 or result3.deleted_count > 0:
        return jsonify({'result': 'success', 'msg': 'Booking berhasil dihapus!'})
    else:
        return jsonify({'result': 'error', 'msg': 'Booking tidak ditemukan!'})

@app.route('/api/create_booking', methods=['POST'])
def create_booking():
    nama_receive = request.form.get('nama_give')
    jam_receive = request.form.get('jam_give')
    tanggal_receive = request.form.get('tanggal_give')  
    durasi_receive = request.form.get('durasi_give')
    lapangan_receive = request.form.get('lapangan_give')
    
        # Pengkondisian untuk memeriksa format tanggal
    try:
        # Coba mengonversi ke objek datetime
        tanggal_obj = datetime.strptime(tanggal_receive, '%Y-%m-%d')
        # Jika berhasil, format ke DD/MM/YYYY
        tanggal_formatted = tanggal_obj.strftime('%d/%m/%Y')
    except ValueError:
        # Jika gagal, coba format lain (misalnya DD/MM/YYYY)
        try:
            tanggal_obj = datetime.strptime(tanggal_receive, '%d/%m/%Y')
            # Jika berhasil, format ke DD/MM/YYYY (tetap sama)
            tanggal_formatted = tanggal_obj.strftime('%d/%m/%Y')
        except ValueError:
            return jsonify({'result': 'error', 'msg': 'Format tanggal tidak valid!'}), 400
        
    doc = {
        'nama' : nama_receive,
        'tanggal': tanggal_formatted,  # Tambahkan tanggal ke dokumen
        'jam' : jam_receive,
        'durasi' : durasi_receive,
        'lapangan' : lapangan_receive,
        'status' : 'Booking',
    }

    if(lapangan_receive == "1"):
        db.booking1s.insert_one(doc)
    elif(lapangan_receive == "2"):
        db.booking2s.insert_one(doc)
    else:
        db.booking3s.insert_one(doc)

    return jsonify({
        'result' : 'success',  'msg' : 'Booking berhasil dibuat!'
    })

@app.route('/jadwal1')
def jadwal1():
    collection = db["booking1s"]
    all_data = list(collection.find({}, {"_id" : False}))
    return render_template('jadwal1.html', data = all_data)


@app.route('/jadwal2')
def jadwal2():
    collection = db["booking2s"]
    all_data = list(collection.find({}, {"_id" : False}))
    return render_template('jadwal2.html', data = all_data)

@app.route('/jadwal3')
def jadwal3():
    collection = db["booking3s"]
    all_data = list(collection.find({}, {"_id" : False}))
    return render_template('jadwal3.html', data = all_data)

@app.route('/api/create_account', methods=['POST'])
def create_account():
    username_receive = request.form.get('username_give')
    email_receive = request.form.get('email_give')
    noTelp_receive = request.form.get('no_telp_give')  # Ambil nomor telepon
    password_receive = request.form.get('password_give')

    existing_user = db.jsausers.find_one({"email": email_receive})
    if existing_user:
        return jsonify({
            'result': 'failed',
            'msg': 'Email sudah digunakan!'
        })
    else:
        doc = {
            'username': username_receive,
            'email': email_receive,
            'no_telp': noTelp_receive,  # Simpan nomor telepon
            'password': password_receive,
        }

        db.jsausers.insert_one(doc)
        return jsonify({
            'result': 'success',
            'msg': 'Akun Anda berhasil dibuat, silahkan login!'
        })
    
@app.route('/api/create_user', methods=['POST'])
def create_user():
    username_receive = request.form.get('username_give')
    email_receive = request.form.get('email_give')
    password_receive = request.form.get('password_give')
    noTelp_receive = request.form.get('no_telp_give')

    existing_user = db.jsausers.find_one({"email": email_receive})
    if existing_user:
        return jsonify({'result': 'failed', 'msg': 'Email sudah digunakan!'})

    # Create new user document
    doc = {
        'username': username_receive,
        'email': email_receive,
        'password': password_receive,
        'no_telp': noTelp_receive
    }

    db.jsausers.insert_one(doc)
    return jsonify({'result': 'success', 'msg': 'Akun berhasil dibuat!'})

@app.route('/api/delete_user', methods=['POST'])
def delete_user():
    email_give = request.form.get('email_give')
    result = db.jsausers.delete_one({'email': email_give})
    
    if result.deleted_count > 0:
        return jsonify({'result': 'success', 'msg': 'User  berhasil dihapus!'})
    else:
        return jsonify({'result': 'error', 'msg': 'User  tidak ditemukan!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)