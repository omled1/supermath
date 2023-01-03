To Run Code
    
    1. "cd supermath/capstone/sheetmaker"

    2. "python manage.py runserver"

    3. CTRL + C to terminate server

Models/Migrations
    
    1. If made changes to models.py, run "python manage.py makemigrations"
    
    2. Run "python manage.py migrate" to apply those migrations


Setup development environment
    * Install python (i.e. python3)
        - on MacOS https://docs.python-guide.org/starting/install3/osx/

    * Install Pipenv - 
        https://docs.python-guide.org/dev/virtualenvs/#virtualenvironments-ref
        https://thoughtbot.com/blog/how-to-manage-your-python-projects-with-pipenv
        
        - python3, use pip3
            pip3 install pipenv

        ex:
            pipenv shell
            pipenv run python my_project.py



To create superuser
    * python manage.py createsuperuser

To run the server
    * python manage.py runserver
