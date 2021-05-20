about _Commerce_ project
-------------------------
**In this project used:** _Python 3.8, Django 3.2, PostgreSQL, 
               Pillow, Faker, pytest, generic View, ModelForm_

This project contain _Auction_ app. \
The application is used to list items to the auction or bid on already exist auctions (after register and log in). \
You don't need to be logged in to view the auctions.


heroku
-------
This is url address to host my app on heroku: \
https://first-project-commerce.herokuapp.com/ \
You can click on link and use this app.

docker
--------
If You have docker, \
First, rename file **_requirements.txt_** to for example **_requirements_main.txt_**, \
Second, rename file **_requirements_docker.txt_** to **_requirements.txt_**. \
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

Screenshots
------------
View, when You no login \
![No login menu photo](https://github.com/andree0/commerce/blob/main/static/screenshots/no_login.png) \
\
View, when You login \
![Login menu photo](https://github.com/andree0/commerce/blob/main/static/screenshots/login.png) \
\
All auctions \
![All auctions photo](https://github.com/andree0/commerce/blob/main/static/screenshots/all_auction.png) \
\
Categories of auction \
![list of categories photo](https://github.com/andree0/commerce/blob/main/static/screenshots/categories.png) \
\
Index view \
![index view photo](https://github.com/andree0/commerce/blob/main/static/screenshots/index_view.png) \
\
View my auction \
![my auction photo](https://github.com/andree0/commerce/blob/main/static/screenshots/my_auctions.png) \
\
View somebody auction \
![somebody auction photo](https://github.com/andree0/commerce/blob/main/static/screenshots/somebody_auctions.png) \
\
View somebody closed auction \
![somebody auction closed photo](https://github.com/andree0/commerce/blob/main/static/screenshots/somebody-auction_closed.png) \
\
View my closed auction \
![my auction closed photo](https://github.com/andree0/commerce/blob/main/static/screenshots/my_auction_closed.png) \
\
View my won auction \
![my won auction photo](https://github.com/andree0/commerce/blob/main/static/screenshots/my_won_auction.png)
