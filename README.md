# News Board Service With User Session Based Authentication
This pack of service contains:
## User Access Service
1. Register API (add user to database)
- `127.0.0.1:8000/register`
2. Login API (get user from database to create user session)
- `127.0.0.1:8000/login`
3. Logout API (delete session)
- `127.0.0.1:8000/logout`
## News Board Service
1. Add News API (Login Required)
- `127.0.0.1:8000/add-news`
2. Edit News API (Login Required)
- `127.0.0.1:8000/edit-news`
3. Delete News API (Login Required)
- `127.0.0.1:8000/delete-news`
4. Get All News API
- `127.0.0.1:8000/get-all-news`
5. Get News By Id API
- `127.0.0.1:8000/get-news-by-id`
6. Download File By Id API
- `127.0.0.1:8000/download-file-by-id`
## Prerequisite to running Gateway and Service
This service uses python, nameko, rabbitmq, redis, and mysql. I assume that you have everything installed on your local machine.
## Steps
1. Clone this repository.
2. Import .sql file from database folder into your local machine mysql database. There are two database to import in total, one for user access service and one for news board service.
3. Open 3 terminals.
4. `nameko run user_access.service` or `make run-user` for running user access service.
5. `nameko run news_board.service` or `make run-news` for running news board service.
6. `nameko run gateway.service` or `make run-gateway` for running gateway.
7. If you are using Postman to test an API, refer to postman folder to get sample request or import .json file into your Postman collection.