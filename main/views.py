from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import ToDoList
from .forms import CreateNewList

def index(response, id):
    todo = ToDoList.objects.get(id=id)

    if response.method == "POST":
        if response.POST.get("save"):
            for item in todo.item_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                item.save()
        elif response.POST.get("newItem"):
            txt = response.POST.get("new")

            if len(txt) > 2:
                todo.item_set.create(text=txt, complete=False)
            else:
                print("inválido.")

    return render(response, 'main/list.html', {"todo": todo})

def home(response):
    return render(response, 'main/home.html', {})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            name= form.cleaned_data["name"]
            todo = ToDoList(name=name)
            todo.save()
            return HttpResponseRedirect("/%i" % todo.id)
    
    else:
        form = CreateNewList()

    return render(response, 'main/create.html', {"form": form })