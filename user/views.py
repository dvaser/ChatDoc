from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import login, logout, get_user_model
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from user.tasks import delete_user

def authenticate_user(email, password):
    User = get_user_model()
    try:
        # Öncelikle CustomUser modelinde kullanıcıyı arayın
        user_custom = CustomUser.objects.get(email=email)
        if user_custom.check_password(password):
            return user_custom

        # Eğer CustomUser modelindeki kullanıcıyı bulamazsanız, User modelinde arayın
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
    except (CustomUser.DoesNotExist, User.DoesNotExist):
        pass
    return None

def signin(request):
    delete_user()  # delete_user görevini çağırarak tüm kullanıcıları kontrol etmesini sağlayın
    if request.user.is_authenticated:
        return redirect("chat")

    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate_user(email=email, password=password)

        if user is not None:
            login(request, user)
            user.reset_delete_date()
            request.session['user_id'] = user.id
            return redirect("chat")
        else:
            return render(request, 'user/login.html', {
                "error":"Email or password not founded!",
                "email": email,
            })

    return render(request, 'user/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        name = request.POST["name"]
        surname = request.POST["surname"]
        password = request.POST["password"]
        re_password = request.POST["re-password"]

        if (username) and (email) and (name) and (surname) and (password) and (re_password):
            if password == re_password:
                print("Parola eş")
                if CustomUser.objects.filter(username=username).exists():
                    return render(request, 'user/register.html', {
                            "error":"Username is being used!", 
                            "username":username,
                            "email": email,
                            "name": name,
                            "surname":surname,
                        })
                else:
                    if CustomUser.objects.filter(email=email).exists():
                        return render(request, 'user/register.html', {
                            "error":"Email is being used!", 
                            "username":username,
                            "email": email,
                            "name": name,
                            "surname":surname,
                        })
                    else:
                        code = send_verification_email(email)  # E-posta göndermek için aşağıdaki fonksiyonu çağırın
                        
                        request.session['username'] = username
                        request.session['email'] = email
                        request.session['name'] = name
                        request.session['surname'] = surname
                        request.session['password'] = password
                        request.session['code'] = code

                        return render(request, 'user/verifyCode.html')

            else:
                return render(request, 'user/register.html', {
                        "error":"Password does not match",
                        "username":username,
                        "email":email,
                        "name":name,
                        "surname":surname,
                    })

        else:
            return render(request, 'user/register.html', {
                    "error":"Missing Information",
                    "username":username,
                    "email":email,
                    "name":name,
                    "surname":surname,
                })

    return render(request, 'user/register.html')

def verifyCode(request):
    if request.method == "POST":
        verification_code = request.POST["verification-code"]
        username = request.session.get("username")
        email = request.session.get("email")
        name = request.session.get("name")
        surname = request.session.get("surname")
        password = request.session.get("password")
        code = request.session.get("code")

        if int(verification_code) == int(code):
            user = CustomUser.objects.create_user(username=username, email=email, first_name=name, last_name=surname, password=password)
            user.save()
            original_user_id = user.get_original_user_id()
            return redirect("login")
        else:
            return render(request, 'user/register.html', {"error": "Verification Code not matching!"})

    return render(request, 'user/verifyCode.html')

def send_verification_email(email):
    # E-posta gönderme işlemini gerçekleştirin
    subject = "Verification Code"
    verification_code = random.randint(100000, 999999)
    message = f"Your verification code is: {verification_code}"
    sender_email = "chatbox_document_ai@hotmail.com"  # Gönderen e-posta adresi
    receiver_email = email  # Alıcı e-posta adresi

    # E-posta mesajını oluşturun
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))


    # Gmail SMTP Ayarları:
    # SMTP Sunucusu: smtp.gmail.com
    # Port: 587 (TLS ile)
    # Kullanıcı Adı: Gmail e-posta adresiniz
    # Parola: Gmail hesabınızın parolası veya uygulama parolası
    
    # Outlook.com (Hotmail) SMTP Ayarları:
    # SMTP Sunucusu: smtp-mail.outlook.com
    # Port: 587 (TLS ile)
    # Kullanıcı Adı: Outlook.com (Hotmail) e-posta adresiniz
    # Parola: Outlook.com (Hotmail) hesabınızın parolası
    
    # SMTP sunucusuna bağlanın ve e-postayı gönderin
    smtp_server = "smtp-mail.outlook.com"  # SMTP sunucusunun adresini ve port numarasını buraya yazın
    smtp_port = 587
    
    smtp_username = "chatbox_document_ai@hotmail.com"
    smtp_password = "adminforchatdoc_AI"

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print("Verification email sent successfully.")
        return verification_code
    except Exception as e:
        print("Error sending verification email:", str(e))

def send_delete_account_email(email):
    # E-posta gönderme işlemini gerçekleştirin
    subject = "Delete Account"
    message = f"Your account will be deleted if you do not log back in within 30 days.\nWe'd love to have you back."
    sender_email = "chatbox_document_ai@hotmail.com"  # Gönderen e-posta adresi
    receiver_email = email  # Alıcı e-posta adresi

    # E-posta mesajını oluşturun
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    # SMTP sunucusuna bağlanın ve e-postayı gönderin
    smtp_server = "smtp-mail.outlook.com"  # SMTP sunucusunun adresini ve port numarasını buraya yazın
    smtp_port = 587
    
    smtp_username = "chatbox_document_ai@hotmail.com"
    smtp_password = "adminforchatdoc_AI"

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print("Delete account email sent successfully.")
    except Exception as e:
        print("Error sending delete account email:", str(e))

def signout(request):
    logout(request)
    return redirect("chat")

def pswForget(request):
    return render(request, 'user/pswForget.html')

def delete_account(request):
    user = request.user
    send_delete_account_email(user.email)
    user.delete_account()   # user icindeki model fonksiyonu calisir (isActive = False)
    delete_user()  # delete_user görevini çağırarak tüm kullanıcıları kontrol etmesini sağlayın
    signout(request)
