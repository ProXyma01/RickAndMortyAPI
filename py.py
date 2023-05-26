import requests
import json
import os
import pandas as pd
from win10toast import ToastNotifier

url = 'https://rickandmortyapi.com/api/'




def save_to_json(data, filename): ## json ფიალში სულ ბოლოს ხელით არის დასამატებელი ]-სიმბოლო
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode) as file:
        if mode == 'w':
            file.write('[')
        elif mode == 'a':
            file.write(',\n')
        json.dump(data, file, indent=4)

def main_request(baseur, endpoint):
    r = requests.get(baseur + endpoint)
    return r.json()

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code)
        return []

data = fetch_data(url)

if data:
    df = pd.DataFrame(data, index=[1])
    table_name = str(input("Enter the table name to save the data: "))
    df.to_csv(f"{table_name}.csv", index=True)
    print("Data saved successfully!")
    toaster = ToastNotifier()
    notification_text = "Data fetched from API and saved to CSV successfully."
    toaster.show_toast("API Data Notification", notification_text, duration=10)

else:
    print("No data fetched from the API.")


while True:
    endpoint = str(input("Choose: episode, character, location or c to check api status  (q to quit): "))
    data = main_request(url, endpoint)
    if endpoint.lower() == 'c':
        response = requests.get(url)
        print("API status code:", response.status_code)
        continue 
    elif endpoint.lower() == 'episode':
        res = str(input("\nType [pages] to see number of pages or Choose nth number of episode [0-19] (q to quit): "))
        x = res
        if res.lower() == 'pages':
            print(data['info'][res])
            continue
        elif res.lower() == 'q':
            break
        elif int(x) <= 19:
            print(data['results'][int(res)])
            save = str(input("Enter file name to save the info or [c] to continue (q to quit): "))
            if save.lower() == 'c': 
                res2 = str(input("Type len to show how many characters played in this episode (q to quit): "))
                if res2.lower() == 'len':
                    print(len(data['results'][int(res)]['characters']))
                    continue
                elif res2.lower() == 'q':
                    break
                print("Invalid Input")
                continue
            elif save.lower() == 'q':
                break
            save_to_json(data['results'][int(res)], save)
            print(f"Json data saved to [{save}]")
            continue
        print("Invalid input")
        continue
    elif endpoint.lower() == 'character':
        res = str(input("\nType [count] to see number of characters or Choose id [0-19] to show character info (q to quit): "))
        x = res
        if res.lower() == 'count':
            print(data['info'][res])
            continue
        elif res.lower() == 'q':
            break
        elif int(x) <= 19:
            print(data['results'][int(res)])
            save = str(input("Enter file name to save the info or [c] to continue (q to quit): "))
            if save.lower() == 'c': 
                res2 = str(input("Type len to show how many episodes this character takes part (q to quit): "))
                if res2.lower() == 'len':
                    print(len(data['results'][int(res)]['episode']))
                    continue
                elif res2.lower() == 'q':
                    break
                print("Invalid Input")
                continue
            elif save.lower() == 'q':
                break
            save_to_json(data['results'][int(res)], save)
            print(f"Json data saved to [{save}]")
            continue
        print("Invalid Input")
        continue
    elif endpoint.lower() == 'location':
        res = str(input("\nType [count] to see number of locations or Choose id [0-19] to show location info (q to quit): "))
        x = res
        if res.lower() == 'count':
            print(data['info'][res])
            continue
        elif res.lower() == 'q':
            break
        elif int(x) <= 19:
            print(data['results'][int(res)])
            save = str(input("Enter file name to save the info or [c] to continue (q to quit): "))
            if save.lower() == 'c': 
                res2 = str(input("Type len to show how many residents this location have (q to quit): "))
                if res2.lower() == 'len':
                    print(len(data['results'][int(res)]['residents']))
                    continue
                elif res2.lower() == 'q':
                    break
                print("Invalid Input")
                continue
            elif save.lower() == 'q':
                break
            save_to_json(data['results'][int(res)], save)
            print(f"Json data saved to [{save}]")
            continue
    elif endpoint.lower() == 'q':
        break
    print("Invalid Input")
    continue