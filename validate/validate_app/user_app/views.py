from django.shortcuts import render, redirect

from .form import UserForm


def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Замените 'success_url' на URL-адрес вашей страницы успешной регистрации
    else:
        form = UserForm()
    return render(request, 'user_app/index.html', {'form': form})
