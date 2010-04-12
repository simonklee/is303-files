from django import forms
from models import Files

class FilesForm(forms.ModelForm):
    '''
    A forms for files model.
    '''
    class Meta:
        model = Files
    
