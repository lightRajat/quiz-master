# Quiz Master

A multi-user app that lets users to attempt quizzes set by the admin.

## Technologies Used

1. `Vue` : as the frontend framework
2. `Flask` : as the backend server
3. `Sqlite` : as the database storage
4. `Bootstrap` : for styling the frontend

## Install Dependencies

### Backend

To install the required dependencies, run these commands

```bash
cd backend
pip install -r requirements.txt
```

### Frontend

To setup node and install required dependencies, run below commands

```bash
cd frontend
npm install
```

## Start Backend Server

Start a terminal session and go into the *backend/* folder first— `cd backend`

### Setup Instructions

1. **Initialize the Database** (Run once before using the app):

   ```bash
   python3 init.py
   ```

   - Creates an empty database scheme in *data/data.db*
   - Populate the database with sample data residing in *data/sample-data/*
   - Sets up the mail creds to be used for sending quiz reminders (*taken from the console*)

2. **Reset the Database** (to have a fresh backend from start):

   ```bash
   python reset.py
   ```
   
   This cleans the database and generated files.

### Start Server

After initializing the database with `init.py`, start the server:

```python
python3 server.py
```

### Combining Above Commands

You can also run `./reinit-server.sh` to run the above 3 commands together which **resets** the backend, **initializes** it again (enter mail-id & password), and starts the server again.

## Start Frontend Server

1. Start a new terminal session and go into the *frontend/* folder first— `cd frontend`
2. Then run `npm run dev` to start the `Vue.js` client.
3. Open the port on your localhost mentioned in the terminal by running the above command.