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

## API Documentation

### Endpoints

#### 1. Subjects

* **Endpoint:** `/subjects`
* **Method:** `GET`
* **Description:** Retrieves a list of all subjects.
* **Response:**
    * **Success (200 OK):**
        ```json
        {
          "subject": [
            {
              "id": 1,
              "name": "Mathematics",
              "description": "Fundamental mathematical concepts"
            },
            // ... more subjects
          ]
        }
        ```
        * **Explanation:** Returns a JSON object containing an array of subject objects. Each subject object includes its `id`, `name`, and `description`.

#### 2. Chapters

* **Endpoint:** `/chapters`
* **Method:** `GET`
* **Description:** Retrieves a list of chapters, optionally filtered by `subject_id`.
* **Query Parameters:**
    * `subject_id` (optional): Filters chapters by the specified subject ID.
* **Response:**
    * **Success (200 OK):**
        ```json
        {
          "chapters": [
            {
              "id": 1,
              "subject_id": 1,
              "name": "Algebra",
              "description": "Introduction to algebraic equations"
            },
            // ... more chapters
          ]
        }
        ```
        * **Explanation:** Returns a JSON object containing an array of chapter objects. Each chapter object includes its `id`, `subject_id`, `name`, and `description`. If `subject_id` is provided, only chapters belonging to that subject are returned. If no subject_id is provided, all chapters are returned.

#### 3. Questions

* **Endpoint:** `/questions`
* **Method:** `GET`
* **Description:** Retrieves a list of questions, optionally filtered by `chapter_id`.
* **Query Parameters:**
    * `chapter_id` (optional): Filters questions by the specified chapter ID.
* **Response:**
    * **Success (200 OK):**
        ```json
        {
          "questions": [
            {
              "id": 1,
              "chapter_id": 1,
              "question": "What is x if 2x + 5 = 11?",
              "option_a": "2",
              "option_b": "3",
              "option_c": "4",
              "option_d": "5",
              "correct_option": "b",
              "score": 1
            },
            // ... more questions
          ]
        }
        ```
        * **Explanation:** Returns a JSON object containing an array of question objects. Each question object includes its `id`, `chapter_id`, `question`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_option`, and `score`. If `chapter_id` is provided, only questions belonging to that chapter are returned. If no chapter_id is provided, all questions are returned.

#### 4. Quizzes

* **Endpoint:** `/quizzes`
* **Method:** `GET`
* **Description:** Retrieves a list of quizzes, optionally filtered by `chapter_id` or `subject_id` (but not both).
* **Query Parameters:**
    * `chapter_id` (optional): Filters quizzes by the specified chapter ID.
    * `subject_id` (optional): Filters quizzes by the specified subject ID.
* **Response:**
    * **Success (200 OK):**
        ```json
        {
          "quizzes": [
            {
              "id": 1,
              "scope": "Chapter",
              "chapter_id": 1,
              "subject_id": null,
              "time": 30,
              "description": "Algebra quiz"
            },
            // ... more quizzes
          ]
        }
        ```
        * **Explanation:** Returns a JSON object containing an array of quiz objects. Each quiz object includes its `id`, `scope`, `chapter_id`, `subject_id`, `time`, and `description`.
    * **Error (400 Bad Request):**
        ```json
        {
          "status": "failed",
          "info": "Provide only one filter: chapter_id or subject_id, but not both"
        }
        ```
        * **Explanation:** Returns an error if both `chapter_id` and `subject_id` are provided in the query parameters.

#### 5. Quiz Questions

* **Endpoint:** `/quiz-questions`
* **Method:** `GET`
* **Description:** Retrieves a list of quiz questions, optionally filtered by `quiz_id`.
* **Query Parameters:**
    * `quiz_id` (optional): Filters quiz questions by the specified quiz ID.
* **Response:**
    * **Success (200 OK):**
        ```json
        {
          "quiz_questions": [
            {
              "id": 1,
              "quiz_id": 1,
              "question_id": 1,
              "order": 1
            },
            // ... more quiz questions
          ]
        }
        ```
        * **Explanation:** Returns a JSON object containing an array of quiz question objects. Each quiz question object includes its `id`, `quiz_id`, `question_id`, and `order`.

#### 6. User Details

* **Endpoint:** `/user/<int:user_id>`
* **Method:** `GET`
* **Description:** Retrieves details of a specific user.
* **Path Parameters:**
    * `user_id` (integer): The ID of the user to retrieve.
* **Authentication:** Requires a valid JWT token.
* **Authorization:** Users can only access their own details, except for admins.
* **Response:**
    * **Success (200 OK):**
        ```json
        {
          "id": 1,
          "name": "John Doe",
          "email": "[email address removed]",
          "username": "johndoe",
          "date_joined": "2023-10-27",
          "profile_pic": "profile.jpg",
          "qualification": "Bachelors",
          "dob": "1990-01-01",
          "date_account_deleted": null
        }
        ```
        * **Explanation:** Returns a JSON object containing the user's details.
    * **Error (404 Not Found):**
        ```json
        {
          "status": "failed",
          "info": "User not found"
        }
        ```
        * **Explanation:** Returns an error if the user with the given ID does not exist.
    * **Error (403 Forbidden):**
        ```json
        {
          "status": "failed",
          "info": "not authorized"
        }
        ```
        * **Explanation:** Returns an error if a user tries to access another user's details without admin privileges.

#### 7. Quiz Attempts

* **Endpoint:** `/user/<int:user_id>/quiz-attempts`
* **Method:** `GET`
* **Description:** Retrieves quiz attempts for a specific user.
* **Path Parameters:**
    * `user_id` (integer): The ID of the user.
* **Authentication:** Requires a valid JWT token.
* **Authorization:** Users can only access their own quiz attempts, except for admins.
* **Response:**
    * **Success (200 OK):**
        ```json
        {
          "quiz_attempts": [
            {
              "id": 1,
              "quiz_id": 1,
              "date_attempted": "2023-10-27",
              "time_taken": 25,
              "score": 80
            },
            // ... more quiz attempts
          ]
        }
        ```
        * **Explanation:** Returns a JSON object containing an array of quiz attempt objects. Each quiz attempt object includes its `id`, `quiz_id`, `date_attempted`, `time_taken`, and `score`.
    * **Error (404 Not Found):**
        ```json
        {
          "status": "failed",
          "info": "User not found"
        }
        ```
        * **Explanation:** Returns an error if the user with the given ID does not exist.
    * **Error (403 Forbidden):**
        ```json
        {
          "status": "failed",
          "info": "Not authorized"
        }
        ```
        * **Explanation:** Returns an error if a user tries to access another user's quiz attempts without admin privileges.