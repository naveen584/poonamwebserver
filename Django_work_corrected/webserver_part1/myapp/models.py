from django.db import models

# Create your models here.
class Seed(models.Model):
	seed_file = models.BinaryField()