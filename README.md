# Restaurant Reservation Multi-tenant System

This Repo is a simple restaurant reservation backend solution. The system support multi-tenancy which means it can serve more than one restaurant. fastapi version of this [repository](https://github.com/IbrahimAdel/resturant-management)


## How to run
Copy the content of `sample.env` file into a new `.env` file.

if you have make command running you can run these two commands 
```bash
make start
make migrate-db
```
`migrate-db` must run in the first time to migrate the database to latest version.

if make is not installed you can replace the command with the following ones

```
docker-compose up -d
alembic upgrade head 
```
just make sure you installed the packages using `pip install -r requirements.txt` in the python env of the project before that.

the project's APIs will be available at [http://127:0:0:1:8000](http://127:0:0:1:8000)