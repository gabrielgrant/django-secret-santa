from django.db import models

class Family(models.Model):
	name = models.CharField(max_length=255, unique=True)
	def __unicode__(self):
		return self.name
	def get_family_giving_counts(self):
		""" Returns the number of members of this family giving to each other family """
		# note: "order_by()" is needed to exclude default ordering
		counts = Person.objects.filter(family=self)  \
			.values('chosen_family')  \
			.order_by()  \
			.annotate(count=models.Count('chosen_family'))
		counts_d = dict((c['chosen_family'], c['count']) for c in counts)
		counts_d.pop(None, None)
		all_counts_d = {}
		for f in Family.objects.all():
			all_counts_d[f] = counts_d.get(f.pk, 0)
		return all_counts_d

class Person(models.Model):
	name = models.CharField(max_length=255, unique=True, db_index=True)
	family = models.ForeignKey(Family, related_name='members')
	key = models.CharField(max_length=40, blank=True)  # length of sha1 hash
	#has_chosen = models.BooleanField(default=False)
	chosen_family = models.ForeignKey(Family, related_name='givers', null=True, blank=True)
	def __unicode__(self):
		return self.name
	def get_allowed_families(self):
		family_giving_counts = self.family.get_family_giving_counts()
		family_giving_counts.pop(self.family, None)
		max_count = max(count for family, count in family_giving_counts.iteritems())
		allowed = set(family for family, count in family_giving_counts.iteritems() if count < max_count)
		if allowed:
			return allowed
		else:
			return set(family_giving_counts.iterkeys())
			
	def get_receiver(self, key):
		if self.chosen_family is not None:
			try:
				return Person.objects.get(key=key)
			except Person.DoesNotExist:
				raise ValueError('Wrong key')
		allowed_families = self.get_allowed_families()
		receiver = Person.objects.filter(  #TODO this should use 1.4's 'select_for_update'
			key='',
			family__in=allowed_families,
		).order_by('?')[:1]
		if len(receiver) != 1:
			raise RuntimeError('No eligible receivers found')
		else:
			receiver = receiver[0]
		self.chosen_family = receiver.family
		receiver.key = key
		self.save()
		receiver.save()
		return receiver


