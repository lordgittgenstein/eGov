from captcha.fields import CaptchaField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import ModelForm, EmailField, CharField, ChoiceField
from django.forms.fields import DateField, IntegerField, BooleanField
from django.forms.forms import Form
from django.forms.models import ModelChoiceField
from django.forms.widgets import Textarea, TextInput, PasswordInput, DateInput
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from corect.models import Complaint, Message, History, Location
from corect.utility import get_offices_over

class CorrespondForm(Form):
    number = IntegerField(widget=TextInput, required=True)
    key = CharField(max_length=10, widget=PasswordInput, required=True)

class DateInputForm(Form):
    date_input = DateField(widget=DateInput(attrs={'class':'datepicker', id:'id_date_input'}))

class HistoryFilterForm(Form):
    event = ChoiceField(choices=History.objects.distinct().values_list('event', 'event'))
    date_input = DateField(widget=DateInput(attrs={'class':'datepicker form-control'}))
    
class MessageForm(ModelForm):
    class Meta:
        model = Message
        widgets = {'text':Textarea(attrs={'class' : 'form-control', 'rows':'3'})}
        fields = ['text']

class MarkingForm(Form):
    resolved = BooleanField()
    unresolved = BooleanField()

class ChangeContactForm(Form):
    key = CharField(max_length=40, widget=PasswordInput, required=True, label='Enter Key')
    phone = CharField(required=False)
    email = EmailField(required=False)

    def __init__(self, old_key, data=None):
        self.old_key = old_key
        super(ChangeContactForm, self).__init__(data=data)

    def clean(self):
        cleaned_data = super(ChangeContactForm, self).clean()
        if self.old_key != self.cleaned_data.get('key'):
            raise ValidationError('Invalid key.')
        if not (cleaned_data.get('phone') or cleaned_data.get('email')):
            raise ValidationError('You must have a valid phone number or a valid email id.')
        return cleaned_data

class ChangeDetailsForm(Form):
    password = CharField(max_length=40, widget=PasswordInput, required=True, label='Current Password')
    phone = CharField(required=False)
    email = EmailField(required=False)

    def __init__(self, user, data=None):
        self.user = user
        super(ChangeDetailsForm, self).__init__(data=data)

    def clean(self):
        cleaned_data = super(ChangeDetailsForm, self).clean()
        if not self.user.check_password(self.cleaned_data.get('password')):
            raise ValidationError('Invalid password.')
        if not (cleaned_data.get('phone') and cleaned_data.get('email')):
            raise ValidationError('You must have a valid phone number and a valid email id.')
        return cleaned_data
    
class ChangeKeyForm(Form):
    key = CharField(max_length=40, widget=PasswordInput, required=True, label='Current Key')
    new = CharField(max_length=40, widget=PasswordInput, required=True, label='New Key')
    repeat = CharField(max_length=40, widget=PasswordInput, required=True, label='Enter Again')

    def __init__(self, old_key, data=None):
        self.old_key = old_key
        super(ChangeKeyForm, self).__init__(data=data)

    def clean(self):
        cleaned_data = super(ChangeKeyForm, self).clean()
        if self.old_key != self.cleaned_data.get('key'):
            raise ValidationError('Invalid key.')
        if cleaned_data.get('new') != cleaned_data.get('repeat'):
            raise ValidationError('Your key entries do not match.')
        return cleaned_data

class ChangePasswordForm(Form):
    password = CharField(max_length=40, widget=PasswordInput, required=True, label='Current Password')
    new = CharField(max_length=40, widget=PasswordInput, required=True, label='New Password')
    repeat = CharField(max_length=40, widget=PasswordInput, required=True, label='Enter Again')

    def __init__(self, user, data=None):
        self.user = user
        super(ChangePasswordForm, self).__init__(data=data)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        if not self.user.check_password(self.cleaned_data.get('password')):
            raise ValidationError('Invalid password.')
        if self.cleaned_data.get('new') != self.cleaned_data.get('repeat'):
            raise ValidationError('Your password entries do not match.')
        if len(self.cleaned_data.get('new')) < 8:
            raise ValidationError('Password too short')
        return cleaned_data
    
def make_form_a():
    class LocationForm(Form):
        class Meta:
            exclude = ('country', 'type')

        temp_jk = 'Jammu and Kashmir'
        state = ChoiceField(required=True,
                    choices=Location.objects.distinct().values_list('state', 'state').filter(state=temp_jk))
        division = ChoiceField(required=False,
                    choices=Location.objects.distinct().values_list('division', 'division').filter(state=temp_jk))
        district = ChoiceField(required=False,
                    choices=Location.objects.distinct().values_list('district', 'district').filter(state=temp_jk))
        subdistrict = ChoiceField(required=False,
                    choices=Location.objects.distinct().values_list('subdistrict', 'subdistrict').filter(state=temp_jk))
        locality = ChoiceField(required=False,
                    choices=Location.objects.distinct().values_list('locality', 'locality').filter(state=temp_jk))

        def clean(self):
            cleaned_data = super(LocationForm, self).clean()

            s = cleaned_data.get('state')
            v = cleaned_data.get('division')
            d = cleaned_data.get('district')
            t = cleaned_data.get('subdistrict')
            l = cleaned_data.get('locality')

            error_msg = 'Select a valid location. Read instruction numbered 1 above.'
            if s and not v and not d and not t and not l:
                if not Location.objects.filter(state=s).count():
                    raise ValidationError(error_msg)
                return cleaned_data
            elif s and v and not d and not t and not l:
                if not Location.objects.filter(state=s, division=v).count():
                    raise ValidationError(error_msg)
                return cleaned_data
            elif s and v and d and not t and not l:
                if not Location.objects.filter(state=s, division=v, district=d).count():
                    raise ValidationError(error_msg)
                return cleaned_data
            elif s and v and d and t and not l:
                if not Location.objects.filter(state=s, division=v, district=d, subdistrict=t).count():
                    raise ValidationError(error_msg)
                return cleaned_data
            elif s and v and d and t and l:
                if not Location.objects.filter(state=s, division=v, district=d, subdistrict=t, locality=l).count():
                    raise ValidationError(error_msg)
                return cleaned_data
            raise ValidationError(error_msg)
    return LocationForm

def make_form_b(location):
    class ComplaintForm(ModelForm):
        class Meta:
            model = Complaint            
            widgets = {'title':TextInput(attrs={'class' : 'form-control'}),
                       'body':Textarea(attrs={'class' : 'form-control', 'rows':'10'})} 
            exclude = ('key', 'resolved', 'wake_up', 'is_read_officer', 'is_read_boss')

        phone = CharField(required=False)
        email = EmailField(required=False)
        office = ModelChoiceField(queryset=get_offices_over(location))
        captcha = CaptchaField(label='Enter text')

        def clean(self):
            cleaned_data = super(ComplaintForm, self).clean()
            phone = cleaned_data.get('phone')
            email = cleaned_data.get('email')
            if not (phone or email):
                raise ValidationError('You must have a valid phone number or a valid email id.')
            
            content = cleaned_data.get('document')
            print content
            content_type = content.content_type.split('/')[0]
            print content_type
            if content_type in settings.CONTENT_TYPES:
                if content._size > settings.MAX_UPLOAD_SIZE:
                    raise ValidationError(_(
                            'Please keep filesize under %s. Current filesize %s') % (
                            filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
            else: raise ValidationError(_('File type is not supported'))
            return cleaned_data

    return ComplaintForm

class BlankComplaintForm(ModelForm):
    class Meta:
        model = Complaint
        widgets = {'title':TextInput(attrs={'class' : 'form-control'}),
                   'body':Textarea(attrs={'class' : 'form-control', 'rows':'10'})}
        exclude = ('key', 'resolved', 'wake_up', 'is_read_officer', 'is_read_boss')

    phone = CharField(required=False)
    email = EmailField(required=False)
    captcha = CaptchaField(label='Enter text')

    def clean(self):
        cleaned_data = super(BlankComplaintForm, self).clean()
        if not (cleaned_data.get('phone') or cleaned_data.get('email')):
            raise ValidationError('You must have a valid phone number or a valid email id.')
        
        try:
            content = cleaned_data.get('document')
            content_type = content.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if content._size > settings.MAX_UPLOAD_SIZE:
                    raise ValidationError(_('Please keep filesize under %s. Current filesize %s') % (
                            filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
            else: raise ValidationError(_('File type is not supported'))
        except: pass

        return cleaned_data