from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import PersonForm,TaskForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        person_form = PersonForm(request.POST)

        if user_form.is_valid() and person_form.is_valid():
            user = user_form.save()
            person = person_form.save(commit=False)
            person.user = user
            person.save()
            login(request, user)
            return redirect("home")
    else:
        user_form = UserCreationForm()
        person_form = PersonForm()

    return render(request, "Register.html", { "user_form": user_form, "person_form": person_form })

# def login_view(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 person = user.person
#                 role = person.role
#                 team = person.team
#
#                 request.session['role'] = role
#                 request.session['team'] = team.name
#
#                 return redirect("home")
#             else:
#                 return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
#     else:
#         form = AuthenticationForm()
#
#     return render(request, 'login.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'person') and user.person is not None:
                    person = user.person
                    role = person.role
                    team = person.team

                    request.session['role'] = role
                    request.session['team'] = team.title if team else 'No team assigned'
                else:
                    request.session['role'] = 'No role assigned'
                    request.session['team'] = 'No team assigned'

                return redirect("home")
            else:
                return render(request, 'Login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = AuthenticationForm()

    return render(request, 'Login.html', {'form': form})


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("home")


@login_required
def tasks(request):
    user = request.user
    try:
        team = request.user.person.team
    except AttributeError:
        return render(request, 'tasks.html', {'tasks': [], 'employees': [], 'error': "אינך משויך לצוות"})

    employees = Person.objects.select_related('user').filter(team=team)
    tasks_qs = Task.objects.filter(team=team)
    status = request.GET.get('status')
    employee_id = request.GET.get('employee')

    if status and status != 'all':
        tasks_qs = tasks_qs.filter(status=status)

    if employee_id:
        if employee_id != 'null':
            tasks_qs = tasks_qs.filter(Executor__user_id=employee_id)
        else:
            tasks_qs = tasks_qs.filter(Executor=None)

    return render(request, 'tasks.html', {
        'tasks': tasks_qs,
        'employees': employees,
    })


def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.team = request.user.person.team

            task.save()
            return redirect('tasks')
        else:
            print(form.errors)
    else:
        form = TaskForm()

    return render(request, 'add_task.html', {'form': form})


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, pk=id)

    if task.Executor:
        messages.error(request, "אי אפשר למחוק משימה שיש לה אחראי.")
        return redirect('tasks')

    task.delete()
    messages.success(request, "המשימה נמחקה בהצלחה.")

    return redirect('tasks')


from django.contrib import messages


@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, pk=id)
    if task.Executor:
        messages.error(request, "אי אפשר לערוך משימה שכבר משויכת לאחראי.")
        return redirect('tasks')

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)

    return render(request, 'Edit_task.html', {'form': form, 'task': task})


@login_required
def update_task_status(request, id):
    # שליפת המשימה או החזרת 404 אם היא לא קיימת
    task = get_object_or_404(Task, pk=id)

    if request.method == "POST":
        new_status = request.POST.get('status')

        # 1. בדיקה שהמשתמש הנוכחי הוא אכן המבצע של המשימה
        if task.Executor.user != request.user:
            messages.error(request, "אינך מורשה לעדכן משימה שאינה משויכת אליך.")
            return redirect('tasks')

        # 2. בדיקה שהמשימה לא נמצאת כבר בסטטוס 'completed'
        if task.status == "completed":
            messages.error(request, "לא ניתן לשנות סטטוס של משימה שהושלמה.")
            return redirect('tasks')

        # עדכון הסטטוס ושמירה
        task.status = new_status
        task.save()
        messages.success(request, f"הסטטוס של '{task.title}' עודכן ל-{new_status}.")

    return redirect('tasks')


@login_required
def assign_task(request, id):
    task = get_object_or_404(Task, pk=id)
    person = get_object_or_404(Person, user=request.user)

    if request.method == "POST":
        if task.Executor is not None:
            messages.error(request, "משימה זו כבר משויכת לאחראי.")
            return redirect('tasks')

        task.Executor = person
        task.save()
        messages.success(request, "המשימה הוקצתה בהצלחה.")
        return redirect('tasks')

    return redirect('tasks')

# @login_required
# def TaskFilterByStatusForm(request):
#      if request.method == "POST":
#          selected_status = request.POST.get('status')
#          if selected_status == 'all':
#              return redirect('tasks')
#          filtered_tasks = Task.objects.filter(status=selected_status)
#          return render(request, 'tasks.html', {'tasks': filtered_tasks})
#      return redirect('tasks')
#
#
# @login_required
# def tasks_sorted_by_executor(request):
#     tasks = Task.objects.all()
#
#     executor_name = request.POST.get('executor', '').strip()
#
#     if executor_name:
#         tasks = tasks.filter(Executor__user__username__icontains=executor_name)
#
#     return render(request, 'tasks.html', {'tasks': tasks})

# @login_required
# def filter_tasks(request):
#     tasks = Task.objects.all()  # כל המשימות בהתחל
#     executor_name = request.POST.get('executor', '').strip()
#     selected_status = request.POST.get('status')
#     if executor_name and (selected_status or selected_status == 'all'):
#         tasks = Task.objects.filter(Executor__user__username__icontains=executor_name, status=selected_status)
#     # סינון לפי סטטוס אם יש
#     if selected_status and selected_status != 'all':
#         tasks = tasks.filter(status=selected_status)
#     # סינון לפי שם מבצע אם יש
#     if executor_name:
#         tasks = tasks.filter(Executor__user__username__icontains=executor_name)
#
#
#     return render(request, 'tasks.html', {'tasks': tasks})










