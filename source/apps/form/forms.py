# Third-Party
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

# Django
from django import forms
from django.utils.translation import ugettext_lazy as _

# Local Django
from form.models import Contact, Register


class ContactForm(forms.ModelForm):
    full_name = forms.CharField(label=_('Name and Surname'), max_length=100)
    email = forms.EmailField(label=_('E-Mail Address'))
    message = forms.CharField(label=_('Your Message'), widget=forms.Textarea)
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget(explicit=True))

    class Meta:
        model = Contact
        fields = ('full_name', 'email', 'message', 'recaptcha')

    def save(self, activity=None, commit=True):
        contact = super(ContactForm, self).save(commit=False)

        if commit and activity:
            try:
                contact = Contact(
                    full_name=self.cleaned_data.get('full_name'),
                    email=self.cleaned_data.get('email'),
                    message=self.cleaned_data.get('message'),
                    activity=activity
                )

                contact.save()
            except:
                contact = None

        return contact


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label=_('First Name'), max_length=100)
    last_name = forms.CharField(label=_('Last Name'), max_length=100)
    email = forms.EmailField(label=_('Email'))
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget(explicit=True))

    class Meta:
        model = Register
        fields = ('first_name', 'last_name', 'email', 'recaptcha')

    def save(self, activity=None, commit=True):
        register = super(RegisterForm, self).save(commit=False)
        created = False

        if commit and activity:
            try:
                register = Register.objects.get(
                    first_name=self.cleaned_data.get('first_name'),
                    last_name=self.cleaned_data.get('last_name'),
                    email=self.cleaned_data.get('email'),
                    activity=activity
                )
            except Register.DoesNotExist:
                register = Register(
                    first_name=self.cleaned_data.get('first_name'),
                    last_name=self.cleaned_data.get('last_name'),
                    email=self.cleaned_data.get('email'),
                    activity=activity
                )
                register.save()
                created = True

        return register, created
