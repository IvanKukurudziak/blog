My Blog
=======

Installation & Running
======================

Requirements
------------

First requirements::

    git clone https://github.com/IvanKukurudziak/blog.git


create virtualenv::

    virtualenv -p python3 env
    . env/bin/activate


change dir and install requirements::

    cd blog
    pip install -r requirements.txt


run migrations::

    python manage.py migrate


run server::

    python manage.py runserver

