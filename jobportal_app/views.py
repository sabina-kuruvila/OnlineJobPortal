from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from JobPortal.settings import BASE_DIR
from .forms import ApplyForm, VacanciesForm

from .models import HR, Candidate,Company, Vacancy


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        try:
            hr =HR.objects.get(user=request.user)
        except HR.DoesNotExist:
            message = 'you are not assigned as HR.Please ask admin to assign.'
            return render(request, "NonHR_page.html", {'message': message})
    
        if hr:
            # Step 2: Check if the user is already linked to a company
            company = hr.company
            if company:
                try:
                    candidates =Candidate.objects.filter(company=hr.company)                
                    context = {'candidates': candidates,
                            'company': hr,
                            'message' : f"Candidates Applied for {hr.company}"
                            }
                    return render(request, "hr.html", context)
                
                # if company for the user doesn't exists, returns an empty candidate list
                except Candidate.DoesNotExist:
                    return redirect('manage_company')
            
    else:
        # fetch all the companies for all unauthenticated users(i.e, jobseekers)      
        vacancies = Vacancy.objects.select_related('company').all()
        print(vacancies)
        context = {'vacancies': vacancies,
                  }
        return render(request, "jobseeker.html", context)
    
##########################################################################################################################  
  
def loginUser(request):
    if request.user.is_authenticated:
        # If the user is already authenticated, redirect them to the home page
        return redirect('home')
    
    if request.method == 'POST':
            user =request.POST.get('username')
            pwd = request.POST.get('userpassword')
            print(user,pwd)

            # Authenticate the user
            user = authenticate(request, username=user,password = pwd)

            if user is not None:
                # If authentication is successful, log in the user
                login(request, user)
                return redirect('home')   
            else:
                # Add an error message if login fails (optional)
                return render(request, 'login.html', {'error': 'Invalid username or password'})

    # For GET requests, render the login page
    form =AuthenticationForm() #want to clear login fields
    return render(request, "login.html", {'form': form})

##########################################################################################################################  
    
def logoutUser(request):
    logout(request)
    request.session['title'] = "Logged Out"
    return redirect('loginUser')  

##########################################################################################################################  

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    Form = UserCreationForm()
    if request.method == 'POST':
        Form = UserCreationForm(request.POST)
        if Form.is_valid():
            curruser = Form.save()
            # Company.objects.create(user = curruser, name = curruser.username)
            return redirect('loginUser')
        
    else:
        Form = UserCreationForm()
        
    return render(request, "register.html", {'form':Form}) 

##########################################################################################################################  

def show_vacancy(request):   
 
    hr = HR.objects.get(user=request.user)
    company_name= hr.company

    vacancies = Vacancy.objects.filter(company=company_name)
    if vacancies.exists():
        return render(request, "show_vacancy.html", {'vacancies':vacancies})
    else:
        return redirect('new_vacancy',request.user)
    
###################################################################################################################

def new_vacancy(request, name):
  
    hr = HR.objects.filter(user__username=name).first()  # Get the HR instance and company
    company = hr.company # Get the Company instance from HR
    
    if request.method == 'POST':
        form = VacanciesForm(request.POST)  # Bind form with POST data

        if form.is_valid():

            vacancy_data = form.cleaned_data

            # Check if a similar vacancy already exists for this company
            existing_vacancy= Vacancy.objects.filter(
                company=company,                                    
                position = vacancy_data['position'],
                description = vacancy_data['description'],
                salary = vacancy_data['salary'],
                experience = vacancy_data['experience'],
                location = vacancy_data['location']
                ).first()
        
            if existing_vacancy:

                # If there's an existing application, inform the user and prevent multiple submissions
                message = "This job vacancy has already been added."
                return render(request, "thank_you.html", {'message': message})
            else:
                # Save the new vacancy
                vacancy = form.save(commit=False)
               
                vacancy.company = company # Link the vacancy to the company
                vacancy.save()
             
                message = 'Vacancy added successfully.'
                return render(request, "thank_you.html", {'message': message})
    else:
        # create a blank form
        form = VacanciesForm()
    return render(request, 'add_vacancy.html', {'form': form})

##########################################################################################################################  

@login_required(login_url='/loginUser')
def update_vacancy(request,vacancy_id):
   
    hr = HR.objects.get(user=request.user)
    company = hr.company

    vacancy = get_object_or_404(Vacancy,id=vacancy_id)
    if request.method == 'POST':          
        form = VacanciesForm(request.POST,instance=vacancy)  # update existing company form
    
        if form.is_valid():
        # Check if the vacancy exists or not
            vacancy_data = form.cleaned_data
            
            existing_vacancy= Vacancy.objects.filter(
                company=company,                                    
                position = vacancy_data['position'],
                description = vacancy_data['description'],
                salary = vacancy_data['salary'],
                experience = vacancy_data['experience'],
                location = vacancy_data['location']
                ).first()
            

            if existing_vacancy:
                # If there's an existing application, inform the user and prevent multiple submissions
                message = "This job vacancy has already been added."
                return render(request, "thank_you.html", {'message': message})
            else:
                vacancy = form.save(commit=False)
                vacancy.company = company # Link the vacancy to the company
                vacancy.save()
                message = 'Vacancy has been updated.'
                return render(request, "thank_you.html", {'message': message})
        
    else:
        form = VacanciesForm(instance=vacancy)
                  
    return render(request, "update_vacancy.html",{'form': form})

##########################################################################################################################  

def apply(request, name):
  
    company = Company.objects.filter(name=name).first()

    if request.method == 'POST':
         # Pass company to the form
        form =ApplyForm(request.POST, request.FILES, initial={'company':company}) # request.FILES for file upload  
        print(request.POST)
        if form.is_valid():

            # Check if the candidate has already applied for this job
            candidate_data = form.cleaned_data
            existing_application = Candidate.objects.filter(
                name=candidate_data['name'],
                DOB=candidate_data['DOB'],
                gender=candidate_data['gender'],
                mobile=candidate_data['mobile'],
                email=candidate_data['email'],
                company=company
            ).first()

            if existing_application:
                # If there's an existing application, inform the user and prevent multiple submissions
                message = "You have already applied for this job."
                return render(request, "thank_you.html", {'message': message, 'name': name})

            # Save the form and create the Application model instance if it is readonly or disabled
            application = form.save(commit=False)

            # Save the application object first to the DB - to generate a primary key (ID), if there's a many-to-many relationship (like company)
            application.save()
        
            application.company.set([company]) # Set the many-to-many relationship

            application.save()

            message = "Your application has been submitted successfully!"
            return render(request, "thank_you.html", {'message': message, 'name':name})    
        
    else:
        # Display the form with initial values (e.g., pre-populate company field)
        form = ApplyForm(initial={'company':company}) # Pass company to form
    
    return render(request, "applyForm.html", {'form': form, 'company':company})

##########################################################################################################################  