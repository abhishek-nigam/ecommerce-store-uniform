# eCommerce store for selling school uniforms

It provides a rich set of functionality for user visiting the website, to add view/search/add products to their carts and finally checkout.
<br>
It also provides an admin panel, using which new schools, uniforms, etc can be added, and existing ones can be managed.

### Dependencies
To run this project you need to install these packages/dependencies in your virtual environment(preferrably) using:
`pip install -r requirements.txt`

### Secrets
This project uses [Razorpay payment gateway](https://razorpay.com).
<br>
Make sure you add your keys and secrets in uniformhai/settings.py for payment functionalty to work.

### How to run:
  - Make sure you have created & activated your virtualenvironment, and installed the dependencies
  `virtualenv venv`
  `.\venv\Scripts\activate` for Windows or `source ./venv/Scripts/activate` or Linux and macOS
  `pip install -r requirements.txt`
  - Make migrations, and migrate
  `python manage.py makemigrations`
  - Migrate changes
  `python manage.py migrate`
  - Finally run server
  `python manage.py runserver`

### Trobleshooting
- If you're facing problems in making migrations after make changes to models or after pulling from GitHub, delete all files in migrations folder in your app, except `__init__.py`, and then tru to make migrations again. You can also try doing this and also deleting the database and then try making migrations, and migrate.

### Development
Want to contribute? Great! Fork me!

### License
MIT

### Say Hi
[Email: abhisheknigam1996@gmail.com](mailto://abhisheknigam1996@gmail.com)<br>
[LinkedIn](https://www.linkedin.com/in/abhishek-nigam25)

*last uplated: 30 July 2018*
