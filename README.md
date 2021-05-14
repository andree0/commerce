about _Commerce_ project
-------------------------
**In this project used:** _Python 3.8, Django 3.2, SQLite3, postgresql, 
               Pillow, Faker, pytest, generic View, ModelForm_

This project contain _Auction_ app. \
The application is used to list items to the auction or bid on already exist auctions (after register and log in). \
You don't need to be logged in to view the auctions.


#heroku
This is url address to host my app on heroku: \
https://first-project-commerce.herokuapp.com/ \
You can click on link and use this app.

#docker
If You have docker, \
First, rename file _requirements.txt_ to for example _requirements_main.txt_, \
Second, rename file _requirements_docker.txt to _requirements.txt_. \
File __requirements.txt__ will to install for during create container docker.
This is necessary due to package conflicts.

After the docker container is created, \
You have to enter the container with the command `sudo docker exec -it [name your container] bash`, \
Next, You execute the command `python mange.py migrate` \
Next, You execute the command `python manage.py create_categories` . \
Now, You can to exit this container by pressing `Ctrl+C` \
and You can to run app with docker by command `sudo docker-compose up` . \
\
If all is right, You can restore previous file names.
