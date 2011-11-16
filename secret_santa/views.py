from django.views.generic import TemplateView, FormView

from .forms import SantaForm
from .models import Family, Person
from .utils import make_key

class ChooseView(FormView):
	form_template_name = 'secret_santa/form.html'
	result_template_name = 'secret_santa/result.html'
	form_class = SantaForm
	def __init__(self, *args, **kwargs):
		self.template_name = self.form_template_name
		super(ChooseView, self).__init__(*args, **kwargs)
	def form_valid(self, form):
		giver = form.cleaned_data['giver']
		receiver = form.cleaned_data.get('receiver')
		if receiver is None:
			receiver = giver.get_receiver(form.cleaned_data['key'])
		context = {'receiver': receiver, 'giver': giver}
		self.template_name = self.result_template_name
		return self.render_to_response(context)

