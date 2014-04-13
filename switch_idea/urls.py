from django.conf.urls import patterns, include, url
from pilot.models import JobPost


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'switch_idea.views.list_jobs', name='list_jobs'),  # HOMEPAGE, DUPLICATE OF VIEW ALL JOBS

    url(r'^job/(?P<id_job>[-\w]+)/$', 'switch_idea.views.job_detail'),  # VIEW SPECIFIC JOB
    url(r'^jobs', 'switch_idea.views.list_jobs', name='list_jobs'),  # VIEW ALL JOBS

    url(r'^login/$', 'switch_idea.views.user_login', name='user_login'),  # FILL OUT USER LOGIN FORM
    url(r'^auth/$', 'switch_idea.views.user_auth', name='user_auth'),  # AUTHORIZE USER AFTER LOGIN

    url(r'^logout/', 'switch_idea.views.user_logout', name='user_logout'),  # LOGOUT

    url(r'^registers/$', 'switch_idea.views.registerStudent', name='registerStudent'),  # REGISTER NEW STUDENT ACCOUNT
    url(r'^registere/$', 'switch_idea.views.registerEmployer', name='registerEmployer'),  # REGISTER NEW EMPLOYER ACCOUNT

    url(r'^create/$', 'switch_idea.views.create', name='create'),  # CREATE JOB POST FORM
    url(r'^createNewEmployer/$', 'switch_idea.views.create_no_auth', name='create_no_auth'),  # CREATE JOB POST FORM NOT LOGGED IN

    url(r'^apply/(?P<id_student>[-\w]+)/(?P<id_jobpost>[-\w]+)/$', 'switch_idea.views.apply', name='apply'),  # FILL IN JOB POST FORM
    url(r'^apply_request/(?P<id_jobpost>[-\w]+)/$', 'switch_idea.views.apply', name='apply'),  #  APPLY FOR JOB REQUEST

    url(r'^createstudent/$', 'switch_idea.views.create_student', name='create_student'),  # CREATE STUDENT ACCOUNT FORM
    url(r'^createemployer/$', 'switch_idea.views.create_employer', name='create_employer'),  # CREATE STUDENT ACCOUNT FORM

    url(r'^students/$', 'switch_idea.views.list_students', name='list_students'),  # LIST ALL STUDENTS
    url(r'^student/(?P<id_user>[-\w]+)/$', 'switch_idea.views.student_detail', name='student_detail'),  # STUDENT PROFILE

    url(r'^employers/$', 'switch_idea.views.list_employers', name='list_employers'),  # LIST ALL STUDENTS
    url(r'^employer/(?P<id_employer>[-\w]+)/$', 'switch_idea.views.employer_detail', name='student_detail'),  # EMPLOYER PROFILE
    url(r'^employeropenings/(?P<user_id>[-\w]+)/$', 'switch_idea.views.manage_openings', name='manage_openings'),  # EMPLOYER JOB OPENINGS

    url(r'^change_name/(?P<id_user>[-\w]+)/$', 'switch_idea.views.change_name', name='change_name'),  # EMPLOYER PROFILE
    url(r'^change_name_finished/$', 'switch_idea.views.change_name_finished', name='change_name_finished'),  # EMPLOYER PROFILE

    url(r'^change_cellphone/$', 'switch_idea.views.change_cellphone', name='change_cellphone'),  # EMPLOYER PROFILE
    url(r'^change_cellphone_finished/$', 'switch_idea.views.change_cellphone_finished', name='change_cellphone_finished'),  # EMPLOYER PROFILE

    url(r'^blog/$', 'switch_idea.views.list_blog', name='list_blog'),
    url(r'^blog/(?P<id_blog_post>[-\w]+)/$', 'switch_idea.views.blog_detail', name='list_blog'),

    url(r'^applicants/(?P<jobpost_id>[-\w]+)/$', 'switch_idea.views.list_applicants', name='list_applicants'),

    url(r'^admin/', include(admin.site.urls)),  # DJANGO ADMIN PANEL
)
