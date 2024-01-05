## IMPORTANT INFORMATION
#### I created this application mainly for the founder of SuperMath. Thus, even though I have published this application on the web, I refrain from sharing the link since I prefer that the access and use of the website be limited to me and the founder only. This is also why I limited the valid usernames a user could use to register an account. So, if you want to try out this web application's features on your own machine, please use the username "demo" when registering an account. Any e-mail address and password will suffice.

## HOW TO RUN THE APPLICATION
1. Ensure that all of the libraries are installed through “pip install -r requirements.txt”
2. Run “cd supermath/capstone”
3. Run “python3 manage.py runserver” or “python manage.py runserver” to run the application
4. “CTRL + C” to close the application

## HOW TO RUN THE APPLICATAION USING Virtual Environment
1. Run source venv/supermath_env/bin/activate
2. Run “cd supermath/capstone”
3. Run “python3 manage.py runserver” or “python manage.py runserver” to run the application
4. “CTRL + C” to close the application


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
    - Contains a page that displays a 500 SERVER ERROR message if there is a server error during runtime.

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
