import urequests

url = "http://192.168.100.51:5000/test?motorcycle="

data ="23.2"

url += data

# data = {
#     "motorcycle" : "H2fromesp"
# }

res = urequests.get(
    url
)

print(res)
res.close()