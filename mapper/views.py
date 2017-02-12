from django.shortcuts import render, HttpResponseRedirect, reverse

from .models import Job
from .forms import JobForm

# Create your views here.


def index(request):
    """Renders main website with welcome message"""
    return render(request, 'mapper/welcome.html', {})


def job_results(request, jobid):
    """Rendering view with job results
    
    Params:
        jobid (str): JobID to retrieve
    """
    
    job = Job.objects.filter(jobid=jobid)[0]
    
    return render(request=request,
                  template_name='mapper/job.html',
                  context={'job':job})

def new_job(request):
    """Renders submission request page"""
    
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)

        if form.is_valid():
            job = form.save(commit=False)
            job.create()
            return HttpResponseRedirect('/results/%s' % job.jobid)
    else:
        form = JobForm()
        
    return render(request=request,
                  template_name='mapper/submission.html',
                  context={'form': form})

def recent_jobs(request):
    """List of recent jobs"""
    latest_10 = Job.objects.order_by('-submit_date')[:10]
    
    return render(request, 'mapper/latest.html', {'latest': latest_10})

def retrieve(request):
    """Job retrieval form site"""
    render(request, 'mapper/retrieval.html')