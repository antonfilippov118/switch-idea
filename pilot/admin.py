from django.contrib import admin
from django.contrib.auth.models import Group
from pilot.models import Employer, Student, Category, Skill, JobPost, JobType, Location, Country, BlogPost, JobApplication



class StudentAdmin(admin.ModelAdmin):
	exclude = ('slug',)


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class SkillAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class EmployerAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'phone_number', 'URL_to_view_openings')


class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_post', 'name', 'total_applicants', 'pub_date', 'expiry_date')
    exclude = ('slug',)


class JobPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'applicants', 'pub_date', 'deadline', 'URL_to_view_applicants')
    exclude = ('slug',)


admin.site.unregister(Group)
admin.site.register(Student, StudentAdmin)
admin.site.register(JobPost, JobPostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(JobType)
admin.site.register(Location)
admin.site.register(Country)
admin.site.register(BlogPost)
admin.site.register(JobApplication, JobTypeAdmin)
