from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    """Simple form for uploading a file and submitting job"""
    class Meta:
        model = Job
        fields = ('input_file', )