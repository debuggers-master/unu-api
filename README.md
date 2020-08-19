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
Some awosem ressume documentation...

## Contributors
- [Emanuel Osorio](https://github.com/emanuelosva)
- [Mario barbosa](https://github.com/mariobarbosa777)
