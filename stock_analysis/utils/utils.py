from rest_framework.response import Response

def api_response(status_code=200, data=None):
    
    if status_code == 200:
        response = {
            "code": status_code,
            "message": 'Success',
            "data": data or {},
        }
    else:
        response = {
            "code": status_code,
            "message": 'Failed',
            "error": data or {},
        }
    return Response(response, status=status_code)