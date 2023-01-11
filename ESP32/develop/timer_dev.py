#from machine import Timer
import utime

def timer_dev():
    # tim = Timer(0)
    # tim.init(mode = Timer.ONE_SHOT, period = 50000000, callback = print("wake up"))
    utime.sleep(5)
    print("wakeup")

def main():
    while True:
        timer_dev()

if __name__ == "__main__":
    main()