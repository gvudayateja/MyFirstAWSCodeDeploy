from django import forms
from blog.models import *


class AuthorForm(forms.ModelForm):
    firstname = forms.CharField(max_length=255, required=True)
    lastname = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Author
        fields = '__all__'

    def clean(self):
        data = super(AuthorForm, self).clean()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        author = Author.objects.filter(firstname__iexact=firstname, lastname__iexact=lastname).exclude(id=self.instance.id)
        if author:
            self.add_error('firstname', 'Author Already Exists with this Name')
        return data

    def clean_email(self):
        email = self.cleaned_data['email']
        author_email = Author.objects.filter(email__iexact=email).exclude(id=self.instance.id)
        if author_email:
            raise forms.ValidationError('Email Already Exists. Please provide some other Email Id')
        return email

    def clean_contact(self):
        contact = self.cleaned_data.get('contact', None)
        try:
            int(contact)
        except:
            raise forms.ValidationError('Contact Number must be in Integers')
        author_contact = Author.objects.filter(contact__iexact=contact).exclude(id=self.instance.id)
        if author_contact:
            raise forms.ValidationError('Contact already Exists. Please Check Your Number!!')
        else:
            min_length = 10
            max_length = 12
            num_length = str(int(contact))
            if len(num_length) < min_length or len(num_length) > max_length:
                raise forms.ValidationError('Contact number must be Min 10 Digits and Max 12 Digits')
        return contact


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']
        cat = Category.objects.filter(name__iexact=name).exclude(id=self.instance.id)
        if cat:
            raise forms.ValidationError('Categoty Already Exists. Please Enter Another Name')
        return name


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = '__all__'


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    re_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'mobile', 'password', 'pin')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        print username
        user_name = User.objects.filter(username__iexact=username).exclude(id=self.instance.id)
        print user_name
        if user_name:
            raise forms.ValidationError('Username Already Registered, Enter Another Username')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        reg_email = User.objects.filter(email__iexact=email).exclude(id=self.instance.id)
        if reg_email:
            raise forms.ValidationError('Email Already Exists, Enter Another Email Id')
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        try:
            int(mobile)
        except:
            raise forms.ValidationError('Mobile Number must be in Integers')
        num_length = str(int(mobile))
        if len(num_length) != 10:
            raise forms.ValidationError('Mobile number must be 10 Digits')
        return mobile

    def clean_pin(self):
        pin = self.cleaned_data['pin']
        if pin != '1234':
            raise forms.ValidationError('Invalid Pin')
        return pin