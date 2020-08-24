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
> Swagger: http://35.239.16.11/docs
> OpemApi: http://35.239.16.11/redoc

#### Url
**API-url**: http://35.239.16.11.com/api/v1

### Operations about users

**Register an user**:
- path: `/auth/signup`
- method: `POST`
- body: {
  email: `str`,
  password: `str`,
  firstName: `str`,
  lastName: `str`,
}

- response (201):
  - acces_token: `str`
  - type_token: `str`
  - user: obj - User data

**Login an user**:
- path: `/auth/login`
- method: `POST`
- body: {
  email: `str`,
  password: `str`,
}

- response (200):
  - access_token: `str`
  - type_token: `str`
  - user: obj - User data

**Update user info**:
- path: `/users`
- method: `PUT`
- body: {
  userId: `str`
  userData: {
    firstName: `str`,
    lastName: `str`,
    email: `str`,
  }
}

- response (200):
  - {"modifiedCount": int}

**Delete user**:
- path: `/users`
- method: `DELETE`
- body
  - userId: `str`

- response (204):
  - empty

### Operations about organizations

**Retrieve organization info**
- path: `/organizations`
- method: `GET`
- body: {
  organizationId: `str`
}

- response (200):
  - organization data

**Create a new organization**:
- path: `/organizations`
- method: `POST`
- body: {
  userId: `str`,
  organizationData: {
    name: `str`
  }
}

- response (201):
  - {"organizationId": `str`}

**Update a organization**:
- path: `/users/organization`
- method: `PUT`
- body: {
  userId: `str`
  organizationId: `str`
  organizationData: {
      name: `str`
  }
}

- response (200):
  - {"modifiedCount": "1"}

**Delete a organization**:
- path: `/users/organization`
- method: `DELETE`
- body: {
  userId: `str`,
  organizationId: `str`,
}

- response (204):
  - empty

### Operations about events

---------------------------------------------------------------------------

**Retrieve event info**:
- path: `/events`
- method: `GET`
- query
  - eventId: `str`
  - filters: List[`str`] (optional)
  - excludes: List[`str`] (optional)

- response (200):
  - eventData: obj - The event info
    - if no querys -> Return all event info
    - if filter -> Return only the fields especified in filter list.
    - if exclude -> Return all info except the fileds in exclude list.

**Retrieve event info from url data**:
- path: `/events/from-url`
- method: `GET`
- query
  - filters: List[`str`] (optional)
  - excludes: List[`str`] (optional)
- body: {
  organizationName: `str`
  eventUrl: `str`
}

- response (200):
  - eventData: obj - The event info
    - if no querys -> Return all event info
    - if filter -> Return only the fields especified in filter list.
    - if exclude -> Return all info except the fileds in exclude list.

**Retrieve all publisehd events**:
- path: `/events/list`
- method: `GET`

- response (200):
  - publishedEvent: List[
    {
      "eventId": `str`,
      "name": `str`,
      "startDate": `str`,
      "shortDescription": `str`
      "organization": `str`,
    },
    ...
  ]

**Return the number of registered participants**:
- path: `/events/count-participants`
- method: `GET`
- query
  - eventId: `str`

- response (200):
  - {"particpants": int }: int - The total regitrated particpants

---------------------------------------------------------------------------

**Create a new event**:
- path: `/events`
- method: `POST`
- body: {
  name: `str`,
  template: `str`,
  url: `str`,,
  startDate: `str`, - date
  organization: `str`,
}

- response (201):
  - detail: {"eventId": `str`}

**Update event info**:
(Complete all event info)
- path: `/events`
- method: `UPDATE`
- body:{
  eventId: `str`
  eventData: {
    name: `str`,
    shortDescription: `str`,
    description: `str`,
    imageHeader: `str`, - ecoded base64 image
    imageEvent: `str`, - ecoded base64 image
    localTime: `str` - eg. "GMT-5"
  }
}

**Delete a event**:
(Complete all event info)
- path: `/events`
- method: `DELETE`
- query:
  - eventId: `str`

---------------------------------------------------------------------------

**Add a collaborator to event**:
- path: `/events/collaborators`
- method: `POST`
- body: {
  eventId: `str`,
  collaboratorData: {
    firstName: `str`,
    lastName: `str`,
    email: `str`,
    password: `str`,
  }
}

- response (201):
  - {"collaboratorId": `str`}

**Add a existing collaborator to event**:
- path: `/events/collaborators`
- method: `POST`
- body: {
  email: `str`,
}

**Remove a collaborators from a event**:
- path: `/events/collaborators`
- method: `DELETE`
- body: {
  eventId: `str`,
  email: `str`,
}

- response (204):
  - empty

---------------------------------------------------------------------------

**Add a new associated**:
- path: `/events/associates`
- method: `POST`
- body: {
  eventId: `str`
  associatedData: {
    name: `str`,
    url: `str`,
    logo: `str`, - ecoded base64 image
  }
}
- response (200):
  - {"associatedId": `str`}

**Update event associates info**:
- path: `/events/associates`
- method: `PUT`
- body: {
  eventId: `str`,
  associatedId: `str`,
  associatedData: {
    name: `str`,
    url: `str`,
    logo: `str`, - ecoded base64 image
  }
}

- response (200):
  - {"modifiedCount": int}

**Delete a associated**:
- path: `/events/associates`
- method: `DELETE`
- body: {
  eventId: `str`,
  associatedId: `str`,
}

---------------------------------------------------------------------------

**Add event day**:
- path: `/events/day`
- method: `POST`
- body: {
  eventId: `str`,
  dayData: {
    date: `str`, - time
  }
}

- response (201):
  - {"dayId": `str`}

**Update a event day**:
- path: `/events/day`
- method: `PUT`
- body: {
  eventId: `str`,
  dayId: `str`,
  dayData: {
    date: `str`, - time
  }
}

- response (200):
  - detail: {"modifiedCount": int}

**Delete a event day**:
- path: `/events/day`
- method: `DELETE`
- body: {
  eventId: `str`,
  dayId: `str`,
}

- response (204):
  - empty

---------------------------------------------------------------------------

**Add a conference**:
- path: `/events/conference`
- method: `POST`
- body: {
  eventId: `str`
  dayId: `str`
  conferenceData: {
    name: `str`,
    description: `str`,
    startHour: `str`, - date
    endHour: `str` -  date
    speakerName: `str`,
    speakerBio: `str`,
    twitter: `str`,
    rol: `str`,
    photo: `str`,
  }
}

- response (201):
  - detail: {"conferenceId": int}

**Update a conference info**:
- path: `/events/conference`
- method: `PUT`
- body: {
  eventId: `str`,
  dayId: `str`,
  conferenceId: `str`
  conferenceData: {
    name: `str`,
    description: `str`,
    startHour: `str`, - date
    endHour: `str` -  date
    speakerName: `str`,
    speakerBio: `str`,
    twitter: `str`,
    rol: `str`,
    photo: `str`,
  }
}

- response (200):
  - detail: {"modifiedCount": int}

**Remove a conference**:
- path: `/events/conference`
- method: `DELETE`
- body: {
  eventId: `str`,
  dayId: `str`,
  conferenceId: `str`,
}

- response (204):
  - empty

---------------------------------------------------------------------------

**Update event publication status**:
- path: `/events/change-status`
- method: `PUT`
- body:
  - eventId: `str`
  - actualStatus: bool - The actual status
- response (200):
  - {"actualStatus": bool} - True if public, flase if private

---------------------------------------------------------------------------

### Models

**User**

```js
user: {
  _id: `ObjectId`,
  userId: `str`,
  email: `str`,
  firstName: `str`,
  lastName: `str`,
  password: `str`,
  organizations: [
    {
      organizationId: `str`,
      name: `str`,
    }
  ],
  myEvents: [
    {
      eventId: `str`,
      organization: `str`,
      name: `str`,
      shortDescription: `str`,
    }
  ],
  collaborations: [
    {
      eventId: `str`,
      organization: `str`,
      name: `str`,
      shortDescription: `str`,
    }
  ]
}
```

**Organization**

```js
organization: {
  _id: `ObjectId`,
  organizationId: `str`,
  name: `str`,
  organizationUrl: `str`,
  events: [
    {
      eventId: `str`,
      name: `str`,
    }
  ]
}
```

**Event**

```js
event: {
  _id: `ObjectId`,
  eventId: `str`,
  organizationId: `str`,
  organizationUrl: `str`, //Generated automatly
  name: `str`,
  url: `str`,
  startDate: `str`, // Date
  template: `str`,
  organization: `str`,
  localization: `str`, // eg. GTM-5
  shortDescription: `str`,
  description: `str`,
  imageHeader: `str`, - ecoded base64 image
  imageEvent: `str`, - ecoded base64 image
  localTime: `str` - eg. "GMT-5"
  speakers: [
    {
      speakerId: `str`,
      speakerName: `str`,
      speakerBio: `str`,
      twitter: `str`,
      rol: `str`,
      photo: `str`,
    }
  ],
  agenda: [
    {
      dayId: `str`,
      date: `str`, // Date
      conferences: [
        {
          conferenceId: `str`,
          name: `str`,
          description: `str`,
          startHour: `str`, - date
          endHour: `str` -  date
          speakerName: `str`,
          rol: `str`,
          photo: `str`,
        }
      ]
    }
  ],
  associates: [
    {
      name: `str`,
      url: `str`,
      logo: `str`, //url
    }
  ],
  collaborators: [
    {
      userId: `str`,
      name: `str`,
      email: `str`,
    }
  ],
  publicationStatus: Boolean // True if is accesible to all public
}

```

**Participants**

```js
participants: {
  eventId: `str`,
  emails: List[`str`],
}
```

## Contributors

- [Emanuel Osorio](https://github.com/emanuelosva)

- [Mario barbosa](https://github.com/mariobarbosa777)
