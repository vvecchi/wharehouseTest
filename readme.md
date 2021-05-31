Assuming you have docker installed and running, this app can be started running in the same folder as this readme file:
`docker-compose up`

This was made using Python Django, the django app can be found in the wharehouseWebApp, 
it connects to a PostgreSQL databse, the setup for the database is inside the `docker-compose.yml`.
The folder nginx has some settings for running a nginx container. 

To run tests from the `wharehouseWebApp`
folder run this command:
`python manage.py test --settings=wharehouseWebApp.settings_dev`

For this project with its times constraints, I didn't feel the need to go for a full backend and frontend decoupled services, 
instead going with a simpler MVC.