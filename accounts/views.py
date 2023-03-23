from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import RegistrationForm
from .models import Account

# Verification Email Imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
    if request.method == 'POST':
        form =RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
                )
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            # mail_subject = 'Please activate your account'
            # message = render_to_string('accounts/account_verification_email.html',{
            #     'user': user,
            #     'domain': current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':  default_token_generator.make_token(user),
            # })
            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()

            # TEMP CODE FOR TESTING
            # temp_data = {
            #     'type': 'account_activation',
            #     'user': user,
            #     'domain': current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':  default_token_generator.make_token(user),
            # }
            # return render(request, 'accounts/dummy_validation_link_page.html', context=temp_data)

            # messages.success(request,'Thankyou for registering with us. we have sent a validation link for verification')
            return redirect('/accounts/login/?command=verification&email='+email)

    else:
        form = RegistrationForm()
    data = {'form': form}
    return render(request, 'accounts/register.html', context=data)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations You\'re Account is Activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Link or Expired')
        return redirect('register')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login Successful. you\'re now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Login credentials. please check your details')
            return redirect('login')
    return render(request, 'accounts/login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # USER PASSWORD RESET

            current_site = get_current_site(request)
            # mail_subject = 'Please reset your account password'
            # message = render_to_string('accounts/reset_password_email.html',{
            #     'user': user,
            #     'domain': current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':  default_token_generator.make_token(user),
            # })
            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()

            # TEMP CODE FOR TESTING

            temp_data = {
                'type':'password_reset',
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':  default_token_generator.make_token(user),
            }
            return render(request, 'accounts/dummy_validation_link_page.html', context=temp_data)

            messages.success(request, 'Password email has been sent to your email address')
            return redirect('login')

        else:
            messages.error(request,'Invalid Email, Account does not exist')
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    print(' ->  inside reset_password_validate')
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'Please Reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This Link has been expired')
        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, 'Passwords Don\'t match please check again')
            return redirect('reset_password')
        else:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password) # must use set_password method dont use save method.
            user.save()
            messages.success(request,'Password Reset Successful')
            del request.session['uid']
            return redirect('login')
    else:
        return render(request, 'accounts/reset_password.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are Logged out Successfully')
    return redirect('login')
