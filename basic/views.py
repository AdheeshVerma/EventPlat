from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Profile
from django.core.mail import send_mail
import random
from .models import Finish
from django.utils import timezone


from .models import UserTextAssignment

# Create your views here.
def index(request):
    return render(request,'actual_home.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')


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
    #Fountain
    ["""
	मैं धूप की किरणें पकड़ता, खुशी से चमकता,
    Every drop जो गिरती है, मैं संगीत बनाता।
    Summer में एक splash, एक नज़ारा ख़ास,
    Find me at the corner of this lively place,
    that’s your task!	I dance with the sun,
     a sparkling display, in a space where students gather and play,
    I'm the pulse of the campus, where energy thrives.
    With water that leeps and a soothing sound. Find me in the heart of this ground.""", 
    """
	मैं धूप की किरणें पकड़ता, खुशी से चमकता,
    Every drop जो गिरती है, मैं संगीत बनाता।
    Summer में एक splash, एक नज़ारा ख़ास,
    Find me at the corner of this lively place, that’s your task!	I dance with the sun, a sparkling display, in a space where students gather and play,
    I'm the pulse of the campus, where energy thrives.
    With water that leeps and a soothing sound. Find me in the heart of this ground."""], 

    #Tree House
    ["""Sun की sunlight, यहाँ पहुँचती है,
        Birds की chirping, मेरे साथ गाती है।
        Ground से ऊपर, Made of wood,
        A perfect hideout for every little planner
        Adventure का ठिकाना, बताओ मुझे, मेरा है कौन सा नाम?
        ये डूढना है तुम्हारा काम!!""",
        """
        In nature I'm nestled, among leaves I reside.
            I sway with breeze but anchored so tight.
            I am a childhood dream with a grown up twist, a place to unwind.
            A refugee from life's bustling chase, what am I that gives u a special space?"""],

    #Symbols (babbage)
    ["""
    In sacred halls, जहाँ faith और devotion मिलती है,
    पुरानी scriptures और teachings का amazing confluence होता है।
    Incense की aroma से लेकर hymns की melody तक,
    Souls soar, a spark in every heart.
    बताओ मुझे, मैं कौन हूँ, where seekers explore?""",
    """
    I am where accountants tap away, on keyboards crunching numbers all day.
        Outside me is a canvas of faith so bright, many paths one universal light. I am a river of faiths that flow, coverging streams for all to know"""], 

    #Picasso
    ["""जहाँ fabric और accessories मिलते हैं एक साथ,
    हर outfit में छिपा है एक नया look का transformation
    Sketches और patterns की होती है buzz,
    Find me there, जहाँ होता है creativity का magic!!""",
    """
    I danced with colours, bold and free. In my hands, the world is a mystery I made something sharp,yet often soft. It broke the rules and soar aloft. The shapes were twisted and colours were bright. From blues to roses I made them sing. Who am I in this realm of light. """],


    #Le corbuiser 
    ["""संगमरमर और concrete का magic यहाँ चलता है,
    हर drawing में छिपी एक नई journey होती है
    History और innovation का है ये fusion,
    जहाँ creativity और structure का होता है perfect blend
    Find me there, जहाँ होती है design की echo,
    जहाँ हर project में hidden है एक नया trend!!""",

    """I spoke of the machine and man's true needs, creating homes where comfort leads. sketching, conceiving, planning and designing guide the way, transforming cities day by day. If your skills are intact you might do wonders. But if not the building might be a blunder. WHO AM I? """], 

    #Hello Future 
    ["""Assessment और evaluation का खेल यहाँ चलता है,
    Documents और deadlines की होती है table पर fight
    Future की planning में छिपा है हर decision,
    Find me there, जहाँ होती है हर student की vision।""",
    
    """In the university's hustle, I stand with pride, offering rides that are gentle and glide,
    I'm where adventures begin and end, for check in and check out you will always depend, 
    Hop in for a journey quick and serene, what am I where eco friendly rides convene?"""], 

    #SQ2
    ["""इस bustling space में, scents intertwine होते हैं,
        हर passing moment में, कुछ divine experience होता है।
        आप gather होते हैं friends के साथ, laughter से भरता है atmosphere,
        Whether it's summer or winter, I remain open,
        खोजो मुझे वहाँ, जहाँ हर story को मिलती है नई life!!"""], 


    #Chai Vyanjan    
    ["""एक hidden spot, जहाँ है comfort का feel,
        चाय और Maggi, सबका है favourite meal.
        Friends के संग, laughter का flow,
        What am I, where the fun begins?""",

        """I'm a hub of laughter, where friendships are brewed, with each sip and bite a sense of gratitude.
        A blend of traditions and modern delight, Snacks and chai flow freely igniting the spark, What am I, a lively hub in the academic park?"""], 

    #Explore stars
    ["""Mirrors के universe में, reflections बनते हैं true,
    Steps की precision और rhythm, सब होते हैं part of the crew
    एक energetic ambiance है, जो हर spirit को elevate कर दे,
    Tell me, Who am I, जो हर move में sparkle भर दे?""",

    """A move thats sharp yet smooth in the flow, you practise here with passion to steal the show. In this space you sweat and refine, learning the rhythm your body's design. You seek a place with symphony's sound where melodies play and your clue is found"""], 

    #Aeroplane 
    ["""Journey का मेरा career, है special और unique,
    2009 में हुआ farewell, memories में हूँ classic
    Training के field में, मैं हूँ maestro,
    What am I, जो aviation को बनाता है smooth?""",

    """I can be grounded or airborne, but I am not a bird.
    I rely on technology yet I am often preffered. I have wings but cant fly alone, I have a body but dont wear clothes.
    Finding me is your next fask folks!"""]
]
# main_list = [
#     ["1 1", "1 2", "1 3"], 
#     ["2 1", "2 2", "2 3"], 
#     ["3 1", "3 2", "3 3"], 
# #    { "chandigarh":["4 1", "4 2", "4 3"]},
#     ["4 1", "4 2", "4 3"],
#     ["5 1", "5 2", "5 3"], 
#     ["6 1", "6 2", "6 3"], 
#     ["7 1", "7 2", "7 3"], 
#     ["8 1", "8 2", "8 3"], 
#     ["9 1", "9 2", "9 3"], 
#     ["10 1", "10 2", "10 3"]
# ]

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
    active_assignment = UserTextAssignment.objects.filter(user=user, used=False).first()

    if request.method == 'POST':
        # Handle Skip Clue
        if request.POST.get('skip') == 'true':
            # Mark the current assignment as used
            if active_assignment:
                active_assignment.used = True
                active_assignment.save()

            # Now assign the next clue
            used_lists = UserTextAssignment.objects.filter(user=user, used=True)
            used_list_ids = [list_item.assigned_list for list_item in used_lists]

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

            return render(request, 'actual_clue.html', {'assigned_text': assigned_value})

        # Handle normal treasure code submission
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
            profile.clue_solved = points
            profile.save()

            if points > 10:
                profile = Profile.objects.get(user=request.user)
                profile.clue_solved = 0
                profile.save()

            return render(request, 'actual_clue.html', {'assigned_text': assigned_value})
        elif treasure_code is not None:
            # Incorrect code, show error and reload the same clue
            if active_assignment:
                messages.error(request, 'Incorrect Treasure Code')
                return render(request, 'actual_clue.html', {'assigned_text': active_assignment.assigned_text})
            else:
                messages.error(request, 'No active clue. Please try again.')
                return redirect('next_clue')

    # If there's already an active assignment, display the same clue
    if active_assignment:
        return render(request, 'actual_clue.html', {'assigned_text': active_assignment.assigned_text})

    # If there's no active assignment and no POST data, start the first assignment
    used_lists = UserTextAssignment.objects.filter(user=user, used=True)
    used_list_ids = [list_item.assigned_list for list_item in used_lists]

    available_lists = [lst for lst in main_list if lst not in used_list_ids]
    if not available_lists:
        return redirect('completion')

    # Shuffle and assign the first clue
    shuffled_list = random.choice(available_lists)
    random.shuffle(shuffled_list)
    assigned_value = shuffled_list[0]

    # Save the new assignment
    new_assignment = UserTextAssignment(user=user, assigned_list=shuffled_list, assigned_text=assigned_value, used=False)
    new_assignment.save()

    return render(request, 'actual_clue.html', {'assigned_text': assigned_value})


# def completion(request):
#     global points
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     points+=1
#     profile.clue_solved=points
#     profile.save()
#     return render(request, 'completed.html')


from django.utils import timezone

def completion(request):
    global points
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Increment points and save profile
    points += 1
    profile.clue_solved = points
    profile.save()
    
    # Record the user's completion with the current date and time
    recorded_time = Finish.objects.create(user=request.user)
    recorded_time.timeout = timezone.now()  # Update the timeout field
    recorded_time.save()

    return render(request, 'completed.html')
