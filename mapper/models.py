from __future__ import unicode_literals
from random import choice
from string import ascii_lowercase, digits
import datetime
import os

from django.db import models
from django.utils import timezone
from BioTaxIDMapper import Mapper

# Create your models here.

def touch(path):
    """Simply creates an empty file. Only for tests."""
    open(path, 'w').close()
    
def rewrite_file(i,o):
    print('Input:{}'.format(i))
    print('Output:{}'.format(o))
    with open(i, 'r') as ifile, open(o, 'w') as ofile:
        for line in ifile:
            ofile.write(line*2)

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
        """Created not to overwrite init method"""
        self.jobid = self.generate_jobid()
        self.output_file = '{}.out'.format(self.jobid)
        self.output_file_path = os.path.abspath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '../files/output/{}'.format(self.output_file)))
        
        input_f = os.path.abspath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '../files/input/', self.input_file.file.name))
        self.submit_date = timezone.now()
        self.expiration_date = timezone.now() + timezone.timedelta(days=14)
        
        self.save()
        
        saved = Job.objects.filter(jobid=self.jobid)[0]
        
        print('\n\n')
        print('Output:{}'.format(saved.output_file_path))
        print('Input:{}'.format(saved.input_file.path))
        print('\n\n')
        #rewrite_file(i=str(saved.input_file.path), o=saved.output_file_path)
        Mapper.map_taxonomies(saved.input_file.path, saved.output_file_path)

    def generate_jobid(self):
        """Generates job id"""
        jobid = ''.join(choice(ascii_lowercase + digits) for i in range(12))
        
        return jobid
        if not Job.objects.filter(jobid=jobid):
             return jobid
        else:
             return self.generate_jobid()

    def __str__(self):
        """Returns job id as a name of db entry"""
        return self.jobid
    
    def expired(self):
        """Returns true if job has expired"""
        
        if self.submit_date <= datetime.datetime.now() - datetime.timedelta(days=14):
            return True
        else:
            return False
        
    def input_name(self):
        return self.input_file.path.split('/')[-1]