# 🚀 FAST FastAPI Preset

**FastAPI template** built with modern Python async patterns.

*This preset provides a solid foundation for building scalable web applications with JWT authentication, database migrations, and clean architecture.*

---

## 📖 Description

This FastAPI Preset is a comprehensive template designed to kickstart your web application development with a proven, well-structured foundation. It demonstrates modern backend development practices including asynchronous programming, JWT-based authentication, database migrations with Alembic, and a clean layered architecture.

**Database Flexibility:** The project supports both SQLite for quick development and testing, and PostgreSQL for production environments.The database setup involves a few simple steps: 

- Configure your .env file with database connection details

- Set up the database engine in database.py

- Configure Alembic for migrations in alembic.ini

All configurations are clearly documented and easy to modify for your specific needs.

**Purpose & Scope:** This preset is perfect for developers of all levels who want to rapidly start their FastAPI projects without spending time on boilerplate setup.This template provides everything you need. It includes essential features like user registration/login, item management with ownership validation, and database migrations - giving you a solid starting point for any web application.

**Note on Development:** This is an actively maintained preset designed to be simple and understandable for everyone. The current version includes core authentication and CRUD operations with clean, well-documented code that's easy to follow. Future updates will focus on making the preset even more beginner-friendly while adding practical features that are useful for real projects. **The goal is to create a template that's both educational for learning and practical for building real applications.**

---

## ✨ Features

- **User Authentication**
  - User registration with email and username validation
  - JWT-based login with secure password hashing
  - Token-based session management with cookies
  - Protected routes with user context

- **Item Management**
  - Create, read, and delete items
  - Ownership-based item operations
  - Prevent duplicate item names per user
  - Public and user-specific item views

- **Database Support**
  - PostgreSQL (recommended for production)
  - SQLite (for development and testing)
  - Async database operations with SQLAlchemy 2.0
  - Alembic database migrations

- **Security**
  - BCrypt password hashing
  - JWT token validation with expiration
  - CORS middleware configuration
  - Input validation with Pydantic schemas

- **API Documentation**
  - Automatic Swagger UI at `/docs`
  - OpenAPI schema generation
  - Detailed endpoint descriptions

---

## 🗂️ Project Structure

```
FastAPIPreset/
├── .venv/                       # Python virtual environment
├── DAO/                         # Data Access Object layer
│   ├── general_dao.py          # Common database operations
│   ├── item_dao.py             # Item-specific database operations
│   └── user_dao.py             # User-specific database operations
├── database/                    # Database configuration and models
│   ├── database.py             # Database engine and session setup
│   ├── models.py               # SQLAlchemy data models
│   ├── response_schemas.py     # Pydantic schemas for API responses
│   └── schema.py               # Pydantic schemas for validation
├── helpers/                     # Utility functions and helpers
│   ├── general_helper.py       # HTTP error handling utilities
│   ├── jwt_helper.py           # JWT token creation
│   ├── password_helper.py      # Password hashing and verification
│   ├── token_helper.py         # Token extraction and validation
│   └── user_helper.py          # User authentication logic
├── repository/                  # Business logic layer
│   ├── item_repository.py      # Item business logic
│   └── user_repository.py      # User business logic
├── routes/                      # API route definitions
│   ├── item_router.py          # Item-related endpoints
│   └── user_router.py          # User-related endpoints
├── migrations/                  # Alembic database migrations
│   ├── versions/               # Migration scripts
│   ├── env.py                  # Alembic environment configuration
│   └── script.py.mako          # Migration template
├── .env                         # Environment variables
├── alembic.ini                  # Alembic configuration
├── config.py                    # Application settings
├── main.py                      # FastAPI application entry point
├── requirements.txt             # Python dependencies
├── test_postgres.py             # PostgreSQL connection tester
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** (recommended: 3.11 or higher)
- **PostgreSQL** (for production) or **SQLite** (for development)
- **pip** (Python package manager)

### Installation & Setup

1. **Clone or download the preset:**
   ```bash
   # If using git
   git clone <your-repository-url>
   cd FastAPIPreset
   
   # Or simply download and extract the preset files
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv .venv
   
   # Activate the virtual environment:
   # Windows:
   .venv\Scripts\Activate
   
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```



### Database Configuration

#### Option A: SQLite (Development - Recommended for beginners)
Update your `.env` file for SQLite:
```env
DB_LITE="sqlite+aiosqlite:///fastapi_preset.db"
DB_LITE_FOR_ALEMBIC="sqlite:///fastapi_preset.db"
```

#### Option B: PostgreSQL (Production - Recommended for big projects)

1. **Install PostgreSQL:**
   - **Windows**: Download from [PostgreSQL Official Site](https://www.postgresql.org/download/windows/)
   - **macOS**: `brew install postgresql`
   - **Linux (Ubuntu)**: `sudo apt install postgresql postgresql-contrib`

2. **Start PostgreSQL service:**
   - **Windows**: Start from Services or use pgAdmin
   - **macOS**: `brew services start postgresql`
   - **Linux**: `sudo systemctl start postgresql`

3. **Create database:**
   ```bash
   psql -U postgres -c "CREATE DATABASE fastapi_preset;"
   ```

4. **Test PostgreSQL connection:**
   ```bash
   python test_postgres.py
   ```



### Environment Configuration

1. **Create a `.env` file** in the root directory:

```env
# Database Configuration
# Choose either SQLite or PostgreSQL:

# SQLite (Development)
DB_LITE="sqlite+aiosqlite:///fastapi_preset.db"
DB_LITE_FOR_ALEMBIC="sqlite:///fastapi_preset.db"

# PostgreSQL (Production)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fastapi_preset
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DATABASE_URL_POSTGRE="postgresql+asyncpg://your_username:your_password@localhost:5432/fastapi_preset"
DATABASE_URL_ALEMBIC_POSTGRE="postgresql://your_username:your_password@localhost:5432/fastapi_preset"

# JWT Authentication
SECRET_KEY=your_very_secure_secret_key_here
ALGORITHM=HS256
```

2. **Generate a secure SECRET_KEY:**
   ```bash
   # Using Node.js (if you have it installed):
   node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
   
   # Or using Python:
   python -c "import secrets; print(secrets.token_hex(32))"
   ```



### Database Migrations with Alembic

1. **Configure Alembic** in `alembic.ini`:
   ```ini
   sqlalchemy.url = postgresql://your_username:your_password@localhost:5432/fastapi_preset
   # OR for SQLite:
   # sqlalchemy.url = sqlite:///fastapi_preset.db
   ```

2. **Run migrations:**
   ```bash
   # Create initial migration (if needed)
   alembic revision --autogenerate -m "Initial migration"
   
   # Apply migrations
   alembic upgrade head
   ```

3. **Common Alembic commands:**
   ```bash
   # Create new migration
   alembic revision --autogenerate -m "Description of changes"
   
   # Apply all pending migrations
   alembic upgrade head
   
   # Rollback last migration
   alembic downgrade -1
   
   # Check current migration status
   alembic current
   
   # Show migration history
   alembic history --verbose
   ```

## Run the Application

1. **Start the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the application:**
   - **API Server**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - **Interactive Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - **Alternative Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📚 API Endpoints

### Authentication Endpoints
- `POST /users/API/sign_up` - User registration
- `POST /users/API/sign_in` - User login
- `POST /users/API/logout` - User logout
- `GET /users/API/me/` - Get current user profile

### User Management
- `GET /users/API/user/{user_id}` - Get user by ID
- `GET /users/API/users_list` - Get all users
- `GET /users/API/me/items` - Get current user's items
- `GET /users/API/me/item/{item_id}` - Get specific user item

### Item Management
- `POST /items/API/create_item` - Create new item (authenticated)
- `POST /items/API/delete_item/{item_id}` - Delete item (owner only)
- `GET /items/API/get_item/{item_id}` - Get item by ID (public)
- `GET /items/API/items` - Get all items (public)

---

## 🛠️ Development

### Architecture Overview

This preset follows a clean architecture pattern:

1. **Routes Layer** (`/routes/`) - HTTP endpoint definitions
2. **Repository Layer** (`/repository/`) - Business logic and validation
3. **DAO Layer** (`/DAO/`) - Data access operations
4. **Models Layer** (`/database/models.py`) - Data models
5. **Helpers** (`/helpers/`) - Utility functions

### Adding New Features

1. **Create a new model** in `database/models.py`
2. **Add Pydantic schemas** in `database/schema.py`
3. **Create DAO methods** in appropriate DAO file
4. **Implement business logic** in repository layer
5. **Define API routes** in router files
6. **Create database migration** with Alembic

### Example: Adding a New Endpoint

```python
# In appropriate router file
@router.post("/new_endpoint")
async def new_feature(
    request: schema.NewSchema,
    current_user: schema.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await repository.new_feature_logic(
        request=request,
        current_user=current_user,
        db=db
    )
```

---

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Issues
- **PostgreSQL connection failed**: 
  - Ensure PostgreSQL service is running
  - Verify credentials in `.env` file
  - Run `python test_postgres.py` to diagnose
  - Check if database exists and user has permissions

- **SQLite database not created**:
  - Check file path in `.env`
  - Ensure directory has write permissions

#### Migration Issues
- **Alembic "empty migration"**:
  - Ensure `target_metadata = Base.metadata` in `migrations/env.py`
  - Verify models are imported in `migrations/env.py`

- **Migration conflicts**:
  - Check current migration state: `alembic current`
  - Resolve conflicts: `alembic stamp head` then `alembic upgrade head`

#### Authentication Issues
- **JWT tokens not working**:
  - Verify `SECRET_KEY` in `.env` matches the one used to create tokens
  - Check token expiration (default: 30 minutes)

- **Password hashing errors**:
  - Ensure `bcrypt` is properly installed
  - Check password length (automatically handled in helpers)

### Debug Mode

Enable detailed logging by setting:
```python
# In database.py - already enabled for development
echo=True  # Set to False in production
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `DB_NAME` | Database name | `fastapi_preset` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | - |
| `SECRET_KEY` | JWT signing key | - |
| `ALGORITHM` | JWT algorithm | `HS256` |

---

## 🤝 Contributing

This preset is designed to be extended and customized for specific project needs. Feel free to:

1. Add new features and endpoints
2. Improve error handling and validation
3. Enhance security measures
4. Add testing suites
5. Extend documentation

---

## 📝 License

This FastAPI Preset is open-source and available for educational and commercial use. Please attribute the original source when using this as a foundation for your projects.

---

## 🆕 What's Next?

After setting up this preset, consider adding:

- **Frontend Integration** (React, Vue, etc.)
- **Email Service** for notifications
- **File Upload** capabilities
- **Redis Integration** for caching
- **Docker Configuration** for containerization
- **Testing Suite** with pytest
- **API Rate Limiting**
- **Background Tasks** with Celery

---

**Happy coding! 🚀**