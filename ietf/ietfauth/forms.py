import re

from django import forms
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.core.urlresolvers import reverse as urlreverse

from ietf.person.models import Person, Email


class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Your email (lowercase)")

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not email:
            return email
        if email.lower() != email:
            raise forms.ValidationError('The supplied address contained uppercase letters.  Please use a lowercase email address.')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('An account with the email address you provided already exists.')
        return email


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput,
                                            help_text="Enter the same password as above, for verification.")

    def clean_password_confirmation(self):
        password = self.cleaned_data.get("password", "")
        password_confirmation = self.cleaned_data["password_confirmation"]
        if password != password_confirmation:
            raise forms.ValidationError("The two password fields didn't match.")
        return password_confirmation


def ascii_cleaner(supposedly_ascii):
    outside_printable_ascii_pattern = r'[^\x20-\x7F]'
    if re.search(outside_printable_ascii_pattern, supposedly_ascii):
        raise forms.ValidationError("Please only enter ASCII characters.")
    return supposedly_ascii

class PersonForm(ModelForm):
    class Meta:
        model = Person
        exclude = ('time', 'user')

    def clean_ascii(self):
        return ascii_cleaner(self.cleaned_data.get("ascii") or u"")

    def clean_ascii_short(self):
        return ascii_cleaner(self.cleaned_data.get("ascii_short") or u"")


class NewEmailForm(forms.Form):
    new_email = forms.EmailField(label="New email address", required=False)

    def clean_new_email(self):
        email = self.cleaned_data.get("new_email", "")
        if email:
            existing = Email.objects.filter(address=email).first()
            if existing:
                raise forms.ValidationError("Email address '%s' is already assigned to account '%s' (%s)" % (existing, existing.person and existing.person.user, existing.person))
        return email


class RoleEmailForm(forms.Form):
    email = forms.ModelChoiceField(label="Role email", queryset=Email.objects.all())

    def __init__(self, role, *args, **kwargs):
        super(RoleEmailForm, self).__init__(*args, **kwargs)

        f = self.fields["email"]
        f.label = u"%s in %s" % (role.name, role.group.acronym.upper())
        f.help_text = u"Email to use for <i>%s</i> role in %s" % (role.name, role.group.name)
        f.queryset = f.queryset.filter(models.Q(person=role.person_id) | models.Q(role=role))
        f.initial = role.email_id
        f.choices = [(e.pk, e.address if e.active else u"({})".format(e.address)) for e in f.queryset]


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="Your email (lowercase)")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(username=email).exists():
            raise forms.ValidationError(mark_safe("Didn't find a matching account. If you don't have an account yet, you can <a href=\"{}\">create one</a>.".format(urlreverse("create_account"))))
        return email


class TestEmailForm(forms.Form):
    email = forms.EmailField(required=False)

