from django.contrib.auth.models import User
from django.db import models
from time import time
import datetime


def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.', '_'), filename)


class JobType(models.Model):
    title = models.CharField(max_length=250, help_text='Internship, Full-time, Part-time.')

    def __unicode__(self):
        return self.title


class Location(models.Model):
    title = models.CharField(max_length=250, help_text='Add items to the location drop down.')

    def __unicode__(self):
        return self.title


class Country(models.Model):
    title = models.CharField(max_length=250, help_text='Add items to the country list drop down.')

    def __unicode__(self):
        return self.title


class Student(models.Model):
    uid = models.ForeignKey(User)
    title = models.CharField(max_length=250, help_text='The student name.')
    resume = models.FileField(upload_to=get_upload_file_name)
    location = models.ForeignKey(Location)
    country = models.ForeignKey(Country)
    prim_interest = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    sec_interest = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    cellphone = models.IntegerField(default=0)
    email_verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class Employer(models.Model):
    uid = models.ForeignKey(User)
    company_name = models.CharField(max_length=250, help_text='(Apple, Microsoft, Sony, Nokia... etc)')
    thumbnail = models.FileField(upload_to=get_upload_file_name)
    e_description = models.TextField(max_length=250, help_text='The company description.')
    LinkedIn = models.CharField(max_length=250, help_text='The employers LinkedIn account.')
    website = models.CharField(max_length=250, help_text='The employers website.')
    Twitter = models.CharField(max_length=250, help_text='The employers Twitter.')
    Facebook = models.CharField(max_length=250, help_text='The employers Facebook.')
    email_verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.company_name

    def URL_to_view_openings(self):
        return '/employeropenings/' + str(self.uid.id)

    def phone_number(self):
        return self.uid.email


class Category(models.Model):
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    description = models.TextField()

    def __unicode__(self):
        return self.title
        

class Skill(models.Model):
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    description = models.TextField()

    def __unicode__(self):
        return self.title


class JobPost(models.Model):
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    type = models.ForeignKey(JobType)
    is_premium = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    j_description = models.TextField()
    responsibilities = models.TextField()
    benefits_perks = models.TextField()
    location = models.ForeignKey(Location)
    skills = models.ManyToManyField(Skill)
    employer = models.ForeignKey(Employer, default=1)
    category = models.ForeignKey(Category, default=1)
    totalViews = models.IntegerField(default=0)
    applicants = models.IntegerField(default=0)
    compensation = models.IntegerField(default=0, help_text='Enter the amount in rupees here.')
    url = models.CharField(max_length=250, help_text='Redirect url.')
    deadline = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(30))

    def company(self):
        return self.employer.company_name

    def URL_to_view_applicants(self):
        return '/employeropenings/' + str(self.employer.uid_id)

    def __unicode__(self):
        return self.title


class JobApplication(models.Model):
    student = models.ForeignKey(Student, default=1)
    jobpost = models.ForeignKey(JobPost, default=1)
    cover_letter = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)

    def expiry_date(self):
        return self.jobpost.deadline

    def name(self):
        return self.student.title

    def job_post(self):
        return self.jobpost.title

    def total_applicants(self):
        return self.jobpost.applicants

    class Meta:
        get_latest_by = "pub_date"


class BlogPost(models.Model):
    title = models.CharField(max_length=250, help_text='The title of the blog post.')
    author = models.ForeignKey(User)
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    thumbnail = models.FileField(upload_to=get_upload_file_name)


class JobPostNewEmployer(models.Model):
    email = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    phone = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    first_name = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    last_name = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    password = models.CharField(max_length=250, help_text='Maximum 250 characters.')

    company_name = models.CharField(max_length=250, help_text='(Recruiter, Chief Executive Officer, etc...)')
    slug = models.SlugField(unique=True, help_text='url name for the employer.')
    thumbnail = models.FileField(upload_to=get_upload_file_name)
    e_description = models.TextField(max_length=250, help_text='The company description.')
    LinkedIn = models.CharField(max_length=250, help_text='The employers LinkedIn account.')
    website = models.CharField(max_length=250, help_text='The employers website.')
    Twitter = models.CharField(max_length=250, help_text='The employers Twitter.')
    Facebook = models.CharField(max_length=250, help_text='The employers Facebook.')

    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    type = models.ForeignKey(JobType)
    is_premium = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    j_description = models.TextField()
    responsibilities = models.TextField()
    benefits_perks = models.TextField()
    location = models.ForeignKey(Location)
    skills = models.ManyToManyField(Skill)
    category = models.ForeignKey(Category, default=1)
    totalViews = models.IntegerField(default=0)
    applicants = models.IntegerField(default=0)
    compensation = models.IntegerField(default=0, help_text='Enter the amount in rupees here.')
    url = models.CharField(max_length=250, help_text='Redirect url.')
    deadline = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.title

