import json
from datetime import date
from utils.models import User
import os

def get_admin_creds() -> dict:
    with open('data/admin-creds.json', 'r') as f:
        creds = json.load(f)
        return creds

def update_admin_password(passwd: str) -> None:
    creds = {
        'username': 'admin',
        'password': passwd,
    }
    with open('data/admin-creds.json', 'w') as f:
        json.dump(creds, f, indent=4)

def get_username_from_email(email: str) -> str:
    return email.split('@')[0]

def get_date_from_string(string) -> date:
    date_values = tuple(map(int, string.split('-')))
    date_object = date(date_values[0], date_values[1], date_values[2])
    return date_object

def save_profile_pic(profile, user):
    # delete existing profile if any
    for file in os.listdir('data/profile-pics'):
        user_id = int(file[:file.find('.')])
        if user_id == user.id:
            os.remove(f'data/profile-pics/{file}')
            break

    if '.' in profile.filename:
        extension = profile.filename[profile.filename.rfind('.') + 1:]
    else:
        extension = 'jpg'
    profile_name = f"{user.id}.{extension}"

    user.profile_pic = profile_name
    profile.save(f"data/profile-pics/{profile_name}")

def get(date) -> str:
    return str(date or '')