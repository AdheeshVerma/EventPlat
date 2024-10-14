from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Blog, Profile
from django.core.mail import send_mail
import random

from .models import UserTextAssignment

# Create your views here.
def index(request):
    return render(request,'actual_home.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contactc.html')


def register(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)
        Team_name = request.POST.get('tname')
        username = request.POST.get('uname')

        if User.objects.filter(email=email).exists():
            messages.warning(request,'Email Already Exists')
            redirect('register')

        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already taken')
            return redirect('register')
        
        else:
            user = User(email = email,password = password,username=username,first_name = Team_name)
            user.set_password(password)
            user.save()
            # subject = "About Regestration"
            # message = f"Hello {username}, You have been registered Successfully on EVENT PLATFORM"
            # email_from = 'adheeshzkp@gmail.com'
            # rec_list = [email]
            # try:
            #     send_mail(subject, message, email_from, rec_list)
            # except Exception as e:
            #     print(f"Error sending email: {e}")
            #     messages.warning(request, "Registration successful, but there was an issue sending the confirmation email.")
            messages.success(request,'Registration Successful')
            return redirect("/")
    return render(request,"actual_register.html")

def login_user(request):
    if request.method=='POST':
        username = request.POST["email"]
        print(username)
        password = request.POST["password"]
        user = authenticate(request, username = username,password=password)
        if user is not None:
            login(request,user)
            return redirect('welcome')
        else:
            messages.warning(request,'Invalid Credentials')
            return redirect('login')
    return render(request,'actual_login.html')

def logout_user(request):
    global points
    points = 0
    logout(request)
    return redirect('/')

def welcome(request):
    return render(request,'actual_welcome.html')


'''def blogpost(request):
    if request.method=='POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        blog = Blog(title=title,content = content,user_id = request.user)
        blog.save()
        messages.success(request,"Blog Submitted Successfully")
        return redirect('/')
    return render(request,"blog_post.html")'''


# =================== Making the list field===============================#

main_list = [
    ["1 1", "1 2", "1 3"], 
    ["2 1", "2 2", "2 3"], 
    ["3 1", "3 2", "3 3"], 
#    { "chandigarh":["4 1", "4 2", "4 3"]},
    ["4 1", "4 2", "4 3"],
    ["5 1", "5 2", "5 3"], 
    ["6 1", "6 2", "6 3"], 
    ["7 1", "7 2", "7 3"], 
    ["8 1", "8 2", "8 3"], 
    ["9 1", "9 2", "9 3"], 
    ["10 1", "10 2", "10 3"]
]

points= 0

user_clue = ""
print("test")

def shuffle_text_lists():
    random.shuffle(main_list)
    return main_list


# ============================= trying next button===========================
@login_required(login_url='login')
def next_clue(request):
    user = request.user
    global points
    # Increment points
    # global points
    # Check if the user already has an assigned clue that hasn't been marked as 'used'
    active_assignment = UserTextAssignment.objects.filter(user=user, used=False).first()
    # active_assignment = UserTextAssignment.objects.filter(user=user, used=False).first()
    
    if request.method == 'POST':
        treasure_code = request.POST.get('TCode')
        print("tcode",treasure_code)
        correct_code = 'qwerty'  # Replace with your correct treasure code

        # Validate the treasure code
        if treasure_code == correct_code:
            # Mark the current assignment as used
            if active_assignment:
                active_assignment.used = True
                active_assignment.save()

            # Now assign the next clue
            used_lists = UserTextAssignment.objects.filter(user=user, used=True)
            used_list_ids = [list_item.assigned_list for list_item in used_lists]

            print("used list id",used_list_ids)
            available_lists = [lst for lst in main_list if lst not in used_list_ids]
            if not available_lists:
                # No more lists available
                return render(request, 'completed.html')

            # Shuffle and assign the next clue
            shuffled_list = random.choice(available_lists)
            random.shuffle(shuffled_list)
            assigned_value = shuffled_list[0]

            # Save the new assignment in the database
            new_assignment = UserTextAssignment(user=user, assigned_list=shuffled_list, assigned_text=assigned_value, used=False)
            new_assignment.save()

            
            
            points += 1

            profile, created = Profile.objects.get_or_create(user=request.user)

            
            # pt = Profile(user = user,clue_solved= points)
            profile.clue_solved=points
            profile.save()
            
            print(points)

            if points>10:
                profile = Profile.objects.get(user=request.user)
                profile.clue_solved = 0
                profile.save()
            # main_list[0][1].remove(assigned_value)
            return render(request, 'actual_clue.html', {'assigned_text': assigned_value})
        elif treasure_code is not None:
            # Incorrect code, show error and reload the same clue
            if active_assignment:
                messages.error(request, 'Incorrect Treasure Code') 
                return render(request, 'actual_clue.html', {'assigned_text': active_assignment.assigned_text})
            else:
                # Handle case where no active assignment exists but an incorrect code was submitted
                messages.error(request, 'No active clue. Please try again.')
                return redirect('next_clue')  # Replace 'clue_start' with your starting clue URL

    # If there's already an active assignment, display the same clue
    if active_assignment:
        return render(request, 'actual_clue.html', {'assigned_text': active_assignment.assigned_text})

    # If there's no active assignment and no POST data, start the first assignment
    used_lists = UserTextAssignment.objects.filter(user=user, used=True)
    used_list_ids = [list_item.assigned_list for list_item in used_lists]

    available_lists = [lst for lst in main_list if lst not in used_list_ids]
    if not available_lists:
        return redirect('completion')
        # points+=1
        # return render(request, 'actual_congrates.html')

    # Shuffle and assign the first clue
    shuffled_list = random.choice(available_lists)
    random.shuffle(shuffled_list)
    assigned_value = shuffled_list[0]

    # Save the new assignment
    new_assignment = UserTextAssignment(user=user, assigned_list=shuffled_list, assigned_text=assigned_value, used=False)
    new_assignment.save()

    return render(request, 'actual_clue.html', {'assigned_text': assigned_value})

def completion(request):
    global points
    points+=1
    return render(request, 'completed.html')
