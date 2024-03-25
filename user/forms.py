from django import forms
from .models import Document
from .models import CustomUser

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'accept': '.pdf, .doc, .txt, .docx'}),
        }

class ImageUploadForm(forms.ModelForm): 
    class Meta:
        model = CustomUser
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'accept': '.jpeg, .jpg, .svg, .png'}),
        }