# Forms
- Simple Forms Backend implementation identical to google forms.
- Post form submission features using pipeline architecture.

## Database Setup
- Using PostgreSQL.
- create a database named atlan using `create database atlan`.
- Add the connection string to env `postgresql://username:password@localhost/atlan`, replacing the username and password with their respective values.

## CodeBase Setup
- Download the code using `git clone https://github.com/bhavesh-20/Atlan-Challenge.git`
- **Or** Download the code using the zip file.
- cd to code-base root directory.
- Create virtual environment for python.
```
pip install virtualenv 
virtualenv venv
source venv/bin/activate #for linux
./venv/scripts/activate #for windows powershell.
pip install -r requirements.txt
```
- .env file: mention the database connection string and jwt secret token in .env. My .env is as follows
```
DATABASE_URI=postgresql://postgres:bhavesh@localhost/atlan
SECRET_KEY=DX7U8Y2RSELX1SWR1C2SNDB1QBF3K8MJM0322E6FE70BHAJ6PDI9EW3QK3BU01JNGRZK1A422UVA553GC4IJOIQHY2BXSVEYLNMK
```
- create database models. Run `python setup_db.py`. All the tables will be created on using the command.
- Migrations can be applied using alembic, but it won't be necessary unless you want to make changes to database models.
```
alembic init migrations
# do some configuration stuff on env.py in migrations folder created from above command
alembic revision --autogenerate
alembic upgrade head
```
- scripts folder contains helper scripts for formatting code etc. Code formatting using black, isort and autoflakes.
- Run the server using `python main.py` or `uvicorn main:app`
- Access Swagger API using `/docs` route.

## Demo Flow for google sheets workflow
- First create a user using the relevant metadata, email, username, mobile_number etc.
- Now Login using this user and create a form using `POST /form` endpoint which returns `form_id` as response if form creation is successful.
- Now using this `form_id` create questions for the form with relevant metadata question, is_required etc using the endpoint `POST /form/{form_id}/question`.
- Create multiple questions.
- In the background a google sheet will be created and shared with the user on form creation. And columns will be updated by questions when each question is being added.
- Now an anonymous user comes in and submits response to this form using the endpoint `POST /form/{form_id}/` using the payload 
```
{
    "user_mobile_number": "XXXXXXXXXX",
    "question_id1": "answer",
    "question_id2": "answer"
}
```
- Validation checks are done on the payload, such as, if a question is required and it is not given as the payload, the form response won't be submitted.
- On successful submission of the response, a pipeline consisting on two jobs, namely, GOOGLE_SHEETS and RECEIPT_SMS are created.
- The scheduler running in the background executes this pipeline and updates the google sheet and also sends the SMS to the user.
- SMS implementation not done, Simply prints the sms content in the console and also writes it in the log file.
- The pipelines can be monitored using the endpoints - `GET /pipeline/form/{form_id}?limit=10` and `GET /pipeline/{pipeline_id}`
- The pipelines write to the log file `log.txt` in the root directory which will be created if it does not exist automatically and can be uses to debug failing pipelines.
- The Routes are neatly documented in SWAGGER API that can be accessed using `/docs` route.
