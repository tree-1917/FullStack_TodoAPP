# 📝 FastAPI Todo Application

This is a FastAPI application for managing todos. The project includes authentication, user management, and CRUD operations for todos.

## 📂 Project Structure

```bash
fastapi-project/
├── database.py       # Database connection and session management
├── main.py           # Main entry point of the application
├── models.py         # Database models
├── routers/          # API route handlers
│   ├── __init__.py
│   ├── auth.py
│   ├── todos.py
│   ├── admin.py
│   └── user.py
├── static/           # Static files (CSS, JS, images, etc.)
├── templates/        # HTML templates
├── todos.db          # SQLite database file
├── requirements.txt  # Python dependencies
└── .gitignore        # Git ignore file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn
- SQLite (default database)

### Installation

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd fastapi-project
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   uvicorn main:app --reload
   ```

5. Access the application at `http://127.0.0.1:8000`.

## 🛠️ API Routes

### Default Routes

#### Root

- **GET** `/`
  - **Description**: Root endpoint
  - **Response**: `{"message": "Welcome to Todo App V0.0"}`

### Auth Routes

- **POST** `/auth/token`

  - **Description**: Login for access token
  - **Response**: `{ "access_token": "token", "token_type": "bearer" }`

- **GET** `/auth/`

  - **Description**: Authentication page
  - **Response**: Renders the authentication HTML page

- **POST** `/auth/`

  - **Description**: Login
  - **Response**: `{"message": "Logged in successfully"}`

- **GET** `/auth/logout`

  - **Description**: Logout
  - **Response**: `{"message": "Logged out successfully"}`

- **GET** `/auth/register`

  - **Description**: Register page
  - **Response**: Renders the registration HTML page

- **POST** `/auth/register`
  - **Description**: Register user
  - **Response**: `{"message": "User registered successfully"}`

### Todo Routes

- **GET** `/todos/`

  - **Description**: Read all todos by user
  - **Response**: List of todos

- **GET** `/todos/add-todo`

  - **Description**: Add new todo
  - **Response**: Renders the add new todo HTML page

- **POST** `/todos/add-todo`

  - **Description**: Add new todo
  - **Response**: `{"message": "Todo added successfully"}`

- **GET** `/todos/edit-todo/{todo_id}`

  - **Description**: Edit todo
  - **Response**: Renders the edit todo HTML page

- **POST** `/todos/edit-todo/{todo_id}`

  - **Description**: Edit todo commit
  - **Response**: `{"message": "Todo updated successfully"}`

- **GET** `/todos/delete/{todo_id}`

  - **Description**: Delete todo
  - **Response**: `{"message": "Todo deleted successfully"}`

- **GET** `/todos/complete/{todo_id}`
  - **Description**: Complete todo
  - **Response**: `{"message": "Todo marked as complete"}`

### User Routes

- **GET** `/user/password`

  - **Description**: Test route
  - **Response**: `{"message": "Password endpoint"}`

- **POST** `/user/password`
  - **Description**: Test route
  - **Response**: `{"message": "Password updated"}`

## 🛠️ Deployment

### Deploying on Render

Deploy your FastAPI application on Render by following these steps:

1. **Create a Render Account**: Sign up on [Render](https://render.com).

2. **Create a New Web Service**:

   - Go to the Render dashboard.
   - Click on "New" and select "Web Service".
   - Connect your GitHub repository containing your FastAPI project.

3. **Configure the Web Service**:

   - Name your service.
   - Choose the branch you want to deploy (e.g., `main`).
   - Set the Build Command to `pip install -r requirements.txt`.
   - Set the Start Command to `uvicorn main:app --host 0.0.0.0 --port 10000`.

4. **Deploy**: Click on "Create Web Service". Render will automatically build and deploy your FastAPI application.

5. **Access Your Application**: Once deployed, Render will provide a URL to access your FastAPI application.

## 📊 API Route Diagram

Here's a visual representation of the API routes:

```plaintext
           +-----------+
           |    /      |
           |  (Root)   |
           +-----------+
                 |
        +--------+--------+
        |                 |
+-------v-------+ +-------v-------+
|   /auth/      | |  /todos/      |
|  (Auth Routes)| |  (Todo Routes)|
+---------------+ +---------------+
```

## 📜 License

This project is licensed under the MIT License.

---
