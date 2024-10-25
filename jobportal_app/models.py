from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location =models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.name if self.name else "Unnamed Company"
    
class HR(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.company.name}:{self.user.username}"
 
class Vacancy(models.Model):
    company = models.ForeignKey(Company, related_name='vacancies', on_delete=models.CASCADE)
    position = models.CharField(max_length=200,null=True)
    description = models.TextField(max_length=2000, null=True)
    experience = models.IntegerField(null=True)
    salary =models.IntegerField(null=True)
    location = models.CharField(max_length=2000, null=True)
    
    def __str__(self):
        return f"{self.company}:{self.position}"

class Candidate(models.Model):
    Category = (
        ('Male','male'),
        ('Female','female'),
        ('Other','other')
    )
    name = models.CharField(max_length=200)
    DOB =models.DateField(null=True)
    gender = models.CharField(max_length=200, choices= Category)
    mobile= models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=200)
    resume = models.FileField(null=True, upload_to="resumes/") # The resume will be uploaded to the 'resumes/' folder
    company = models.ManyToManyField(Company, related_name='candidates')

    def __str__(self):
        return self.name
    

