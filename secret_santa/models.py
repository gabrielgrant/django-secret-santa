from django.db import models

class Family(models.Model):
	name = models.CharField(max_length=255, unique=True)
	def __unicode__(self):
		return self.name + ': ' + ', '.join(m.name for m in self.members.all())
	def get_family_giving_counts(self):
		""" Returns the number of members of this family giving to each other family """
		# note: "order_by()" is needed to exclude default ordering
		counts = Person.objects.filter(family=self)  \
			.values('chosen_family')  \
			.order_by()  \
			.annotate(models.Count('chosen_family'))
		return counts

class Person(models.Model):
	name = models.CharField(max_length=255, unique=True, db_index=True)
	family = models.ForeignKey(Family, related_name='members')
	key = models.CharField(max_length=40, blank=True)  # length of sha1 hash
	#has_chosen = models.BooleanField(default=False)
	chosen_family = models.ForeignKey(Family, related_name='givers', null=True, blank=True)
	def get_allowed_families(self):
		family_giving_counts = self.family.get_family_giving_counts()
		family_giving_counts.pop(None)
		family_giving_counts.pop(self.family)
		min_count = min(count for family, count in family_giving_counts.iteritems())
		return set(family for family, count in family_giving_counts.iteritems() if count == min_count)
			
	def get_receiver(self):
		if not isinstance(giver, Person):
			if isinstance(giver, basestring):
				giver = Person.objects.get(giver)
			else:
				raise TypeError('giver must be a Person model or a name string')
		allowed_families = self.get_allowed_families()
		receiver = Person.objects.filter(
			key=None,
			family__in=allowed_families,
		).order_by('?')[:0]
		if len(receiver) == 1:
			return receiver
		else:
			raise RuntimeError('No eligible receivers found')


