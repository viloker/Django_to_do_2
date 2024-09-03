from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from .models import TasksModels, UserModel
from .forms import TasksForm, LoginForm

""" check user"""


def check_session(request):
    if 'email' not in request.session.keys():
        return False
    return True


""" about"""


class AboutView(View):

    def get(self, request):
        # del request.session['email']
        # print(request.session.keys())
        return render(request, 'about.html')

    def post(self, request):
        if check_session(request):
            return redirect('tasks')
        return redirect('login')


""" log in"""


class LoginView(View):

    def get(self, request):
        forms = LoginForm()
        return render(request, 'login.html', {'forms': forms})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user_email = form.cleaned_data['email']
            request.session['email'] = user_email
            print(user_email)

            # якщо користувача нема то я його додаю
            try:
                user = UserModel.objects.get(email=user_email)

                if user.password != form.cleaned_data['password']:
                    return redirect('login')


            except UserModel.DoesNotExist:
                user = UserModel(email=user_email,
                                 password=form.cleaned_data['password'])
                user.save()
            return redirect('tasks')


""" tasks """


class TasksView(View):
    def get(self, request):
        if not check_session(request):
            return redirect('login')

        tasks = TasksModels.objects.filter(user=UserModel.objects.get(email=request.session.get('email')))
        forms = TasksForm()

        return render(request, 'tasks.html', {"tasks": tasks, 'forms': forms})

    def post(self, request):
        form = TasksForm(request.POST)

        if form.is_valid():
            user = UserModel.objects.get(email=request.session['email'])
            task = TasksModels(user=user, task=form.cleaned_data['task'])
            task.save()

        # delete task
        if "task_id" in request.POST:
            task_id = request.POST.get('task_id')
            TasksModels.objects.get(pk=task_id).delete()

        # update task
        if "update_task" in request.POST:
            task_id = request.POST.get("update_task")

        return redirect('tasks')


""" Update """
class UpdateView(View):
    def get(self, request, task_id):
        task = TasksModels.objects.get(pk=task_id)
        return render(request, 'update.html', {'task': task})

    def post(self, request, task_id):
        if "new_task" not in request.POST:
            return redirect('update', task_id)

        task = TasksModels.objects.get(pk=task_id)
        task.task = request.POST.get("new_task")
        task.save()

        return redirect('tasks')

