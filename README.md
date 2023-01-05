## DISTINCTIVENESS AND COMPLEXITY

I think my program satisfies the distinctiveness and complexity requirement because:

1. The product and business logic of the application is unique. No past projects created a math problem sheet model that featured multiplication, division, and addition/subtraction questions. These problem sheets are primarily found in SuperMath, the mental math program I was formerly a part of. Since I wanted to make the sheets the same structure as the ones found in SuperMath, I had to follow many guidelines. It was more complex than generating random integers, with the problems getting progressively more challenging. As seen in how I generate the data in my views.py, I had to ensure that there were no negative answers for all problem sheets, no decimal answers for division sheets, and limited negative operands for addition and subtraction sheets. I also had to ensure that these rules were enforced whenever a user edited a sheet.

2. Ability to print conveniently. These sheets were meant to be done on physical paper, so I needed to add the ability to print. I had to ensure that the printing page looked identical to past problem sheets from SuperMath, so it wasn’t as simple as just printing whatever was being shown on sheet.html. No past projects had this feature to print data in a formatted and convenient way like this.

3. Implementing obtaining the browser’s timezone, a fundamental feature that Django surprisingly lacks. Django has a library called tz, which allows you to convert DateTime objects to a specific timezone or to “local time” by using a filter. However, applying this filter would only convert the time to the timezone defined in settings.py, which by default, was UTC. Of course, users of my website could be anywhere in the world, which is why I had to find a way to convert the created/modified times in sheet.html to be respectful of the browser’s timezone. Django had no simple way to do this, so I devised an elegant and efficient way to handle this limitation. I created a JavaScript function that would inject the browser’s timezone as a value in a hidden input field in the login form. Whenever a valid user logs in, the browser’s timezone is passed in the POST request to views.py, which I then set as the timezone to be used when filtering the created/modified times in sheet.html.

## WHAT’S CONTAINED IN EACH FILE

- Settings.dev.py
    - A copy of settings.py except DEBUG is set to “True.” I replace settings.py with the contents of this file when I am running the web application locally on my computer.

- Settings.prod.py
    - A copy of settings.py except DEBUG is set to “False.” I replace settings.py with the contents of this file when I push the changes to Git and pull the new changes on PythonAnywhere, the website I am hosting my web application on.

- Sheetmaker.js
    - Contains all of the JavaScript for the application.

- Styles.css 
    - Contains all of the styling for the application.

- Index.html 
    - Contains the HTML for the home page.

- Layout_print.html
    - Serves as a layout template for sheet_item_print.html.

- Layout.html
    - Serves as a layout template for index.html, login.html, register.html, sheet_item_edit.html, sheet_item.html, and sheet.html.

- Login.html
    - Contains the form for existing users to log in.

- Register.html 
    - Contains the form for visitors to register.

- Sheet_item_edit.html 
    - Contains the page where users can edit the numbers on the page, the sheet name, and, optionally, the sheet subname.

- Sheet_item_print.html 
    - Contains a page that formats the data from the sheet to be suited for printing (A4 or standard printing size) and/or saving as a PDF.

- Sheet_item.html 
    - Contains a page of the sheet and its details: the problem data, its name, and its subname. It also contains the buttons to print and edit the sheet.

- Sheet.html 
    - Contains a page that displays a list of the user’s created sheets for that specific section (Multiplication, Division, Arithmetic). It presents the sheet’s IDs, name, when it was created, when it was modified, and buttons that allow users to view the sheets or delete them.

- 404.html
    - Contains a page that displays a 404 NOT FOUND message if the path is not found.

- 500.html
    - Contains a page that displays a 505 SERVER ERROR message if there is a server error during runtime.

- Models.py 
    - Contains the User model and the Sheet model.

- Urls.py 
    - Contains all paths that are used in the application.

- Views.py 
    - Contains all of the functions that handle HTTP requests and returns HTTP responses or renders templates. Also contains the business logic for creating, storing, editing, and deleting the problem sheets.

- .gitignore 
    - Contains what files to ignore when pushing and pulling to Git. Since the data and caches on my local system are different from PythonAnywhere, I specify that when I push these changes, these files get ignored to prevent creating conflicts.
    
- Requirements.txt 
    - Contains all of the required libraries needed to run this application.

## HOW TO RUN THE APPLICATION
1. Ensure that all of the libraries are installed through “pip install -r requirements.txt”
2. Run “cd supermath/capstone”
3. Run “python3 manage.py runserver” or “python manage.py runserver” to run the application
4. “CTRL + C” to close the application

## ADDITIONAL INFORMATION
- I made this application specifically for the founder of SuperMath. When I heard that she was creating these problem sheets manually, I decided to make this web application to make the process as easy as possible. I thought that this would be a good way to give back, especially since I greatly benefitted from the program by teaching me a very valuable skill.
- Because I made this application for the founder of SuperMath, I restricted which users could access the features of this website which I am hosting on PythonEverywhere. TO TEST OUT THIS APPLICATION, PLEASE USE THE USERNAME "cs50w" WHEN REGISTERING AN ACCOUNT.