'''

Create an application that interfaces with the user via the CLI - prompt the user with a menu such as:

Please select from the following options (enter the number of the action you'd like to take):
1) Create a new account (POST)
2) View all your tasks (GET)
3) View your completed tasks (GET)
4) View only your incomplete tasks (GET)
5) Create a new task (POST)
6) Update an existing task (PATCH/PUT)
7) Delete a task (DELETE)

It is your responsibility to build out the application to handle all menu options above.

'''
def menu():
    while True:
        import requests
        from pprint import pprint
        base_url = "http://demo.codingnomads.co:8080/tasks_api/users"
        print("Please select from the following options:\n"
              "1) Create a new account\n"
              "2) View your First Name\n"
              "3) View your Last Name\n"
              "4) View only your email\n"
              "5) Create a new email\n"
              "6) Update your name\n"
              "7) Delete your info")
        selection = input()

        if selection == "1":
            x = input("First_name: ")
            y = input("Last_name: ")
            z = input("Email: ")
            body = {
                "first_name": x,
                "last_name": y,
                "email": z,
            }
            response = requests.post(base_url, json=body)
            print(response.status_code)
            break

        elif selection == "2":
            x = input("Type your email: ")
            user_email = {
                "email" : x
            }
            response = requests.get(base_url, params=user_email)
            info = (response.json())
            pprint(info['data'][0]['first_name'])
            break

        elif selection == "3":
            x = input("Type your email: ")
            user_email = {
                "email": x
            }
            response = requests.get(base_url, params=user_email)
            info = (response.json())
            pprint(info['data'][0]['last_name'])
            break

        elif selection == "4":
            x = input("Type your email: ")
            user_email = {"email": x}
            response = requests.get(base_url, params=user_email)
            info = (response.json())
            pprint(info['data'][0]['email'])
            break

        elif selection == "5":
            x = int(input("Type your id: "))
            z = input("first_name: ")
            a = input("last_name: ")
            y = input("Type your new email: ")
            updated_info = {
                "id": x,
                "first_name": z,
                "last_name": a,
                "email": y
            }
            response = requests.put(base_url, json=updated_info)
            print(response.status_code)
            response = requests.get(base_url, params=updated_info)
            info = (response.json())
            print(f"Your new email is: {info['data'][0]['email']}")
            break

        elif selection == "6":
            x = int(input("Type your id: "))
            z = input("Update your first name: ")
            a = input("last_name: ")
            y = input("Type your email: ")
            updated_name = {
                "id": x,
                "first_name": z,
                "last_name": a,
                "email": y
            }
            response = requests.put(base_url, json=updated_name)
            status = response.status_code

            if status == 200:
                print("Your first name has beeen updated.")

            response = requests.get(base_url, params=updated_name)
            info = (response.json())
            print(f"Your new email is: {info['data'][0]['email']}")
            break

        elif selection == "7":
            x = input("Type your id: ")
            response = requests.delete(base_url + "/"+x)
            print(response.status_code)
            response = requests.get(base_url)
            print(response.content)
            break

        else:
            print(f"{selection} is not a valid entry.")
            prompt = input('Would you like to try again? Type "Y" for yes or "N" for no: ').capitalize()
            if prompt == "Y":
                continue
            elif prompt == "N":
                print("Thank you for coming by. Good bye.")
                break
            else:
                print(f"{prompt} is not a valid entry. Please try again later.")
                break
menu()