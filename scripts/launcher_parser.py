import schedule
from datetime import datetime
from .parser import orders_check 
import time

def main():
    schedule.every(3).seconds.do(orders_check)
    while True:
        schedule.run_pending()

        # try:
        #     schedule.run_pending()
        # except Exception as e:
        #     cur_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

        #     with open("errors_parser.txt", "a") as f:
        #         f.write(f'Error time was at {cur_time}: ')
        #         f.write(f'{e}')
        #         f.write(2*'\n')

        #     time.sleep(120)
        #     main()

main()

