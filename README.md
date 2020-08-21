# Unu - Api

**unu-api** is a REST Full API to manage the backend operations for Unu app.

## Installation
Clone this repository:

```
git clone git@github.com:debuggers-master/unu-api.git
```

## Setup workspace
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

Docs: http://35.239.16.11/docs
BasePath: http://35.239.16.11.com/api/v1

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
  - userData: obj - The data for update

- response (200):
  - detail: {"modified_count": "1"}

**Delete user**:
- path: `/users`
- method: `DELETE`
- body
  - userId: str

- response (204):
  - empty

### Operations about organizations

**Retrieve organization info**
- path: `/organizations`
- method: `GET`
- body
  - organizationId: str

- response (200):
  - organization data

**Create a new organization**:
- path: `/organizations`
- method: `POST`
- body

  - userId: str
  - organizationData

- response (201):
  - detail: {"organizationId": str}

**Update a organization**:
- path: `/users/organization`
- method: `PUT`
- body
  - userId: str
  - organizationId: str
  - organizationData: obj - The info for update

- response (200):
  - detail: {"modifiedCount": "1"}

**Delete a organization**:
- path: `/users/organization`
- method: `POST`
- body
  - userId: str
  - organizationId: str

- response (204):
  - empty

### Operations about events

**Retrieve event info**:
- path: `/events`
- method: `GET`
- query
  - eventId: str
  - filters: List[str] (optional)
  - excludes: List[str] (optional)

- response (200):
  - eventData: obj - The event info
    - if no querys -> Return all event info
    - if filter -> Return only the fields especified in filter list.
    - if exclude -> Return all info except the fileds in exclude list.

**Retrieve event info from url data**:
- path: `/events/from-url`
- method: `GET`
- query
  - filters: List[str] (optional)
  - excludes: List[str] (optional)
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
  event = {"eventId": str, "name": str, "startDate": str, "organizationName": str}

**Return the number of registered participants**:
- path: `/events/count-participants`
- method: `GET`
- query
  - eventId: str

- response (200):
  - {"particpants": int }: int - The total regitrated particpants

**Create a new event**:
- path: `/events`
- method: `POST`
- body: (eventData)
  - url: str
  - name: str
  - startDate: str
  - template: str
  - shortDescription: str
  - description: str
  - banner: image
  - organizationName: str

- response (201):
  - detail: {"eventId": str}

**Add a collaborators to event**:
- path: `/events/collaborators`
- method: `POST`
- body:
  - eventId: str
  - collaboratorData: obj
- response (201):
  - {"collaboratorId": str}

**Add a new speaker**:
- path: `/events/speakers`
- method: `POST`
- body:
  - eventId: str
  - speakerData: obj
- response (201):
  - {"speakerId": str}

**Add a new associated**:
- path: `/events/associates`
- method: `POST`
- body:
  - eventId: str
  - associatedData: obj
- response (200):
  - {"associatedId": str}

-----------------------------------
**Add event day**:
- path: `/events/day`
- method: `POST`
- body:
  - eventId: str
  - dayId: str
  - new_data: obj - The new data
- response (200):
  - detail: {"modified_count": int}

**Add a conference**:
- path: `/events/conference`
- method: `POST`
- body:
  - eventId: str
  - dayId: str
  - conferenceId: str
  - new_data: obj - The new data
- response (200):
  - detail: {"modified_count": int}
---------------------------------------------

**Update event principal info**:
- path: `/events`
- method: `PUT`
- body:
  - eventId: str
  - newData: obj - The new data
- response (200):
  - {"modified_count": int}

**Update event collaborators info**:
- path: `/events/collaborators`
- method: `PUT`
- body:
  - eventId: str
  - collaboratorEmail: str
  - newData: obj - The new data
- response (200):
  - {"modified_count": int}

**Update event speakers info**:
- path: `/events/speakers`
- method: `PUT`
- body:
  - eventId: str
  - speakerId: str
  - newData: obj - The new data
- response (200):
  - {"modified_count": int}

**Update event associates info**:
- path: `/events/associates`
- method: `PUT`
- body:
  - eventId: str
  - associatedId: str
  - newData: obj - The new data
- response (200):
  - {"modified_count": int}

**Update event publication status**:
- path: `/events/change-status`
- method: `PUT`
- body:
  - eventId: str
  - actualStatus: bool - The actual status
- response (200):
  - {"actualStatus": bool} - True if public, flase if private

-----------------------------------
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
---------------------------------------------

**Delete event**:
- path: `/events/`
- method: `DELETE`
- query:
  - event_field: (Enun)
    - all - Delete all event
    - agenda - Delete all agenda
    - day - Delete a specific day
    - conference - Delete a especific conference
    - speakers - Delete a specific speaker
    - collaborator - Delete a specific collaborator
    - associates- Delete a specific assoicate

- body:
  - eventId: str
  - <fieldId>: str
    - if all -> None
    - if agenda -> None *
    - if day -> dayId: str *
    - if conference -> conferenceId: str *
    - if speakers -> speakerId: str
    - if collaborator -> collaboratorId: str
    - if associates -> associatedId: str

-reponse: (204)
  - empty


**Principal models**

```js
userData: {
  email: str
  firstName: str
  lastName: str
}
```

```js
organizationData: {
  name: str
  description: str
}
```

```js
eventData: {
  eventId: str,
  organizationId: str,
  organizationName: str, //Generated automatly
  url: str,
  name: str,
  startDate: Date,
  template: str,
  localization: str,
  banner: image,
  decription: str,
  shortDescription: str,
  collaborators: [],
  speakers: [],
  agenda: [],
  associates: [],
  publicationStatus: bool
}

```

```js
collaboratorData: {
  collaboratorId: str, // Generated automatly
  firstName: str,
  lastName: str,
  email: str,
  password: str,
}
```

```js
speakerData: {
    speakerId: str, // Generated automatly
    name: str,
    biography: str,
    twitter: url,
    photo: image,
  }
```

```js
associatedData: {
  speakerId: str, // Generated automatly
  name: str,
  url:url,
  logo: image,
  tag: str,
}
```

## Contributors

- [Emanuel Osorio](https://github.com/emanuelosva)

- [Mario barbosa](https://github.com/mariobarbosa777)
