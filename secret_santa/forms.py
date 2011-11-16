from django import forms

from .models import Person
from .utils import make_key

class SantaForm(forms.Form):
	giver = forms.TypedChoiceField(
		label='Your name',
		help_text='To avoid picking yourself',
		coerce=lambda x: Person.objects.get(name=x),
		empty_value=None,
	)
	password = forms.CharField(label='Choose a password', widget=forms.PasswordInput)
	def __init__(self, *args, **kwargs):
		super(SantaForm, self).__init__(*args, **kwargs)
		choices = [(p.name, p.name) for p in Person.objects.all()]
		self.fields['giver'].choices = choices
	def clean(self):
		cleaned_data = super(SantaForm, self).clean()
		giver = cleaned_data.get('giver')
		password = cleaned_data.get('password')
		if giver and password:
			# only process if the fields are present and validated so far
			key = make_key(giver.name, password)
			if giver.chosen_family is not None:
				try:
					receiver = Person.objects.get(key=key)
				except Person.DoesNotExist:
					raise forms.ValidationError(
						"%s, you've already chosen a password, but the password you just entered does not match." % giver.name
					)
				cleaned_data['receiver'] = receiver
			cleaned_data['key'] = key
		return cleaned_data
