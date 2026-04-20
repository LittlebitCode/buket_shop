from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import EmailVerification


import threading

def send_verification_code(user):
    def send_email_task():
        try:
            verification, created = EmailVerification.objects.get_or_create(user=user)
            code = verification.generate_code()
            subject = 'Kode Verifikasi Admin A&A Bouquet'
            message = f'Halo Admin, kode verifikasi masuk Anda adalah: {code}.'
            
            # Jika user adalah Admin, kirim ke email khusus ini
            recipient = 'adityakurniantoaji@gmail.com' if user.is_staff else user.email
            
            send_mail(subject, message, None, [recipient], fail_silently=False)
            print(f"DEBUG: Email berhasil dikirim ke {recipient}")
        except Exception as e:
            print(f"DEBUG ERROR EMAIL: {str(e)}")
    
    threading.Thread(target=send_email_task).start()


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('shop_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            # Semua user (termasuk Admin) wajib verifikasi kode
            send_verification_code(user)
            request.session['pending_user_id'] = user.pk
            return redirect('verify_code')
        
        messages.error(request, 'Username atau password salah.')

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('shop_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        if password != password2:
            messages.error(request, 'Password tidak cocok.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar.')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=first_name, last_name=last_name
            )
            # Send verification code
            send_verification_code(user)
            request.session['pending_user_id'] = user.pk
            messages.success(request, 'Akun berhasil dibuat. Silakan periksa email Anda untuk kode verifikasi.')
            return redirect('verify_code')

    return render(request, 'accounts/register.html')


def verify_code_view(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('login')
    
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            verification = EmailVerification.objects.get(user=user, code=code)
            # Log the user in
            auth_login(request, user)
            del request.session['pending_user_id']
            messages.success(request, f'Verifikasi berhasil! Selamat datang, {user.first_name or user.username}.')
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('shop_home')
        except EmailVerification.DoesNotExist:
            messages.error(request, 'Kode verifikasi salah.')
            
    display_email = 'adityakurniantoaji@gmail.com' if user.is_staff else user.email
    return render(request, 'accounts/verify.html', {'email': display_email})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        
        user.first_name = first_name
        user.email = email
        
        if new_password:
            user.set_password(new_password)
            user.save()
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
        else:
            user.save()
            
        messages.success(request, 'Profil Anda berhasil diperbarui!')
        return redirect('profile')
        
    return render(request, 'accounts/profile.html', {'user': user})

