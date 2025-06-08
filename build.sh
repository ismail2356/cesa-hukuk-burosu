#!/bin/bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_about_page
python manage.py createsu
