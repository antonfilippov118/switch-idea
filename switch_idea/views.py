from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from pilot.models import Student, Employer, Category, JobPost, Skill, BlogPost, JobType, Location, Country
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from pilot.forms import JobForm, StudentForm, EmployerForm, JobApplicationForm, JobApplication, NewEmployerJobForm
from django.core.context_processors import csrf
from django.db import IntegrityError
from django.template import RequestContext
import datetime

# Create your views here.
def home(request):
    args = {}
    args['greet'] = "Hello, world. You're at the switch idea homepage index."
    return render_to_response('index.html', args)


def list_jobs(request):
    args = {}
    jobposts = JobPost.objects.all()
    applicants = JobApplication.objects.all()
    args['jobposts'] = JobPost.objects.order_by('-pub_date')[:10]

    if Student.objects.filter(uid=request.user.id):
        args['is_student'] = True

    try:
        args['uid'] = request.user.id
        args['first_name'] = request.user.first_name
        args['username'] = request.user.username
    except AttributeError:
        args['first_name'] = None

    args['employers'] = Employer.objects.all()
    args['students'] = Student.objects.all()
    args['jobtypes'] = JobType.objects.all()
    args['locations'] = Location.objects.all()
    args['user_objects'] = User.objects.all()

    args['categories'] = Category.objects.all()

    if Employer.objects.filter(uid_id=request.user.id):
        args['accountType'] = "employer"
    else:
        args['accountType'] = "student"

    totalJobs = 0
    totalApplicants = 0

    for item in jobposts:
        totalJobs += 1

    for item in applicants:
        totalApplicants += 1

    args['totalJobs'] = totalJobs
    args['totalApplicants'] = totalApplicants

    return render_to_response('job_list.html', args)


def job_detail(request, id_job):
    args = {}
    objJob = JobPost.objects.get(id=id_job)
    args['title'] = objJob.title
    args['description'] = objJob.j_description
    args['responsibilities'] = objJob.responsibilities
    args['benefits_perks'] = objJob.benefits_perks
    args['jobid'] = objJob.id
    args['pub_date'] = objJob.pub_date
    employer_id = objJob.employer_id

    employer = Employer.objects.get(id=employer_id)
    args['employer'] = employer


    try:
        args['first_name'] = request.user.first_name
        args['username'] = request.user.username
        args['uid'] = request.user.id
    except AttributeError:
        args['first_name'] = None

    if Student.objects.filter(uid=request.user.id):
        args['is_student'] = True

    args['student_id'] = request.user.id
    args['jobpost'] = objJob

    args['jobtype'] = JobType.objects.get(id=objJob.type_id)
    args['location'] = Location.objects.get(id=objJob.location_id)

    args['employers'] = Employer.objects.all()

    return render_to_response('job_detail.html', args)


def list_students(request):
    args = {}
    students = Student.objects.all()
    args['students'] = students
    args['user_students'] = User.objects.all()

    totalStudents = 0
    totalVerified = 0
    totalUnverified = 0

    for item in students:
        totalStudents += 1
        if item.email_verified:
            totalVerified += 1
        else:
            totalUnverified += 1

    if Student.objects.filter(uid=request.user.id):
        args['is_student'] = True

    args['totalVerified'] = totalVerified
    args['totalUnverified'] = totalUnverified
    args['totalStudents'] = totalStudents
    args['username'] = request.user.username
    args['uid'] = request.user.id
    return render_to_response('student_list.html', args)


def list_employers(request):
    args = {}
    employers = Employer.objects.all()
    jobposts = JobPost.objects.all()
    args['employers'] = employers
    args['user_employers'] = User.objects.all()

    if Student.objects.filter(uid=request.user.id):
        args['is_student'] = True

    totalEmployers = 0
    totalVerified = 0
    totalUnverified = 0


    for item in employers:
        totalEmployers += 1
        if item.email_verified:
            totalVerified += 1
        else:
            totalUnverified += 1


    args['jobposts'] = JobPost.objects.all()
    args['totalVerified'] = totalVerified
    args['totalUnverified'] = totalUnverified
    args['totalEmployers'] = totalEmployers
    args['username'] = request.user.username
    args['uid'] = request.user.id
    return render_to_response('employer_list.html', args)


def student_detail(request, id_user):
    args = {}
    try:
        args['uid'] = request.user.id
        args['first_name'] = request.user.first_name
        args['username'] = request.user.username
    except AttributeError:
        args['first_name'] = None
    args['user'] = User.objects.get(id=id_user)
    args['student'] = Student.objects.get(uid_id=id_user)
    args['username'] = request.user.username
    args['uid'] = request.user.id
    if Student.objects.filter(uid=request.user.id):
        args['is_student'] = True
    return render_to_response('student_detail.html', args)


def employer_detail(request, id_employer):
    args = {}
    try:
        args['uid'] = request.user.id
        args['first_name'] = request.user.first_name
        args['username'] = request.user.username
    except AttributeError:
        args['first_name'] = None
    args['user'] = User.objects.get(id=id_employer)
    args['employer'] = Employer.objects.get(id=id_employer)
    args['uid'] = request.user.id
    args['username'] = request.user.username
    if Student.objects.filter(uid=request.user.id):
        args['is_student'] = True
    return render_to_response('employer_detail.html', args)


def user_login(request):
    return render_to_response('login_form.html')


def user_auth(request):
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')

    user = authenticate(username=username, password=password)

    # Get current username that's logged in
    args = {}
    args['username'] = request.user.username
    args['uid'] = request.user.id
    args['error'] = "Please check if your user name and password are correct."

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/jobs')
        else:
            return render_to_response('login_form.html', args)
    else:
        return render_to_response('login_form.html', args)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/jobs')


def registerStudent(request):
    username_get = request.GET.get('username', '')
    password_get = request.GET.get('password', '')
    repassword = request.GET.get('repassword', '')
    email_get = request.GET.get('email_get', '')
    first_name = request.GET.get('first_name', '')
    last_name = request.GET.get('last_name', '')

    # fix me later
    if request.method != 'GET':
        return render_to_response('registration_page.html')

    if not username_get:
        args = {}
        args['error'] = "Please enter a valid email address."
        return render_to_response('registration_page.html', args)

    if password_get != repassword:
        args = {}
        args['error'] = "The passwords you've entered do not match."
        return render_to_response('registration_page.html', args)

    if password_get == "":
        args = {}
        args['error'] = "Invalid password."
        return render_to_response('registration_page.html', args)

    if len(password_get) < 6:
        args = {}
        args['error'] = "Your password must contain at least 6 characters."
        return render_to_response('registration_page.html', args)

    if username_get.find("@") == -1:
        args = {}
        args['error'] = "Please enter a valid email address."
        return render_to_response('registration_page.html', args)

    check4dupe = User.objects.filter(username=username_get)
    if not check4dupe:
        user = User.objects.create_user(username_get, email_get, password_get)
        user.last_name = last_name
        user.first_name = first_name
        user.save()
        # user_profile = User_Profile(uid=user)  # register student or employee
        # user_profile.save()
    else:
        args = {}
        args['error'] = "That user name has already been taken."
        return render_to_response('registration_page.html', args)

    args = {}
    args['error'] = "Thanks for signing up! Tell us a little more about yourself."
    user = authenticate(username=username_get, password=password_get)
    login(request, user)
    args['username'] = request.user.username
    return HttpResponseRedirect('/createstudent/')


def change_name(request, id_user):
    if Student.objects.filter(uid=request.user.id):
        args['is_student'] = True
    return render_to_response('newname_form.html')


def change_name_finished(request):
    first_name = request.GET.get('first_name', '')
    last_name = request.GET.get('last_name', '')

    if request.method != 'GET':
        return render_to_response('newname_form.html')

    if not first_name:
        args = {}
        args['error'] = "Please enter a valid first name."
        return render_to_response('newname_form.html', args)

    if not last_name:
        args = {}
        args['error'] = "Please enter a valid last name."
        return render_to_response('newname_form.html', args)

    args = {}
    u1 = User.objects.get(id=request.user.id)
    args['uid'] = u1.id

    u1.first_name = first_name
    u1.last_name = last_name
    u1.save()

    return HttpResponseRedirect('/jobs/')


def change_cellphone(request):
    if Student.objects.filter(uid=request.user.id):
        args = {}
        args['is_student'] = True
    return render_to_response('newphone_form.html', args)


def change_cellphone_finished(request):
    cellphone = request.GET.get('cellphone', '')

    if request.method != 'GET':
        return render_to_response('newphone_form.html')

    if not cellphone:
        args = {}
        args['error'] = "Please enter a valid mobile phone."
        return render_to_response('newphone_form.html', args)

    args = {}
    u1 = User.objects.get(id=request.user.id)
    args['uid'] = u1.id

    u1.email = cellphone
    u1.save()

    return HttpResponseRedirect('/jobs/')


def registerEmployer(request):
    username_get = request.GET.get('username', '')
    password_get = request.GET.get('password', '')
    repassword = request.GET.get('repassword', '')
    email_get = request.GET.get('email_get', '')
    first_name = request.GET.get('first_name', '')
    last_name = request.GET.get('last_name', '')

    # fix me later
    if request.method != 'GET':
        return render_to_response('registration_page.html')

    if not username_get:
        args = {}
        args['error'] = "Please enter a valid email address."
        return render_to_response('registration_page.html', args)

    if password_get != repassword:
        args = {}
        args['error'] = "The passwords you've entered do not match."
        return render_to_response('registration_page.html', args)

    if password_get == "":
        args = {}
        args['error'] = "Invalid password."
        return render_to_response('registration_page.html', args)

    if len(password_get) < 6:
        args = {}
        args['error'] = "Your password must contain at least 6 characters."
        return render_to_response('registration_page.html', args)

    if username_get.find("@") == -1:
        args = {}
        args['error'] = "Please enter a valid email address."
        return render_to_response('registration_page.html', args)

    check4dupe = User.objects.filter(username=username_get)
    if not check4dupe:
        user = User.objects.create_user(username_get, email_get, password_get)
        user.last_name = last_name
        user.first_name = first_name
        user.save()
    else:
        args = {}
        args['error'] = "That user name has already been taken."
        return render_to_response('registration_page.html', args)

    args = {}
    args['error'] = "Thanks for signing up! Tell us a little more about yourself."
    user = authenticate(username=username_get, password=password_get)
    login(request, user)
    args['username'] = request.user.username
    return HttpResponseRedirect('/createemployer/')


def create(request):
    if Student.objects.filter(uid=request.user.id):
        return HttpResponseRedirect('/jobs')
    if request.user.is_authenticated() is False:
        return HttpResponseRedirect('/createNewEmployer')
    if request.POST:
        post_values = request.POST.copy()
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)

            slug = str(obj.title) + "-" + str(obj.id)
            obj.slug = slug

            userid = Employer.objects.get(uid_id=request.user.id)
            obj.employer_id = userid.uid_id  # DUMMY VALUE FOR THE EMPLOYER WHO WROTE THIS JOB POST

            obj.save()
            return HttpResponseRedirect('/jobs')
    else:
        form = JobForm()
        form.author = request.user
    args = {}
    try:
        args['first_name'] = request.user.first_name
        args['username'] = request.user.username
        args['uid'] = request.user.id
    except AttributeError:
        args['first_name'] = None
    args.update(csrf(request))
    args['form'] = form
    args['username'] = request.user.username
    args['uid'] = request.user.id
    return render_to_response('newpost.html', args)


def create_no_auth(request):
    if Student.objects.filter(uid=request.user.id):
        return HttpResponseRedirect('/jobs')
    if request.POST:
        logout(request)
        post_values = request.POST.copy()
        form = NewEmployerJobForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)

            username_get = obj.email
            email_get = obj.phone
            first_name = obj.first_name
            last_name = obj.last_name
            password_get = obj.password

            try:
                user = User.objects.create_user(username_get, email_get, password_get)
            except IntegrityError as e:
                return render_to_response('userexistserror.html')
            user.last_name = last_name
            user.first_name = first_name
            user.save()

            slug = str(obj.title) + "-" + str(obj.id)
            obj.slug = slug

            u1 = User.objects.get(username=username_get)
            e1 = Employer(uid=u1, company_name=obj.company_name, thumbnail=obj.thumbnail, LinkedIn=obj.LinkedIn, website=obj.website, Twitter=obj.Twitter, Facebook=obj.Facebook, e_description=obj.e_description)
            e1.save()

            jp = JobPost(title=obj.title, type_id=obj.type_id, is_premium=False, pub_date=obj.pub_date, j_description=obj.j_description, responsibilities=obj.responsibilities, benefits_perks=obj.benefits_perks, location_id=obj.location_id, employer_id=e1.id, category_id=obj.category_id, compensation=obj.compensation, url=obj.url, deadline=obj.deadline)
            jp.save()

            userid = User.objects.get(username=username_get)
            obj.employer_id = userid.id  # DUMMY VALUE FOR THE EMPLOYER WHO WROTE THIS JOB POST
            obj.save()
            return HttpResponseRedirect('/jobs')
    else:
        form = NewEmployerJobForm()
        form.author = request.user
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['username'] = request.user.username
    args['uid'] = request.user.id
    return render_to_response('newpostnewemployer.html', args)


def apply(request, id_student, id_jobpost):
    args = {}
    args['current_path'] = request.get_full_path()
    args['student_id'] = id_student
    args['jobid'] = str(id_jobpost) + "/"
    username = request.user

    if request.user.is_authenticated() is False:
        args = {}
        args['jobposts'] = JobPost.objects.all()
        args['error'] = 'You must be signed in before applying for a job.'
        args['username'] = request.user.username
        return render_to_response('job_list.html', args)
    if request.POST:
        post_values = request.POST.copy()
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)

            studentobj = Student.objects.get(uid_id=int(id_student))
            jobpostobj = JobPost.objects.get(id=int(id_jobpost))

            obj.student_id = int(studentobj.id)  # THE STUDENT WRITING THE APPLICATION
            obj.jobpost_id = int(jobpostobj.id)  # WRITE CORRECT JOB POST TO THE SUBMITTED APPLICATION
            jobpost = JobPost.objects.get(id=id_jobpost)
            jobpost.applicants += 1
            jobpost.save()

            obj.save()
            return HttpResponseRedirect('/jobs')
    else:
        form = JobApplicationForm()
        form.author = request.user
        args.update(csrf(request))
        args['form'] = form
        args['username'] = request.user.username
        args['uid'] = request.user.id
        return render_to_response('apply.html', args)


def create_student(request):
    if request.user.is_authenticated() is False:
        args = {}
        args['jobposts'] = JobPost.objects.all()
        args['error'] = 'You must be signed in before setting up a student account.'
        args['username'] = request.user.username
        return render_to_response('job_list.html', args)
    if request.POST:
        post_values = request.POST.copy()
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            obj = form.save(commit=False)
            # obj.author = request.user.id
            obj.uid = User.objects.get(id=request.user.id)   # THE USER WHO SUBMITTED NEW STUDENT ACCOUNT FORM
            obj.title = 'Student'
            obj.save()
            return HttpResponseRedirect('/jobs')
    else:
        form = StudentForm()
        form.author = request.user
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['username'] = request.user.username
    args['uid'] = request.user.id
    return render_to_response('newstudent.html', args)


def create_employer(request):
    if request.user.is_authenticated() is False:
        args = {}
        args['jobposts'] = JobPost.objects.all()
        args['error'] = 'You must be signed in before setting up an employer account.'
        args['username'] = request.user.username
        return render_to_response('job_list.html', args)
    if request.POST:
        post_values = request.POST.copy()
        form = EmployerForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            delete = Employer.objects.filter(uid_id=request.user.id)
            delete.delete()
            # obj.author = request.user.id
            obj.uid = User.objects.get(id=request.user.id)   # THE USER WHO SUBMITTED NEW EMPLOYER ACCOUNT FORM
            obj.save()
            return HttpResponseRedirect('/jobs')
    else:
        form = EmployerForm()
        form.author = request.user
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['username'] = request.user.username
    args['uid'] = request.user.id
    return render_to_response('newemployer.html', args)


def update_employer(request):
    if request.user.is_authenticated() is False:
        args = {}
        args['jobposts'] = JobPost.objects.all()
        args['error'] = 'You must be signed in before setting up an employer account.'
        args['username'] = request.user.username
        return render_to_response('job_list.html', args)


def manage_openings(request, user_id):
    args = {}
    if Student.objects.filter(uid=request.user.id):
        return HttpResponseRedirect('/jobs')
    obj_employer = Employer.objects.get(uid_id=user_id)
    jobposts = JobPost.objects.filter(employer_id=obj_employer.id)
    args['jobposts'] = jobposts
    totalposts = 0
    totalactive = 0
    totalexpired = 0
    totalpremium = 0
    for item in jobposts:
        if item.is_premium:
            totalpremium += 1
        if item.pub_date < item.deadline:
            totalactive += 1
        elif item.pub_date > item.deadline:
            totalexpired += 1

        totalposts += 1

    args['totalpremium'] = str(totalpremium)
    args['totalposts'] = str(totalposts)
    args['activeposts'] = str(totalactive)
    args['expiredposts'] = str(totalexpired)
    args['username'] = request.user.username
    args['employer'] = obj_employer
    return render_to_response('openings_list.html', args)


def list_applicants(request, jobpost_id):
    if Student.objects.filter(uid=request.user.id):
        return HttpResponseRedirect('/jobs')
    args = {}
    args['students'] = Student.objects.all()
    #try:
    #    args['jobapplication'] = JobApplication.objects.get(jobpost_id=jobpost_id)
    #except JobApplication.DoesNotExist:
    #    args['jobapplication'] = None
    args['jobapplication'] = JobApplication.objects.all()
    args['jobpost'] = JobPost.objects.get(id=jobpost_id)
    args['username'] = request.user.username
    args['user_objects'] = User.objects.all()
    if Employer.objects.filter(uid_id=request.user.id):
        args['accountType'] = "employer"
    else:
        args['accountType'] = "student"
    return render_to_response('applicants_list.html', args)


def list_blog(request):
    args = {}
    args['blogs'] = BlogPost.objects.all()
    args['username'] = request.user.username
    args['admin'] = User.objects.filter(is_superuser=1)
    return render_to_response('blog_list.html', args)


def blog_detail(request, id_blogpost):
    args = {}
    args['blog'] = BlogPost.objects.get(id=id_blogpost)
    args['username'] = request.user.username
    return render_to_response('blog_detail.html', args)