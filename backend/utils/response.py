from fastapi.responses import JSONResponse


def success_response(data, message="success"):
    return {"success": True, "message": message, "data": data}


def error_response(message, status_code=500, error_type="error"):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {"type": error_type, "message": message},
        },
    )
