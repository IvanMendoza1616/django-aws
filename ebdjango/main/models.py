from django.db import models

# Create your models here.
class ToDoList(models.Model):
	name = models.CharField(max_length = 200)

	def __str__(self):
		return self.name

class Item(models.Model):
	todolist = models.ForeignKey(ToDoList, on_delete = models.CASCADE)
	text = models.CharField(max_length = 300)
	complete = models.BooleanField()

	def __str__(self):
		return self.text

class Recipe(models.Model):
	name = models.CharField(max_length = 200)
	quantity = models.IntegerField()

	def __str__(self):
		return self.name

class Ingredient(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE)
	text = models.CharField(max_length = 300)
	quantity = models.FloatField()

	def __str__(self):
		return self.text

class Preparation(models.Model):
	recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE)
	preparation = models.CharField(max_length = 1000)

	def __str__(self):
		return self.preparation