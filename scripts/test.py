from turbo_parser.models import Order
import time
# use command "python manage.py runscript test"
t=0

def run():
    orders = Order.objects.all()

    for i in orders:
        print(i)

    global t
    t=t+1
    print(t)

    time.sleep(5)
    run()

