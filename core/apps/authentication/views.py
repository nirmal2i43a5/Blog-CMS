
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .models import Subscription
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import View
from core.apps.blog.token import account_activation_token
from core.apps.authentication.forms import UserRegisterForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.template.loader import render_to_string


def login_view(request):
    
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = User.objects.filter(email=email)
            if user.exists():
                # use = User.objects.filter(email = email).first()
                user = get_object_or_404(User, email=email)
                user = authenticate(username=user.username, password=password)
                if request.user.is_authenticated:
                    login(request, user)
                    return redirect('blog:home')
                if request.user.is_superuser:
                    login(request, user)
                    return redirect('home:dashboard')
                elif user is not None:
                    login(request, user)
                    return redirect("blog:home")
                else:
                    messages.error(request, "Invalid credentials.")
            else:
                messages.error(request, "Invalid Email address.")

    return render(request, "authentication/login.html", {"form": form, 'title': 'Login'})


class UserRegisterView(View):
    """
      View to let users register
    """
    template_name = 'authentication/register.html'
    context_object = {
        "form": UserRegisterForm(),
        'title': 'Register'
    }

    def get(self, request):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        form = UserRegisterForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False  # User cannot login without email subscription
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Study Better Way Account'
            message = render_to_string('authentication/account_activation_email.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': account_activation_token.make_token(user),
                                       })
            user.email_user(subject, message)

            return redirect('account_activation_sent')

        else:
            messages.error(request, "Please provide valid information.")
            # Redirect user to register page
            return render(request, self.template_name, self.context_object)


class AccountActivationSentView(View):

    def get(self, request):
        context = {
            'title': 'Account Activation Sent'
        }
        return render(request, 'account/verification_sent.html', context)
        # return render(request, 'authentication/account_activation_sent.html',context)


class ActivateView(View):

    def get(self, request, uidb64, token):
        print("success", "---------------------------")
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            username = user.username
            messages.success(request, f"Congratulations {username} !!! "
                                      f"Your account was created and activated "
                                      f"successfully"
                             )
            return redirect('login')
        else:
            return render(request, 'authentication/account_activation_invalid.html')


class UserLogoutView(View):
    """
     Logs user out of the dashboard.
    """
    # template_name = 'authentication/logout.html'

    def get(self, request):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect('login')


class SubscriptionView(View):

    def post(self, request, *args, **kwargs):
        user_email = request.POST['email']
        user = Subscription.objects.create(email=user_email)
        current_site = get_current_site(request)
        subject = 'Activate Your Newsletters Subscription Account for  Study Better Way'
        message = render_to_string('authentication/subscription_email_activate.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': account_activation_token.make_token(user),
                                   })
        email_from = settings.EMAIL_HOST_USER
        email_to = [user.email, ]
        send_mail(subject, message, email_from, email_to)

        messages.success(request, "Subscribed Successfully!")
        return render(request, 'authentication/account_activation_sent.html')

        # current_site = get_current_site(request)
        # subject = 'Activate Your Study Better Way Account'
        # message = render_to_string('authentication/account_activation_email.html',
        # {
        #     'user': subscription,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(subscription.pk)),
        #     'token': account_activation_token.make_token(subscription),
        # })
        # subscription.email_user(subject, message)

        # return redirect('account_activation_sent')

        # else:
        #     messages.error(request, "Please provide valid information.")
        #     # Redirect user to register page
        #     return render(request, self.template_name, self.context_object)


class SubscriptionActivateView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Subscription.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, f"Congratulations {user.email} !!! "
                                      f"Your account was activated "
                                      f"successfully"
                             )
            return render(request, 'authentication/subscription_success.html')
        else:
            return render(request, 'authentication/account_activation_invalid.html')


class SendEmail(LoginRequiredMixin,View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'account/_contact_form.html')
    
    def post(self, request, *args, **kwargs):
        template = render_to_string('account/blog_contact_message.html', {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })

        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,  # sender
            ['nirmalpandey27450112@gmail.com']  # receiver
        )

        email.fail_silently = False

        email.send()
        # messages.success(request,'Your message was successfully sent. I will do my best to get back to you in a timely manner :)')
        return render(request, 'account/blog_user_message_sent.html')



