# daily-briefing
A system that tells you and answers questions about your day.

`$python daily_briefing.py` to see a test example

## Google API Credentials
You need to authorize the google api to have access to your calendar and mail account.

1. NOTE: For the following steps, make sure to use the same project to authenticate, so that our single daily_briefing app can have access both your calendar and mail.
2. Go https://developers.google.com/gmail/api/quickstart/python. Click the big blue button that says "ENABLE THE GMAIL API", follow the instructions...
3. Go to https://developers.google.com/calendar/quickstart/python. Click the big blue button that says "ENABLE THE GOOGLE CALENDAR API".

You'll have to download a file called `credentials.json`. Put it in the `./config` directory of this project (just to keep things tidy). And put the `token.json` in the that `/.config` folder.

## Text-To-Speech
Need mpg321 installed on your computer. for mac `$brew install mpg321`

## Virtual Environment Set Up
To isolate the dependencies we use in our project (so they aren't installed in your whole system and isolated to your project), we will use virtualenv, which is a popular package used to do this.

1. Check if you have `pip` which is the most commonly used python package manager. If you don't, install it by following the instructions here: https://pip.pypa.io/en/stable/installing/
2. If you don't already have `virtualenv`, install it by running:

```python
pip install virtualenv
```
This will install the python virtualenv package on your computer.

3. Create a virtualenv in your project folder by running:

```python
virtualenv venv
```
This will create a virtualenv named  `venv`. You'll see a new `venv` folder in the directory as well. This folder is .gitignored, so it will not be tracked by git (this is what should happen).

## Usage

#### Whenever you work on this project...
Navigate to the working directory and run this command:

```python
source venv/bin/activate
```

This will activate your virtualenv, which ensures that the python interpreter you use will be from the virtualenv and any external packages you install will be available to you.

#### Whenever you want to install a new library...

Make sure your virtualenv is active (to make sure the library isn't installed on your whole system, only your virtualenv). Then, run:

```python
pip install <my_package>
```
where `<my_package>` is the name of the pip distribution of the package. Most libraries give you the specific pip command to install them.

After doing this, run:

```python
pip freeze > requirements.txt
```
*What this does*: `pip freeze` outputs a list of the current project dependencies and redirects them into a file named `requirements.txt`.
*Why we do this*: So that when someone pulls from the repo and the project has new dependencies, they can simply install the newly listed dependencies by running:
```python
pip install -r requirements.txt
```

#### When you're done working...
Simply run:

```python
deactivate
```
This deactivates your virtualenv and sets your PATH variable back to normal. Recommend doing this.
