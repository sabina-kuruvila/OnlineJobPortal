from django import forms
from django.contrib.auth.models import User
from .models import HR, Candidate, Company, Vacancy 

class ApplyForm(forms.ModelForm):
    class Meta:
        model = Candidate  # The model this form is linked to
        fields = ['name', 'DOB', 'gender', 'mobile', 'email', 'resume']  # Include all fields from the Candidate model


    # Override company field to display as text and # Display company as a disabled text field
    company = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}),required=True)

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super(ApplyForm, self).__init__(*args, **kwargs) # Call the parent's __init__ method
        if company:
            self.fields['company'].queryset = Company.objects.filter(id=company.id)
            self.fields['company'].initial = company


class VacanciesForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields =['position', 'description', 'experience', 'salary', 'location']
