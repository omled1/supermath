# File to specify the rules for generating the problems for each of the problem sheets (multiplication, division, arithmetic)

# Dictionary that contains the rules for each of the aspects of a problem on a sheet for each level
config = dict()

# Multiplication configuration (each set is a level)
# First min and max represents the minimum and maximum value of the first number for that level respectively
# Second min and max represents the minimum and maximum value of the second number for that level respectively
config["multiplication"] = {
    "first_set": {
        "first_min": 10,
        "first_max": 99,
        "second_min": 2,
        "second_max": 9
    },
    "second_set": {
        "first_min": 100,
        "first_max": 999,
        "second_min": 2,
        "second_max": 9
    },
    "third_set": {
        "first_min": 10,
        "first_max": 99,
        "second_min": 10,
        "second_max": 99
    },
    "fourth_set": {
        "first_min": 100,
        "first_max": 999,
        "second_min": 10,
        "second_max": 99
    },
    "fifth_set": {
        "first_min": 100,
        "first_max": 999,
        "second_min": 100,
        "second_max": 999
    }
}

# Division configuration (each set is a level)
# First min and max represents the minimum and maximum value of the first number for that level respectively
# Second min and max represents the minimum and maximum value of the second number for that level respectively
# Outlier count represents the number of "outliers" or easier problems that are found within a level
config["division"] = {
    "first_set": {
        "first_min": 100,
        "first_max": 999,
        "second_min": 2,
        "second_max": 9,
        "outlier_count": 3
    },
    "second_set": {
        "first_min": 1000,
        "first_max": 9999,
        "second_min": 2,
        "second_max": 9,
        "outlier_count": 3
    },
    "third_set": {
        "first_min": 1000,
        "first_max": 9999,
        "second_min": 10,
        "second_max": 99,
        "outlier_count": 3
    },
    "fourth_set": {
        "first_min": 10000,
        "first_max": 99999,
        "second_min": 10,
        "second_max": 99,
        "outlier_count": 4
    },
    "fifth_set": {
        "first_min": 10000,
        "first_max": 99999,
        "second_min": 100,
        "second_max": 999,
        "outlier_count": 3
    }
}

# Arithmetic configuration (each set is a level)
# Set problems represents the number of problems for the level
# Number count represents the number of numbers per problem
# Min and max represent the maximum and minimum for each of the numbers in a problem
# Negative percent represents the chance of a negative number should appear
config["arithmetic"] = {
    "first_set": {
        "set_problems": 10,
        "number_count": 3,
        "min": 10,
        "max": 99,
        "negative_percent": 10
    },
    "second_set": {
        "set_problems": 30,
        "number_count": 4,
        "min": 10,
        "max": 99,
        "negative_percent": 10
    },
    "third_set": {
        "set_problems": 20,
        "number_count": 5,
        "min": 10,
        "max": 99,
        "negative_percent": 10
    },
    "fourth_set": {
        "set_problems": 10,
        "number_count": 6,
        "min": 10,
        "max": 99,
        "negative_percent": 10
    },
    "fifth_set": {
        "set_problems": 10,
        "number_count": 7,
        "min": 10,
        "max": 99,
        "negative_percent": 10
    },
    "sixth_set": {
        "set_problems": 20,
        "number_count": 7,
        "min": 100,
        "max": 999,
        "negative_percent": 100 # It's 100 because it's based off the digits of the numbers in the level which is three digits in this case
    }
}