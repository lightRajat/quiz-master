import json
from datetime import date
from utils.models import User

def get_admin_creds() -> dict:
    with open('data/admin-creds.json', 'r') as f:
        creds = json.load(f)
        return creds

def get_username_from_email(email: str) -> str:
    return email.split('@')[0]

def get_date_from_string(string) -> date:
    date_values = tuple(map(int, string.split('-')))
    date_object = date(date_values[0], date_values[1], date_values[2])
    return date_object

def save_profile_pic(profile, user):
    if '.' in profile.filename:
        extension = profile.filename[profile.filename.rfind('.') + 1:]
    else:
        extension = 'jpg'
    
    last_user = User.query.order_by(User.id.desc()).first()
    
    if last_user:
        current_user_id = last_user.id + 1
    else:
        current_user_id = 1
    
    profile_name = f"{current_user_id}.{extension}"

    user.profile_pic = profile_name
    profile.save(f"data/profile-pics/{profile_name}")

def get(date) -> str:
    return str(date or '')