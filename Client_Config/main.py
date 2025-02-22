# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Configuration, ClientType, Provider, RequestType, ClientApiKey, User, Location, UserRole, InteractorRole, PetType, Sex, InteractionCategory
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
import os
from google.cloud.sql.connector import Connector
import sqlalchemy
from fastapi.responses import FileResponse

# Initialize Cloud SQL Python Connector object
connector = Connector()

# Cloud SQL connection details
INSTANCE_CONNECTION_NAME = "talky-conversational-ai:us-central1:get-talky-db"  # Replace with your instance connection name
DB_USER = "postgres"  # Replace with your database user
DB_PASS = 'U"vQE"j8tZU4jD$r'  # Replace with your database password
DB_NAME = "get-talky-demo"

# Function to create the database connection
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",  # Use pg8000 driver for PostgreSQL
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn

# Create engine using the connection pool
engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",  # Updated dialect for PostgreSQL
    creator=getconn,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Get Talky Command Center API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html
@app.get("/")
async def read_index():
    return FileResponse("index.html")

# Serve edit-config.html
@app.get("/edit-config.html")
async def read_edit_config():
    return FileResponse("edit-config.html")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Models
class ConfigurationCreate(BaseModel):
    client_id: Optional[UUID] = None
    name: str
    elevenlabs_model: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None
    client_internal_id: Optional[str] = None
    client_type_id: int
    about_us: Optional[str] = None
    services: Optional[str] = None

class ProviderCreate(BaseModel):
    configuration_id: int
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None

class RequestTypeCreate(BaseModel):
    configuration_id: int
    name: str
    description: Optional[str] = None
    length: Optional[int] = None
    display_order: Optional[int] = None

class ClientApiKeyCreate(BaseModel):
    configuration_id: int
    name: str
    api_key: str

class UserCreate(BaseModel):
    configuration_id: int
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    role_id: int

class LocationCreate(BaseModel):
    configuration_id: int
    name: str
    phone_number: Optional[str] = None
    operating_hours: Optional[str] = None
    address: Optional[str] = None

class EnumCreate(BaseModel):
    name: str
    description: Optional[str] = None

# Enum Endpoints
@app.post("/client-type/", response_model=EnumCreate)
def create_client_type(client_type: EnumCreate, db: Session = Depends(get_db)):
    db_client_type = ClientType(**client_type.dict())
    db.add(db_client_type)
    db.commit()
    db.refresh(db_client_type)
    return client_type

@app.get("/client-type/")
def get_client_types(db: Session = Depends(get_db)):
    return db.query(ClientType).all()

@app.delete("/client-type/{client_type_id}")
def delete_client_type(client_type_id: int, db: Session = Depends(get_db)):
    db_client_type = db.query(ClientType).filter(ClientType.id == client_type_id).first()
    if not db_client_type:
        raise HTTPException(status_code=404, detail="Client type not found")
    db.delete(db_client_type)
    db.commit()
    return {"message": "Client type deleted successfully"}

# Repeat for other enums
@app.post("/user-role/", response_model=EnumCreate)
def create_user_role(user_role: EnumCreate, db: Session = Depends(get_db)):
    db_user_role = UserRole(**user_role.dict())
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)
    return user_role

@app.get("/user-role/")
def get_user_roles(db: Session = Depends(get_db)):
    return db.query(UserRole).all()

@app.delete("/user-role/{user_role_id}")
def delete_user_role(user_role_id: int, db: Session = Depends(get_db)):
    db_user_role = db.query(UserRole).filter(UserRole.id == user_role_id).first()
    if not db_user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    db.delete(db_user_role)
    db.commit()
    return {"message": "User role deleted successfully"}

# Interactor Role endpoints
@app.post("/interactor-role/", response_model=EnumCreate)
def create_interactor_role(interactor_role: EnumCreate, db: Session = Depends(get_db)):
    db_interactor_role = InteractorRole(**interactor_role.dict())
    db.add(db_interactor_role)
    db.commit()
    db.refresh(db_interactor_role)
    return interactor_role

@app.get("/interactor-role/")
def get_interactor_roles(db: Session = Depends(get_db)):
    return db.query(InteractorRole).all()

@app.delete("/interactor-role/{interactor_role_id}")
def delete_interactor_role(interactor_role_id: int, db: Session = Depends(get_db)):
    db_interactor_role = db.query(InteractorRole).filter(InteractorRole.id == interactor_role_id).first()
    if not db_interactor_role:
        raise HTTPException(status_code=404, detail="Interactor role not found")
    db.delete(db_interactor_role)
    db.commit()
    return {"message": "Interactor role deleted successfully"}

# Pet Type endpoints
@app.post("/pet-type/", response_model=EnumCreate)
def create_pet_type(pet_type: EnumCreate, db: Session = Depends(get_db)):
    db_pet_type = PetType(**pet_type.dict())
    db.add(db_pet_type)
    db.commit()
    db.refresh(db_pet_type)
    return pet_type

@app.get("/pet-type/")
def get_pet_types(db: Session = Depends(get_db)):
    return db.query(PetType).all()

@app.delete("/pet-type/{pet_type_id}")
def delete_pet_type(pet_type_id: int, db: Session = Depends(get_db)):
    db_pet_type = db.query(PetType).filter(PetType.id == pet_type_id).first()
    if not db_pet_type:
        raise HTTPException(status_code=404, detail="Pet type not found")
    db.delete(db_pet_type)
    db.commit()
    return {"message": "Pet type deleted successfully"}

# Sex endpoints
@app.post("/sex/", response_model=EnumCreate)
def create_sex(sex: EnumCreate, db: Session = Depends(get_db)):
    db_sex = Sex(**sex.dict())
    db.add(db_sex)
    db.commit()
    db.refresh(db_sex)
    return sex

@app.get("/sex/")
def get_sexes(db: Session = Depends(get_db)):
    return db.query(Sex).all()

@app.delete("/sex/{sex_id}")
def delete_sex(sex_id: int, db: Session = Depends(get_db)):
    db_sex = db.query(Sex).filter(Sex.id == sex_id).first()
    if not db_sex:
        raise HTTPException(status_code=404, detail="Sex not found")
    db.delete(db_sex)
    db.commit()
    return {"message": "Sex deleted successfully"}

# Interaction Category endpoints
@app.post("/interaction-category/", response_model=EnumCreate)
def create_interaction_category(interaction_category: EnumCreate, db: Session = Depends(get_db)):
    db_interaction_category = InteractionCategory(**interaction_category.dict())
    db.add(db_interaction_category)
    db.commit()
    db.refresh(db_interaction_category)
    return interaction_category

@app.get("/interaction-category/")
def get_interaction_categories(db: Session = Depends(get_db)):
    return db.query(InteractionCategory).all()

@app.delete("/interaction-category/{interaction_category_id}")
def delete_interaction_category(interaction_category_id: int, db: Session = Depends(get_db)):
    db_interaction_category = db.query(InteractionCategory).filter(InteractionCategory.id == interaction_category_id).first()
    if not db_interaction_category:
        raise HTTPException(status_code=404, detail="Interaction category not found")
    db.delete(db_interaction_category)
    db.commit()
    return {"message": "Interaction category deleted successfully"}

# CRUD Endpoints
@app.post("/configurations/", response_model=ConfigurationCreate)
def create_configuration(config: ConfigurationCreate, db: Session = Depends(get_db)):
    db_config = Configuration(**config.dict(exclude_unset=True))
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return config

@app.get("/configurations/")
def get_configurations(db: Session = Depends(get_db)):
    return db.query(Configuration).all()

@app.get("/configurations/{config_id}")
def read_configuration(config_id: int, db: Session = Depends(get_db)):
    config = db.query(Configuration).filter(Configuration.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config

@app.put("/configurations/{config_id}", response_model=ConfigurationCreate)
def update_configuration(config_id: int, config: ConfigurationCreate, db: Session = Depends(get_db)):
    db_config = db.query(Configuration).filter(Configuration.id == config_id).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    for key, value in config.dict(exclude_unset=True).items():
        setattr(db_config, key, value)
    db.commit()
    db.refresh(db_config)
    return config

@app.post("/providers/", response_model=ProviderCreate)
def create_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    db_provider = Provider(**provider.dict(exclude_unset=True))
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return provider

@app.post("/request_types/", response_model=RequestTypeCreate)
def create_request_type(request_type: RequestTypeCreate, db: Session = Depends(get_db)):
    db_request_type = RequestType(**request_type.dict(exclude_unset=True))
    db.add(db_request_type)
    db.commit()
    db.refresh(db_request_type)
    return request_type

@app.post("/client_api_keys/", response_model=ClientApiKeyCreate)
def create_api_key(api_key: ClientApiKeyCreate, db: Session = Depends(get_db)):
    db_api_key = ClientApiKey(**api_key.dict())
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return api_key

@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict(exclude_unset=True))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user

@app.post("/locations/", response_model=LocationCreate)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = Location(**location.dict(exclude_unset=True))
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return location

@app.get("/providers/{config_id}")
def get_providers(config_id: int, db: Session = Depends(get_db)):
    providers = db.query(Provider).filter(Provider.configuration_id == config_id).all()
    return providers

@app.get("/request_types/{config_id}")
def get_request_types(config_id: int, db: Session = Depends(get_db)):
    request_types = db.query(RequestType).filter(RequestType.configuration_id == config_id).all()
    return request_types

@app.get("/locations/{config_id}")
def get_locations(config_id: int, db: Session = Depends(get_db)):
    locations = db.query(Location).filter(Location.configuration_id == config_id).all()
    return locations

@app.get("/client_api_keys/{config_id}")
def get_api_keys(config_id: int, db: Session = Depends(get_db)):
    api_keys = db.query(ClientApiKey).filter(ClientApiKey.configuration_id == config_id).all()
    return api_keys

@app.get("/users/{config_id}")
def get_users(config_id: int, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.configuration_id == config_id).all()
    return users

@app.delete("/providers/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    db_provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not db_provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    db.delete(db_provider)
    db.commit()
    return {"message": "Provider deleted successfully"}

@app.delete("/request_types/{request_type_id}")
def delete_request_type(request_type_id: int, db: Session = Depends(get_db)):
    db_request_type = db.query(RequestType).filter(RequestType.id == request_type_id).first()
    if not db_request_type:
        raise HTTPException(status_code=404, detail="Request type not found")
    db.delete(db_request_type)
    db.commit()
    return {"message": "Request type deleted successfully"}

@app.delete("/locations/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_location)
    db.commit()
    return {"message": "Location deleted successfully"}

@app.delete("/client_api_keys/{api_key_id}")
def delete_api_key(api_key_id: int, db: Session = Depends(get_db)):
    db_api_key = db.query(ClientApiKey).filter(ClientApiKey.id == api_key_id).first()
    if not db_api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    db.delete(db_api_key)
    db.commit()
    return {"message": "API key deleted successfully"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}