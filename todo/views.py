from django.shortcuts import render, get_object_or_404
from .models import Todo


def view(request, id):
    message = ""
    todo = None
    user = request.user
    try:
        if user.is_authenticated:
            todo = Todo.objects.get(id=id, user=user)
        else:
            message = "請先登入..."
    except Exception as e:
        print(e)
        message = "無此代辦事項"

    return render(request, "./todo/view.html", {"todo": todo, "message": message})


# Create your views here.
def todo(request):
    user = request.user
    todos = None
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)
        print(todos)

    return render(request, "./todo/todo.html", {"todos": todos})