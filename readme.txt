Current dependencies listed in requirments.txt

Before running, please run these commands to ensure that environment's variables are all up to date with the project. (Can copy and paste the following commands in)

-----------

python -m venv api-env
api-env\Scripts\activate
pip install -r requirements.txt
set FLASK_APP=app 
set FLASK_ENV=development
flask db init
flask db migrate
flask db upgrade
flask run

-----------

Execute unit tests after by calling (in another instance of CMD):
Note that the unit tests take really long to complete (unitTest1 ~10-15s, unitTest2 ~30-60s)

-----------

api-env\Scripts\activate
python unitTest1.py
python unitTest2.py

-----------