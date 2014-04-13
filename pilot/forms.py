__author__ = 'mateuszandrzejczuk'
from django import forms
from models import Student, Employer, Category, JobPost, Skill, JobApplication, BlogPost, JobPostNewEmployer


class JobForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ('title', 'type', 'j_description', 'category', 'responsibilities', 'benefits_perks', 'location', 'url', 'compensation', 'skills')

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        # for fieldname in ['title', 'body', 'thumbnail', 'categories']:
            # self.fields[fieldname].help_text = None


class NewEmployerJobForm(forms.ModelForm):
    class Meta:
        model = JobPostNewEmployer
        fields = ('first_name', 'last_name', 'email', 'password', 'phone', 'company_name', 'thumbnail', 'e_description', 'LinkedIn', 'website', 'Twitter', 'Facebook', 'title', 'type', 'j_description', 'category', 'responsibilities', 'benefits_perks', 'location', 'url', 'compensation', 'skills')

    def __init__(self, *args, **kwargs):
        super(NewEmployerJobForm, self).__init__(*args, **kwargs)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('location', 'country', 'prim_interest', 'sec_interest', 'resume')

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('thumbnail', 'LinkedIn', 'website', 'Twitter', 'Facebook')

    def __init__(self, *args, **kwargs):
        super(EmployerForm, self).__init__(*args, **kwargs)


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ('cover_letter',)

    def __init__(self, *args, **kwargs):
        super(JobApplicationForm, self).__init__(*args, **kwargs)




