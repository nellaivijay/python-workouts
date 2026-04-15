"""
Web Development - FastAPI Basics Example
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="User Management API",
    description="A simple user management API built with FastAPI",
    version="1.0.0"
)


# Pydantic models for data validation
class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None


class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True


# In-memory database (for demonstration)
users_db: dict = {}
user_id_counter = 1


# Sample data initialization
def init_sample_data():
    """Initialize with sample data"""
    global user_id_counter
    sample_users = [
        UserCreate(name="Alice Johnson", email="alice@example.com", age=28),
        UserCreate(name="Bob Smith", email="bob@example.com", age=35),
        UserCreate(name="Charlie Brown", email="charlie@example.com", age=42)
    ]
    
    for user_data in sample_users:
        user = User(id=user_id_counter, **user_data.dict())
        users_db[user_id_counter] = user
        user_id_counter += 1


# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to User Management API",
        "version": "1.0.0",
        "endpoints": {
            "users": "/api/users",
            "user_by_id": "/api/users/{user_id}",
            "health": "/api/health",
            "docs": "/docs"
        }
    }


# Health check endpoint
@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "total_users": len(users_db),
        "version": "1.0.0"
    }


# CRUD Operations
@app.get("/api/users", response_model=List[User])
def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of users to return")
):
    """Get all users with pagination"""
    users = list(users_db.values())
    return users[skip:skip + limit]


@app.get("/api/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get a specific user by ID"""
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/api/users", response_model=User, status_code=201)
def create_user(user: UserCreate):
    """Create a new user"""
    global user_id_counter
    
    # Check if email already exists
    for existing_user in users_db.values():
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(id=user_id_counter, **user.dict())
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    
    return new_user


@app.put("/api/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """Update an existing user"""
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only provided fields
    update_data = user_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    # Check email uniqueness if email is being updated
    if 'email' in update_data:
        for existing_user in users_db.values():
            if existing_user.email == user.email and existing_user.id != user_id:
                raise HTTPException(status_code=400, detail="Email already registered")
    
    return user


@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    """Delete a user"""
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    del users_db[user_id]
    return {"message": "User deleted successfully"}


# Search endpoint
@app.get("/api/users/search/", response_model=List[User])
def search_users(
    name: Optional[str] = Query(None, description="Search by name"),
    email: Optional[str] = Query(None, description="Search by email"),
    min_age: Optional[int] = Query(None, ge=0, description="Minimum age"),
    max_age: Optional[int] = Query(None, ge=0, description="Maximum age")
):
    """Search users with filters"""
    users = list(users_db.values())
    
    if name:
        users = [user for user in users if name.lower() in user.name.lower()]
    
    if email:
        users = [user for user in users if email.lower() in user.email.lower()]
    
    if min_age is not None:
        users = [user for user in users if user.age and user.age >= min_age]
    
    if max_age is not None:
        users = [user for user in users if user.age and user.age <= max_age]
    
    return users


# Statistics endpoint
@app.get("/api/users/stats")
def get_user_stats():
    """Get user statistics"""
    users = list(users_db.values())
    
    if not users:
        return {
            "total_users": 0,
            "average_age": 0,
            "age_distribution": {}
        }
    
    ages = [user.age for user in users if user.age is not None]
    average_age = sum(ages) / len(ages) if ages else 0
    
    # Age distribution
    age_distribution = {}
    for user in users:
        if user.age:
            age_group = f"{(user.age // 10) * 10}-{(user.age // 10) * 10 + 9}"
            age_distribution[age_group] = age_distribution.get(age_group, 0) + 1
    
    return {
        "total_users": len(users),
        "average_age": round(average_age, 1),
        "age_distribution": age_distribution
    }


def main():
    """Main function to demonstrate FastAPI application"""
    print("FastAPI Web Application Example")
    print("=" * 50)
    
    # Initialize sample data
    init_sample_data()
    print(f"Initialized {len(users_db)} sample users")
    
    print("\nFastAPI Features Demonstrated:")
    print("✓ Automatic API documentation (Swagger UI)")
    print("✓ Pydantic models for data validation")
    print("✓ Type hints and automatic data conversion")
    print("✓ Query parameters and validation")
    print("✓ Response models")
    print("✓ Exception handling")
    print("✓ CRUD operations")
    print("✓ Search and filtering")
    print("✓ Statistics endpoints")
    
    print("\nTo run this application:")
    print("1. Install dependencies:")
    print("   pip install fastapi uvicorn")
    print("2. Run the server:")
    print("   uvicorn fastapi_basics:app --reload")
    print("3. Access the API:")
    print("   - API: http://127.0.0.1:8000")
    print("   - Documentation: http://127.0.0.1:8000/docs")
    print("   - Alternative docs: http://127.0.0.1:8000/redoc")
    
    print("\nAvailable Endpoints:")
    print("  GET  / - API information")
    print("  GET  /api/health - Health check")
    print("  GET  /api/users - Get all users")
    print("  GET  /api/users/{id} - Get specific user")
    print("  POST /api/users - Create user")
    print("  PUT  /api/users/{id} - Update user")
    print("  DELETE /api/users/{id} - Delete user")
    print("  GET  /api/users/search/ - Search users")
    print("  GET  /api/users/stats - User statistics")


if __name__ == "__main__":
    main()
    
    # To actually run the server, uncomment the following:
    # init_sample_data()
    # uvicorn.run(app, host="127.0.0.1", port=8000)