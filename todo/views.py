from django.shortcuts import render
from .models import Todo
# Create your views here.

def todo(request):
    user=request.user
    todos=None
    if user.is_authenticated:
        todos=Todo.objects.filter(user=user)
        print(todos)
    


    return render(request,"./todo/todo.html",{"todos":todos})


