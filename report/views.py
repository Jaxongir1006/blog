from django.shortcuts import render,redirect
from .forms import SubscribeForm
from blogging.signals import new_signal

def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            new_signal.send(sender=None, mydata = form.cleaned_data.get("email"))
            form.save()

    url = request.META.get('HTTP_REFERER')

    return redirect(url)