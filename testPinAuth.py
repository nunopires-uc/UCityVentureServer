from getRides import check_for_matches, load_rides_from_file

token = "7898+hb546ehn7e5j85e78jjn4+456g74h56h7we4h76weh764we+0"

PIN = token.split("+")[0]

ID_PASSENGER = token.split("+")[1]

ID_PROVIDER = token.split("+")[2]

STATUS = token.split("+")[3]


print("PIN: " + PIN)
print("ID_PASSENGER: " + ID_PASSENGER)
print("ID_PROVIDER: " + ID_PROVIDER)
print("STATUS: " + STATUS)


rides_list = load_rides_from_file('rides.json')


print(check_for_matches(rides_list, ID_PASSENGER, ID_PROVIDER))