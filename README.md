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

#### Complete documentation

> Swagger: https://unu-api.tk/docs

> OpenApi: https://unu-api.tk/redoc

### Url
**base_path**: `https://unu-api.tk/api/v1`
* auth routes use the base root `/`

### Authorization
All routes excpet `auth/login` & `auth/signup` require the Authorization header.

```
headers: {Authorization: `Bearer {acces_token}`}
```

### Operations about users

**Register an user**:
- path: `/auth/signup`
- method: `POST`
- body:
```
{
  email: str,
  password: str,
  firstName: str,
  lastName: str,
}
```

- response (201):
```
{  
  acces_token: str
  type_token: str
  user: obj // User data
}
```

**Login an user**:
- path: `/auth/login`
- method: `POST`
- body:
```
{
  email: str,
  password: str,
}
```

- response (200):
```
{  
  acces_token: str
  type_token: str
  user: obj // User data
}
```

**Update user info**:
- path: `/users`
- method: `PUT`
- body:
```
{
  userId: str
  userData: {
    firstName: str,
    lastName: str,
    email: str,
  }
}
```

- response (200):
  - `{modifiedCount: int}`

**Delete user**:
- path: `/users`
- method: `DELETE`
- query:
  - userId: str

- response (204):
  - `empty`

### Operations about organizations

**Retrieve organization info**
- path: `/organizations`
- method: `GET`
- query:
  - organizationId: str

- response (200):
  - organization data

**Create a new organization**:
- path: `/organizations`
- method: `POST`
- body:
```
{
  userId: str,
  organizationData: {
    organizationName: str,
    organizationLogo: str,
  }
}
```

- response (201):
  - `{"organizationId": str}`

**Update a organization**:
- path: `/users/organization`
- method: `PUT`
- body: 
```
{
  userId: str
  organizationData: {
    organizationId: str
    organizationName: str,
    organizationLogo: str,
  }
}
```

- response (200):
  - `{modifiedCount: int}`

**Delete a organization**:
- path: `/users/organization`
- method: `DELETE`
- body:
```
{
  userId: str,
  organizationId: str,
}
```

- response (204):
  - `empty`

### Operations about events

---------------------------------------------------------------------------

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
  - organizationName: str,
  - url: str, (The event url)
  - filters: List[str] (optional)
  - excludes: List[str] (optional)

- response (200):
  - eventData: obj - The event info
    - if no querys -> Return all event info
    - if filter -> Return only the fields especified in filter list.
    - if exclude -> Return all info except the fileds in exclude list.

**Retrieve all publisehd events**:
- path: `/events/list`
- method: `GET`

- response (200):
  - publishedEvents:
  ```
  List[
    {
      "eventId": str,
      "name": str,
      "startDate": str,
      "shortDescription": str
      "organizationName": str,
      "publicationStatus": str,
      "imageEvent": str,
    },
    ...
  ]
  ```

**Return the number of registered participants**:
- path: `/events/count-participants`
- method: `GET`
- query
  - eventId: str

- response (200):
  - `{"particpants": int }` - int -> The total regitrated particpants

---------------------------------------------------------------------------

**Create a new event**:
- path: `/events`
- method: `POST`
- body:
```
{
  name: str,
  template: str,
  url: str,
  startDate: str, - date
  organizationName: str,
}
```

- response (201):
  - `{"eventId": str}`

**Update event info**:
(Complete all event info)
- path: `/events`
- method: `UPDATE`
- body:
```
{
  eventId: str
  eventData: {
    name: str,
    shortDescription: str,
    description: str,
    titleHeader: str,
    imageHeader: str, - ecoded base64 image
    imageEvent: str, - ecoded base64 image
    localTime: str - eg. "UTC-5"
  }
}
```

- response (200):
  - `{"modifiedCount": int}`

**Delete all event**:
- path: `/events`
- method: `DELETE`
- query:
  - eventId: str

- response (204):
  - `empty`

---------------------------------------------------------------------------

**Add a collaborator to event**:
- path: `/events/collaborators`
- method: `POST`
- body:
```
{
  eventId: str,
  collaboratorData: {
    firstName: str,
    lastName: str,
    email: str,
    password: str,
  }
}
```

- response (201):
  - `{"collaboratorId": str}`

**Add a existing collaborator to event**:
- path: `/events/collaborators?existing=True`
- method: `POST`
- body: {
    eventId: str,
    email: str,
}

**Remove a collaborators from a event**:
- path: `/events/collaborators`
- method: `DELETE`
- body: 
```
{
  eventId: str,
  email: str,
}
```

- response (204):
  - `empty`

---------------------------------------------------------------------------

**Add a new associated**:
- path: `/events/associates`
- method: `POST`
- body:
```
{
  eventId: str
  associatedData: {
    name: str,
    url: str,
    logo: str, - ecoded base64 image
  }
}
```
- response (201):
  - `{"associatedId": str}`

**Update event associates info**:
- path: `/events/associates`
- method: `PUT`
- body:
```
{
  eventId: str,
  associatedData: {
    associatedId: str,
    name: str,
    url: str,
    logo: str, - ecoded base64 image
  }
}
```

- response (200):
  - `{modifiedCount: int}`

**Delete a associated**:
- path: `/events/associates`
- method: `DELETE`
- body:
```
{
  eventId: str,
  associatedId: str,
}
```

- response (204):
  - `empty`

---------------------------------------------------------------------------

**Add event day**:
- path: `/events/day`
- method: `POST`
- body:
```
{
  eventId: str,
  dayData: {
    date: str, - time
  }
}
```

- response (201):
  - {"dayId": str}

**Update a event day**:
- path: `/events/day`
- method: `PUT`
- body:
```
{
  eventId: str,
  dayData: {
    dayId: str,
    date: str, - time
  }
}
```

- response (200):
  - `{modifiedCount: int}`

**Delete a event day**:
- path: `/events/day`
- method: `DELETE`
- body:
```
{
  eventId: str,
  dayId: str,
}
```

- response (204):
  - `empty`

---------------------------------------------------------------------------

**Add a conference**:
- path: `/events/conference`
- method: `POST`
- body:
```
{
  eventId: str
  dayId: str
  conferenceData: {
    name: str,
    description: str,
    startHour: str, - date
    endHour: str -  date
    speakerName: str,
    speakerBio: str,
    twitter: str,
    rol: str,
    speakerPhoto: str, - ecoded base64 image
  }
}
```

- response (201):
  - `{"conferenceId": int}`

**Update a conference info**:
- path: `/events/conference`
- method: `PUT`
- body:
```
{
  eventId: str,
  dayId: str,
  conferenceData: {
    conferenceId: str
    name: str,
    description: str,
    startHour: str, - date
    endHour: str -  date
    speakerName: str,
    speakerBio: str,
    twitter: str,
    rol: str,
    speakerPhoto: str,
    speakerId: str
  }
}
```

- response (200):
  - `{modifiedCount: int}`

**Remove a conference**:
- path: `/events/conference`
- method: `DELETE`
- body:
```
{
  eventId: str,
  dayId: str,
  conferenceId: str,
  speakerId: str,
}
```

- response (204):
  - `empty`

---------------------------------------------------------------------------

**Update event publication status**:
- path: `/events/change-status`
- method: `PUT`
- body:
```
{
  eventId: str
  actualStatus: Boolean // The actual status
}
```
- response (200):
  - `{"actualStatus": bool}` - True if public, flase if private

---------------------------------------------------------------------------

### Models

**User**

```js
user: {
  _id: `ObjectId`,
  userId: str,
  email: str,
  firstName: str,
  lastName: str,
  password: str,
  organizations: [
    {
      organizationId: str,
      organizationName: str,
    }
  ],
  myEvents: [
    {
      eventId: str,
      organizationName: str,
      name: str,
      shortDescription: str,
    }
  ],
  collaborations: [
    {
      eventId: str,
      organizationName: str,
      name: str,
      shortDescription: str,
    }
  ]
}
```

**Organization**

```js
organization: {
  _id: `ObjectId`,
  organizationId: str,
  organizationName: str,
  organizationUrl: str,
  organizationLogo: str,
  events: [
    {
      eventId: str,
      name: str,
    }
  ]
}
```

**Event**

```js
event: {
  _id: `ObjectId`,
  eventId: str,
  organizationId: str,
  organizationUrl: str, //Generated automatly
  organizationName: str,
  name: str,
  url: str,
  startDate: str, // Date
  template: str,
  titleHeader: str,
  shortDescription: str,
  description: str,
  imageHeader: str, - ecoded base64 image
  imageEvent: str, - ecoded base64 image
  localTime: str - eg. "UTC-5"
  speakers: [
    {
      speakerId: str,
      speakerName: str,
      speakerBio: str,
      twitter: str,
      rol: str,
      speakerPhoto: str,
    }
  ],
  agenda: [
    {
      dayId: str,
      date: str, // Date
      conferences: [
        {
          name: str,
          description: str,
          startHour: str,
          endHour: str,
          conferenceId: str,
          speakerName: str,
          speakerBio: str,
          twitter: str,
          rol: str,
          speakerPhoto: str,
          speakerId: str
        }
      ]
    }
  ],
  associates: [
    {
      name: str,
      url: str,
      logo: str, //url
      associatedId: str,
    }
  ],
  collaborators: [
    {
    email: str,
    firstName: str,
    lastName: str,
    }
  ],
  publicationStatus: Boolean // True if is accesible to all public
}

```

**Participants**

```js
participants: {
  eventId: str,
  emails: List[str],
}
```

## Contributors

- [Emanuel Osorio](https://github.com/emanuelosva)

- [Mario barbosa](https://github.com/mariobarbosa777)
