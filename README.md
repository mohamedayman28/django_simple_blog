# Django Simple Blog
<!-- Brief description goes here -->

#### Jump to:
* [Setting up locally](#setting-up-locally)
* [File Browser package error](#file-browser-package-error)
* [Populate database with dummy data](#populate-database-with-dummy-data)


## Setting up locally

To set the site up locally, you'll need to have Python 3.6 or higher version installed on your local machine. Once that is done and ready, proceed to download the repository with the next steps.


### 1. Make the directory for development:
```bash
mkdir simple_blog
cd simple_blog
```


### 2. Create virtualenv:

**Note:** You may want to change the Python version, I'm also using Linux Ubuntu-based OS, so depending on your OS you may use different commands for creating a python virtual environment.

```bash
sudo apt-get install python3-pip
sudo apt-get install python3.6-venv
python3.6 -m venv blog_env
```


### 3. Activate virtualenv:
```bash
source blog_env/bin/activate
```


### 4. Download the repository:
```bash
git init
git clone https://github.com/mohamedayman28/django_simple_blog
```


### 5. Install required packages:
```bash
cd django_simple_blog
pip install -r requirements.txt
```


### 6. Migrate:
```bash
python manage.py makemigrations
python manage.py migrate
```

If the migrations doesn't apply to all apps, you may need to migrate each app individually

```bash
python manage.py makemigrations posts
python manage.py migrate posts
```


### 7. Create Super User:
```bash
python manage.py createsuperuser
```
Only authors allowed to write posts, and you will need to create author manually.


### 8. Run the app:
```bash
python manage.py runserver
```


### File Browser package error
You may encounter this log error while using filebrowser
```
Error finding Upload-Folder (site.storage.location + site.directory). Maybe it does not exist?
```
If that the case, create folder in the app root directory (with manage.py and
the templates folder) named as the name set in the settings.MEDIA_ROOT


### Populate database with dummy data
I included a file called factories, regarding the test purposes it's originally
developed for, I use it to populate the database with dummy data, so it's up to
you to remove the file or keep it.

Anyway, this is how I populate the database:

* First activate Django shell
```python
python manage.py shell
```

* then import PostFactory and loop over the number of times you want your database
to get populated
```python
from posts.factories import PostFactory

# Populate database 20 times with different text.
for i in range(20):
    PostFactory()
```

**Note:** The previous steps does not follow the best practice or a SAVING TIME
approach, and I didn't invest time for enhancement or search for a better approach
since I needed the population once, so enhancement is up to you.
