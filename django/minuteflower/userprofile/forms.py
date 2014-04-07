from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.core import mail
import random,string,md5
from django.contrib.sites.models import get_current_site
from django.template import Context, loader
from django.utils.http import int_to_base36
from django.contrib.auth.views import password_reset
from django.contrib.auth.tokens import default_token_generator

class ChangePasswordForm(forms.Form):
    password = forms.CharField()
    password2 = forms.CharField()

    def clean(self):
        cd = super(ChangePasswordForm, self).clean()
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("Passwords do not match")

        return cd

    def save(self, request):
        cd = self.cleaned_data
        request.user.set_password(cd.get('password'))
        request.user.save()
        user = authenticate(username=request.user.username, password=cd.get('password'))
        login(request, user)
        return request.user.is_authenticated() and (user != None)

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=("E-mail"), max_length=75)

    def clean_email(self):
        """
        Validates that an active user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(
                                email__iexact=email,
                                is_active=True
                            )
        if len(self.users_cache) == 0:
            raise forms.ValidationError(("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))

        return email

    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        from django.core.mail import send_mail
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            t = loader.get_template(email_template_name)
            c = {
                'email': user.email,
                'domain': "minuteflower.webfactional.com",
                'site_name': "Minuteflower",
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            send_mail(("Password reset on Minuteflower"),
                t.render(Context(c)), from_email, [user.email])
class UpdateSettingsForm(forms.Form):
    salary = forms.DecimalField(decimal_places=2, max_digits=19, required=False)
    pp_email = forms.EmailField(max_length=255, required=False)
    email = forms.EmailField(max_length=255, required=False)
    minute_value = forms.DecimalField(decimal_places=2, max_digits=19, required=False)
    favorite_charities = forms.CharField(max_length=255, required=False)
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)

    def save(self, request):
        cd = self.cleaned_data

        if not request.user.is_authenticated():
            return False
        if cd['salary']:
            request.user.get_profile().salary = cd['salary']
            request.user.get_profile().minute_value = round(float(cd['salary']) / 48 / 40 / 60, 2)
        if cd['pp_email']:
            request.user.get_profile().pp_email = cd['pp_email']
        if cd['email']:
            request.user.email = cd['email']
        if cd['minute_value']:
            request.user.get_profile().minute_value = cd['minute_value']
        if cd['first_name']:
            request.user.first_name = cd['first_name']
        if cd['last_name']:
            request.user.last_name = cd['last_name']
        if cd['favorite_charities']:
            favorite_charities = request.user.get_profile().favorite_charities
	    if cd['favorite_charities'] in favorite_charities:
		request.user.get_profile().favorite_charities = favorite_charities.replace(',' + cd['favorite_charities'] , '')
	    else:
		request.user.get_profile().favorite_charities += ',' + cd['favorite_charities']

        request.user.get_profile().save()
        request.user.save()
        return True


class UserEmailCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
