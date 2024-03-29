from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from .models import Recipe, Ingredient, Preparation
from .forms import CreateNewRecipe

# Create your views here.

def index(response, id):
	ls = Recipe.objects.get(id = id)

	if response.method == "POST":
		print(response.POST)
		if response.POST.get("save_ingredients"):
			for ingredient in ls.ingredient_set.all():
				ingredient.quantity = response.POST.get("q" + str(ingredient.id))
				ingredient.text = response.POST.get("t" + str(ingredient.id))
				ingredient.section = response.POST.get("s" + str(ingredient.id))
				ingredient.save()
			for preparation in ls.preparation_set.all():
				preparation.preparation = response.POST.get(str(preparation.id))
				preparation.save()


		elif response.POST.get("newIngredient"):
			txt = response.POST.get("new_ingredient")
			if response.POST.get("new_quantity") == "":
				quantity = 0
			else:
				quantity = response.POST.get("new_quantity")

			if len(txt) > 1:
				ls.ingredient_set.create(text=txt, quantity=quantity)
			else:
				print("Invalid input")


		elif response.POST.get("delete"):
			n = response.POST.get("delete")
			d = ls.ingredient_set.get(id = n)
			d.delete()

	return render(response, "main/list.html", {"ls":ls})

def home(response):
	return render(response, "main/home.html", {})

def create(response):
	if response.method == "POST":
		form = CreateNewRecipe(response.POST)

		if form.is_valid():
			n = form.cleaned_data["name"]
			r = Recipe(name = n, quantity = 0)
			r.save()
			r.preparation_set.create(preparation="Write preparation")
		return HttpResponseRedirect("/%i" %r.id)

	else:
		form = CreateNewRecipe()
	return render(response, "main/create.html", {"form":form})


def recipes(response):
	#rl = Recipe.objects.all()				#Display by id order
	rl = Recipe.objects.order_by('-meal')	#Display in alphabetical order

	if response.method == "POST":
		print(response.POST)
		if response.POST.get("save_recipes"):
			for recipe in rl:
				if (response.POST.get("q" + str(recipe.id)) == ""):
					recipe.quantity = 0
					recipe.meal = response.POST.get("m" + str(recipe.id))
				else:
					recipe.quantity = response.POST.get("q" + str(recipe.id))
					recipe.meal = response.POST.get("m" + str(recipe.id))
				recipe.save()
		elif response.POST.get("clear_recipes"):
			for recipe in rl:
				recipe.quantity = 0
				recipe.save()

	return render(response, "main/recipes.html", {"rl":rl})

def shoppinglist(response):
	sl = []
	ql = []
	temp = []
	shoppinglist = ""
	rl = Recipe.objects.order_by('name').exclude(quantity=0)
	for recipe in rl:
		for ingredient in recipe.ingredient_set.all():
			if (ingredient.section + "#" + ingredient.text) not in sl:
				sl.append(ingredient.section + "#" + ingredient.text)
				ql.append(ingredient.quantity*recipe.quantity)
			else:
				ql[sl.index(ingredient.section + "#" + ingredient.text)] += ingredient.quantity

	for i in range(len(sl)):
		if (ql[i] % 1 == 0):
			temp.append(str(sl[i]) + " x " + str(int(ql[i])) + "\n")
		else:
			temp.append(str(sl[i]) + " x " + str(round(ql[i],1)) + "\n")

	temp = sorted(temp)

	for i in range(len(temp)):
		temp1 = temp[i].split("#")
		shoppinglist += temp1[1]


	return render(response, "main/shoppinglist.html", {"shoppinglist":shoppinglist})


def delete(response):
	#rl = Recipe.objects.all()				#Display by id order
	rl = Recipe.objects.order_by('name')	#Display in alphabetical order

	if response.method == "POST":
		print(response.POST)

		if response.POST.get("delete"):
			n = response.POST.get("delete")
			d = rl.get(id = n)
			d.delete()

	return render(response, "main/delete.html", {"rl":rl})
