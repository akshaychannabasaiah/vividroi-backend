
from fastapi import FastAPI
from app.configuration.getConfig import Config
# routers
from app.routers import chatService, config, benchmark
from fastapi.middleware.cors import CORSMiddleware

# get the config file
configuration = Config()

API_ID = configuration.API_ID
API_VERSION = configuration.API_VERSION

# fastAPI Instance
app = FastAPI(
    title="Vivid ROI Backend (API ID: "
    + str(API_ID) + ")", docs_url="/", version=configuration.API_VERSION
)


origins = [
    "https://vividroi.azurewebsites.net",
    "https://vividroi-react.azurewebsites.net",
    "https://localhost",
    "https://localhost:41250",
    "https://localhost:8080",
    "https://localhost:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://127.0.0.1:5173",
    "https://vividroi.com",
    "https://www.vividroi.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include the routers
app.include_router(config.router)
app.include_router(benchmark.router)
app.include_router(chatService.router)


# needed to start the application locally for development/debugging purpose. Will never be called on K8s.
if configuration.is_local:
    import uvicorn
    if __name__ == '__main__':
        # if run locally, the port might already be in use, just use another one then.
        uvicorn.run(app, host='127.0.0.1', port=41250)
