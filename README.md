# FastAPI

### Description
This project is a simple Todo API that allows users to perform create, read, update, and delete operations. The database used in this project is SQLite, and the ORM used is SQLAlchemy. The framework used is FastAPI.

### Features
- User registration and authentication using JWT tokens.

### Endpoints
- **GET** `/` - Welcome message
- **POST** `/auth/register-page` - Register a new user
- **POST** `/auth/login-page` - Login a user
- **POST** `/todos/add-todo-page` - Add a new Todo
- **GET** `/todos/todo` - Get all Todo
- **GET** `/todos/{id}` - Get a Todo by id
- **PUT** `/todos/edit-todo-page` - Update a Todo by id
- **DELETE** `/todos/{id}` - Delete a Todo by id

### License
This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/licenses/MIT) file for details.
