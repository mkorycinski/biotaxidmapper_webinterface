import datetime
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.utils import timezone

from .models import Job
from .forms import JobForm
from BioTaxIDMapper.Mapper import map_taxonomies

# Create your views here.


def rewrite_file(i, o):
    with open(i, 'r') as ifile, open(o, 'w') as ofile:
        for line in ifile:
            ofile.write(line*2)

def index(request):
    return render(request, 'mapper/welcome.html', {})

def job_results(request, jobid):
    """Rendering view with job results"""
    
    job = Job.objects.filter(jobid=jobid)
    
    return render(request=request,
                  template_name='mapper/job_results.html',
                  context={'job':job})

def new_job(request):
    """Submission request page"""
    
    
    # form = JobForm()
    # return render(request, 'mapper/submission.html', {'form': form})
    
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)

        if form.is_valid():
            print('goes to this custom thing!')
            job = form.save(commit=False)
            # job.jobid = job.generate_jobid()
            # job.output_file = '%s.out' % job.jobid
            # job.submit_date = timezone.now()
            job.create()
            # input_file = form.cleaned_data['input_file']
            # post = m.Post.objects.create(input_file=input_file)
            
            # rewrite_file(job.input_file.path, job.output_file)
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

def job_results(request, jobid):
    """Views results of a given job"""
    
    jobb = Job.objects.filter(jobid=jobid)[0]
    
    return render(request, 'mapper/job.html', {'job': jobb})

def retrieve(request):
    """Job retrieval form site"""
    render(request, 'mapper/retrieval.html')