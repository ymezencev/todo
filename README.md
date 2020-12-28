# To do application
## Python, Django project
### Try using it: http://130.193.34.182/todo/all/
### A Django web application to add and organize tasks. To do application makes you more productive. Project for educational purposes.

### Cool things about this app:
* Add as many tasks as you need
* Group tasks by categories
* Create your own categories
* The most important tasks could be found in "Important" category
* You can add tasks to important from any page
* App design is simple and useful


![todo-app-interface](https://user-images.githubusercontent.com/60066986/97801859-ca2f7000-1c50-11eb-9db3-38d054aeeffa.png)

# Installation 
1. Clone this repository into your directory
```
cd git
https://github.com/ymezencev/todo.git
cd todo
```
2. Install requirements
```
python -m venv env
. env/bin/activate
pip install -r requirements.txt
```

3. Configure database
```
vim src/config/settings.py
# for aqlite3 just incomment
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
# for postgres - install postgres
```
4. Set up your virtual env vars
```
DJANGO_SECRET_KEY=''
# for postgres
DB_NAME=''
DB_USER=''
DB_PASSWD=''

```
5. Start the app
```
cd todo
pyrhon manage.py runserver
```
# Enjoy it!
