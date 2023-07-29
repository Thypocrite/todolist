from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm
from datetime import datetime
from django.contrib.auth.decorators import login_required


@login_required
def create(request):
    message = ""
    user = request.user
    form = TodoForm()
    if not user.is_authenticated:
        message = "請先登入..."
    else:
        if request.method == "POST":
            print(request.POST)
            # 產生對應的TodoForm跟todo物件
            form = TodoForm(request.POST)
            if form.is_valid():
                todo = form.save(commit=False)
                # 指定user
                todo.user = request.user
                todo.save()
                message = "建立todo成功!"
                return redirect("todo")

    return render(
        request, "./todo/create.html", {"form": form, "message": message, "user": user}
    )


@login_required
def view(request, id):
    message = ""
    form, todo = None, None
    user = request.user
    try:
        if user.is_authenticated:
            todo = Todo.objects.get(id=id, user=user)
            form = TodoForm(instance=todo)
            if request.method == "POST":
                if request.POST.get("update"):
                    form = TodoForm(request.POST, instance=todo)
                    if form.is_valid():
                        temp_todo = form.save(commit=False)
                        if temp_todo.completed:
                            temp_todo.date_completed = datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                        else:
                            temp_todo.date_completed = None
                        temp_todo.save()
                        message = "修改成功!"
                    else:
                        message = "修改錯誤!"
                else:
                    todo.delete()
                    return redirect("todo")

        else:
            message = "請先登入..."
    except Exception as e:
        print(e)
        message = "無此代辦事項"

    return render(
        request,
        "./todo/view.html",
        {"todo": todo, "form": form, "message": message},
    )


def get_todos(request, completed=False, reverse=False):
    user = request.user
    todos = None
    if user.is_authenticated:
        sort_command = "-created" if reverse else "created"
        todos = Todo.objects.filter(user=user, completed=completed).order_by(
            sort_command
        )

    return todos


@login_required
def completed(request):
    todos = get_todos(request, completed=True)
    return render(request, "./todo/completed.html", {"todos": todos})


# Create your views here.
def todo(request):
    todos = get_todos(request, completed=False, reverse=True)
    return render(request, "./todo/todo.html", {"todos": todos})
