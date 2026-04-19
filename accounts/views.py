from django.shortcuts import render, redirect
from .forms import RegisterForm
from app.models import Profile


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            role = 'owner' if form.cleaned_data.get('is_owner') else 'visitor'
            Profile.objects.create(user=user, role=role)

            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})