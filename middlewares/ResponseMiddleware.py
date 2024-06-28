import json

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class ResponseMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Bypass middleware for documentation routes
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
            return await call_next(request)

        try:
            response = await call_next(request)

            # Attempt to parse response as JSON
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            try:
                response_json = json.loads(response_body.decode('utf-8'))
            except json.JSONDecodeError:
                # If the response is not JSON, return it as is
                return response

            if response.status_code == 200:
                formatted_response = response_json
            else:
                detail = response_json.get('detail', 'Unknown error')
                if isinstance(detail, str):
                    message = detail
                else:
                    message = f"{detail[0]['loc'][1]} {detail[0].get('msg', detail)}"

                formatted_response = {
                    "code": response.status_code,
                    "message": message
                }

            response = JSONResponse(status_code=response.status_code, content=formatted_response)
            return response

        except Exception as e:
            formatted_response = {
                "code": 500,
                "message": str(e)
            }
            response = JSONResponse(status_code=500, content=formatted_response)
            return response
