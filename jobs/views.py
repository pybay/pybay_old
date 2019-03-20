from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from .models import Job
from .forms import JobForm

def create(request):
    form = JobForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('job_thanks'))
    return render(request, 'jobs/create.html', {'form': form})

def list(request):
  return render(request, "jobs/index.html", {'jobs': Job.visible.all()})

def thanks(request):
  return render(request, "jobs/thanks.html")

def detail(request, slug):
  job = get_object_or_404(Job, url=slug)
  return render(request, "jobs/detail.html", {'job': job})
