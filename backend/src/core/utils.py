from .loggers import LoggerSingleton
from datetime import datetime, timezone
import time

logger = LoggerSingleton.get_instance()


def error_object(request_id, message, code):
    if code==500:
        logger.exception(f"Exception occured={message}, status_code={code}", \
                         extra={"correlation_id": request_id, "taken_time_ms": None})
    else:
        logger.error(f"Error={message}, status_code={code}", \
                     extra={"correlation_id": request_id, "taken_time_ms": None})
    
    return {"error":{
            "code": code,
            "message": message
        }
    }

def get_current_utc_datetime(format="%Y-%m-%d %H:%M:%S"):
    # Get current datetime in UTC and format it
    return datetime.now(timezone.utc).strftime(format)

def get_taken_time_in_milliseconds(start_time: float) -> float:
    """Returns the time taken in milliseconds since the given start time."""
    # Get the current time
    end_time = time.time()
    # Calculate the elapsed time in seconds
    elapsed_time = end_time - start_time
    # Convert seconds to milliseconds (1 second = 1000 milliseconds)
    elapsed_time_ms = elapsed_time * 1000
    elapsed_time_ms = round(elapsed_time_ms, 2)
    return elapsed_time_ms