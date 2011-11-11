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
			receiver = giver.get_receiver(form.cleaned_data['key'])
		context = {'receiver': receiver, 'giver': giver}
		return self.render_to_response(context)

