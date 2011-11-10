import random

from django.test import TestCase

from .models import Family, Person
from .views import ChooseView
from .utils import make_key

# test that it works fine if people select the same password
class BaseSantaTestCase(TestCase):
	def setUp(self):
		for i in range(3):
			f = Family.objects.create(name='fam%s' % i)
			setattr(self, 'f%s' % i, f)
			for j in range(3):
				p = Person.objects.create(name='fam%s mem%s' % (i, j), family=f)
				setattr(self, 'f%s_m%s' % (i, j), p)

class ChooseViewTests(BaseSantaTestCase):
	pass
class FamilyModelTests(BaseSantaTestCase):
	def test_get_family_giving_counts_none(self):
		counts = {self.f0: 0, self.f1: 0, self.f2: 0}
		self.assertEqual(self.f1.get_family_giving_counts(), counts)
		self.f1_m1.chosen_family = self.f2
		self.f1_m1.save()
		counts[self.f2] = 1
		self.assertEqual(self.f1.get_family_giving_counts(), counts)
		self.f1_m2.chosen_family = self.f0
		self.f1_m2.save()
		counts[self.f0] = 1
		self.assertEqual(self.f1.get_family_giving_counts(), counts)
		self.f2_m1.chosen_family = self.f0
		self.f2_m1.save()
		counts[self.f2] = 0
		self.assertEqual(self.f2.get_family_giving_counts(), counts)

class PersonModelTests(BaseSantaTestCase):
	def test_get_allowed_families(self):
		fam_set = set([self.f0, self.f2])
		self.assertEqual(self.f1_m0.get_allowed_families(), fam_set)
		self.f1_m1.chosen_family = self.f2
		self.f1_m1.save()
		fam_set = set([self.f0])
		self.assertEqual(self.f1_m0.get_allowed_families(), fam_set)
		self.f1_m2.chosen_family = self.f0
		self.f1_m2.save()
		fam_set = set([self.f0, self.f2])
		self.assertEqual(self.f1_m0.get_allowed_families(), fam_set)
	def test_get_receiver(self):
		recv1 = self.f1_m1.get_receiver('akey'*10)
		recv2 = self.f1_m1.get_receiver('akey'*10)
		self.assertEqual(recv1, recv2)
		self.assertRaises(ValueError, self.f1_m1.get_receiver, 'bkey'*10)
	def test_all_get_receivers(self):
		people = list(Person.objects.all())
		random.shuffle(people)
		for p in people:
			key = make_key(p.name, 'the same pass')
			print p, p.get_receiver(key)

class SantaFormTests(BaseSantaTestCase):
	pass

