# regulately back-end
Making it easier to understand and influence new government regulations with Python NLP

A project from the second [Debug Politics](http://www.debugpolitics.com/) hackathon in San Francisco. You can see other projects using the [regulations.gov](https://www.regulations.gov/) [API](http://regulationsgov.github.io/developer) in the [regulationsgov organization](https://github.com/regulationsgov) and their [API showcase](https://www.regulations.gov/apiOverview?page=showcase).

## Installing

 - Create a virtual environment in the project folder with `virtualenv venv`
 - Activate the virtual environment with `source venv/bin/activate` (or `source venv/Scripts/activate` if you're on Windows)
 - Install the necessary packages with `pip install requirements.txt`
 - You'll need to create a MongoDB database and save the connection string and database name to a file called ExternalServices.py (in the top level project directory). This file will need the globals DATABASE (the name of the mongo database you plan to use) and MONGO_STRING (the connection string you intend to use), i.e.
 
 ```
MONGO_STRING = 'mongodb://<dbuser>:<dbpassword>@ds127958.mlab.com:27958'
DATABASE = 'regulately'
REG_API_KEY = '<your_regulations_gov_api_key>'
 ```