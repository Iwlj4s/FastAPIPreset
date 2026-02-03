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

- **Clean Architecture**
   - Repository pattern for business logic

   - DAO (Data Access Object) layer for database operations

   - Request Context for dependency management

   - Generic Response Schemas with type safety

- **🔍 Data Validation System** *(Early Development)*
  - `ValidationService` for centralized data integrity checks
  - Global uniqueness validation (prevent duplicates across database)
  - Per-user uniqueness validation (prevent duplicates within user's records)
  - Early error detection (validation before database commit)
  - Extensible rule-based configuration

- **Modern Response Handling**
  - Generic `DataResponse[T]` for single object endpoints
  - Generic `ListResponse[T]` for collection endpoints  
  - Type-safe response schemas with Pydantic
  - Consistent API response structure

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
├── .venv/                      # Python virtual environment
├── context/                    # Context dataclasses
│   ├── request_context.py       # Request context
├── DAO/                        # Data Access Object layer
│   ├── general_dao.py           # Common database operations
│   ├── item_dao.py              # Item-specific database operations
│   └── user_dao.py              # User-specific database operations
├── database/                   # Database configuration and models
│   ├── database.py              # Database engine and session setup
│   ├── models.py                # SQLAlchemy data models
│   ├── response_schemas.py      # Generic Pydantic schemas for API responses
│   └── schema.py                # Pydantic schemas for validation
├── helpers/                    # Utility functions and helpers
│   ├── general_helper.py        # HTTP error handling utilities
│   ├── jwt_helper.py            # JWT token creation
│   ├── password_helper.py       # Password hashing and verification
│   ├── token_helper.py          # Token extraction and validation
│   └── user_helper.py           # User authentication logic
├── services/                   # Business logic and validation services
│   ├── validation_services.py   # Data validation and uniqueness checks
│   ├── item_services.py         # Item-related business logic
│   └── user_services.py         # User-related business logic
├── repository/                 # Business logic layer
│   ├── item_repository.py       # Item business logic
│   └── user_repository.py       # User business logic
├── routes/                     # API route definitions
│   ├── item_router.py           # Item-related endpoints
│   └── user_router.py           # User-related endpoints
├── migrations/                 # Alembic database migrations
│   ├── versions/                # Migration scripts
│   ├── env.py                   # Alembic environment configuration
│   └── script.py.mako           # Migration template
├── .env                        # Environment variables
├── alembic.ini                 # Alembic configuration
├── config.py                   # Application settings
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── test_postgres.py            # PostgreSQL connection tester
└── README.md                   # This file
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

<details> <summary><strong>💡 Note: API Testing Tools Recommendation</strong></summary>
For testing API endpoints, I recommend using specialized tools:

- [Yaak](https://yaak.app/) - Modern, intuitive interface with excellent user experience

   - Clean, distraction-free design
   
   - Easy request organization
   
   - Great for beginners

- [Postman](https://www.postman.com/) - Industry standard with extensive features

   - Comprehensive testing capabilities
   
   - Environment variables and collections
   
   - Team collaboration features

Why use these tools?

- Better than browser testing: Proper handling of different HTTP methods

- Header management: Easy JWT token and authentication header setup

- Request organization: Save and organize your API calls

- Environment variables: Manage different configurations (local/dev/prod)

- Response inspection: Detailed view of headers, status codes, and response bodies

**Personal Recommendation:** Try Yaak first - it's lightweight, clean interface makes API testing much more enjoyable, especially when learning FastAPI!
And it's kinda pretty, lol 
<img width="1159" height="649" alt="изображение" src="https://github.com/user-attachments/assets/f9689241-a99c-4c69-ac5f-830cdb8b0f63" />

</details>


## 📚 API Endpoints

### Authentication Endpoints
- `POST /api/v1/users/sign_up` - User registration
- `POST /api/v1/users/sign_in` - User login (returns JWT token in cookie)
- `POST /api/v1/users/logout` - User logout (clears authentication cookie)

### User Management (Protected Routes)
- `GET /api/v1/users/` - Get all users (public)
- `GET /api/v1/users/user/{user_id}` - Get user profile by ID (public)
- `GET /api/v1/users/me/` - Get current authenticated user's profile (protected)
- `PATCH /api/v1/users/me/update` - Update current user profile (protected, with ValidationService)
- `GET /api/v1/users/me/items` - Get all items of current user (protected)
- `GET /api/v1/users/me/item/{item_id}` - Get specific item of current user (protected)

### Item Management
- `GET /api/v1/items/` - Get all items with user info (public)
- `GET /api/v1/items/item/{item_id}` - Get item by ID with user info (public)
- `POST /api/v1/items/create_item` - Create new item (protected, with ValidationService)
- `PATCH /api/v1/items/update_item/{item_id}` - Update item (protected, with ValidationService, ownership verification)
- `DELETE /api/v1/items/delete_item/{item_id}` - Delete item (protected, owner only)

---

## 🔄Request Context Pattern
### What is Request Context?

Request Context is a pattern that provides a convenient way to pass common dependencies (database, current user, logger, etc.) between application layers.

### Two Approaches to Dependencies
### Approach 1: Request Context (Recommended)

#### Using context:

```python
from context.request_context import RequestContext, get_request_context

@user_router.get("/me/items")
async def get_current_user_items(context: RequestContext = Depends(get_request_context)):
    """
    - **context**: Request Context contains:
        - **db**: Database session
        - **current_user**: Authenticated user
    """
    return await user_repository.get_current_user_items(current_user=context.current_user, 
                                                        db=context.db)
```

Advantages:
- Clean function signatures
- Easy to add new dependencies
- Centralized management
- Simplifies testing

### Approach 2: Standard FastAPI Dependencies

### Without context:

```python
@user_router.get("/me/items")
async def get_current_user_items(current_user: schema.User = Depends(get_current_user),
                                 db: AsyncSession = Depends(get_db)):
    """
    - **current_user**: Authenticated user
    - **db**: Database session
    """
    return await user_repository.get_current_user_items(current_user=current_user, 
                                                        db=db)
```

When to use:
-   Simple endpoints with 1-2 dependencies
-   When you need explicit control over dependencies
-   Better clarity for beginners


### How to Add New Dependencies to Context

1. Add field to RequestContext (`/context/request_context.py`):

```python
    @dataclass
    class RequestContext:
        db: AsyncSession
        current_user: "schema.User"
        logger: logging.Logger  # New dependency
        cache: RedisClient     # New dependency

    Update context factory:

    async def get_request_context(db: AsyncSession = Depends(get_db),
                                  current_user: "schema.User" = Depends(get_current_user),
                                  logger: logging.Logger = Depends(get_logger),      # New 
                                  cache: RedisClient = Depends(get_redis_client)     # New 
                                  ) -> RequestContext:
        return RequestContext(db=db, 
                              current_user=current_user, 
                              logger=logger,     # New 
                              cache=cache        # New 
                              )
```
 Now all endpoints automatically get access!

### Migration Between Approaches

### From context to standard dependencies:

**BEFORE (with context)**
```python
async def some_endpoint(context: RequestContext = Depends(get_request_context)):
    user = context.current_user
    db = context.db
```

**AFTER (without context)**
```python
async def some_endpoint(current_user: schema.User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    user = current_user
    db = db
```

### Usage Examples
### With Context (recommended for complex projects):

```python
@user_router.get("/me/items")
async def get_current_user_items(context: RequestContext = Depends(get_request_context)):
    """
    Using Request Context - clean signature,
    easy to add new dependencies.
    """
    return await user_repository.get_current_user_items(current_user=context.current_user, 
                                                        db=context.db)
```

### Without Context (simpler for beginners):

```python
@user_router.get("/me/items")  
async def get_current_user_items(
    current_user: schema.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Standard FastAPI approach - explicit dependencies,
    better for understanding data flow.
    """
    return await user_repository.get_current_user_items(
        current_user=current_user, 
        db=db
    )
```

### Advantages of Each Approach

Request Context
- Scalability - easy to add services
- Code cleanliness - short function signatures
- Consistency - unified interface for all dependencies
- Testability - one mock for all dependencies

Standard Dependencies 
- Clarity - explicitly see which dependencies are used
- Flexibility - different dependencies for different endpoints
- Simplicity - fewer abstractions to learn
- Standard - follows FastAPI documentation


---

## 🔍 Validation System

### ValidationService (Early Development)

The `ValidationService` is a centralized validation system that ensures data integrity by checking for duplicate values in globally unique and per-user unique fields **before database operations**.

**Current Status:** ⚠️ *This feature is actively being developed and currently supports update operations. Future versions will extend it to create and delete operations.*

#### Key Features

- **Global Unique Field Validation** - Prevents duplicate values across entire database
  - Example: Email addresses, usernames must be globally unique
  
- **Per-User Unique Field Validation** - Prevents duplicates within a single user's records
  - Example: Item names must be unique per user (one user cannot have two items named "My Item")

- **Extensible Rules** - Easy to add new validation rules without changing validation logic

#### How It Works

```
Request Data
    ↓
ValidationService.validate_update()
    ↓
Check VALIDATION_RULES for model
    ↓
For each unique field in update data:
  - Check if value already exists (exclude current record)
  - Raise HTTPException(409) if duplicate found
    ↓
✓ All checks pass → Continue to database update
✗ Duplicate found → Raise HTTPException(409) before commit
```

#### VALIDATION_RULES Configuration

```python
# In services/validation_services.py
VALIDATION_RULES = {
    "User": {
        "unique_fields": ["email", "name"],           # Globally unique
        "required_fields": ["email", "name", "password"],
        # "unique_per_user_fields": []  # Users don't have per-user unique fields
    },

    "Item": {
        "unique_fields": [],                          # Items can have same name globally
        "required_fields": ["name", "user_id"],
        "unique_per_user_fields": ["name"]           # But not per user
    }
}
```

#### Adding Validation Rules for New Models

1. **Add model to VALIDATION_RULES:**

```python
VALIDATION_RULES = {
    # ... existing rules ...
    
    "Project": {
        "unique_fields": ["slug"],                    # Projects have globally unique slugs
        "required_fields": ["name", "slug", "user_id"],
        "unique_per_user_fields": ["name", "code"]   # But names and codes unique per user
    }
}
```

2. **That's it!** `ValidationService` automatically handles all validation.

#### Usage Example

```python
# In repository or DAO layer
from services.validation_services import ValidationService

# Before updating a record:
await ValidationService.validate_update(
    model_class=models.Item,
    record=existing_item,              # Current database record
    update_data={"name": "New Name"},  # Data being updated
    db=db_session
)

# If duplicate found → HTTPException(409) raised
# If validation passes → Safe to proceed with update
await db_session.commit()
```

#### Response Examples

**Successful Update (No Duplicates):**
```json
{
  "status": 200,
  "message": "Item updated successfully",
  "data": { ... }
}
```

**Validation Error (Duplicate Found):**
```json
{
  "status": 409,
  "detail": "Value 'Gaming Laptop' for field 'name' already exists for this user"
}
```

#### Technical Details

**Method: `check_field_duplicates`**
- Checks if a value exists for a field across entire table
- Excludes current record from search (allows keeping same value during update)
- Returns: `True` if duplicate found, `False` if safe

**Method: `check_field_duplicates_per_user`**
- Checks if a value exists for a field within specific user's records
- Requires model to have `user_id` attribute
- Excludes current record by ID
- Returns: `True` if duplicate found for user, `False` if safe

**Safety Net: IntegrityError Handling**
```python
# In GeneralDAO.update_record()
try:
    await db.commit()
except IntegrityError as e:
    # Catches any database constraint violations
    # that ValidationService might have missed
    await db.rollback()
    raise HTTPException(status_code=409, detail="...")
```

---

## 🛠️ Development

### Architecture Overview

This preset follows a clean architecture pattern:

1. **Routes Layer** (`/routes/`) 
   - HTTP endpoint definitions

   - Request validation with Pydantic schemas

   - Dependency injection

   - Response formatting

2. **Repository Layer** (`/repository/`)
   - Business logic and validation

   - Error handling

   - Data transformation between layers

   - Coordinates between routes and DAO

3. **DAO Layer** (`/DAO/`)
   - Data access operations

   - Database queries and transactions

   - Model-specific operations

   - Generic operations for any model

4. **Models & Schemas** (`/database/`)
   - SQLAlchemy data models

   - Pydantic schemas for request validation

   - Response schemas for API responses

   - Database configuration

5. **Services Layer** (`/services/`)
   - `ValidationService` - Centralized data validation and uniqueness checks
   - Item services - Item-related business logic
   - User services - User-related business logic

6. **Helpers** (`/helpers/`)
   - Utility functions

   - JWT token management

   - Password hashing

   - Error handling utilities

### Adding New Features

1. **Create a new model** in `database/models.py`

```python
# In database/models.py
class NewModel(Base):
    """
    New model description.
    Explain the purpose and relationships of this model.
    """
    __tablename__ = 'new_model'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(
        String, 
        nullable=False, 
        server_default="No description"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # Many-to-one relationship with User model
    user: Mapped["User"] = relationship(
        "User",
        back_populates="new_model",  # Make sure to add this back_populates to User model
        lazy="selectin"
    )
```
Don't forget to update the User model to include the back relationship:
```python
# In User class, add:
new_model: Mapped[List["NewModel"]] = relationship(
    "NewModel",
    back_populates="user",
    lazy="selectin"
)
```

2. **Add Pydantic schemas** in `database/schema.py`

```python
# In database/schema.py
class NewModelCreate(BaseModel):
    name: str = Field(..., min_length=3)
    description: Optional[str] = None

class NewModelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
```

3. **Create Response Schemas**
```python
# In database/response_schemas.py
class NewModelResponse(BaseModel):
    id: int
    name: str
    description: str
    user_id: int
    
    class Config:
        from_attributes = True

# No need to create response wrapper classes - use generics!
```

4. **Implement DAO Methods**
```python
# In DAO/new_model_dao.py
class NewModelDAO:
    @classmethod
    async def create_new_model(cls, db: AsyncSession, request: schema.NewModelCreate, user_id: int):
        new_model = models.NewModel(
            name=request.name,
            description=request.description,
            user_id=user_id
        )
        db.add(new_model)
        await db.commit()
        await db.refresh(new_model)
        return new_model
```

**Note:** Updates are handled universally through `GeneralDAO.update_record()` which automatically uses `ValidationService` for validation. No need to create custom update methods!

5. **Add Validation Rules (If Needed)**

If your model has unique fields, add validation rules to `ValidationService`:

```python
# In services/validation_services.py - Update VALIDATION_RULES dictionary

VALIDATION_RULES = {
    # ... existing models ...
    
    "NewModel": {
        "unique_fields": [],                      # Fields unique across entire DB
        "required_fields": ["name", "user_id"],
        "unique_per_user_fields": ["name"]       # Fields unique per user
    }
}
```

Then `ValidationService` automatically validates these fields on updates!

6. **Add Repository Logic**
```python
# In repository/new_model_repository.py
async def create_new_model(
    request: schema.NewModelCreate,
    current_user: schema.User,
    db: AsyncSession
) -> response_schemas.DataResponse[NewModelResponse]:  # Use generic response
    # Business logic and validation
    new_model = await NewModelDAO.create_new_model(
        db=db,
        request=request,
        user_id=current_user.id
    )
    
    return response_schemas.DataResponse[NewModelResponse](
        message="New model created successfully",
        status_code=200,
        data=response_schemas.NewModelResponse(
            id=new_model.id,
            name=new_model.name,
            description=new_model.description,
            user_id=new_model.user_id
        )
    )
```

7. **Define API Routes**
```python
# In routes/new_model_router.py
@router.post("/create_new_model")
async def create_new_model_endpoint(
    request: schema.NewModelCreate,
    context: RequestContext = Depends(get_request_context)
) -> response_schemas.DataResponse[NewModelResponse]:  # Specify return type
    return await new_model_repository.create_new_model(
        request=request,
        current_user=context.current_user,
        db=context.db
    )
```

### Example: Adding a New Endpoint

```python
# In appropriate router file
@router.post("/new_endpoint")
async def new_feature(
    request: schema.NewSchema,
    current_user: schema.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> DataResponse[NewModelResponse]:  # Specify return type
    return await repository.new_feature_logic(
        request=request,
        current_user=current_user,
        db=db
    )
```


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

## 🚀 Recent Updates

### ValidationService (Early Development)

A new **data validation system** has been added to ensure data integrity at the application level, before database operations. 

**What Changed:**
- Added `ValidationService` for centralized validation
- Moved validation logic from DAO layer to service layer
- Early error detection (409 before commit, not IntegrityError from DB)
- Easy to extend - just add rules to `VALIDATION_RULES` dictionary

**Current Implementation:**
- Supports update operations with `validate_update()` method
- Checks globally unique fields and per-user unique fields
- Automatically integrated into `GeneralDAO.update_record()`

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
