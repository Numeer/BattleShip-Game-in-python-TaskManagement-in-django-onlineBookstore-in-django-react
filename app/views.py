from django.core.mail import EmailMessage, send_mail
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import *
from django import forms



def send_task_notification_email(subject, message, recipient_list):
    subject = subject
    message = message
    from_email = 'numeer.qadri@arbisoft.com'
    recipient_list = recipient_list
    fail_silently = False
    send_mail(subject, message, from_email, recipient_list)


# Create your views here.
@login_required(login_url='login')
def home_page(request):
    return render(request, 'home.html')


def signup_page(request):
    # subject = 'subject'
    # message = 'message'
    # from_email = 'numeer.qadri@arbisoft.com'
    # recipient_list = ['qaadrinumeer@gmail.com']
    # send_mail(subject, message, from_email, recipient_list)
    if request.method == 'POST':
        uname = request.POST.get('fullname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pwd')
        pass2 = request.POST.get('pwd2')
        if pass1 == pass2:
            if User.objects.filter(username=uname).exists():
                return render(request, 'register.html', {'error': 'Username already taken'})
            elif User.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error': 'Email already taken'})
            else:
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                return redirect('login')
        else:
            return render(request, 'register.html', {'error': 'Password and confirm password must be same'})
    return render(request, 'register.html')


def login_page(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('pwd')
        user = authenticate(request, username=uname, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'User is not authenticated'})
    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('desc')
        due_date = request.POST.get('dueDate')
        assign_to_username = request.POST.get('assignTo')
        assign_to_user = User.objects.get(username=assign_to_username)

        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            status='new',
            assigned_user=assign_to_user,
            created_by=request.user
        )
        print("hello")
        if 'attachment' in request.FILES:
            uploaded_file = request.FILES['attachment']
            print(uploaded_file)
            attachment = Attachment(task=task, file=uploaded_file)
            attachment.save()

        # Send email notification to the assigned user
        # subject = 'New Task Assigned'
        # message = f'A new task has been assigned to you. Task Title: {title}'
        # recipient_list = [assign_to_user.email]
        # print(recipient_list)
        # send_task_notification_email(subject, message, recipient_list)

        return redirect('list')
    else:
        available_users = User.objects.all()
        return render(request, 'createTask.html', {'available_users': available_users})


@login_required(login_url='login')
def task_list_view(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        end_date = request.POST.get('end_date')
        assigned_user = request.POST.get('assigned_user')
        Flag = True
        if status and status != "No":
            Flag = False
            tasks = Task.objects.all().filter(status=status)
        if end_date and end_date != "":
            Flag = False
            due = timezone.datetime.strptime(end_date, '%Y-%m-%d')
            tasks = Task.objects.all().filter(due_date__date__lte=due.date())
        if assigned_user and assigned_user != "No":
            Flag = False
            tasks = Task.objects.all().filter(assigned_user__username=assigned_user)
            # pass
        if Flag:
            tasks = Task.objects.all().order_by('due_date', 'status')
            assigned_task_user = []
            for task in tasks:
                if task.assigned_user.id == request.user.id:
                    assigned_task_user.append(task.assigned_user.id)
            available_users = User.objects.all()
            return render(request, 'taskList.html',
                          {'tasks': tasks, 'assigned_task_user': assigned_task_user,
                           'available_users': available_users})
        elif not Flag:
            available_users = User.objects.all()
            return render(request, 'taskList.html', {'tasks': tasks, 'available_users': available_users})

    else:
        tasks = Task.objects.all().order_by('due_date', 'status')

        assigned_task_user = []
        for task in tasks:
            if task.assigned_user.id == request.user.id:
                assigned_task_user.append(task.assigned_user.id)
        available_users = User.objects.all()
        return render(request, 'taskList.html',
                  {'tasks': tasks, 'assigned_task_user': assigned_task_user, 'available_users': available_users})


@login_required(login_url='login')
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = task.comments.all()

    return render(request, 'taskDetail.html', {'task': task, 'comments': comments})


@login_required(login_url='login')
def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        text = request.POST.get('comment')
        user = User.objects.get(id=request.user.id)
        comment = Comment.objects.create(task=task, user=user, text=text)

    return redirect('details', task_id=task_id)


@login_required(login_url='login')
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.created_by == request.user or task.assigned_user == request.user:
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('desc')
            due_date = request.POST.get('dueDate')
            status = request.POST.get('status')

            task.title = title
            task.description = description
            task.due_date = due_date
            task.status = status
            task.save()

            return redirect('details', task_id=task_id)

        else:
            return render(request, 'update.html', {'task': task})

    else:
        messages.error(request, 'You do not have permission to update this task.')
        return redirect('details', task_id=task_id)


@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.created_by == request.user or request.user.is_superuser:
        if request.method == 'POST':
            task.delete()
            return redirect('list')
        else:
            return render(request, 'delete.html', {'task': task})
    else:
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('details', task_id=task_id)
