# Nutrivore

Nutrivore API made with FastAPI

<hr/>

## Getting started

### 1. Installing dependencies 
- Dependencies are found in the `requirements.txt` file and should be installed into your environment.
- **venv** will be used to demonstrate. Run the command `Python -m venv env` to create the virtual environment. 
- Activate the virtual environment created and run the command `pip install -r requirements.txt` to install the requirements
> **Note**
> You need to create a copy of the `.env.example` and rename it to `.env` then add the mongoDB connection string to connect to the database

### 2.  Starting the server
- Start the server by running the command `uvicorn app.main:app`. This should start the api server at http://127.0.0.1:8000. You can change the port number with the flag `--port` e.g. `uvicorn app.main:app --port 8080`
- 
### 3.  Using the API
Once the server is running, you can view the api documentation by appending the following to the URL:
- `/docs` to view Swagger UI documentation 
>![image](https://user-images.githubusercontent.com/59659920/229376702-6425e10d-e193-4b37-aebe-55e743b23f49.png)

- `/redoc` to view ReDoc UI documentation
>![image](https://user-images.githubusercontent.com/59659920/229376777-c88dcaae-580e-46a5-b627-9876ef7f7f44.png)
