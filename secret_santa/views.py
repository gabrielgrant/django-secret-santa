from django.views.generic import TemplateView, FormView

from .forms import SantaForm
from .models import Family, Person
from .utils import make_key

class ChooseView(FormView):
	template_name = 'secret_santa/index.html'
	form_class = SantaForm
	def form_valid(self, form):
		giver = form.cleaned_data['giver']
		receiver = form.cleaned_data.get('receiver')
		if receiver is None:
			receiver = giver.get_receiver()
		return self.render_to_response(receiver=receiver, giver=giver)
		return 
		giver_name = form.cleaned_data['name']
		password = form.cleaned_data['password']
		make_key(giver.name, password)
		try:
			receiver = Person.objects.get(key=key)
		except Person.DoesNotExist:
			giver = Person.objects.get(name=name)

