from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


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
