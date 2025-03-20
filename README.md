# Quiz Master

It is a multi-user app (one requires an administrator and other users) that acts as an exam preparation site for multiple courses.

## Start Backend Server

Start a terminal session and go into the *backend/* folder first— `cd backend`

### Setup Instructions

1. **Initialize the Database** (Run once before using the app):

   ```bash
   python3 init.py
   ```

   - Creates an empty database scheme in *data/data.db*
   - Populate the database with sample data residing in *data/sample-data/*

2. **Reset the Database** (to clear all the project data):

   ```bash
   python reset.py
   ```
   
   This cleans the database for a fresh start.

### Start Server

After initializing the database with `init.py`, start the server by running below command:

```python
python3 app.py
```