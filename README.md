# django Store App
This project was created with django framework which is built on python language

## __getting started__
<br/>

### <mark style="background-color: whitesmoke;font-weight: bold;padding: 4px">1- creating a virtual environment</mark>

<br />

> first we need a virtual environment with python.

In windows we can write this command in the terminal inside root directory: 

```
python -m venv venv
```

and for linux and macOS (also inside the root directory):
```
python3 -m venv venv
```

### <mark style="background-color: whitesmoke;font-weight: bold;padding: 4px">2- activating the virtual environment</mark>

<br />

>second we want to activate this virtual environment.

for windows we can activate it by running this command in the same directory that __virtual environment__ has:
```
venv\Scripts\activate
```

and for linux and macOS:

```
source venv/bin/activate
```

 ### <mark style="background-color: whitesmoke;font-weight: bold; padding: 4px">3- installing dependicies</mark> 

<br/>

> Then we should install the required modules for this project by running this command __when the virtual environment is activated__.

```
pip install -r requirements.txt
```

 ### <mark style="background-color: whitesmoke;font-weight: bold; padding: 4px">4- migrating the data to the database</mark> 

<br/>

>__when we are activating the venv__ we should run these commands to migrate the data to the database:

```
python manage.py makemigrations
```

then:

```
python manage.py migrate
```

 ### <mark style="background-color: whitesmoke;font-weight: bold; padding: 4px">5- creating an admin for the website</mark>
 <br/>

 >if we want to access the admin url through  __/admin__ end point then we should create it the admin by running this command:

 ```
python manage.py createsuperuser
```

then we can determine his information.

 ### <mark style="background-color: whitesmoke;font-weight: bold; padding: 4px">6- running the server</mark>
 <br/>

 > Finally, we can run the server like this:

 ```
 python manage.py runserver
 ```

 we can go to http://localhost:8000 to access the website, and access the admin panel by going to http://localhost:8000/admin.

 we can deactivate the venv by running this command:
 ```
 deactivate
 ```
