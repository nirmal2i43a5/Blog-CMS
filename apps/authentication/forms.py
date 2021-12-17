

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# below form is from bona blog form

from django.contrib.auth.models import User

# Blog app imports
from apps.blog.models.author_models import Profile


class UserUpdateForm(forms.ModelForm):
    """
        Creates form for user to update their account.
    """
    email = forms.EmailField(widget=
                             forms.EmailInput(attrs={
                                                     'name': "email",
                                                     'id': "email",
                                                     'class': "form-control",
                                                    }
                                              ),
                             )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {

            'first_name': forms.TextInput(attrs={
                'name': "first-name",
                'class': "form-control",
                'id': "first-name"
            }),

            'last_name': forms.TextInput(attrs={
                'name': "last-name",
                'class': "form-control",
                'id': "last-name"
            }),

            'username': forms.TextInput(attrs={
                'name': "username",
                'class': "form-control",
                'id': "username"
            }),
        }


class ProfileUpdateForm(forms.ModelForm):
    """
       Creates form for user to update their Profile.
    """
    class Meta:
        model = Profile
        fields = [
                  'image', 'banner_image', 'job_title', 'bio', 'address',
                  'city', 'country', 'zip_code', 'twitter_url', 'github_url',
                  'facebook_url', 'instagram_url'
                  ]

        widgets = {

            'job_title': forms.TextInput(attrs={
                'name': "job-title",
                'class': "form-control",
                'id': "job-title"
            }),

            'bio': forms.Textarea(attrs={
                'name': "bio",
                'class': "form-control",
                'id': "bio", "rows": "5",
            }),

            'address': forms.TextInput(attrs={
                'name': "address",
                'class': "form-control",
                'id': "address"
            }),

            'city': forms.TextInput(attrs={
                'name': "city",
                'class': "form-control",
                'id': "city"
            }),

            'country': forms.TextInput(attrs={
                'name': "country",
                'class': "form-control",
                'id': "country"
            }),

            'zip_code': forms.TextInput(attrs={
                'name': "zip-code",
                'class': "form-control",
                'id': "zip-code"
            }),

            'image': forms.FileInput(attrs={
                "class": "form-control clearablefileinput",
                "type": "file",
                "id": "profileImage",
            }),

            'banner_image': forms.FileInput(attrs={
                "class": "form-control clearablefileinput",
                "type": "file",
                "id": "bannerImage",
            }),

            'facebook_url': forms.TextInput(attrs={
                'name': "facebook-account-url",
                'class': "form-control",
                'id': "github-account-url"
            }),

            'twitter_url': forms.TextInput(attrs={
                'name': "twitter-account-url",
                'class': "form-control",
                'id': "twitter-account-url"
            }),

            'instagram_url': forms.TextInput(attrs={
                'name': "instagram-account-url",
                'class': "form-control",
                'id': "instagram-account-url"
            }),

            'github_url': forms.TextInput(attrs={
                'name': "github-account-url",
                'class': "form-control",
                'id': "github-account-url"
            }),

        }


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    """
        Creates User registration form for signing up.
    """

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)

    email = forms.EmailField(max_length=254, required=True, widget=
                             forms.EmailInput(attrs={
                                 "name": "email", "class": "input100",
                                 "placeholder": "Email"
                                                    }
                                              ),
                             help_text='Required. Input a valid email address.'
                             )
    password1 = forms.CharField(label='Password', widget=
                                forms.PasswordInput(attrs={
                                 "name": "password1", "class": "input100",
                                 "placeholder": "Password"
                                                    }
                                                    ),
                                )

    password2 = forms.CharField(label = 'Confirm Password', widget=
                                forms.PasswordInput(attrs={
                                 "name": "password2", "class": "input100",
                                 "placeholder": "Confirm Password"
                                                    }

                                                    ),
                                )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {

            "username": forms.TextInput(attrs={
                "name": "username", "class": "input100",
                "placeholder": "Username"
            }),


        }


    