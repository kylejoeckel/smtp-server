
# Email SMTP Server

General email smtp server for sending emails such as a contact form

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them. For example:

- Python 3.8+
- Serverless Framework
- Any other dependencies

```bash
npm install -g serverless
```

### Installing

A step-by-step series of examples that tell you how to get a development environment running.

1. Clone the repository

```bash
git clone https://yourrepositorylink.com
cd your-project-directory
```

2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required Python packages

```bash
pip install -r requirements.txt
```

4. Set up environment variables

Copy the `.env.example` to `.env` and adjust the values to match your setup.

```bash
cp .env.example .env
```

## Deployment

Instructions on how to deploy the project on a live system. This could vary widely between Serverless applications, but a general approach would be:

```bash
serverless deploy
```

### Unit Tests

To run unit tests, you can use the following command:

```bash
python -m unittest discover tests
```

Or to run a specific test file:

```bash
python -m unittest tests/test_email_functions.py
```

## Usage

```python
# Example of using the API to send an email
import requests

response = requests.post("https://your-api-endpoint.com/send_email", json={
    "from_address": "sender@example.com",
    "to_address": "recipient@example.com",
    "subject": "Hello",
    "body": "Hello, world!",
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "smtp_username": "user",
    "smtp_password": "password"
})

print(response.json())
```

## Built With

List the major frameworks/libraries used to bootstrap your project. For example:

- [Serverless Framework](https://www.serverless.com/) - The web framework used
- [Python](https://python.org/) - Programming language

## Authors

* **Kyle Joeckel** - *Initial work* - [kylejoeckel](https://github.com/kylejoeckel)

