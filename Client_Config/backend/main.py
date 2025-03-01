# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Configuration, ClientType, Provider, RequestType, ClientApiKey, User, Location, UserRole, InteractorRole, PetType, Sex, InteractionCategory, ProviderType, Pet, Interactor, Request, Content, Interaction
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID
import os
from google.cloud.sql.connector import Connector
import sqlalchemy
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
from pathlib import Path
from fastapi import APIRouter

# Initialize Cloud SQL Python Connector object
connector = Connector()

# Cloud SQL connection details
INSTANCE_CONNECTION_NAME = "talky-conversational-ai:us-central1:get-talky-db"
DB_NAME = "get-talky-demo"
DB_USER = "postgres"  # Replace with your actual database user
DB_PASS = '1g&A3/"RjK.GLGFS'  # Replace with your actual database password

# Function to create the database connection
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
        enable_iam_auth=True
    )
    return conn

# Create engine using the connection pool
engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
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

# Create an APIRouter for /api endpoints
api_router = APIRouter()

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
    twilio_phone_number: Optional[str] = None
    twilio_phone_number_sid: Optional[str] = None

class ProviderCreate(BaseModel):
    configuration_id: int
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    provider_type_id: int
    request_type_ids: List[int] = []

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

class ConfigurationData(BaseModel):
    elevenlabs_voice_id: Optional[str] = None
    about_us: Optional[str] = None
    services: Optional[str] = None
    twilio_phone_number: Optional[str] = None
    locations: List[dict] = []
    request_types: List[dict] = []
    providers: List[dict] = []

# New Pydantic models for POST requests
class PetCreate(BaseModel):
    id: int
    pet_type_id: int
    name: str
    age: Optional[int] = None
    sex_id: Optional[int] = None

class InteractorCreate(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    verified: Optional[bool] = False

class RequestCreate(BaseModel):
    id: int
    request_type_id: int
    provider_id: int
    request_time: Optional[datetime] = None

class ContentCreate(BaseModel):
    id: int
    interactor_role_id: int
    text: str
    timestamp: Optional[datetime] = None

class InteractionCreate(BaseModel):
    id: int
    configuration_id: int
    interaction_type_id: Optional[int] = None
    interaction_summary: Optional[str] = None
    interactor_name: Optional[str] = None
    interaction_category_id: Optional[int] = None
    interactor_id: Optional[int] = None
    request_id: Optional[int] = None
    pet_id: Optional[int] = None
    contents: Optional[List[ContentCreate]] = None

# Move all existing API endpoints to use the router
@api_router.post("/client-type/", response_model=EnumCreate)
def create_client_type(client_type: EnumCreate, db: Session = Depends(get_db)):
    db_client_type = ClientType(**client_type.dict())
    db.add(db_client_type)
    db.commit()
    db.refresh(db_client_type)
    return client_type

@api_router.get("/client-type/")
def get_client_types(db: Session = Depends(get_db)):
    return db.query(ClientType).all()

@api_router.delete("/client-type/{client_type_id}")
def delete_client_type(client_type_id: int, db: Session = Depends(get_db)):
    db_client_type = db.query(ClientType).filter(ClientType.id == client_type_id).first()
    if not db_client_type:
        raise HTTPException(status_code=404, detail="Client type not found")
    db.delete(db_client_type)
    db.commit()
    return {"message": "Client type deleted successfully"}

# Repeat for other enums
@api_router.post("/user-role/", response_model=EnumCreate)
def create_user_role(user_role: EnumCreate, db: Session = Depends(get_db)):
    db_user_role = UserRole(**user_role.dict())
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)
    return user_role

@api_router.get("/user-role/")
def get_user_roles(db: Session = Depends(get_db)):
    return db.query(UserRole).all()

@api_router.delete("/user-role/{user_role_id}")
def delete_user_role(user_role_id: int, db: Session = Depends(get_db)):
    db_user_role = db.query(UserRole).filter(UserRole.id == user_role_id).first()
    if not db_user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    db.delete(db_user_role)
    db.commit()
    return {"message": "User role deleted successfully"}

# Interactor Role endpoints
@api_router.post("/interactor-role/", response_model=EnumCreate)
def create_interactor_role(interactor_role: EnumCreate, db: Session = Depends(get_db)):
    db_interactor_role = InteractorRole(**interactor_role.dict())
    db.add(db_interactor_role)
    db.commit()
    db.refresh(db_interactor_role)
    return interactor_role

@api_router.get("/interactor-role/")
def get_interactor_roles(db: Session = Depends(get_db)):
    return db.query(InteractorRole).all()

@api_router.delete("/interactor-role/{interactor_role_id}")
def delete_interactor_role(interactor_role_id: int, db: Session = Depends(get_db)):
    db_interactor_role = db.query(InteractorRole).filter(InteractorRole.id == interactor_role_id).first()
    if not db_interactor_role:
        raise HTTPException(status_code=404, detail="Interactor role not found")
    db.delete(db_interactor_role)
    db.commit()
    return {"message": "Interactor role deleted successfully"}

# Pet Type endpoints
@api_router.post("/pet-type/", response_model=EnumCreate)
def create_pet_type(pet_type: EnumCreate, db: Session = Depends(get_db)):
    db_pet_type = PetType(**pet_type.dict())
    db.add(db_pet_type)
    db.commit()
    db.refresh(db_pet_type)
    return pet_type

@api_router.get("/pet-type/")
def get_pet_types(db: Session = Depends(get_db)):
    return db.query(PetType).all()

@api_router.delete("/pet-type/{pet_type_id}")
def delete_pet_type(pet_type_id: int, db: Session = Depends(get_db)):
    db_pet_type = db.query(PetType).filter(PetType.id == pet_type_id).first()
    if not db_pet_type:
        raise HTTPException(status_code=404, detail="Pet type not found")
    db.delete(db_pet_type)
    db.commit()
    return {"message": "Pet type deleted successfully"}

# Sex endpoints
@api_router.post("/sex/", response_model=EnumCreate)
def create_sex(sex: EnumCreate, db: Session = Depends(get_db)):
    db_sex = Sex(**sex.dict())
    db.add(db_sex)
    db.commit()
    db.refresh(db_sex)
    return sex

@api_router.get("/sex/")
def get_sexes(db: Session = Depends(get_db)):
    return db.query(Sex).all()

@api_router.delete("/sex/{sex_id}")
def delete_sex(sex_id: int, db: Session = Depends(get_db)):
    db_sex = db.query(Sex).filter(Sex.id == sex_id).first()
    if not db_sex:
        raise HTTPException(status_code=404, detail="Sex not found")
    db.delete(db_sex)
    db.commit()
    return {"message": "Sex deleted successfully"}

# Interaction Category endpoints
@api_router.post("/interaction-category/", response_model=EnumCreate)
def create_interaction_category(interaction_category: EnumCreate, db: Session = Depends(get_db)):
    db_interaction_category = InteractionCategory(**interaction_category.dict())
    db.add(db_interaction_category)
    db.commit()
    db.refresh(db_interaction_category)
    return interaction_category

@api_router.get("/interaction-category/")
def get_interaction_categories(db: Session = Depends(get_db)):
    return db.query(InteractionCategory).all()

@api_router.delete("/interaction-category/{interaction_category_id}")
def delete_interaction_category(interaction_category_id: int, db: Session = Depends(get_db)):
    db_interaction_category = db.query(InteractionCategory).filter(InteractionCategory.id == interaction_category_id).first()
    if not db_interaction_category:
        raise HTTPException(status_code=404, detail="Interaction category not found")
    db.delete(db_interaction_category)
    db.commit()
    return {"message": "Interaction category deleted successfully"}

# Provider Type endpoints
@api_router.post("/provider-type/", response_model=EnumCreate)
def create_provider_type(provider_type: EnumCreate, db: Session = Depends(get_db)):
    db_provider_type = ProviderType(**provider_type.dict())
    db.add(db_provider_type)
    db.commit()
    db.refresh(db_provider_type)
    return provider_type

@api_router.get("/provider-type/")
def get_provider_types(db: Session = Depends(get_db)):
    return db.query(ProviderType).all()

@api_router.delete("/provider-type/{provider_type_id}")
def delete_provider_type(provider_type_id: int, db: Session = Depends(get_db)):
    db_provider_type = db.query(ProviderType).filter(ProviderType.id == provider_type_id).first()
    if not db_provider_type:
        raise HTTPException(status_code=404, detail="Provider type not found")
    db.delete(db_provider_type)
    db.commit()
    return {"message": "Provider type deleted successfully"}

# CRUD Endpoints
@api_router.post("/configurations/", response_model=ConfigurationCreate)
def create_configuration(config: ConfigurationCreate, db: Session = Depends(get_db)):
    db_config = Configuration(**config.dict(exclude_unset=True))
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return config

@api_router.get("/configurations/")
def get_configurations(db: Session = Depends(get_db)):
    return db.query(Configuration).all()

@api_router.get("/configurations/{config_id}")
def read_configuration(config_id: int, db: Session = Depends(get_db)):
    config = db.query(Configuration).filter(Configuration.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config

@api_router.put("/configurations/{config_id}", response_model=ConfigurationCreate)
def update_configuration(config_id: int, config: ConfigurationCreate, db: Session = Depends(get_db)):
    db_config = db.query(Configuration).filter(Configuration.id == config_id).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    for key, value in config.dict(exclude_unset=True).items():
        setattr(db_config, key, value)
    db.commit()
    db.refresh(db_config)
    return config

@api_router.post("/providers/", response_model=ProviderCreate)
def create_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    db_provider = Provider(
        configuration_id=provider.configuration_id,
        first_name=provider.first_name,
        last_name=provider.last_name,
        phone_number=provider.phone_number,
        email=provider.email,
        provider_type_id=provider.provider_type_id
    )
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)

    # Add request type associations
    if provider.request_type_ids:
        request_types = db.query(RequestType).filter(RequestType.id.in_(provider.request_type_ids)).all()
        db_provider.request_types.extend(request_types)
        db.commit()
        db.refresh(db_provider)

    return provider

@api_router.post("/request_types/", response_model=RequestTypeCreate)
def create_request_type(request_type: RequestTypeCreate, db: Session = Depends(get_db)):
    db_request_type = RequestType(**request_type.dict(exclude_unset=True))
    db.add(db_request_type)
    db.commit()
    db.refresh(db_request_type)
    return request_type

@api_router.post("/client_api_keys/", response_model=ClientApiKeyCreate)
def create_api_key(api_key: ClientApiKeyCreate, db: Session = Depends(get_db)):
    db_api_key = ClientApiKey(**api_key.dict())
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return api_key

@api_router.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict(exclude_unset=True))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user

@api_router.post("/locations/", response_model=LocationCreate)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = Location(**location.dict(exclude_unset=True))
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return location

@api_router.get("/providers/{config_id}")
def get_providers(config_id: int, db: Session = Depends(get_db)):
    providers = db.query(Provider).options(
        joinedload(Provider.request_types)
    ).filter(Provider.configuration_id == config_id).all()
    return providers

@api_router.get("/request_types/{config_id}")
def get_request_types(config_id: int, db: Session = Depends(get_db)):
    request_types = db.query(RequestType).filter(RequestType.configuration_id == config_id).all()
    return request_types

@api_router.get("/locations/{config_id}")
def get_locations(config_id: int, db: Session = Depends(get_db)):
    locations = db.query(Location).filter(Location.configuration_id == config_id).all()
    return locations

@api_router.get("/client_api_keys/{config_id}")
def get_api_keys(config_id: int, db: Session = Depends(get_db)):
    api_keys = db.query(ClientApiKey).filter(ClientApiKey.configuration_id == config_id).all()
    return api_keys

@api_router.get("/users/{config_id}")
def get_users(config_id: int, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.configuration_id == config_id).all()
    return users

@api_router.delete("/providers/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    db_provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not db_provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    db.delete(db_provider)
    db.commit()
    return {"message": "Provider deleted successfully"}

@api_router.delete("/request_types/{request_type_id}")
def delete_request_type(request_type_id: int, db: Session = Depends(get_db)):
    db_request_type = db.query(RequestType).filter(RequestType.id == request_type_id).first()
    if not db_request_type:
        raise HTTPException(status_code=404, detail="Request type not found")
    db.delete(db_request_type)
    db.commit()
    return {"message": "Request type deleted successfully"}

@api_router.delete("/locations/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    db.delete(db_location)
    db.commit()
    return {"message": "Location deleted successfully"}

@api_router.delete("/client_api_keys/{api_key_id}")
def delete_api_key(api_key_id: int, db: Session = Depends(get_db)):
    db_api_key = db.query(ClientApiKey).filter(ClientApiKey.id == api_key_id).first()
    if not db_api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    db.delete(db_api_key)
    db.commit()
    return {"message": "API key deleted successfully"}

@api_router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@api_router.get("/configuration-data/{client_id}", response_model=ConfigurationData)
def get_configuration_data(client_id: UUID, db: Session = Depends(get_db)):
    # Query configuration by UUID
    config = db.query(Configuration).filter(Configuration.client_id == client_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    # Get locations
    locations = db.query(Location).filter(Location.configuration_id == config.id).all()
    location_data = [
        {
            "name": loc.name,
            "phone": loc.phone_number,
            "operating_hours": loc.operating_hours,
            "address": loc.address
        }
        for loc in locations
    ]

    # Get request types
    request_types = db.query(RequestType).filter(RequestType.configuration_id == config.id).all()
    request_type_data = [{"name": rt.name} for rt in request_types]

    # Get providers with their types and request types
    providers = (
        db.query(Provider)
        .options(joinedload(Provider.request_types))
        .filter(Provider.configuration_id == config.id)
        .all()
    )
    
    provider_data = []
    for provider in providers:
        # Get provider type name
        provider_type = db.query(ProviderType).filter(ProviderType.id == provider.provider_type_id).first()
        provider_type_name = provider_type.name if provider_type else None

        # Get request type names for this provider
        request_type_names = [rt.name for rt in provider.request_types] if provider.request_types else []

        provider_data.append({
            "name": f"{provider.first_name} {provider.last_name}",
            "provider_type": provider_type_name,
            "request_types": request_type_names
        })

    return ConfigurationData(
        elevenlabs_voice_id=config.elevenlabs_voice_id,
        about_us=config.about_us,
        services=config.services,
        twilio_phone_number=config.twilio_phone_number,
        locations=location_data,
        request_types=request_type_data,
        providers=provider_data
    )

# New endpoints for getting request types and providers by client_id
@api_router.get("/{client_id}/request_types")
def get_request_types_by_client_id(client_id: UUID, db: Session = Depends(get_db)):
    """Get request types for a client by client_id (UUID)"""
    # First find the configuration by client_id
    config = db.query(Configuration).filter(Configuration.client_id == client_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    # Then get the request types for that configuration
    request_types = db.query(RequestType).filter(RequestType.configuration_id == config.id).all()
    return request_types

@api_router.get("/{client_id}/providers")
def get_providers_by_client_id(client_id: UUID, db: Session = Depends(get_db)):
    """Get providers for a client by client_id (UUID)"""
    # First find the configuration by client_id
    config = db.query(Configuration).filter(Configuration.client_id == client_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    # Then get the providers for that configuration with their request types
    providers = db.query(Provider).options(
        joinedload(Provider.request_types)
    ).filter(Provider.configuration_id == config.id).all()
    return providers

# New POST endpoints for pets, interactors, requests, and interactions
@api_router.post("/pets/", response_model=PetCreate)
def create_pet(pet: PetCreate, db: Session = Depends(get_db)):
    """Create a new pet record"""
    db_pet = Pet(**pet.dict(exclude_unset=True))
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return pet

@api_router.post("/interactors/", response_model=InteractorCreate)
def create_interactor(interactor: InteractorCreate, db: Session = Depends(get_db)):
    """Create a new interactor record"""
    db_interactor = Interactor(**interactor.dict(exclude_unset=True), date_added=datetime.now())
    db.add(db_interactor)
    db.commit()
    db.refresh(db_interactor)
    return interactor

@api_router.post("/requests/", response_model=RequestCreate)
def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    """Create a new request record"""
    if not request.request_time:
        request.request_time = datetime.now()
    db_request = Request(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return request

@api_router.post("/interactions/", response_model=InteractionCreate)
def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    """Create a new interaction record with optional content"""
    # Create the interaction
    interaction_data = interaction.dict(exclude={"contents"})
    db_interaction = Interaction(**interaction_data)
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    
    # Add contents if provided
    if interaction.contents:
        for content_item in interaction.contents:
            content_data = content_item.dict()
            if not content_data.get("timestamp"):
                content_data["timestamp"] = datetime.now()
            db_content = Content(interaction_id=db_interaction.id, **content_data)
            db.add(db_content)
        db.commit()
    
    return interaction

# Include the API router
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)