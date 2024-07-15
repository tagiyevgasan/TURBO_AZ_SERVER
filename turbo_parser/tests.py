from django.test import TestCase

# Create your tests here.
import time
# use command "python manage.py runscript test"
t=2

def run():

    # global t
    t=t+1
    print(t)


run()

