# Unu - Api

**unu-api** is a REST Full API to manage the backend operations for Unu app.

## Installation
Clone this repository:

```
git clone git@github.com:debuggers-master/unu-api.git
```

## Seutup worksapce
If you want to contribute to this API, first you can make some configurations
to work correctly and according with our style code guide.

#### Create a virtual enviroment and install all dependencies
Run in the root directory:

```bash
python3 -m venv .env
source .env/bin/activate
pip3 install -r app/requirements.txt
pip3 install -r app/requirements.dev.txt
```

This step enable the correct function of the linter and preconfigured style code guides.

#### Set the enviroment variables
Go to the file named `app/.env.example` and rename to `app/.env`
After that fill all required env variables.
This step is totally needed.

#### Run the application
If you want to initialize the uvicorn server for development run in the root directory:

```bash
source scripts/dev.sh
```

This command initalize the server and reload on any change in the source code.

If you want to run for production, exec:

```bash
source scripts/start.sh
```

If you made any change in the Dockerfile or you added some new package in the requirements.txt file, you must run:

```bash
source scripts/build.sh
# And then
source scripts/dev.sh
```

## Api endpoints

BasePath: https://some_domai.com/api/v1

### Operations about users

**Register an user**:
- path: `/auth/signup`
- method: `POST`
- body
  - email: str
  - password: str
  - firstName: str
  - lastName: str

- response (201):
  - acces_token: str
  - type_token: str
  - user: obj - User data

**Login an user**:
- path: `/auth/login`
- method: `POST`
- body
  - email: str
  - password: str

- response (200):
  - access_token: str
  - type_token: str
  - user: obj - User data

**Update user info**:
- path: `/users`
- method: `PUT`
- body
  - userId: str
  - user_data: obj - The data for update

- response (200):
  - detail: {"modified_count": "1"}

**Delete user**:
- path: `/users`
- method: `DELETE`
- body
  - userId: str

- response (204):
  - empty

**Create a new organization**:
- path: `/users/organizations`
- method: `POST`
- body
  - name: str
  - description: str
  - userId: str

- response (201):
  - detail: {"organizationId": str}

**Update a organization**:
- path: `/users/organization`
- method: `PUT`
- body
  - userId: str
  - organizationId: str
  - organization_data: obj - The info for update

- response (200):
  - detail: {"modified_count": "1"}

**Delete a organization**:
- path: `/users/organization`
- method: `POST`
- body
  - ownerId: str
  - organizationId: str

- response (204):
  - empty

### Operations about events

**Retrieve event info**:
- path: `/events`
- method: `GET`
- query
  - eventId: str
  - filter: List[str] (optional)
  - exclude: List[str] (optional)

- response (200):
  - eventData: obj - The event info
    - if no querys -> Return all event info
    - if filter -> Return only the fields especified in filter list.
    - if exclude -> Return all info except the fileds in exclude list.

**Retrieve event info from url data**:
- path: `/events/getFromUrl`
- method: `GET`
- query
  - filter: List[str] (optional)
  - exclude: List[str] (optional)
- body:
  - organizationName: str
  - eventUrl: str

- response (200):
  - eventData: obj - The event info
    - if no querys -> Return all event info
    - if filter -> Return only the fields especified in filter list.
    - if exclude -> Return all info except the fileds in exclude list.

**Retrieve all publisehd events**:
- path: `/events/list`
- method: `GET`

- response (200):
  - publishedEvent: List[event]
  event = {"eventId": str, "name": str, "startDate": str, "url": url}

**Retrieve event info**:
- path: `/events`
- method: `POST`
- body:
  - url: str
  - name: str
  - startDate: str
  - template: str

- response (201):
  - detail: {"eventId": str}

**Update event minimun info**:
- path: `/events/minInfo`
- method: `PUT`
- body:
  - eventId: str
  - new_data: obj - The new data
- response (200):
  - detail: {"modified_count": int}

**Update event extra info**:
- path: `/events/extraInfo`
- method: `PUT`
- body:
  - eventId: str
  - new_data: obj - The new data
- response (200):
  - detail: {"modified_count": int}

**Update event collaborators info**:
- path: `/events/collaborators`
- method: `PUT`
- body:
  - eventId: str
  - collaboratorId: str
  - new_data: obj - The new data
- response (200):
  - detail: {"modified_count": int}

**Update event banner**:
- path: `/events/banners`
- method: `PUT`
- body:
  - eventId: str
  - new_data: obj - The new data
- response (200):
  - detail: {"modified_count": int}

**Update event speakers info**:
- path: `/events/speakers`
- method: `PUT`
- body:
  - eventId: str
  - speakerId: str
  - new_data: obj - The new data
- response (200):
  - detail: {"modified_count": int}

**Update event day info**:
- path: `/events/day`
- method: `PUT`
- body:
  - eventId: str
  - dayId: str
  - new_data: obj - The new data
- response (200):
  - detail: {"modified_count": int}

**Update event conference info**:
- path: `/events/conference`
- method: `PUT`
- body:
  - eventId: str
  - dayId: str
  - conferenceId: str
  - new_data: obj - The new data
- response (200):
  - detail: {"modified_count": int}

**Update event associates info**:
- path: `/events/associates`
- method: `PUT`
- body:
  - eventId: str
  - associatedId: str
  - new_data: obj - The new data
- response (200):
  - detail: {"modified_count": int}

**Update event publication status**:
- path: `/events/publicationStatus`
- method: `PUT`
- body:
  - eventId: str
- response (200):
  - detail: {"modified_count": int}

**Delete event**:
- path: `/events/`
- method: `DELETE`
- query:
  - event_field: (Enun)
    - all - Delete event
    - agenda - Delete all agenda
    - day - Delet a specific day
    - conference - Delete a especific conference
    - speakers - Delete a specific speaker
    - collaborator - Delete a specific collaborator
    - associates- Delete a specific assoicate

- body:
  - eventId: str
  - field_id: str
    - if all -> ""
    - if agenda -> ""
    - if day -> dayId
    - if conference -> conferenceId
    - if speakers -> speakerId
    - if collaborator -> collaboratorId
    - if associates -> associatedId

-reponse: (204)
  - empty

**Retrieve event info**:
- path: `/events/count-participants`
- method: `GET`
- query
  - eventId: str

- response (200):
  - detail: int - The total regitrated particpants


## Contributors

- [Emanuel Osorio](https://github.com/emanuelosva)

- [Mario barbosa](https://github.com/mariobarbosa777)
