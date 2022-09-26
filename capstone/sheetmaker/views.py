from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .config import config
import random

# Create your views here.

def index(request):
    return render(request, "sheetmaker/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "sheetmaker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "sheetmaker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "sheetmaker/register.html")

@login_required
def history(request):
    return render(request, "sheetmaker/history.html")

def multiplication(request):
    problems = []
    dupcheck = {}
    m_config = config["multiplication"]
    config_keys = list(m_config.keys())
    counter = 0
    for key in config_keys:
        current_set = m_config[key]
        while len(problems) < (counter + 20):
            new_problem = dict()
            new_problem["first"] = random.randint(current_set["first_min"], current_set["first_max"])
            new_problem["second"] = random.randint(current_set["second_min"], current_set["second_max"])
            new_problem["answer"] = new_problem["first"] * new_problem["second"]
            key_query = "%ix%ix%i" % (new_problem["first"], new_problem["second"], new_problem["answer"])
            if not dupcheck.get(key_query):
                problems.append(new_problem)
                dupcheck[key_query] = True
        counter += 20
    return render(request, "sheetmaker/sheet.html", {
        "sheet_type": "Multiplication",
        "problems": problems
    })


def division(request):
    problems = []
    dupcheck = {}
    d_config = config["division"]
    config_keys = list(d_config.keys())
    counter = 0
    for key in config_keys:
        current_set = d_config[key]
        while len(problems) < (counter + 20):
            new_problem = dict()
            new_problem["first"] = random.randint(current_set["first_min"], current_set["first_max"])
            if (is_prime_number(new_problem["first"]) == True):
                while is_prime_number(new_problem["first"] == True):
                    new_problem["first"] = random.randint(current_set["first_min"], current_set["first_max"])
            new_problem["second"] = random.randint(current_set["second_min"], current_set["second_max"])
            if (new_problem["first"] % new_problem["second"] != 0):
                first_factors = factors(new_problem["first"], current_set["second_min"], current_set["second_max"] + 1)
                if (not first_factors):
                    while not first_factors:
                        new_problem["first"] = random.randint(current_set["first_min"], current_set["first_max"])
                        first_factors = factors(new_problem["first"], current_set["second_min"], current_set["second_max"] + 1)
                new_problem["second"] = random.choice(first_factors)
            new_problem["answer"] = new_problem["first"] // new_problem["second"]
            key_query = "%i-%i-%i" % (new_problem["first"], new_problem["second"], new_problem["answer"])
            if not dupcheck.get(key_query):
                problems.append(new_problem)
                dupcheck[key_query] = True
        index_list = []
        while len(index_list) < current_set["outlier_count"]:
            index = random.randint(counter, len(problems) - 1)
            if index in index_list:
                while index in index_list:
                    index = random.randint(counter, len(problems) - 1)
            problems[index]["first"] = random.randint(current_set["first_min"] // 10, current_set["first_max"] // 10)
            first_factors = factors(problems[index]["first"], current_set["second_min"], current_set["second_max"] + 1)
            if (not first_factors):
                while not first_factors:
                    problems[index]["first"] = random.randint(current_set["first_min"] // 10, current_set["first_max"] // 10)
                    first_factors = factors(problems[index]["first"], current_set["second_min"], current_set["second_max"] + 1)
            problems[index]["second"] = random.choice(first_factors)
            problems[index]["answer"] = problems[index]["first"] // problems[index]["second"]
            key_query = "%i-%i-%i" % (problems[index]["first"], problems[index]["second"], problems[index]["answer"])
            if not dupcheck.get(key_query):
                index_list.append(index)
                dupcheck[key_query] = True
        counter += 20   
    return render(request, "sheetmaker/sheet.html", {
        "sheet_type": "Division",
        "problems": problems
    })

NEGATIVE_MAX_COUNT = 2
def arithmetic(request):
    problems = []
    dupcheck = {}
    a_config = config["arithmetic"]
    config_keys = list(a_config.keys())
    counter = 0
    for key in config_keys:
        current_set = a_config[key]
        while len(problems) < (counter + current_set["set_problems"]):
            new_problem = dict()
            number_list = []
            negative_numbers = 0
            for i in range(0, current_set["number_count"]):
                if i > 0:
                    random_int = random.randint(0, current_set["max"])
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
                    number_list.append(random.randint(current_set["min"], current_set["max"]))
            new_problem["numbers"] = number_list
            new_problem["answer"] = sum(number_list)
            key_query = ""
            for number in number_list:
                key_query += str(number)
            key_query += str(new_problem["answer"])
            if not dupcheck.get(key_query):   
                problems.append(new_problem)
                dupcheck[key_query] = True
        counter += current_set["set_problems"]
    return render(request, "sheetmaker/sheet.html", {
        "sheet_type": "Addition/Subtraction",
        "problems": problems
    })

def is_prime_number(x):
    if x >= 2:
        for y in range (2, x):
            if not (x % y):
                return False 
    else:
        return False
    return True

def factors(x, min, max):
    factors = []
    for i in range(min, max):
        if x % i == 0:
            factors.append(i)
    return factors
