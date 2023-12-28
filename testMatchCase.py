from datetime import datetime
from getRides import load_rides_from_file

ride_list = load_rides_from_file("rides.json")

print(ride_list)

# 'ProviderID': 'E4J3K2oCDgcCjJSe7Vn2yyV16yo1', 'UserID': '9z16DWF8JWMQ3ZaNqCYZnQ9Zl7n1'

def check_for_matches(ride_list, id_passenger, id_provider):

    today_str = datetime.now().strftime("%d/%m/%Y")
    print(today_str)
    for ride in ride_list:


        ride_date_str = ride['time'].split(' ')[0]
        print(ride_date_str)
        # If the ride date is not today, continue to the next iteration
        # Check if the current provider matches the given ID_PROVIDER
        if ride['provider'] == id_provider:
            if ride_date_str == today_str:
            # Check if ID_PASSENGER matches any in the list
                if id_passenger in ride['ride_passengers']:
                    return 1  # Match found
    return -1  # No match found


print(check_for_matches(ride_list, '9z16DWF8JWMQ3ZaNqCYZnQ9Zl7n1', 'E4J3K2oCDgcCjJSe7Vn2yyV16yo1'))