# How To Setup Locally

To run the API locally follow the steps below. Before procedding ensure to install the package virtualenv globally using: `pip install virtualenv`

- Create a Virtual Environment(Ensure virtualenv has be installed globally)

  ```
      virtualenv .venv
  ```

- Activate Virtual Environment with

  ```
      source .venv/bin/activate
  ```

- Install dependencies

  ```
      pip install -r requirements.txt
  ```

- Setup Postgres Database

  - Create database
  - Create uuid_generate_v4 extension
  - Save database credentials

- Create .env file from env.sample:

  - If ENVIRONMENT is set as Production, set up Database Details (Postgres DB)
  - Else you can ignore it and only set values for and DEBU(Bool) and if you fancy API Tittle
  - Fill out the AWS CREDENTIALS found in env.sample
  - Do not forget other variables also

  ENVIRONMENT= If it isn't set to PRODUCTION, it defaults to LOCAL and uses SQLite instead of Postgres.

  DEBUG= Isn't used for now. It would determine if the API logs would be sys out (show on the Terminal). This would come to play when I fully configure logging.

- You can also run tests with:

  ```
      pytest
  ```

- You can then start Up API with

  ```
      uvicorn main:app --reload
  ```

## NOTE

- I dont have acess to the repo with the email service, so I couldn't pull that. I decided to comment out lines of code that involves sending out messags. The messages are instead logged out. This is especailly useful for creating and activating an account.

- The Swagger and Redoc Documntation can be found on the following urls:

### To view the current version (v.1.0) documentation

      - Swagger - http://127.0.0.1:8000/v1_0/docs
      - Redoc - http://127.0.0.1:8000/v1_0/redoc

### To view the available versions

- Swagger - <http://127.0.0.1:8000/docs>
- Redoc - <http://127.0.0.1:8000/redoc>
