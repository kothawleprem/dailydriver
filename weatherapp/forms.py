from django import forms

class LocationForm(forms.Form):
    text = forms.CharField(max_length=45,
        widget=forms.TextInput(
            attrs={'class':'form-control','placeholder':'Enter YOur City','aria-label':'Location','aria-describeby':'add-btn'}))