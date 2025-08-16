import uuid, time
from fastapi import FastAPI, Request, status
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .app import api_router
from .core.loggers import LoggerSingleton
from .core.utils import get_taken_time_in_milliseconds, error_object

# instantiating the logger
logger = LoggerSingleton.get_instance()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # task run at appication startup
    yield
    # release the resources
    

# Create the FastAPI app
app = FastAPI(lifespan=lifespan, docs_url="/docs", redoc_url="/redoc")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    err_obj = error_object(message=f"Invalid input: {exc.errors()}",
                            code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content=err_obj, status_code=err_obj["error"]["code"])


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    # Check if the "X-Correlation-ID" header is passed
    request_id = request.headers.get("X-Correlation-ID")
    
    # If no X-Correlation-ID is passed, generate a new UUID
    if not request_id:
        request_id = str(uuid.uuid4())
    
    # Store the request_id in request.state to make it accessible in the route handler
    request.state.request_id = request_id
    
    start_time = time.time()
    # Log the incoming request along with the request_id for tracing
    logger.info(f"---------- Incoming request to {request.url.path} ----------", \
                    extra={"correlation_id": request_id, "taken_time_ms": None})
    
    # Proceed with the request processing
    response = await call_next(request)

    taken_time = get_taken_time_in_milliseconds(start_time)
    logger.info(f"---------- endpoint={request.url.path} is completed ---------- ", \
                    extra={"correlation_id": request_id, "taken_time_ms": taken_time})

    # Add the X-Correlation-ID header to the response
    response.headers["X-Correlation-ID"] = request_id
    
    return response


# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow the frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"], # "PUT", "DELETE"
    allow_headers=["*"],  # Allow all headers
)


# Include the router with the /api prefix
# Assuming api_router, cron_router, and another_router are already defined
routers = [
    (api_router, "/api")
]

# Iterate over the list of routers and include them
for router, prefix in routers:
    app.include_router(router, prefix=prefix)