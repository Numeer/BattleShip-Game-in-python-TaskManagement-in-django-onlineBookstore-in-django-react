from django.core.mail import EmailMessage, send_mail
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from .models import *


def send_task_notification_email(subject, message, recipient_list):
    subject = subject
    message = message
    from_email = 'numeer.qadri@arbisoft.com'
    recipient_list = recipient_list
    fail_silently = False
    send_mail(subject, message, from_email, recipient_list)


# Create your views here.
class HomeView(View):
    @method_decorator(login_required, name='login')
    def get(self, request):
        return render(request, 'home.html')


class signup_page(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
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


#
#
class login_page(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        uname = request.POST.get('username')
        pass1 = request.POST.get('pwd')
        user = authenticate(request, username=uname, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'User is not authenticated'})


class logout_page(View):
    @method_decorator(login_required, name='login')
    def get(self, request):
        logout(request)
        return redirect('login')


class create_task(View):
    @method_decorator(login_required, name='login')
    def post(self, request):
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
        if 'attachment' in request.FILES:
            uploaded_file = request.FILES['attachment']
            attachment = Attachment(task=task, file=uploaded_file)
            attachment.save()

        # Send email notification to the assigned user
        # subject = 'New Task Assigned'
        # message = f'A new task has been assigned to you. Task Title: {title}'
        # recipient_list = [assign_to_user.email]
        # send_task_notification_email(subject, message, recipient_list)

        return redirect('list')

    @method_decorator(login_required, name='login')
    def get(self, request):
        available_users = User.objects.all()
        return render(request, 'createTask.html', {'available_users': available_users})


class task_list_view(View):
    @method_decorator(login_required, name='login')
    def post(self, request):
        status = request.POST.get('status')
        end_date = request.POST.get('end_date')
        assigned_user = request.POST.get('assigned_user')
        search_filter = request.POST.get('search_filter')
        Flag = True
        print(search_filter)
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
        if search_filter and search_filter != "":
            Flag = False
            tasks = Task.objects.filter(description__icontains=search_filter)
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

    @method_decorator(login_required, name='login')
    def get(self, request):
        tasks = Task.objects.all().order_by('due_date', 'status')
        assigned_task_user = []
        for task in tasks:
            if task.assigned_user.id == request.user.id:
                assigned_task_user.append(task.assigned_user.id)
        available_users = User.objects.all()
        return render(request, 'taskList.html',
                      {'tasks': tasks, 'assigned_task_user': assigned_task_user, 'available_users': available_users})


class task_detail(View):
    @method_decorator(login_required, name='login')
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        comments = task.comments.all()
        return render(request, 'taskDetail.html', {'task': task, 'comments': comments})


class add_comment(View):
    @method_decorator(login_required, name='login')
    def get(self, request, task_id):
        return redirect('details', task_id=task_id)

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        text = request.POST.get('comment')
        user = User.objects.get(id=request.user.id)
        comment = Comment.objects.create(task=task, user=user, text=text)
        messages.error(request, 'Comment added Successfully!')
        return redirect('details', task_id=task_id)


class update_task(View):
    @method_decorator(login_required, name='login')
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if task.created_by == request.user or task.assigned_user == request.user:
            return render(request, 'update.html', {'task': task})
        else:
            messages.error(request, 'You do not have permission to update this task.')
            return redirect('details', task_id=task_id)

    def post(self, request, task_id):
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
                messages.error(request, 'Task Updated Successfully!')
                return redirect('details', task_id=task_id)


class delete_task(View):
    @method_decorator(login_required, name='login')
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if task.created_by == request.user or request.user.is_superuser:
            return render(request, 'delete.html', {'task': task})
        else:
            messages.error(request, 'You do not have permission to delete this task.')
            return redirect('details', task_id=task_id)

    @method_decorator(login_required, name='login')
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if task.created_by == request.user or request.user.is_superuser:
            task.delete()
            messages.error(request, 'Task deleted Successfully!')
            return redirect('list')
