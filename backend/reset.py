import os, shutil

# check if project already reset
if not os.path.exists('data/data.db'):
    exit(0)

# remove database
os.remove('data/data.db')

# remove pycache
shutil.rmtree('utils/__pycache__/')

# remove sample binary data
shutil.rmtree('data/profile-pics/')
os.mkdir('data/profile-pics')

# reset admin creds
creds = '''{\n\t"username": "admin",\n\t"password": "admin"\n}'''
with open("data/admin-creds.json", 'w') as f:
    f.write(creds)

print("Project reset!")