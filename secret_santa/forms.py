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
		giver = self.cleaned_data['giver']
		password = self.cleaned_data['password']
		key = make_key(giver.name, password)
		if giver.chosen_family is not None:
			try:
				receiver = Person.objects.get(key=key)
			except Person.DoesNotExist:
				raise Form.ValidationError(
					"You've already chosen, but the password you entered does not match."
				)
			self.cleaned_data['receiver'] = receiver
		self.cleaned_data['key'] = key
		return self.cleaned_data
