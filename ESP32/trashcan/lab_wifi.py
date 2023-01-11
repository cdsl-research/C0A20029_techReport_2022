import webrepl
import network

wifi = ""
def lab_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    wifi.connect("CDSL-A910-11n", "11n-ky56$HDxgp")

    webrepl.start(password = "cdsl")

if __name__ == "__main__":
    lab_wifi()