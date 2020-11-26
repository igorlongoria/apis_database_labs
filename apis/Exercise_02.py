'''
Building on the previous example, create a list of all of the emails of the users and print
the list to the console.

'''
import requests
from pprint import pprint
url = "http://demo.codingnomads.co:8080/tasks_api/users"
response = requests.get(url)

dict_ = response.json()
#pprint(dict_["data"][0]["email"])
#pprint(dict_["data"][2]["email"])
#for j in dict_.values():
#    x = j
#    print(type(x))
list_of_dicts = list(dict_.values())[0]
print(type(list_of_dicts))
list_emails = [i["email"] for i in list_of_dicts]
pprint(list_emails)