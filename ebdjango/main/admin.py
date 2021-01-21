from django.contrib import admin
from .models import ToDoList, Item
from .models import Recipe, Ingredient, Preparation
# Register your models here.
admin.site.register(ToDoList)
admin.site.register(Item)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Preparation)