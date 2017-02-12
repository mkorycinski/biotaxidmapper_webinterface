from __future__ import unicode_literals
from random import choice
from string import ascii_lowercase, digits
import datetime
import os

from django.db import models
from django.utils import timezone
from BioTaxIDMapper import Mapper

# Create your models here.

class Job(models.Model):
    """Model representing job object"""
    
    input_file = models.FileField(upload_to='./input/')
    jobid = models.CharField(max_length=12, default='0')
    output_file = models.CharField(max_length=255, default='tmp.out')
    output_file_path = models.CharField(max_length=255,
                                        default='./output/tmp.out')
    submit_date = models.DateTimeField(default=timezone.now())
    expiration_date = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=14))
    
    def create(self):
        """Created not to overwrite init method."""
        
        # Generate unique JobID
        self.jobid = self.generate_jobid()
        
        # Set paths for output file handling
        self.output_file = '{}.out'.format(self.jobid)
        self.output_file_path = os.path.abspath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '../files/output/{}'.format(self.output_file)))
        
        # Set submission date to now, and expiration date
        # to 14 days ahead.
        self.submit_date = timezone.now()
        self.expiration_date = timezone.now() + timezone.timedelta(days=14)
        
        # Save in the database
        self.save()
        
        # That needs to be tackled. Before Job object is saved in the
        # database paths to input files are incorrect - path to the
        # directory is not final (rather temporary) and filename is as
        # the filename submitted by the user. If such file exists in the
        # input folder - django adds suffix no to overwrite already existing
        # file. This is the name we are looking for. As a fast solution
        # it was easier to retrieve saved record from the database since
        # then all the paths are correct. On SSD should work fast but
        # perhaps there is a faster and more elegant way, but it's already
        # 2 am. TO BE CONSIDERED FOR REFACTORING LATER!!!
        saved = Job.objects.filter(jobid=self.jobid)[0]
        
        # Run map_taxonomies on input file and save results under
        # output file
        Mapper.map_taxonomies(saved.input_file.path, saved.output_file_path)

    def generate_jobid(self):
        """Generates unique job id recursively"""
        
        # generate 12 char long job id
        jobid = ''.join(choice(ascii_lowercase + digits) for i in range(12))
        
        # if job with generated id does not exist - return jobid
        if not Job.objects.filter(jobid=jobid):
             return jobid
        
        # if exists - try again
        else:
             return self.generate_jobid()

    def __str__(self):
        """Returns job id as a name of db entry"""
        return self.jobid
    
    def expired(self):
        """Returns true if job has expired, false if not"""
        
        if self.submit_date <= datetime.datetime.now() - datetime.timedelta(days=14):
            return True
        else:
            return False
        
    def input_name(self):
        """Returns input file name without a path."""
        return self.input_file.path.split('/')[-1]