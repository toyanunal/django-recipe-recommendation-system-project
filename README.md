# Recipe Recommendation System
This is the repo for our recipe recommendation system project called "Show Me What You Got (SMWYG)".

The SMWYG system allows users to search for recipes by selecting a group of ingredients, portion, and an additional cost. These ingredients can be based on what users choose to eat or which ingredients are readily available in their homes. The system lists all recipes with selected ingredients in addition to missing ingredients that are within the given additional cost range. After that, users can filter recipes based on meal types (i.e., breakfast, lunch, dinner, dessert, and snack); based on certain diet types (i.e., healthy, low carb, vegan, and vegetarian); and based on effort (i.e., easy, moderate, hard). After filtering recipes, users can select a certain recipe and see the names, recipe amounts, and missing amounts, as well as the additional cost of purchasing those insufficient ingredients. Users can sign up and log in to the system. Registered users can keep track of their inventory in terms of ingredient names and quantities. Users can easily remove ingredients of completed recipes from their pantry by marking them as complete.

## Technologies Used
<ul>
<li>Atom (as text editor)</li>
<li>Chrome (as web browser)</li>
<li>Python (as language)</li>
<li>Django (as framework)</li>
<li>Pillow and Django-Autoslug (as modules)</li>
<li>SQLite (as database)</li>
<li>HTML, CSS and Bootstrap (for front-end development)</li>
<li>JavaScript (for pop-up messages)</li>
</ul>

## Deployed Application
* [https://toyanunal.pythonanywhere.com/](https://toyanunal.pythonanywhere.com/)

## Screenshots
### Home page
![Home](https://user-images.githubusercontent.com/59750131/177047779-9f35dcf9-35ac-4949-9eb8-b355a5f3827a.png)
### User Input page
![Input](https://user-images.githubusercontent.com/59750131/177047784-eced9481-24a2-46f8-b8a1-f4db169dc891.png)
### Pantry Create page
![Pantry](https://user-images.githubusercontent.com/59750131/177047785-34684318-65fd-45e9-8e1a-fa5c87e2b41e.png)
### Recipe List page
![List](https://user-images.githubusercontent.com/59750131/177047790-e717252d-ca3b-4931-b314-0d51bb285a5d.png)
### Recipe Detail page
![Detail](https://user-images.githubusercontent.com/59750131/177047795-74af9d0e-f854-4a41-b59d-b1656b1261f3.png)

## Installation
Navigate to your projects directory.
Go to Anaconda, Atom or Command prompt and run the following codes.
```bash
git clone https://github.com/toyanunal/django-recipe-recommendation-system-project.git && cd django-recipe-recommendation-system-project
conda create --name djangoenv django
conda activate djangoenv
pip install -r requirements.txt
cd /rrs_project/
```

## Create Admin
You can create an admin user using command prompt.
```bash
python manage.py createsuperuser
```

You can access the django admin page at **http://127.0.0.1:8000/admin** and login with superuser's username and password.

## Database Setup
Migrate db.sqlite3 file to the Django database using the following codes.
```bash
python manage.py makemigrations
python manage.py migrate
```

## Run Application
Run the application.
```bash
python manage.py runserver
```

## Register & Login
You can create an account using **_Register_** page of the application and log into that account using **_Login_** page of the application.
You can also get started as **_Guest_** by clicking **_Get Started_** button.

## Deployment
Apply the following steps to deploy this application to the **https://www.pythonanywhere.com**

Check out [this link](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/) for official guide.

<ins>An example walkthrough for Django application deployment on Pythonanywhere:</ins>

Consoles > Start a new console > Other > Bash
```bash
mkvirtualenv --python=python3.9 djangoenv
workon djangoenv
pip install -U django==3.2.5
pip install Pillow
pip install django-autoslug
git clone https://github.com/toyanunal/django-recipe-recommendation-system-project.git
cd django-recipe-recommendation-system-project/
cd rrs_project/
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
toyanunal
toyanunal@gmail.com
password
```

Web > Add a new web app > Next > Manual configuration > Python 3.9 > Next

Web > Virtualenv > Enter path to a virtualenv > `/home/toyanunal/.virtualenvs/djangoenv`

Web > Code > Source code > `/home/toyanunal/django-recipe-recommendation-system-project/rrs_project`

Web > Code > WSGI configuration file > click on the link > delete all > add the following code > Save > close tab
```bash
import os
import sys
path = '/home/toyanunal/django-recipe-recommendation-system-project/rrs_project'
if path not in sys.path:
    sys.path.append(path)
os.chdir(path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rrs_project.settings')
import django
django.setup()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Web > Static files > URL > Enter URL > `/static/admin`

Web > Static files > Directory > Enter path > `/home/toyanunal/.virtualenvs/djangoenv/lib/python3.9/site-packages/django/contrib/admin/static/admin`

Web > Static files > URL > Enter URL > `/static/`

Web > Static files > Directory > Enter path > `/home/toyanunal/django-recipe-recommendation-system-project/rrs_project/rrs_app/static`

Web > Static files > URL > Enter URL > `/media/`

Web > Static files > Directory > Enter path > `/home/toyanunal/django-recipe-recommendation-system-project/rrs_project/rrs_app/static/images`

Files > click on `django-recipe-recommendation-system-project` > click on `rrs_project` > click on `rrs_project` > click on `settings.py` > add `ALLOWED_HOSTS = ['toyanunal.pythonanywhere.com']` > Save > close tab

Files > click on `django-recipe-recommendation-system-project` > click on `rrs_project` > click on `rrs_project` > click on `settings.py` > add `DEBUG=False` > Save > close tab

Web > Reload > click on `Reload toyanunal.pythonanywhere.com`

Browser > go to [https://toyanunal.pythonanywhere.com/](https://toyanunal.pythonanywhere.com/)
