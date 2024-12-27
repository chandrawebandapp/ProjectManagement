# ProjectManagement

### Create a Virtual Environment
#### Set up a virtual environment to manage dependencies.
###### python -m venv venv
###### source venv/bin/activate   # On macOS/Linux

###### venv\Scripts\activate      # On Windows


### Install Dependencies
#### Install the required Python packages:
###### pip install -r requirements.txt



### Apply Database Migrations
#### Run the following commands to set up the database schema:
###### python manage.py makemigrations
###### python manage.py migrate

### Create a Superuser (Optional)
#### To access the admin interface, create a superuser:
###### python manage.py createsuperuser 


### Run the Development Server
#### Start the local development server:
###### python manage.py runserver
