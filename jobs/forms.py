from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.forms import ModelForm

from .models import Job

class JobForm(ModelForm):

    details = forms.CharField(label="Summary", widget=forms.Textarea, max_length="400", help_text="A brief description (Max 400 chars.)")

    class Meta:
        model = Job
        fields = ['title', 'company', 'location', 'contact_email', 'contact_phone', 'logo', 'details', 'lengthy_details', 'link']


    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-myform'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-5'
        super(JobForm, self).__init__(*args, **kwargs)
