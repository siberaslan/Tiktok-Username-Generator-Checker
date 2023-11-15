import requests
import random
import string
import pyfiglet
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

ascii_banner = pyfiglet.figlet_format("""Tiktok Username Checker Ekmeklikedi
""")
print(ascii_banner)

# Renkleri başlat
init()

def generate_random_username(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def check_username_availability(username):
    try:
        response = requests.get(f"https://www.tiktok.com/@{username}")
        if response.status_code == 200:
            print(f"{Fore.GREEN}[ + ] Username '@{username}' is available.{Style.RESET_ALL}")
            return username
        else:
            print(f"{Fore.GREEN}[ + ] Username '@{username}' is not available.{Style.RESET_ALL}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"{Fore.GREEN}[ + ] An error occurred: {str(e)}{Style.RESET_ALL}")
        return None

def save_available_usernames(available_usernames):
    with open("available_usernames.txt", "a") as file:
        for username in available_usernames:
            if username:
                file.write(f"{username}\n")

def main():
    try:
        username_length = int(input(f"{Fore.GREEN}[ + ] How many characters should the username have? {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.GREEN}[ + ] You did not enter a valid number. Defaulting to checking 10 usernames with 5 threads.{Style.RESET_ALL}")
        username_length = 4

    try:
        num_usernames = int(input(f"{Fore.GREEN}[ + ] How many usernames do you want to generate and check? {Style.RESET_ALL}"))
        num_threads = int(input(f"{Fore.GREEN}[ + ] How many threads do you want to use? {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.GREEN}[ + ] You did not enter valid numbers. Defaulting to checking 10 usernames with 5 threads.{Style.RESET_ALL}")
        num_usernames = 10
        num_threads = 5

    usernames = [generate_random_username(username_length) for _ in range(num_usernames)]
    available_usernames = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(check_username_availability, username) for username in usernames]

    for future in futures:
        result = future.result()
        if result:
            available_usernames.append(result)

    save_available_usernames(available_usernames)

if __name__ == "__main__":
    main()
