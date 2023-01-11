import machine

t = machine.Timer(0)

def main():
    print("timer")

print("timer start")
t.init(period = 5000000, mode = t.ONE_SHOT, callback = lambda t:main())