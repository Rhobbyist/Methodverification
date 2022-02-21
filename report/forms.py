from django import forms

class UploadFileForm(forms.Form):
    fileuploads = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
    