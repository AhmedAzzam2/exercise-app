from email.policy import default
from unicodedata import category
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os

class Post(models.Model):
	exercisename = models.ForeignKey('Category', on_delete=models.CASCADE)
	hour = models.IntegerField(default=0 )
	min = models.IntegerField(default=0)
	file = models.FileField(null=True,blank=True,upload_to='Files')
	content = models.TextField()
	date_Posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	# required min or hour
	def get_required_min(self):
		if self.min == 0:
			return self.hour
		else:
			return self.hour + self.min / 60
	def __str__(self):
		return self.exercisename

	def extension(self):
		name, extension = os.path.splitext(self.file.name)
		return extension

	def get_absolute_url(self):
		return reverse('Post-detail', kwargs={'pk': self.pk})
		
		



class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	image = models.ImageField(upload_to='images/') 

	def __str__(self):
		return self.name

	def countyear(self):
		cat = Post.objects.filter( exercisename=self.id).filter( date_Posted__year__gte= timezone.now().year)  
		calc =0 
		for c in cat:
			calc = calc+( (c.hour*60) + c.min )
		return ("%02d:%02d" % (divmod(calc, 60)))

	def countmonth(self):
		cat = Post.objects.filter( exercisename=self.id).filter( date_Posted__month__gte= timezone.now().month)
		calc =0 
		for c in cat:
			calc = calc+( (c.hour*60) + c.min )
		return ("%02d:%02d" % (divmod(calc, 60)))

	def countday(self):
		cat = Post.objects.filter( exercisename=self.id).filter( date_Posted__day__gte= timezone.now().day,
																date_Posted__month__gte= timezone.now().month
																)
		calc =0 
		for c in cat:
			calc = calc+( (c.hour*60) + c.min )
		return ("%02d:%02d" % (divmod(calc, 60)))
	def get_absolute_url(self):
		return reverse('Category-detail', kwargs={'pk': self.pk})
		