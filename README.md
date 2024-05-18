# Running the Application Locally
## Prerequisites
Before running the application, ensure you have the following installed on your local machine:

* Python 3.8+
* pip (Python package installer)

## Setup Instructions

### Install Dependencies:

Install the required dependencies using pip:
```
pip install -r requirements.txt
```

## Run the app

```
uvicorn main:app --reload
```

## API Endpoints
Here are the main API endpoints available in the application:

### Create Lead:

* Endpoint: POST /leads/
* Description: Create a new lead.
* Request Body:
```
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "resume": "Resume text or URL"
}
```

### Get Leads:

* Endpoint: GET /leads/
* Description: Retrieve a list of leads.
* Query Parameters: skip, limit

### Update Lead State:

* Endpoint: PUT /leads/{lead_id}
* Description: Update the state of a lead.
* Request Body:

```
{
  "state": "REACHED_OUT"
}

```


### Test the app 

## with curl 

### Create a lead 

```angular2html
curl -X POST "http://127.0.0.1:8000/leads/" -H "Content-Type: application/json" -d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "resume": "Resume text or URL"
}'
```

### Get leads 

```angular2html
curl -X GET "http://127.0.0.1:8000/leads/"
```

### Update a lead 

```angular2html
curl -X PUT "http://127.0.0.1:8000/leads/{lead_id}" -H "Content-Type: application/json" -d '{
  "state": "REACHED_OUT"
}'
```

## with FastAPI docs 

FastAPI provides docs with which the endpoints can be tested as well: `http://127.0.0.1:8000/docs`

## TO DO:

Several improvements can be made, eg. 

## Code structuring

Code could be structured in 

```angular2html
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── database.py
└── utils
    └── email.py
```

## API responses 

Api responses could be more detailed eg with 400 Bad Request and less detailed messages 

## Authentication 

Authentication should be added 