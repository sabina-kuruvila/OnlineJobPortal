from django.contrib import admin
from .models import *

# Register your models here.


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_companies', 'email', 'mobile', 'resume')  # Adding more fields if needed
    list_filter = ('company',)
    # Custom method to display the companies
    def get_companies(self, obj):
        return ", ".join([company.name for company in obj.company.all()])
    
    # Optional: to specify a column name
    get_companies.short_description = 'Companies'


class HR_Admin(admin.ModelAdmin):
    list_display = ('user', 'company') 

admin.site.register(Company)
admin.site.register(HR, HR_Admin)
admin.site.register(Vacancy)
admin.site.register(Candidate, CandidateAdmin)


