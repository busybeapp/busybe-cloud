from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

ALLOWED_ORIGINS = {
    "https://clear-slate-8b4de92f5776.herokuapp.com",
    "https://cloud.busybeapp.com",
    "https://app.busybeapp.com"
}


class CORSEnforcerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("Origin")

        # If Origin is provided but not in allowed list, return 403
        if origin and origin not in ALLOWED_ORIGINS:
            return JSONResponse(
                status_code=403,
                content={"detail": "CORS policy does not allow this origin"},
            )

        response = await call_next(request)

        # Only set CORS headers if the origin is allowed
        if origin in ALLOWED_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = \
                "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = \
                "Authorization, Content-Type"
            response.headers["Access-Control-Allow-Credentials"] = "true"

        return response
