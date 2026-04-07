# Status Code:
'''
- http status code is used to help the client (the user or system submitting data to the server) to understand what happened on the server side application.
- Basically it allows for the user who submits his/her request to know if his submission was successfull or not .

1xx : “Request received, still processing”

2xx : Success
[GET] - 200 OK → Request successful
[POST]- 201 Created → New resource created (POST)
[PUT] - 204 No Content → Success but no response body

3xx :  Redirection 
 - 301 : Moved Permanently
 - 302 : Found

4xx : Client Error
 - 400 Bad Request → Wrong input
 - 401 Unauthorized → Not logged in
 - 403 Forbidden → No permission
 - 404 Not Found → Resource doesn’t exist
 - 422 Unprocessable Entity → Validation error 

5xx : Server Error
 - 500 Internal Server Error → Something broke
 - 502 Bad Gateway
 - 503 Service Unavailable
'''
