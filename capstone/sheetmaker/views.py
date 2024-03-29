from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import User, Sheet
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from .config import config
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.http import require_http_methods
from datetime import datetime
import random
import logging
import json

# For debugging purposes
logger = logging.getLogger('django')

# List of superusers
SUPERUSERS = [2, 5]

# Creating views

def error_404_view(request, exception):
    return render(request, 'sheetmaker/404.html')

def error_500_view(request):
    return render(request, 'sheetmaker/500.html')

# Home page
def index(request):
    return render(request, "sheetmaker/index.html")

# Log in page
def login_view(request):
    authenticated_users = ["kyledelmo", "mwatanabe", "cs50w", "ldelmo", "demo"] # Only restricting access to this program to myself, the SuperMath founder, and CS50 grader(s)
    
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        timezone = request.POST["localtimezone"] # Getting timezone for displaying the correct created/modified time for the sheets
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            if username in authenticated_users: # Only allowing some users to use this 
                login(request, user)
                request.session['localtimezone'] = timezone # Set the timezone for the entire session

                redirect_uri = request.POST['next']
                if redirect_uri  == request.path or redirect_uri == "":
                    # Avoid loops and prevent errors
                    redirect_uri = "/"
                    
                return redirect(redirect_uri)
            else:
                return render(request, "sheetmaker/login.html", {
                    "message": "Unauthorized user."
                })
        else:
            return render(request, "sheetmaker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "sheetmaker/login.html")

# Log out page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Register page
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"] 

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "sheetmaker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "sheetmaker/register.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(reverse("login"))
    else:
        return render(request, "sheetmaker/register.html")

# Create a multiplication sheet
@login_required(login_url="/login")
def createNewMultiplicationSet(request): 
    user = request.user.id
    data = newMultiplicationData() # Generating problem data
    new_sheet = Sheet(user_id=user, problem_data=data, sheet_type="multiplication") # Creating and saving a new Sheet object
    new_sheet.save()
    sheet_id = new_sheet.id 
    return redirect(f"/multiplication/{sheet_id}/view")

# Deleting a multiplication sheet object
@login_required(login_url="/login")
@require_http_methods(["POST"])
def deleteMultiplicationSet(request):
    if request.method == "POST":
        sheet_id = request.POST.get("sheet_id")
        sheet = Sheet.objects.get(id=sheet_id)
        sheet.delete()
        return redirect("/multiplication")

# Editing a multiplication sheet object
@login_required(login_url="/login")
@require_http_methods(["POST"])
def editMultiplicationSet(request):
    if request.method == "POST":
        # Getting submitted form inputs to update multiplication sheet object
        sheet_id = request.POST.get("sheet_id")
        current_sheet = Sheet.objects.get(id=sheet_id)
        new_sheet_name = request.POST.get("sheet_name")
        new_sheet_subname = request.POST.get("sheet_subname")
        new_answer_sheet_name = request.POST.get("sheet_answer_name")

        # Updating problem data
        first_numbers = request.POST.getlist('first')
        second_numbers = request.POST.getlist('second')
        answer_numbers = request.POST.getlist('answer')

        # Function to splice problems into JSON data for each level
        def spliceData(start, end):
            data = []
            for i in range(start, end):
                data.append({
                    "number": i+1,
                    "first": first_numbers[i],
                    "second": second_numbers[i],
                    "answer": answer_numbers[i]
                })
            return data

        level1Data = spliceData(0,20)
        level2Data = spliceData(20,40)
        level3Data = spliceData(40,60)
        level4Data = spliceData(60,80)
        level5Data = spliceData(80,100)

        jsonData = [
            { 
                'levelName': 'Level 1',
                'numberSet': level1Data
            },
            { 
                'levelName': 'Level 2',
                'numberSet': level2Data
            },
            { 
                'levelName': 'Level 3',
                'numberSet': level3Data
            },
            { 
                'levelName': 'Level 4',
                'numberSet': level4Data
            },
            { 
                'levelName': 'Level 5',
                'numberSet': level5Data
            }
        ]

        # Updating sheet object
        current_sheet.problem_data = jsonData
        current_sheet.sheet_name = new_sheet_name
        current_sheet.sheet_subname = new_sheet_subname
        current_sheet.sheet_answer_name = new_answer_sheet_name
        current_sheet.modified = datetime.utcnow()
        current_sheet.save()

        return redirect(f"multiplication/{sheet_id}/view")

# Creating the multiplication data (random problems generated with guidelines)
def newMultiplicationData():
    problems = []
    dupcheck = {} # Dictionary for checking for duplicates
    m_config = config["multiplication"] # Going into config.py and obtaining the rules for generating the multiplication problems
    config_keys = list(m_config.keys())
    counter = 0 # Level counter
    problem_counter = 0 # Problem counter
    for key in config_keys:
        current_set = m_config[key] # Current level
        while len(problems) < (counter + 20):
            new_problem = dict()
            new_problem["number"] = problem_counter + 1  
            new_problem["first"] = random.randint(current_set["first_min"], current_set["first_max"]) # First operand
            new_problem["second"] = random.randint(current_set["second_min"], current_set["second_max"]) # Second operand
            new_problem["answer"] = new_problem["first"] * new_problem["second"] # Answer
            key_query = "%ix%ix%i" % (new_problem["first"], new_problem["second"], new_problem["answer"]) # Creates a unique query to log in the problem to prevent duplicates
            if not dupcheck.get(key_query):
                problems.append(new_problem)
                dupcheck[key_query] = True
                problem_counter += 1
        counter += 20
        data = [
            { 
                'levelName': 'Level 1',
                'numberSet': problems[0:20]
            },
            { 
                'levelName': 'Level 2',
                'numberSet': problems[20:40]
            },
            { 
                'levelName': 'Level 3',
                'numberSet': problems[40:60]
            },
            { 
                'levelName': 'Level 4',
                'numberSet': problems[60:80]
            },
            { 
                'levelName': 'Level 5',
                'numberSet': problems[80:100]
            }
        ]
    return data

# Showing all the user's multiplication sheets
@login_required(login_url="/login")
def multiplication(request):
    global SUPERUSERS
    if request.user.id in SUPERUSERS:
        sheets = Sheet.objects.filter(sheet_type="multiplication")
    else:  
        sheets = Sheet.objects.filter(sheet_type="multiplication", user_id=request.user.id)
    return render(request, "sheetmaker/sheet.html", {
        "sheet_type": "Multiplication",
        "sheets": reversed(sheets),
        "localtimezone": request.session["localtimezone"]
    })

# Showing the individual multiplication sheet and its details
@login_required(login_url="/login")
@xframe_options_sameorigin
def multiplication_view(request, id, action):
    pageTemplate = "sheetmaker/sheet_item.html" # Default template if a simple get request
    flat_list = []
    # Two print data lists to store the data of the problems to make it more convenient for setting up the printing page
    printData1 = []
    printData2 = []
    sheet = Sheet.objects.get(id=id)
    data = sheet # For clarity
    answer_sheet_name = data.sheet_answer_name

    if action == "edit":
        pageTemplate = "sheetmaker/sheet_item_edit.html"

    if action == "print":
        pageTemplate = "sheetmaker/sheet_item_print.html"
        for problem in data.problem_data:
            flat_list += problem["numberSet"]
        
        # Creating separate print data due to how the sheets are meant to be structured
        for i in range(0, 25):
            printData1.append([flat_list[i], flat_list[i+25]])
        
        for i in range(50, 75):
            printData2.append([flat_list[i], flat_list[i+25]])
    
    return render(request, pageTemplate, {
        "sheet_type": "Multiplication",
        "breadcrumb": "multiplication", # Shown in the nav bar
        "sheet_data": data,
        "sheet_print_data_1": printData1,
        "sheet_print_data_2": printData2,
        "answer_sheet": answer_sheet_name
    })

# Create a division sheet
@login_required(login_url="/login")
def createNewDivisionSet(request):
    user = request.user.id
    data = newDivisionData() # Generating problem data
    new_sheet = Sheet(user_id=user, problem_data=data, sheet_type="division")
    new_sheet.save()
    sheet_id = new_sheet.id 
    return redirect(f"/division/{sheet_id}/view")

# Deleting a division sheet object
@login_required(login_url="/login")
@require_http_methods(["POST"])
def deleteDivisionSet(request):
    if request.method == "POST":
        sheet_id = request.POST.get("sheet_id")
        sheet = Sheet.objects.get(id=sheet_id)
        sheet.delete()
        return redirect("/division")

# Editing a division sheet object (idential to editing multiplication sheet)
@login_required(login_url="/login")
@require_http_methods(["POST"])
def editDivisionSet(request):
    if request.method == "POST":
        # Generating submitted form inputs to update division sheet object
        sheet_id = request.POST.get("sheet_id")
        current_sheet = Sheet.objects.get(id=sheet_id)
        new_sheet_name = request.POST.get("sheet_name")
        new_sheet_subname = request.POST.get("sheet_subname")
        new_answer_sheet_name = request.POST.get("sheet_answer_name")

        # Updating problem data
        first_numbers = request.POST.getlist('first')
        second_numbers = request.POST.getlist('second')
        answer_numbers = request.POST.getlist('answer')

        # Function to splice problems into JSON data for each level
        def spliceData(start, end):
            data = []
            for i in range(start, end):
                data.append({
                    "number": i+1,
                    "first": first_numbers[i],
                    "second": second_numbers[i],
                    "answer": answer_numbers[i]
                })
            return data

        level1Data = spliceData(0,20)
        level2Data = spliceData(20,40)
        level3Data = spliceData(40,60)
        level4Data = spliceData(60,80)
        level5Data = spliceData(80,100)

        jsonData = [
            { 
                'levelName': 'Level 1',
                'numberSet': level1Data
            },
            { 
                'levelName': 'Level 2',
                'numberSet': level2Data
            },
            { 
                'levelName': 'Level 3',
                'numberSet': level3Data
            },
            { 
                'levelName': 'Level 4',
                'numberSet': level4Data
            },
            { 
                'levelName': 'Level 5',
                'numberSet': level5Data
            }
        ]

        # Updating sheet object
        current_sheet.problem_data = jsonData
        current_sheet.sheet_name = new_sheet_name
        current_sheet.sheet_subname = new_sheet_subname
        current_sheet.sheet_answer_name = new_answer_sheet_name
        current_sheet.modified = datetime.utcnow()
        current_sheet.save()

        return redirect(f"division/{sheet_id}/view")

# Creating the division data (random problems generated with guidelines)
def newDivisionData():
    problems = []
    dupcheck = {} # Dictionary for checking for duplicates
    d_config = config["division"] # Going into config.py and obtaining the rules for generating the division problems
    config_keys = list(d_config.keys())
    counter = 0 # Level counter
    problem_counter = 0 # Problem counter
    for key in config_keys:
        current_set = d_config[key] # Current level
        while len(problems) < (counter + 20):
            new_problem = dict()
            new_problem["number"] = problem_counter + 1
            new_problem["first"] = random.randint(current_set["first_min"], current_set["first_max"])
            if (is_prime_number(new_problem["first"]) == True): # Do not want the first number to a prime number
                while (is_prime_number(new_problem["first"]) == True): # Re-call the randint function until the number is not a prime number
                    new_problem["first"] = random.randint(current_set["first_min"], current_set["first_max"])
            first_factors = factors(new_problem["first"], current_set["second_min"], current_set["second_max"] + 1, current_set["answer_length"]) # Getting the factors of the first number from a certain range as defined in config
            if (not first_factors): # In case first number does not have any factors
                while not first_factors:
                    new_problem["first"] = random.randint(current_set["first_min"], current_set["first_max"]) # Chooses a new first number
                    first_factors = factors(new_problem["first"], current_set["second_min"], current_set["second_max"] + 1, current_set["answer_length"]) # Gets factors again
            new_problem["second"] = random.choice(first_factors) # Chooses a random factor from first_factors to be the second number
            new_problem["answer"] = new_problem["first"] // new_problem["second"]
            key_query = "%i-%i-%i" % (new_problem["first"], new_problem["second"], new_problem["answer"]) # Creates a unique query to log in the problem to prevent duplicates
            if not dupcheck.get(key_query):
                problems.append(new_problem)
                dupcheck[key_query] = True
                problem_counter += 1
        index_list = []
        # Replacing some problems with "outliers" or easier problems (explained in config.py)
        while len(index_list) < current_set["outlier_count"]:
            index = random.randint(counter, len(problems) - 1) # Picking a random spot
            if index in index_list: # If we already replaced that problem, generate another spot
                while index in index_list:
                    index = random.randint(counter, len(problems) - 1)
            problems[index]["first"] = random.randint(current_set["first_min"] // 10, current_set["first_max"] // 10) # Picking a smaller number depending on the level
            first_factors = factors(problems[index]["first"], current_set["second_min"], current_set["second_max"] + 1, current_set["answer_length"]) # Getting the factors of the new number
            if (not first_factors): # Generating new first numbers if there are no factors for the current first number
                while not first_factors:
                    problems[index]["first"] = random.randint(current_set["first_min"] // 10, current_set["first_max"] // 10)
                    first_factors = factors(problems[index]["first"], current_set["second_min"], current_set["second_max"] + 1, current_set["answer_length"])
            problems[index]["second"] = random.choice(first_factors) # Picking second number from first factor
            problems[index]["answer"] = problems[index]["first"] // problems[index]["second"] # Answer
            key_query = "%i-%i-%i" % (problems[index]["first"], problems[index]["second"], problems[index]["answer"]) # Create a unique query to log in the problem to prevent duplicates
            if not dupcheck.get(key_query):
                index_list.append(index)
                dupcheck[key_query] = True
        counter += 20   
        data = [
            { 
                'levelName': 'Level 1',
                'numberSet': problems[0:20]
            },
            { 
                'levelName': 'Level 2',
                'numberSet': problems[20:40]
            },
            { 
                'levelName': 'Level 3',
                'numberSet': problems[40:60]
            },
            { 
                'levelName': 'Level 4',
                'numberSet': problems[60:80]
            },
            { 
                'levelName': 'Level 5',
                'numberSet': problems[80:100]
            }
        ]
    return data

# Showing all the user's division sheets
@login_required(login_url="/login")
def division(request):
    global SUPERUSERS
    if request.user.id in SUPERUSERS:
        sheets = Sheet.objects.filter(sheet_type="division")
    else:
        sheets = Sheet.objects.filter(sheet_type="division", user_id=request.user.id)
    return render(request, "sheetmaker/sheet.html", {
        "sheet_type": "Division",
        "sheets": reversed(sheets),
        "localtimezone": request.session["localtimezone"]
    }) 

# Showing the individual division sheet and its details
@login_required(login_url="/login")
@xframe_options_sameorigin
def division_view(request, id, action):
    pageTemplate = "sheetmaker/sheet_item.html" # Default template if a simple get request
    flat_list = []
    # (similar to multiplication) Two print data lists to store the data of the problems to make it more convenient for setting up the printing page
    printData1 = []
    printData2 = []
    sheet = Sheet.objects.get(id=id)
    data = sheet # For clarity
    answer_sheet_name = data.sheet_answer_name

    if action == "edit":
        pageTemplate = "sheetmaker/sheet_item_edit.html"

    if action == "print":
        pageTemplate = "sheetmaker/sheet_item_print.html"
        for problem in data.problem_data:
            flat_list += problem["numberSet"]
        
        # Creating separate print data due to how the sheets are meant to be structured
        for i in range(0, 25):
            printData1.append([flat_list[i], flat_list[i+25]])
        
        for i in range(50, 75):
            printData2.append([flat_list[i], flat_list[i+25]])

    return render(request, pageTemplate, {
        "sheet_type": "Division",
        "breadcrumb": "division", # Shown in the nav bar
        "sheet_data": data,
        "sheet_print_data_1": printData1,
        "sheet_print_data_2": printData2,
        "answer_sheet": answer_sheet_name
    })

# Create an arithmetic sheet
@login_required(login_url="/login")
def createNewArithmeticSet(request):
    user = request.user.id

    # Generating problem data based on subtype
    subtype = request.POST.get("subtype")
    if subtype == "Mitori":
        data = newArithmeticData()
    elif subtype == "Mitori Addition":
        data = newArithmeticAdditionData()
    elif subtype == "Challenged":
        data = newChallengedData()
    elif subtype == "Challenged Addition":
        data = newChallengedAdditionData()

    new_sheet = Sheet(user_id=user, problem_data=data, sheet_type="arithmetic", sheet_subtype=subtype)
    new_sheet.save()
    sheet_id = new_sheet.id 
    return redirect(f"/arithmetic/{sheet_id}/view")

# Deleting a division sheet object
@login_required(login_url="/login")
def deleteArithmeticSet(request):
    if request.method == "POST":
        sheet_id = request.POST.get("sheet_id")
        sheet = Sheet.objects.get(id=sheet_id)
        sheet.delete()
        return redirect("/arithmetic")

# Editing an arithmetic sheet
@login_required(login_url="/login")
@require_http_methods(["POST"])
def editArithmeticSet(request):
    if request.method == "POST":
        # Generating submitted form inputs to update arithmetic sheet object
        sheet_id = request.POST.get("sheet_id")
        current_sheet = Sheet.objects.get(id=sheet_id)
        new_sheet_name = request.POST.get("sheet_name")
        new_sheet_subname = request.POST.get("sheet_subname")
        new_answer_sheet_name = request.POST.get("sheet_answer_name")

        if current_sheet.sheet_subtype == "Mitori" or current_sheet.sheet_subtype == "Mitori Addition":
            # Different number of levels and different problems to multiplication and division 
            levels = [[] for i in range(0, 6)]

            # Each level has a specific number of numbers per problem which can be found through
            # number of numbers in the level / number of answers in the level 
            # which can then be used to update the data of the arithmetic sheet object
            problem_counter = 1
            for i in range(0, len(levels)):
                current_level_numbers = request.POST.getlist(f"Level {i+1}_numbers")
                current_level_answers = request.POST.getlist(f"Level {i+1}_answer")
                splice = int(len(current_level_numbers) / len(current_level_answers))
                for j in range(0, len(current_level_answers)):
                    problem_numbers = current_level_numbers[splice*j:splice*(j+1)]
                    problem_answer = current_level_answers[j]
                    problem = {"number": problem_counter, "numbers": problem_numbers, "answer": problem_answer}
                    levels[i].append(problem)
                    problem_counter += 1

            jsonData = [
                {
                    'levelName': 'Level 1',
                    'numberSet': levels[0]
                },
                {
                    'levelName': 'Level 2',
                    'numberSet': levels[1]
                },
                {
                    'levelName': 'Level 3',
                    'numberSet': levels[2]
                },
                {
                    'levelName': 'Level 4',
                    'numberSet': levels[3]
                },
                {
                    'levelName': 'Level 5',
                    'numberSet': levels[4]
                },
                {
                    'levelName': 'Level 6',
                    'numberSet': levels[5]
                }
            ]
        elif current_sheet.sheet_subtype == "Challenged" or current_sheet.sheet_subtype == "Challenged Addition":
            # Different number of levels and different problems to multiplication and division 
            levels = [[] for i in range(0, 3)]

            # Each level has a specific number of numbers per problem which can be found through
            # number of numbers in the level / number of answers in the level 
            # which can then be used to update the data of the arithmetic sheet object
            problem_counter = 1
            for i in range(0, len(levels)):
                current_level_numbers = request.POST.getlist(f"Level {i+1}_numbers")
                current_level_answers = request.POST.getlist(f"Level {i+1}_answer")
                splice = int(len(current_level_numbers) / len(current_level_answers))
                for j in range(0, len(current_level_answers)):
                    problem_numbers = current_level_numbers[splice*j:splice*(j+1)]
                    problem_answer = current_level_answers[j]
                    problem = {"number": problem_counter, "numbers": problem_numbers, "answer": problem_answer}
                    levels[i].append(problem)
                    problem_counter += 1
            
            jsonData = [
                {
                    'levelName': 'Level 1',
                    'numberSet': levels[0]
                },
                {
                    'levelName': 'Level 2',
                    'numberSet': levels[1]
                },
                {
                    'levelName': 'Level 3',
                    'numberSet': levels[2]
                }
            ]

        # Updating sheet object
        current_sheet.problem_data = jsonData
        current_sheet.sheet_name = new_sheet_name
        current_sheet.sheet_subname = new_sheet_subname
        current_sheet.sheet_answer_name = new_answer_sheet_name
        current_sheet.modified = datetime.utcnow()
        current_sheet.save()

        return redirect(f"arithmetic/{sheet_id}/view")

# Creating the arithmetic data (random problems generated with guidelines)
NEGATIVE_MAX_COUNT = 2 # Max 2 negative numbers per level
def newArithmeticData():
    problems = []
    dupcheck = {} # Dictionary for checking for duplicates
    a_config = config["arithmetic"] # Going into config.py and obtaining the rules for generating the arithmetic problems
    config_keys = list(a_config.keys())
    counter = 0 # Level counter
    problem_counter = 0 # Problem counter
    for key in config_keys:
        current_set = a_config[key] # Current level
        while len(problems) < (counter + current_set["set_problems"]):
            new_problem = dict()
            new_problem["number"] = problem_counter + 1
            number_list = []
            negative_numbers = 0
            for i in range(0, current_set["number_count"]): # Generating the list of numbers for the problem
                if i > 0:
                    random_int = random.randint(0, current_set["max"])
                    # Randomizing for chances of getting a negative number and making sure that it doesn't make the sum of the problem negative
                    if random_int < current_set["negative_percent"] and negative_numbers < NEGATIVE_MAX_COUNT and sum(number_list) >= current_set["min"]:
                        negative_numbers += 1
                        negative_int = random.randint(current_set["min"], current_set["max"])
                        if (sum(number_list) - negative_int) < 0: 
                            while (sum(number_list) - negative_int) < 0:
                                negative_int = random.randint(current_set["min"], current_set["max"])
                            number_list.append(negative_int * -1)
                        else:
                            number_list.append(negative_int * -1)
                    else:
                        number_list.append(random.randint(current_set["min"], current_set["max"]))
                else:
                    # First number can't be a negative number
                    number_list.append(random.randint(current_set["min"], current_set["max"]))
            new_problem["numbers"] = number_list
            new_problem["answer"] = sum(number_list) # Answer
            key_query = ""
            for number in number_list:
                key_query += str(number)
            key_query += str(new_problem["answer"]) # Create a unique query to log in the problem to prevent duplicates
            if not dupcheck.get(key_query):   
                problems.append(new_problem)
                dupcheck[key_query] = True
                problem_counter += 1
        counter += current_set["set_problems"]  
        data = [
            { 
                'levelName': 'Level 1',
                'numberSet': problems[0:10]
            },
            { 
                'levelName': 'Level 2',
                'numberSet': problems[10:40]
            },
            { 
                'levelName': 'Level 3',
                'numberSet': problems[40:60]
            },
            { 
                'levelName': 'Level 4',
                'numberSet': problems[60:70]
            },
            { 
                'levelName': 'Level 5',
                'numberSet': problems[70:80]
            },
            {
                'levelName': 'Level 6',
                'numberSet': problems[80:100]
            }
        ]
    return data

# Creating the arithmetic data where there is only positive numbers(random problems generated with guidelines)
ADDITION_NEGATIVE_MAX_COUNT = 0 # No negative numbers
def newArithmeticAdditionData():
    problems = []
    dupcheck = {} # Dictionary for checking for duplicates
    a_config = config["arithmetic"] # Going into config.py and obtaining the rules for generating the arithmetic problems
    config_keys = list(a_config.keys())
    counter = 0 # Level counter
    problem_counter = 0 # Problem counter
    for key in config_keys:
        current_set = a_config[key] # Current level
        while len(problems) < (counter + current_set["set_problems"]):
            new_problem = dict()
            new_problem["number"] = problem_counter + 1
            number_list = []
            negative_numbers = 0
            for i in range(0, current_set["number_count"]): # Generating the list of numbers for the problem
                if i > 0:
                    random_int = random.randint(0, current_set["max"])
                    # Randomizing for chances of getting a negative number and making sure that it doesn't make the sum of the problem negative
                    if random_int < current_set["negative_percent"] and negative_numbers < ADDITION_NEGATIVE_MAX_COUNT and sum(number_list) >= current_set["min"]:
                        negative_numbers += 1
                        negative_int = random.randint(current_set["min"], current_set["max"])
                        if (sum(number_list) - negative_int) < 0: 
                            while (sum(number_list) - negative_int) < 0:
                                negative_int = random.randint(current_set["min"], current_set["max"])
                            number_list.append(negative_int * -1)
                        else:
                            number_list.append(negative_int * -1)
                    else:
                        number_list.append(random.randint(current_set["min"], current_set["max"]))
                else:
                    # First number can't be a negative number
                    number_list.append(random.randint(current_set["min"], current_set["max"]))
            new_problem["numbers"] = number_list
            new_problem["answer"] = sum(number_list) # Answer
            key_query = ""
            for number in number_list:
                key_query += str(number)
            key_query += str(new_problem["answer"]) # Create a unique query to log in the problem to prevent duplicates
            if not dupcheck.get(key_query):   
                problems.append(new_problem)
                dupcheck[key_query] = True
                problem_counter += 1
        counter += current_set["set_problems"]  
        data = [
            { 
                'levelName': 'Level 1',
                'numberSet': problems[0:10]
            },
            { 
                'levelName': 'Level 2',
                'numberSet': problems[10:40]
            },
            { 
                'levelName': 'Level 3',
                'numberSet': problems[40:60]
            },
            { 
                'levelName': 'Level 4',
                'numberSet': problems[60:70]
            },
            { 
                'levelName': 'Level 5',
                'numberSet': problems[70:80]
            },
            {
                'levelName': 'Level 6',
                'numberSet': problems[80:100]
            }
        ]
    return data

# Creating the arithmetic data for the challenged group (random problems generated with guidelines)
CHALLENGED_NEGATIVE_MAX_COUNT = 3
def newChallengedData():
    problems = []
    dupcheck = {}
    c_config = config["challenged"]
    config_keys = list(c_config.keys())
    counter = 0
    problem_counter = 0
    for key in config_keys:
        current_set = c_config[key]
        negative_numbers = 0

        if key == "first_set":
            negative_challenge_count = 3
            negative_chance = 20
            while len(problems) < (counter + current_set["set_problems"]):
                new_problem = dict()
                new_problem["number"] = problem_counter + 1
                negative_number_count = 0

                number_list = []
                for j in range(0, current_set["number_count"]):
                    negative_number = random.randint(0, 99)
                    if negative_number < negative_chance and j != 0 and negative_number_count < negative_challenge_count and (sum(number_list) > 1):
                        negative_number_count += 1
                        number = random.randint(current_set["min"], current_set["max"])
                        if (sum(number_list) - number) < 0:
                            valid_negative = False
                            while valid_negative == False:
                                number = random.randint(current_set["min"], current_set["max"])
                                if (sum(number_list) - number) >= 0:
                                    valid_negative = True
                            number *= -1
                            number_list.append(number)
                        else:
                            number *= -1
                            number_list.append(number)
                    else:
                        number = random.randint(current_set["min"], current_set["max"])
                        number_list.append(number)

                new_problem["numbers"] = number_list
                new_problem["answer"] = sum(number_list)
                key_query = ""
                for number in number_list:
                    key_query += str(number)
                key_query += str(new_problem["answer"])
                if not dupcheck.get(key_query):
                    problems.append(new_problem)
                    dupcheck[key_query] = True
                    problem_counter += 1
            counter += current_set["set_problems"]
        else:
            while len(problems) < (counter + current_set["set_problems"]):
                new_problem = dict()
                new_problem["number"] = problem_counter + 1

                number_list = []
                valid_problem = False
                while valid_problem == False:
                    numbers = []
                    for i in range(0, current_set["number_count"]):
                        numbers.append(random.randint(10, current_set["max"]))
                    number_lis = []
                    for number in numbers:
                        number_lis.append(get_pos_nums(number))
                    tens_sum = 0
                    ones_sum = 0
                    for lis in number_lis:
                        ones_sum += lis[0]
                        tens_sum += lis[1]
                    if ones_sum < 10 and tens_sum < 10:
                        number_list = numbers
                        valid_problem = True

                negative_chance = random.randint(0, 99)
                if negative_chance < current_set["negative_percent"] and negative_numbers < CHALLENGED_NEGATIVE_MAX_COUNT:
                    negative_numbers += 1
                    random_index = random.randint(1, current_set["number_count"] - 1)
                    problem_copy = number_list
                    valid_negative = False
                    while valid_negative == False:
                        negative_int = (random.randint(10, 77)) * -1
                        problem_copy[random_index] = negative_int
                        list_sum = 0
                        for k in range(0, random_index):
                            list_sum += problem_copy[k]
                        if list_sum < 0:
                            while list_sum < 0:
                                negative_int = (random.randint(10, 77)) * -1
                                problem_copy[random_index] = negative_int
                                list_sum = 0
                                for l in range(0, random_index):
                                    list_sum += problem_copy[l]
                        sum_pos = get_pos_nums(list_sum)
                        if len(sum_pos) < 2:
                            sum_pos.insert(0, 0)
                        negative_pos = get_pos_nums(negative_int*-1)
                        if (sum_pos[0] - negative_pos[0] >= 0) and (sum_pos[1] - negative_pos[1] >= 0):
                            number_list[random_index] = negative_int
                            valid_negative = True 
                
                new_problem["numbers"] = number_list
                new_problem["answer"] = sum(number_list)
                key_query = ""
                for number in number_list:
                    key_query += str(number)
                key_query += str(new_problem["answer"])
                if not dupcheck.get(key_query):
                    problems.append(new_problem)
                    dupcheck[key_query] = True
                    problem_counter += 1
            counter += current_set["set_problems"]
    data = [
        {
            'levelName': 'Level 1',
            'numberSet': problems[0:30]
        },
        {
            'levelName': 'Level 2',
            'numberSet': problems[30:40]
        },
        {
            'levelName': 'Level 3',
            'numberSet': problems[40:50]
        }
    ]
    return data

# Creating the arithmetic data for the challenged group (random problems generated with guidelines)
CHALLENGED_NEGATIVE_MAX_COUNT = 0
def newChallengedAdditionData():
    problems = []
    dupcheck = {}
    c_config = config["challenged"]
    config_keys = list(c_config.keys())
    counter = 0
    problem_counter = 0
    for key in config_keys:
        current_set = c_config[key]

        if key == "first_set":
            while len(problems) < (counter + current_set["set_problems"]):
                new_problem = dict()
                new_problem["number"] = problem_counter + 1

                number_list = []
                for j in range(0, current_set["number_count"]):
                    number = random.randint(current_set["min"], current_set["max"])
                    number_list.append(number)

                new_problem["numbers"] = number_list
                new_problem["answer"] = sum(number_list)
                key_query = ""
                for number in number_list:
                    key_query += str(number)
                key_query += str(new_problem["answer"])
                if not dupcheck.get(key_query):
                    problems.append(new_problem)
                    dupcheck[key_query] = True
                    problem_counter += 1
            counter += current_set["set_problems"]
        else:
            while len(problems) < (counter + current_set["set_problems"]):
                new_problem = dict()
                new_problem["number"] = problem_counter + 1

                number_list = []
                valid_problem = False
                while valid_problem == False:
                    numbers = []
                    for i in range(0, current_set["number_count"]):
                        numbers.append(random.randint(current_set["min"], current_set["max"]))
                    number_lis = []
                    for number in numbers:
                        number_lis.append(get_pos_nums(number))
                    tens_sum = 0
                    ones_sum = 0
                    for lis in number_lis:
                        ones_sum += lis[0]
                        tens_sum += lis[1]
                    if ones_sum < 10 and tens_sum < 10:
                        number_list = numbers
                        valid_problem = True
                
                new_problem["numbers"] = number_list
                new_problem["answer"] = sum(number_list)
                key_query = ""
                for number in number_list:
                    key_query += str(number)
                key_query += str(new_problem["answer"])
                if not dupcheck.get(key_query):
                    problems.append(new_problem)
                    dupcheck[key_query] = True
                    problem_counter += 1
            counter += current_set["set_problems"]
    data = [
        {
            'levelName': 'Level 1',
            'numberSet': problems[0:30]
        },
        {
            'levelName': 'Level 2',
            'numberSet': problems[30:40]
        },
        {
            'levelName': 'Level 3',
            'numberSet': problems[40:50]
        }
    ]
    return data

# Showing all the user's arithmetic sheets
@login_required(login_url="/login")
def arithmetic(request):
    global SUPERUSERS
    if request.user.id in SUPERUSERS:
        sheets = Sheet.objects.filter(sheet_type="arithmetic")
    else:   
        sheets = Sheet.objects.filter(sheet_type="arithmetic", user_id=request.user.id)
    return render(request, "sheetmaker/sheet.html", {
        "sheet_type": "Arithmetic",
        "sheets": reversed(sheets),
        "localtimezone": request.session["localtimezone"]
    }) 

# Showing the individual sheet and its details
@login_required(login_url="/login")
@xframe_options_sameorigin
def arithmetic_view(request, id, action):
    pageTemplate = "sheetmaker/sheet_item.html" # Default template if a simple get request
    flat_list = []
    # Two print data lists to store the answers to make it more convenient for setting up the printing page
    printData1 = []
    printData2 = []
    sheet = Sheet.objects.get(id=id)
    data = sheet # For clarity
    answer_sheet_name = data.sheet_answer_name

    if action == "edit":
        pageTemplate = "sheetmaker/sheet_item_edit.html"

    if action == "print":
        pageTemplate = "sheetmaker/sheet_item_print.html"
        if data.sheet_subtype == "Mitori" or data.sheet_subtype == "Mitori Addition":
            flat_list = []
            # Adding all of the problems to a flat list to make it easier for splicing and printing
            for problem in data.problem_data:
                flat_list += problem["numberSet"]

            # Creating print data for the answers
            for i in range(0, 25):
                printData1.append([flat_list[i], flat_list[i+25]])
        
            for i in range(50, 75):
                printData2.append([flat_list[i], flat_list[i+25]])

            return render(request, pageTemplate, {
                "sheet_type": "Arithmetic",
                "breadcrumb": "arithmetic", # Shown in the nav bar
                "sheet_data": data,
                # All of the problems divided into their levels
                "sheet_print_data1": flat_list[0:10],
                "sheet_print_data2": flat_list[10:20],
                "sheet_print_data3": flat_list[20:30],
                "sheet_print_data4": flat_list[30:40],
                "sheet_print_data5": flat_list[40:50],
                "sheet_print_data6": flat_list[50:60],
                "sheet_print_data7": flat_list[60:70],
                "sheet_print_data8": flat_list[70:80],
                "sheet_print_data9": flat_list[80:90],
                "sheet_print_data10": flat_list[90:100],
                "sheet_answer_data1": printData1,
                "sheet_answer_data2": printData2,
                "answer_sheet": answer_sheet_name
            })
        elif data.sheet_subtype == "Challenged" or data.sheet_subtype == "Challenged Addition":
            flat_list = []
            for problem in data.problem_data:
                flat_list += problem["numberSet"]

            # for i in range(0, 30):
            #     printData1.append([flat_list[i], flat_list[i+30]])
            for i in range(0, 25):
                printData1.append([flat_list[i], flat_list[i+25]])
        
            # for i in range(50, 60):
            #     printData2.append([flat_list[i], []])

            return render(request, pageTemplate, {
                "sheet_type": "Arithmetic",
                "breadcrumb": "arithmetic",
                "sheet_data": data,
                "sheet_print_data1": flat_list[0:10],
                "sheet_print_data2": flat_list[10:20],
                "sheet_print_data3": flat_list[20:30],
                "sheet_print_data4": flat_list[30:40],
                "sheet_print_data5": flat_list[40:50],
                # "sheet_print_data6": flat_list[50:60],
                "sheet_answer_data1": printData1,
                "sheet_answer_data2": printData2,
                "answer_sheet": answer_sheet_name
            })

    
    return render(request, pageTemplate, {
        "sheet_type": "Arithmetic",
        "breadcrumb": "arithmetic", # Shown in the nav bar
        "sheet_data": data
    })

# Generating a new set of data whenever the user presses the "refresh" button
@require_http_methods(["POST"])
def generateNewSet(request):
    if request.method == "POST":
        
        # Getting the data from the fetch request
        data = json.loads(request.body)
        sheet_id = data.get("sheetId")
        level = data.get("level")
        autosave = data.get("autosave")

        # Querying the correct sheet from the database
        current_sheet = Sheet.objects.get(id=sheet_id)
        type = current_sheet.sheet_type
        data = current_sheet.problem_data

        # Generating the new problem data
        new_data = {}
        if type == "multiplication":
            new_data = newMultiplicationData()
        elif type == "division":
            new_data = newDivisionData()
        elif type == "arithmetic":
            subtype = current_sheet.sheet_subtype
            if subtype == "Mitori":
                new_data = newArithmeticData()
            elif subtype == "Mitori Addition":
                new_data = newArithmeticAdditionData()
            elif subtype == "Challenged":
                new_data = newChallengedData()
            elif subtype == "Challenged Addition":
                new_data = newChallengedAdditionData()

        # Only autosavess if the user is not in edit mode
        if autosave == True:
            current_sheet.problem_data[level-1] = new_data[level-1]
            current_sheet.save()
        
        return JsonResponse(new_data[level-1], safe=False)


# Function to find if the inputted number is a prime number
def is_prime_number(x):
    if x >= 2:
        for y in range (2, x):
            if not (x % y):
                return False 
    else:
        return False
    return True

# Function to find the factors of a number within a given range
def factors(x, min, max, length):
    factors = []
    for i in range(min, max):
        if x % i == 0:
            quotient = str(int(x / i))
            if len(quotient) == length:
                factors.append(i)
    return factors

# Function to return a list of numbers originating from their positions in the inputted numnber
def get_pos_nums(num):
    pos_nums = []
    while num != 0:
        pos_nums.append(num % 10)
        num = num // 10
    return pos_nums