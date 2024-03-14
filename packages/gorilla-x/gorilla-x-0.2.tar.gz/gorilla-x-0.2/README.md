# Gorilla-ex

## Overview

TODO

## Quick Setup

Install the required dependencies

```sh
pip3 install -r requirements.txt
```

**Rest API Dependencies**\
Mkcert to support OAuth2 token exchange [required for Slack Integration]

```sh
brew install mkcert
mkcert -install
mkcert localhost
```

Mkcert creates a local certificate authority, enabling Gorilla to establish secure communication for OAuth2 token exchange between localhost and interacting services. The command may prompt the user to pass in their password.

**Database Dependencies**  
Additional pip requirements are needed for database functionalities

```sh
pip3 install -r db_requirements.txt
```

See the sections below for specific database integrations.

## CLI Usage

Give authorizations and perform OAuth2 token exchanges with services Gorilla currently support

```sh
python3 cli.py -authorize <service_name>
```

Prompt Execution

```sh
#example: python3 cli.py -e send a slack message to @johndoe on slack
python3 cli.py -e <prompt>
```

List all commands Gorilla current supports and their usages

```sh
python3 cli.py -h OR python3 cli.py -help
```

## Database Setups

To test out database interactions locally, each database server requires its own setup

#### MySQL

- Install MySQL Server
  - For non-Mac, [install server here](https://dev.mysql.com/downloads/mysql/)
    - Make sure to add `mysql` to path!
  - Mac: Run `brew install mysql`
- Follow `.env.example` and create a `.env` in the root directory with your MySQL credentials (user, password, host)
- Import the example database using `demo/mysql_setup.py` by running:
  ```sh
  cd demo
  python3 mysql_setup.py <your_database_name>
  ```
- Then put the name you picked inside `.env` as the database name

### Filesystem / Database

- Uncomment the demo function for the desired system to test in `examples.py`
- Run
  ```sh
  python3 examples.py
  ```

## Credentials & Authorization Token
There are two types of credentials the user can add to the execution engine.  

1.) [**OAuth 2.0**](https://oauth.net/2/) 

Gorilla-ex follows the standard OAuth 2.0 token exchanges flow. Running the command below will redirect the user to the browser, where they will be prompted to grant permissions to Gorilla for a specific set of scopes.
```sh
  python3 cli.py -authorize <gmail, slack, discord>
```
After Gorilla-ex receives the token for a service, it will automatically be able to recognize the keyword in future prompts, enabling the user to perform actions on that particular platform. Additionally, the token will not be exposed to the LLM and will only be visible during execution.

We continually seek to expand our support for additional services. The authorization logic for each service resides in the authorization/scripts folder. We warmly welcome interested contributors to submit a pull request introducing a new authorization flow. **Your contributions are highly appreciated 🚀**

2.) **Raw API Key** 

If the user wants to add services not supported by OAuth2, they can do so by calling the function below with `service` and `key` as parameters:  
```sh 
python3 cli.py -insert_creds alpha_vantage {API_KEY}
```
The key will be stored in Gorilla-ex's secret store and passed on to the LLM during prompting.
