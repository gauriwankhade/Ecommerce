from django import forms
from django.forms import ModelForm
from .models import Consumer

from django.contrib.auth.hashers  import make_password, check_password 



class RegisterForm(ModelForm):
	class Meta:
		model = Consumer
		fields = ['username','email','first_name','last_name','password']

	password = forms.CharField(
    	widget=forms.PasswordInput()
	)

	def clean_username(self):
		username = self.cleaned_data['username']

		try:
			user = Consumer.objects.get(username=username)
		except:
			return username
		raise forms.ValidationError(u'Username "%s" is already in use.' % username)

	def clean_email(self):
		email = self.cleaned_data['email']

		try:
			email= Consumer.objects.get(email=email)
		except:
			return email
		raise forms.ValidationError('email already registered')


	
	

class LoginForm(forms.Form):
	username = forms.CharField(required=True, max_length= 100,
								widget = forms.TextInput(
								attrs = {
										'type' : 'text',
										})
								)
	password = forms.CharField(required=True, widget = forms.PasswordInput(
				attrs={
		                'type': 'password',
		                
		            }))
					


	# def clean_user(self):
	# 	username = self.cleaned_data['username']

	# 	try:
	# 		user = Consumer.objects.get(username=username)
	# 	except Consumer.DoesNotExist:
	# 		raise forms.ValidationError('user does not exist')
	# 	return user

class ContactForm(forms.Form):
	name = forms.CharField(required=True, max_length= 100,
								widget = forms.TextInput(
								attrs = {
										'type' : 'text',
										'placeholder': 'Enter name '})
								)
	email = forms.EmailField(required=True, widget = forms.TextInput(
				attrs={
					'type': 'text',
					'placeholder': 'Enter your email'
					}))
					
	comment	 = forms.CharField(required=True,
								widget = forms.TextInput())
									
	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = ''
		self.fields['email'].label = ''
		self.fields['comment'].label = "What do you want to say?"
		
					




	