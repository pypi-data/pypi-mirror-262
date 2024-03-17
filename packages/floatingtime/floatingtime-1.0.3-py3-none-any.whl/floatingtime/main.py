import os
import schedule
import sys
import time
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from floatingtime.time_window import TimeWindow


def run_job():
    tw = TimeWindow()
    tw.show()


def run():
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        run_job()
        quit()

    # schedule.every().hour.at("29:55").do(run_job)
    schedule.every().hour.at("59:55").do(run_job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run()
