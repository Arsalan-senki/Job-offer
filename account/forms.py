from django.forms import ModelForm
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class EmployerRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "First Name :"
        self.fields['last_name'].label = "Last Name :"
        self.fields['password1'].label = "Password :"
        self.fields['password2'].label = "Confirm Password :"
        self.fields['email'].label = "Email :"
        self.fields['gender'].label = "Gender :"
        self.fields['telephone_number'].label = 'Telephone number :'
        self.fields['certificate'].label = 'Certificate :'
        self.fields['degree'].label = 'Degree :'
        self.fields['age'].label = 'Age :'
        
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter First Name',})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter Last Name',})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email',})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter Password',})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password',})
        self.fields['telephone_number'].widget.attrs.update({'placeholder':'Enter your phone number',})
        self.fields['certificate'].widget.attrs.update({'placeholder':'Enter your certificate'})
        self.fields['age'].widget.attrs.update({'placeholder':'Enter your age'})

    class Meta:
        model=CustomUser
        fields = ['first_name', 'last_name', 'email',
                   'password1', 'password2', 'gender',
                     'telephone_number', 'certificate',
                       'degree', 'age']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = UserCreationForm.save(self,commit=False)
        user.is_employer = True
        if commit:
            user.save()
        return user


class EmployeeRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['gender'].required = True
        self.fields['first_name'].label = "First Name :"
        self.fields['last_name'].label = "Last Name :"
        self.fields['password1'].label = "Password :"
        self.fields['password2'].label = "Confirm Password :"
        self.fields['email'].label = "Email :"
        self.fields['gender'].label = "Gender :"
        self.fields['telephone_number'].label = 'Telephone number :'
        self.fields['certificate'].label = 'Certificate :'
        self.fields['degree'].label = 'Degree :'
        self.fields['age'].label = 'Age :'

        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter First Name',})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter Last Name',})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email',})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter Password',})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password',})
        self.fields['telephone_number'].widget.attrs.update({'placeholder':'Enter your phone number',})
        self.fields['certificate'].widget.attrs.update({'placeholder':'Enter your certificate'})
        self.fields['age'].widget.attrs.update({'placeholder':'Enter your age'})

    class Meta:
        model=CustomUser
        fields = ['first_name', 'last_name', 'email',
                   'password1', 'password2', 'gender',
                     'telephone_number', 'certificate',
                       'degree', 'age']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        if not gender:
            raise forms.ValidationError("Gender is required")
        return gender

    def save(self, commit=True):
        user = UserCreationForm.save(self,commit=False)
        user.is_employer = False
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email =  forms.EmailField(
    widget=forms.EmailInput(attrs={ 'placeholder':'Email',})) 
    password = forms.CharField(strip=False,widget=forms.PasswordInput(attrs={'placeholder':'Password',}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("User Does Not Exist.")

            if not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")

            if not user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user