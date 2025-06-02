from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.DB.database import Base, engine  # Ensure correct imports

import sys
from pathlib import Path

# Add the project root to sys.path for module resolution
sys.path.append(str(Path(__file__).resolve().parent.parent))


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    head_id = Column(Integer, ForeignKey("employees.id"))


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    designation = Column(String)
    date_joined = Column(Date)


class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String, unique=True)
    name = Column(String)
    category = Column(String)
    location = Column(String)
    purchase_date = Column(Date)
    warranty_until = Column(Date)
    assigned_to = Column(Integer, ForeignKey("employees.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    status = Column(Enum("In Use", "Under Maintenance", "Retired", name="asset_status"))


class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    reported_by = Column(Integer, ForeignKey("employees.id"))
    description = Column(Text)
    status = Column(Enum("Reported", "In Progress", "Resolved", name="log_status"))
    assigned_technician = Column(Integer, ForeignKey("employees.id"))
    resolved_date = Column(Date)


class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)


class AssetVendorLink(Base):
    __tablename__ = "asset_vendor_link"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    service_type = Column(String)
    last_service_date = Column(Date)


# Create all tables in the database
Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")
