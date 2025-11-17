from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from Todos.models import Todo


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()
        return redirect("login")
    return render(request, "signup.html")


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("home")
    return render(request, "login.html")


def logoutUser(request):
    logout(request)
    return redirect("login")


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        addTodo(request)
    todo = None
    todos = Todo.objects.filter(user=request.user, completed=False)
    return render(request, "index.html", {"user": request.user, "todos": todos})


def addTodo(request):
    title = request.POST.get("title")
    todo = Todo(title=title, user=request.user)
    return todo.save()


def edit(request, id):
    todo = Todo.objects.get(id=id)
    if request.method == "POST":
        todo.title = request.POST.get("title")
        todo.save()
        return redirect("home")
    todos = Todo.objects.filter(user=request.user, completed=False)
    return render(
        request, "index.html", {"user": request.user, "todos": todos, "todo": todo}
    )


def mark(request, id):
    todo = Todo.objects.get(id=id)
    todo.completed = True
    todo.save()
    return redirect("home")


def delete(request, id):
    todo = Todo.objects.get(id=id)
    todo.delete()
    return redirect("home")
