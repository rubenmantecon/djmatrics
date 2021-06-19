# djmatrics
Matrics Reloaded! FOSS that allows new students and the school's Administration to manage their enrollment process via web and mobile.

I understand why Laravel is such a popular framework, but **Django > Laravel**. Must be because *[Python doesn't suck balls](https://blog.codinghorror.com/the-php-singularity/).*

Please see the [matrics-app repo](https://github.com/AWS2/matrics-app/tree/dev) for the mobile version.

## Setup
### Prerequisites
- Python 3
- Pip

Clone and `cd` into the repo. Then set up the virtual environment.

### Virtual environment
You will need to set up a Python virtual environment. I like setting up a `.virtualenvs` folder and sourcing from there:

```
python3 -m venv ~/.virtualenvs/matrics

source ~/.virtualenvs/matrics/bin/activate

pip install -r requirements.txt
```

 If you are interested on differences between `venv` and `virtualenv`, see [here](https://stackoverflow.com/questions/44091886/whats-the-difference-between-virtualenv-and-m-venv-in-creating-virtual-env).


### Create a superuser
This one is a Django's default, but it will come in handy:
```
./manage.py createsuperuser
```

### Populate the database
There are multiple commands available for populating the database. Please refer to `core/management/commands`.
Some of relevance are shown. Remember that they are executed with `./manage.py`:

- `create_users`
- `import_enrolments <path/to/csv>`
- `populate_DB`

### Run a development server
`./manage.py runserver`

## API
### Login posibilities

*Standard Login*

endpoint: api/token : POST
pass: Email (email) and Password (password) as form-data
recieve: 
{
    Token: Token key,
    StatusEnrolment: Gets the status of the enrolment,
    BoolWizard: true || false (if the user has already completed the wizard checks as true, if not, false),
    UserId: The id of the user, to be used later for the autologin
}


*AutoLogin*

endpoint: api/verify : GET
pass: UserId (UID) and Token (Authorization) as headers
recieve: true || false (depends if the token still exists and belongs to the same user)



*Update Wizard*

endpoint: api/updatewizard : POST
pass: Token (Authorization) as header
recieve: nothing


*Get Wizard*

endpoint: api/getwizard : GET
pass: Token (Authorization) as header
recieve:
{
    image_rights: true || false
    excursions: true || false
    extracurricular: true || false
}


*Get Requirement Status*

endpoint: api/getreqstatus : GET
pass: Token (Authorization) as header
recieve:
{
    Id of requirements: state of those requirements,
}


*User Info*

endpoint: api/user : GET
pass: Token (Authorization) as header
recieve:
{
    Username: info,
    First name: info,
    Lastname: info,
    DNI: info,
    Birthplace: info,
    Birthday: info,
    Address: info,
    City: info,
    Postal Code: info,
    Phone number: info,
    Emergency number: info
}


*Profile and requirements*

endpoint: api/profileandrequirements : GET
pass: Token (Authorization) as header
recieve:
{
    Name: Name of the profile requirements,
    Description: A brief description of the profile of requirement,
    Type: Type of profile,
    Requirements: { 
        Id of the requirements: Name of the requirement,
    }
}


*Profiles and requirements*

endpoint: api/profilesandrequirements : GET
pass: Token (Authorization) as header
recieve:
{
    Id of the profile of requirements: {
        Name: Name of the profile requirements,
        Description: A brief description of the profile of requirement,
        Type: Type of profile,
        Requirements: [ 
           Name of the requirement,
        ]
    },
}


*Upload Requirements*

endpoint: api/uploadreq : POST
pass: Token (Authorization) as header
recieve:
{
    name: Name of the career
    code: Code of the career
    desc: Description of the career
    hours: How long is the career
    start: When it starts
    end: When it ends
    modules: {
        ID of MP: {
            id: ID of the MP,
            name: Name of the MP,
            code: Code of the MP,
            desc: Description of the MP,
            ufs: {
                ID of UF {
                    id: ID of the UF,
                    name: Name of the UF,
                    code: Code of the UF,
                    desc: Description of the UF
                },
            }
        },
    }
}


*Upload Requirements*

endpoint: api/uploadreq : POST
pass: Token (Authorization) as header and JSON { Id of the requirement: Document at base 64 }
recieve: Nothing

