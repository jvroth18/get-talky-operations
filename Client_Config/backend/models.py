from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import uuid4

Base = declarative_base()

# Enum Tables (in get_talky_enum schema)
class ClientType(Base):
    __tablename__ = "client_type"
    __table_args__ = {'schema': 'get_talky_enum'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    active = Column(Boolean, default=True)

class UserRole(Base):
    __tablename__ = "user_role"
    __table_args__ = {'schema': 'get_talky_enum'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    active = Column(Boolean, default=True)

class InteractorRole(Base):
    __tablename__ = "interactor_role"
    __table_args__ = {'schema': 'get_talky_enum'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    active = Column(Boolean, default=True)

class PetType(Base):
    __tablename__ = "pet_types"
    __table_args__ = {'schema': 'get_talky_enum'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    active = Column(Boolean, default=True)

class Sex(Base):
    __tablename__ = "sex"
    __table_args__ = {'schema': 'get_talky_enum'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    active = Column(Boolean, default=True)

class InteractionCategory(Base):
    __tablename__ = "interaction_category"
    __table_args__ = {'schema': 'get_talky_enum'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    active = Column(Boolean, default=True)

class ProviderType(Base):
    __tablename__ = "provider_type"
    __table_args__ = {'schema': 'get_talky_enum'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    active = Column(Boolean, default=True)

# Main Tables
class Configuration(Base):
    __tablename__ = "configuration"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(UUID(as_uuid=True), default=uuid4, unique=True)
    name = Column(String(255))
    elevenlabs_model = Column(String(255))
    elevenlabs_voice_id = Column(String(255))
    client_internal_id = Column(String(255))
    client_type_id = Column(Integer, ForeignKey("get_talky_enum.client_type.id"))
    about_us = Column(String(255))
    services = Column(String(255))
    twilio_phone_number = Column(String(255))
    twilio_phone_number_sid = Column(String(255))
    # locations = Column(String(255))

    client_type = relationship("ClientType")
    providers = relationship("Provider", back_populates="configuration")
    request_types = relationship("RequestType", back_populates="configuration")
    locations = relationship("Location", back_populates="configuration")
    api_keys = relationship("ClientApiKey", back_populates="configuration")
    billing_info = relationship("BillingInformation", back_populates="configuration")
    users = relationship("User", back_populates="configuration")
    interactions = relationship("Interaction", back_populates="configuration")

# Association table for providers and request types
providers_request_types = Table(
    'providers_request_types',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('request_type_id', Integer, ForeignKey('request_types.id')),
    Column('provider_id', Integer, ForeignKey('providers.id'))
)

class Provider(Base):
    __tablename__ = "providers"
    
    id = Column(Integer, primary_key=True)
    configuration_id = Column(Integer, ForeignKey("configuration.id"))
    provider_type_id = Column(Integer, ForeignKey("get_talky_enum.provider_type.id"))
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(255))
    email = Column(String(255))
    date_added = Column(DateTime)
    date_updated = Column(DateTime)
    active = Column(Boolean, default=True)

    configuration = relationship("Configuration", back_populates="providers")
    requests = relationship("Request", back_populates="provider")
    request_types = relationship("RequestType", secondary=providers_request_types, back_populates="providers")

class RequestType(Base):
    __tablename__ = "request_types"
    
    id = Column(Integer, primary_key=True)
    configuration_id = Column(Integer, ForeignKey("configuration.id"))
    name = Column(String(255))
    description = Column(String(255))
    length = Column(Integer)
    display_order = Column(Integer)
    active = Column(Boolean, default=True)

    configuration = relationship("Configuration", back_populates="request_types")
    requests = relationship("Request", back_populates="request_type")
    providers = relationship("Provider", secondary=providers_request_types, back_populates="request_types")

class InteractionType(Base):
    __tablename__ = "interaction_types"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    phone_number = Column(String(255))
    phone_number_sid = Column(String(255))

    interactions = relationship("Interaction", back_populates="interaction_type")

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True)
    configuration_id = Column(Integer, ForeignKey("configuration.id"))
    name = Column(String(255))
    phone_number = Column(String(255))
    operating_hours = Column(String(255))
    address = Column(String(255))

    configuration = relationship("Configuration", back_populates="locations")

class ClientApiKey(Base):
    __tablename__ = "client_api_keys"
    
    id = Column(Integer, primary_key=True)
    configuration_id = Column(Integer, ForeignKey("configuration.id"))
    name = Column(String(255))
    api_key = Column(String(255))
    active = Column(Boolean, default=True)
    date_added = Column(DateTime)

    configuration = relationship("Configuration", back_populates="api_keys")

class BillingInformation(Base):
    __tablename__ = "billing_information"
    
    id = Column(Integer, primary_key=True)
    configuration_id = Column(Integer, ForeignKey("configuration.id"))
    plaid_access_token = Column(String(255))
    date_added = Column(DateTime)
    active = Column(Boolean, default=True)

    configuration = relationship("Configuration", back_populates="billing_info")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    configuration_id = Column(Integer, ForeignKey("configuration.id"))
    first_name = Column(String(255))
    last_name = Column(String(255))  # Fixed from timestamp to String
    phone_number = Column(String(255))
    email = Column(String(255))
    role_id = Column(Integer, ForeignKey("get_talky_enum.user_role.id"))
    date_added = Column(DateTime)
    active = Column(Boolean, default=True)

    configuration = relationship("Configuration", back_populates="users")
    role = relationship("UserRole")

class Interaction(Base):
    __tablename__ = "interaction"
    
    id = Column(Integer, primary_key=True)
    configuration_id = Column(Integer, ForeignKey("configuration.id"))
    interaction_type_id = Column(Integer, ForeignKey("interaction_types.id"))
    interaction_summary = Column(String(255))
    interactor_name = Column(String(255))
    interaction_category_id = Column(Integer, ForeignKey("get_talky_enum.interaction_category.id"))
    interactor_id = Column(Integer, ForeignKey("interactor.id"))
    request_id = Column(Integer, ForeignKey("request.id"))
    pet_id = Column(Integer, ForeignKey("pet.id"))

    configuration = relationship("Configuration", back_populates="interactions")
    interaction_type = relationship("InteractionType", back_populates="interactions")
    category = relationship("InteractionCategory")
    interactor = relationship("Interactor")
    request = relationship("Request")
    pet = relationship("Pet")
    contents = relationship("Content", back_populates="interaction")
    funnels = relationship("Funnel", back_populates="interaction")

class Interactor(Base):
    __tablename__ = "interactor"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(255))
    email = Column(String(255))
    verified = Column(Boolean, default=False)
    date_added = Column(DateTime)

    interactions = relationship("Interaction", back_populates="interactor")

class Request(Base):
    __tablename__ = "request"
    
    id = Column(Integer, primary_key=True)
    request_type_id = Column(Integer, ForeignKey("request_types.id"))
    provider_id = Column(Integer, ForeignKey("providers.id"))
    request_time = Column(DateTime)

    request_type = relationship("RequestType", back_populates="requests")
    provider = relationship("Provider", back_populates="requests")
    interactions = relationship("Interaction", back_populates="request")

class Pet(Base):
    __tablename__ = "pet"
    
    id = Column(Integer, primary_key=True)
    pet_type_id = Column(Integer, ForeignKey("get_talky_enum.pet_types.id"))
    name = Column(String(255))
    age = Column(Integer)
    sex_id = Column(Integer, ForeignKey("get_talky_enum.sex.id"))

    pet_type = relationship("PetType")
    sex = relationship("Sex")
    interactions = relationship("Interaction", back_populates="pet")

class Content(Base):
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True)
    interaction_id = Column(Integer, ForeignKey("interaction.id"))
    interactor_role_id = Column(Integer, ForeignKey("get_talky_enum.interactor_role.id"))
    text = Column(String(255))
    timestamp = Column(DateTime)

    interaction = relationship("Interaction", back_populates="contents")
    interactor_role = relationship("InteractorRole")

class Funnel(Base):
    __tablename__ = "funnel"
    
    id = Column(Integer, primary_key=True)
    interaction_id = Column(Integer, ForeignKey("interaction.id"))
    entry_time = Column(DateTime)
    exit_time = Column(DateTime)
    interaction_block = Column(String(255))

    interaction = relationship("Interaction", back_populates="funnels")