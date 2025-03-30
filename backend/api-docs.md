## API Documentation

### Subjects

1.  **GET** `/subjects`

    * **Description:** Retrieves a list of all subjects.
    * **Parameters:** None.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "name": "Mathematics",
                        "description": "Fundamental mathematical concepts"
                    },
                    {
                        "id": 2,
                        "name": "Science",
                        "description": "Exploration of scientific principles"
                    }
                ],
                "info": "Resource Successfully Fetched"
            }
            ```
        * **200 OK (No results):**
            ```json
            {
                "status": "success",
                "data": [],
                "info": "No Resource Were Found"
            }
            ```

2.  **GET** `/subject/<int:id>`

    * **Description:** Retrieves a specific subject by ID.
    * **Parameters:**
        * `id` (integer): The ID of the subject.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": {
                    "id": 1,
                    "name": "Mathematics",
                    "description": "Fundamental mathematical concepts"
                },
                "info": "Resource Successfully Fetched"
            }
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```

3.  **POST** `/subjects`

    * **Description:** Creates a new subject.
    * **Parameters (form-data):**
        * `name` (string, required): The name of the subject.
        * `description` (string, optional): The description of the subject.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **201 Created:**
            ```json
            {
                "status": "success",
                "data": {
                    "id": 3,
                    "name": "History",
                    "description": "The study of past events"
                },
                "info": "Resource Created Successfully"
            }
            ```
        * **400 Bad Request:** (Invalid Foreign Key, Invalid Data)
            ```json
            {"status": "failed", "info": "Invalid Data"}
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **409 Conflict:** (Resource Already Exists)
            ```json
            {"status": "failed", "info": "Resource Already Exists"}
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

4.  **PUT** `/subject/<int:id>`

    * **Description:** Updates a subject by ID.
    * **Parameters (JSON):**
        * `name` (string, optional): The updated name of the subject.
        * `description` (string, optional): The updated description of the subject.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "info": "Resource Successfully Updated"
            }
            ```
        * **400 Bad Request:** (Invalid Foreign Key, Invalid Data)
            ```json
            {"status": "failed", "info": "Invalid Data"}
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```
        * **409 Conflict:** (Resource Already Exists)
            ```json
            {"status": "failed", "info": "Resource Already Exists"}
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

5.  **DELETE** `/subject/<int:id>`

    * **Description:** Deletes a subject by ID.
    * **Parameters:**
        * `id` (integer): The ID of the subject.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "info": "Resource Successfully Deleted"
            }
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```
        * **409 Conflict:** (Foreign Key Dependent)
            ```json
            {
                "status": "failed",
                "info": "Has Foreign Key Dependencies"
            }
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

### Chapters

1.  **GET** `/chapters`

    * **Description:** Retrieves a list of all chapters or chapters filtered by `subject_id`.
    * **Parameters:**
        * `subject_id` (integer, optional): Filters chapters by subject ID.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "subject_id": 1,
                        "name": "Chapter 1",
                        "description": "Introduction to chapter 1"
                    },
                    {
                        "id": 2,
                        "subject_id": 1,
                        "name": "Chapter 2",
                        "description": "Advanced topics in chapter 2"
                    }
                ],
                "info": "Resource Successfully Fetched"
            }
            ```
        * **200 OK (No results):**
            ```json
            {
                "status": "success",
                "data": [],
                "info": "No Resource Were Found"
            }
            ```

2.  **GET** `/chapter/<int:id>`

    * **Description:** Retrieves a specific chapter by ID.
    * **Parameters:**
        * `id` (integer): The ID of the chapter.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": {
                    "id": 1,
                    "subject_id": 1,
                    "name": "Chapter 1",
                    "description": "Introduction to chapter 1"
                },
                "info": "Resource Successfully Fetched"
            }
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```

3.  **POST** `/chapters`

    * **Description:** Creates a new chapter.
    * **Parameters (form-data):**
        * `subject_id` (integer, required): The ID of the associated subject.
        * `name` (string, required): The name of the chapter.
        * `description` (string, optional): The description of the chapter.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **201 Created:**
            ```json
            {
                "status": "success",
                "data": {
                    "id": 3,
                    "subject_id": 1,
                    "name": "New Chapter",
                    "description": "A newly created chapter"
                },
                "info": "Resource Created Successfully"
            }
            ```
        * **400 Bad Request:** (Invalid Foreign Key, Invalid Data)
            ```json
            {"status": "failed", "info": "Invalid Data"}
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **409 Conflict:** (Resource Already Exists)
            ```json
            {"status": "failed", "info": "Resource Already Exists"}
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

4.  **PUT** `/chapter/<int:id>`

    * **Description:** Updates a chapter by ID.
    * **Parameters (JSON):**
        * `subject_id` (integer, optional): The updated ID of the associated subject.
        * `name` (string, optional): The updated name of the chapter.
        * `description` (string, optional): The updated description of the chapter.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "info": "Resource Successfully Updated"
            }
            ```
        * **400 Bad Request:** (Invalid Foreign Key, Invalid Data)
            ```json
            {"status": "failed", "info": "Invalid Data"}
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```
        * **409 Conflict:** (Resource Already Exists)
            ```json
            {"status": "failed", "info": "Resource Already Exists"}
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

5.  **DELETE** `/chapter/<int:id>`

    * **Description:** Deletes a chapter by ID.
    * **Parameters:**
        * `id` (integer): The ID of the chapter.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "info": "Resource Successfully Deleted"
            }
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```
        * **409 Conflict:** (Foreign Key Dependent)
            ```json
            {
                "status": "failed",
                "info": "Has Foreign Key Dependencies"
            }
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

### Questions

1.  **GET** `/questions`

    * **Description:** Retrieves a list of all questions or questions filtered by `chapter_id`.
    * **Parameters:**
        * `chapter_id` (integer, optional): Filters questions by chapter ID.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "chapter_id": 1,
                        "question": "What is 2 + 2?",
                        "option_a": "3",
                        "option_b": "4",
                        "option_c": "5",
                        "option_d": "6",
                        "correct_option": "b",
                        "score": 1
                    },
                    {
                        "id": 2,
                        "chapter_id": 1,
                        "question": "What is the capital of France?",
                        "option_a": "London",
                        "option_b": "Berlin",
                        "option_c": "Paris",
                        "option_d": "Rome",
                        "correct_option": "c",
                        "score": 2
                    }
                ],
                "info": "Resource Successfully Fetched"
            }
            ```
        * **200 OK (No results):**
            ```json
            {
                "status": "success",
                "data": [],
                "info": "No Resource Were Found"
            }
            ```

2.  **GET** `/question/<int:id>`

    * **Description:** Retrieves a specific question by ID.
    * **Parameters:**
        * `id` (integer): The ID of the question.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": {
                    "id": 1,
                    "chapter_id": 1,
                    "question": "What is 2 + 2?",
                    "option_a": "3",
                    "option_b": "4",
                    "option_c": "5",
                    "option_d": "6",
                    "correct_option": "b",
                    "score": 1
                },
                "info": "Resource Successfully Fetched"
            }
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```

3.  **POST** `/questions`

    * **Description:** Creates a new question.
    * **Parameters (form-data):**
        * `chapter_id` (integer, required): The ID of the associated chapter.
        * `question` (string, required): The question text.
        * `option_a` (string, required): Option A.
        * `option_b` (string, required): Option B.
        * `option_c` (string, required): Option C.
        * `option_d` (string, required): Option D.
        * `correct_option` (string, required): The correct option (a, b, c, or d).
        * `score` (integer, required): The score for the question.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **201 Created:**
            ```json
            {
                "status": "success",
                "data": {
                    "id": 3,
                    "chapter_id": 1,
                    "question": "What is 3 * 3?",
                    "option_a": "6",
                    "option_b": "9",
                    "option_c": "12",
                    "option_d": "15",
                    "correct_option": "b",
                    "score": 1
                },
                "info": "Resource Created Successfully"
            }
            ```
        * **400 Bad Request:** (Invalid Foreign Key, Invalid Data)
            ```json
            {"status": "failed", "info": "Invalid Data"}
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **409 Conflict:** (Resource Already Exists)
            ```json
            {"status": "failed", "info": "Resource Already Exists"}
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

4.  **PUT** `/question/<int:id>`

    * **Description:** Updates a question by ID.
    * **Parameters (JSON):**
        * `chapter_id` (integer, optional): The updated ID of the associated chapter.
        * `question` (string, optional): The updated question text.
        * `option_a` (string, optional): Updated Option A.
        * `option_b` (string, optional): Updated Option B.
        * `option_c` (string, optional): Updated Option C.
        * `option_d` (string, optional): Updated Option D.
        * `correct_option` (string, optional): The updated correct option.
        * `score` (integer, optional): the updated score.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "info": "Resource Successfully Updated"
            }
            ```
        * **400 Bad Request:** (Invalid Foreign Key, Invalid Data)
            ```json
            {"status": "failed", "info": "Invalid Data"}
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```
        * **409 Conflict:** (Resource Already Exists)
            ```json
            {"status": "failed", "info": "Resource Already Exists"}
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

5.  **DELETE** `/question/<int:id>`

    * **Description:** Deletes a question by ID.
    * **Parameters:**
        * `id` (integer): The ID of the question.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "info": "Resource Successfully Deleted"
            }
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```
        * **409 Conflict:** (Foreign Key Dependent)
            ```json
            {
                "status": "failed",
                "info": "Has Foreign Key Dependencies"
            }
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

### Quiz

1.  **GET** `/quizzes`

    * **Description:** Retrieves a list of all quizzes or quizzes filtered by `chapter_id` or `subject_id`.
    * **Parameters:**
        * `chapter_id` (integer, optional): Filters quizzes by chapter ID.
        * `subject_id` (integer, optional): Filters quizzes by subject ID.
        * **Note:** `chapter_id` and `subject_id` cannot be used together.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "scope": "Chapter",
                        "chapter_id": 1,
                        "subject_id": null,
                        "time": 30,
                        "description": "Quiz for chapter 1"
                    },
                    {
                        "id": 2,
                        "scope": "Subject",
                        "chapter_id": null,
                        "subject_id": 1,
                        "time": 60,
                        "description": "Quiz for subject 1"
                    }
                ],
                "info": "Resource Successfully Fetched"
            }
            ```
        * **200 OK (No results):**
            ```json
            {
                "status": "success",
                "data": [],
                "info": "No Resource Were Found"
            }
            ```
        * **400 Bad Request:**
            ```json
            {
                "status": "failed",
                "info": "Invalid Query Paramters"
            }
            ```

2.  **GET** `/quiz/<int:id>`

    * **Description:** Retrieves a specific quiz by ID.
    * **Parameters:**
        * `id` (integer): The ID of the quiz.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": {
                    "id": 1,
                    "scope": "Chapter",
                    "chapter_id": 1,
                    "subject_id": null,
                    "time": 30,
                    "description": "Quiz for chapter 1"
                },
                "info": "Resource Successfully Fetched"
            }
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```

3.  **POST** `/quizzes`

    * **Description:** Creates a new quiz.
    * **Parameters (form-data):**
        * `scope` (string, required): The scope of the quiz (e.g., "Chapter", "Subject").
        * `chapter_id` (integer, optional): The ID of the associated chapter.
        * `subject_id` (integer, optional): The ID of the associated subject.
        * `time` (integer, required): The time limit for the quiz (in minutes).
        * `description` (string, optional): The description of the quiz.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **201 Created:**
            ```json
            {
                "status": "success",
                "data": {
                    "id": 3,
                    "scope": "Subject",
                    "chapter_id": null,
                    "subject_id": 2,
                    "time": 45,
                    "description": "New quiz for subject 2"
                },
                "info": "Resource Created Successfully"
            }
            ```
        * **400 Bad Request:** (Invalid Foreign Key, Invalid Data)
            ```json
            {"status": "failed", "info": "Invalid Data"}
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **409 Conflict:** (Resource Already Exists)
            ```json
            {"status": "failed", "info": "Resource Already Exists"}
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

4.  **PUT** `/quiz/<int:id>`

    * **Description:** Updates a quiz by ID.
    * **Parameters (JSON):**
        * `scope` (string, optional): The updated scope of the quiz.
        * `chapter_id` (integer, optional): The updated ID of the associated chapter.
        * `subject_id` (integer, optional): The updated ID of the associated subject.
        * `time` (integer, optional): The updated time limit for the quiz.
        * `description` (string, optional): The updated description of the quiz.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "info": "Resource Successfully Updated"
            }
            ```
        * **400 Bad Request:** (Invalid Foreign Key, Invalid Data)
            ```json
            {"status": "failed", "info": "Invalid Data"}
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```
        * **409 Conflict:** (Resource Already Exists)
            ```json
            {"status": "failed", "info": "Resource Already Exists"}
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

5.  **DELETE** `/quiz/<int:id>`

    * **Description:** Deletes a quiz by ID.
    * **Parameters:**
        * `id` (integer): The ID of the quiz.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "info": "Resource Successfully Deleted"
            }
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```
        * **409 Conflict:** (Foreign Key Dependent)
            ```json
            {
                "status": "failed",
                "info": "Has Foreign Key Dependencies"
            }
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

### QuizQuestion

1.  **GET** `/quiz-questions`

    * **Description:** Retrieves the questions associated with a quiz.
    * **Parameters:**
        * `quiz_id` (integer, optional): Filters questions by quiz ID. If not provided, retrieves all quiz-question associations.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": [
                    {
                        "quiz_id": 1,
                        "question_id": 1
                    },
                    {
                        "quiz_id": 1,
                        "question_id": 2
                    }
                ],
                "info": "Resource Successfully Fetched"
            }
            ```
        * **200 OK (No results):**
            ```json
            {
                "status": "success",
                "data": [],
                "info": "No Resource Were Found"
            }
            ```

2.  **POST** `/quiz-questions`

    * **Description:** Associates questions with a quiz. Deletes previous associations and adds new ones based on the provided data.
    * **Parameters (JSON):**
        * `quiz_id` (integer, required): The ID of the quiz.
        * `question_ids` (array of integers, required): An array of question IDs to associate with the quiz.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "info": "Questions Updated"
            }
            ```
        * **400 Bad Request:** (Invalid Foreign Key, Invalid Data)
            ```json
            {"status": "failed", "info": "Invalid Data"}
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {"status": "failed", "info": "Unauthorized"}
            ```
        * **500 Internal Server Error:**
            ```json
            {"status": "failed", "info": "Internal Server Error"}
            ```

### User

1.  **GET** `/users`

    * **Description:** Retrieves a list of all users (admin only).
    * **Parameters:** None.
    * **Authentication:** JWT required (admin only).
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "username": "johndoe",
                        "date_joined": "2023-10-26T10:00:00",
                        "qualification": "Bachelors",
                        "dob": "1990-01-01",
                        "date_account_deleted": null,
                        "profile_pic": "/uploads/profile1.jpg"
                    },
                    {
                        "id": 2,
                        "name": "Jane Smith",
                        "email": "jane.smith@example.com",
                        "username": "janesmith",
                        "date_joined": "2023-10-27T12:00:00",
                        "qualification": "Masters",
                        "dob": "1985-05-15",
                        "date_account_deleted": null,
                        "profile_pic": "/uploads/profile2.jpg"
                    }
                ],
                "info": "Resource Successfully Fetched"
            }
            ```
        * **403 Forbidden:**
            ```json
            {
                "status": "failed",
                "info": "Unauthorized"
            }
            ```

2.  **GET** `/user/<int:user_id>`

    * **Description:** Retrieves a specific user's information.
    * **Parameters:**
        * `user_id` (integer): The ID of the user.
    * **Authentication:** JWT required. User can retrieve their own information, admin can retrieve any user.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "username": "johndoe",
                    "date_joined": "2023-10-26T10:00:00",
                    "qualification": "Bachelors",
                    "dob": "1990-01-01",
                    "date_account_deleted": null,
                    "profile_pic": "/uploads/profile1.jpg"
                },
                "info": "Resource Successfully Fetched"
            }
            ```
        * **401 Unauthorized:**
            ```json
            {
                "status": "failed",
                "info": "User Not Found"
            }
            ```
        * **403 Forbidden:**
            ```json
            {
                "status": "failed",
                "info": "Unauthorized"
            }
            ```

3.  **PUT** `/user/<int:user_id>`

    * **Description:** Updates a specific user's information.
    * **Parameters (form-data):**
        * `username` (string, optional): The updated username.
        * `email` (string, optional): The updated email address.
        * `name` (string, required): The updated name.
        * `qualification` (string, optional): The updated qualification.
        * `dob` (string, optional): The updated date of birth (YYYY-MM-DD).
        * `password` (string, optional): The updated password.
        * `image` (file, optional): The updated profile picture.
    * **Authentication:** JWT required. User can only update their own information.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "info": "Resource Successfully Updated"
            }
            ```
        * **400 Bad Request:** (Invalid Foreign Key, Invalid Data)
            ```json
            {
                "status": "failed",
                "info": "Invalid Data"
            }
            ```
        * **401 Unauthorized:**
            ```json
            {
                "status": "failed",
                "info": "Unauthorized"
            }
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```
        * **409 Conflict:** (Email or Username Already Exists)
            ```json
            {
                "status": "failed",
                "info": "Email or Username Already Exists"
            }
            ```
        * **500 Internal Server Error:**
            ```json
            {
                "status": "failed",
                "info": "Internal Server Error"
            }
            ```

### Attempt

1.  **GET** `/attempts`

    * **Description:** Retrieves a list of all attempts (admin only) or attempts by a specific user (admin or the user).
    * **Parameters:**
        * `user_id` (integer, optional): Filters attempts by user ID.
    * **Authentication:** JWT required.
        * Admin: Can retrieve all attempts or filter by `user_id`.
        * User: Can only retrieve their own attempts or filter by their own `user_id`.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": [
                    {
                        "id": 1,
                        "user_id": 1,
                        "quiz_id": 1,
                        "date_attempted": "2023-10-26T10:00:00",
                        "time_taken": 30,
                        "score": 8,
                        "total_time": 60,
                        "total_score": 10
                    },
                    {
                        "id": 2,
                        "user_id": 1,
                        "quiz_id": 2,
                        "date_attempted": "2023-10-27T12:00:00",
                        "time_taken": 45,
                        "score": 7,
                        "total_time": 60,
                        "total_score": 10
                    }
                ],
                "info": "Resource Successfully Fetched"
            }
            ```
        * **200 OK (No results):**
            ```json
            {
                "status": "success",
                "data": [],
                "info": "No Resource Were Found"
            }
            ```
        * **403 Forbidden:** (Unauthorized)
            ```json
            {
                "status": "failed",
                "info": "Unauthorized"
            }
            ```

2.  **GET** `/attempt/<int:id>`

    * **Description:** Retrieves a specific attempt by ID.
    * **Parameters:**
        * `id` (integer): The ID of the attempt.
    * **Authentication:** JWT required.
        * Admin: Can retrieve any attempt.
        * User: Can only retrieve their own attempt.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": {
                    "id": 1,
                    "user_id": 1,
                    "quiz_id": 1,
                    "date_attempted": "2023-10-26T10:00:00",
                    "time_taken": 30,
                    "score": 8,
                    "total_time": 60,
                    "total_score": 10
                },
                "info": "Resource Successfully Fetched"
            }
            ```
        * **401 Unauthorized:**
            ```json
            {
                "status": "failed",
                "info": "Unauthorized"
            }
            ```
        * **404 Not Found:**
            ```json
            {
                "status": "failed",
                "info": "Resource Not Found"
            }
            ```

3.  **POST** `/attempts`

    * **Description:** Creates a new attempt.
    * **Parameters (form-data):**
        * `quiz_id` (integer, required): The ID of the quiz.
        * `user_id` (integer, required): The ID of the user.
        * `time_taken` (integer, required): The time taken for the attempt.
        * `score` (integer, required): The score obtained in the attempt.
        * `total_time` (integer, required): total time assigned to the quiz.
        * `total_score` (integer, required): total score of the quiz.
    * **Authentication:** Not required.
    * **Response:**
        * **201 Created:**
            ```json
            {
                "status": "success",
                "data": {
                    "id": 3,
                    "quiz_id": 1,
                    "user_id": 2,
                    "date_attempted": "2023-10-28T14:00:00",
                    "time_taken": 25,
                    "score": 9,
                    "total_time": 30,
                    "total_score": 10
                },
                "info": "Resource Created Successfully"
            }
            ```
        * **400 Bad Request:** (Invalid Foreign Key, Invalid Data)
            ```json
            {
                "status": "failed",
                "info": "Invalid Data"
            }
            ```
        * **500 Internal Server Error:**
            ```json
            {
                "status": "failed",
                "info": "Internal Server Error"
            }
            ```

### AttemptQuestion

1.  **GET** `/attempt-questions`

    * **Description:** Retrieves the questions and answers associated with a specific attempt.
    * **Parameters:**
        * `attempt_id` (integer, required): The ID of the attempt.
    * **Authentication:** Not required.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "data": [
                    {
                        "attempt_id": 1,
                        "question_id": 1,
                        "selected_answer": "b",
                        "correct_answer": "b"
                    },
                    {
                        "attempt_id": 1,
                        "question_id": 2,
                        "selected_answer": "c",
                        "correct_answer": "c"
                    }
                ],
                "info": "Resource Successfully Fetched"
            }
            ```
        * **200 OK (No results):**
            ```json
            {
                "status": "success",
                "data": [],
                "info": "No Resource Were Found"
            }
            ```

2.  **POST** `/attempt-questions`

    * **Description:** Associates question answers with an attempt.
    * **Parameters (JSON):**
        * `attempt_id` (integer, required): The ID of the attempt.
        * `questions` (array of objects, required): An array of question answer objects.
            * `question_id` (integer, required): The ID of the question.
            * `selected_answer` (string, required): The user's selected answer.
            * `correct_answer` (string, required): The correct answer.
    * **Authentication:** Not required.
    * **Response:**
        * **200 OK:**
            ```json
            {
                "status": "success",
                "info": "Questions Updated"
            }
            ```
        * **400 Bad Request:** (Invalid Foreign Key, Invalid Data)
            ```json
            {
                "status": "failed",
                "info": "Invalid Data"
            }
            ```
        * **500 Internal Server Error:**
            ```json
            {
                "status": "failed",
                "info": "Internal Server Error"
            }
            ```