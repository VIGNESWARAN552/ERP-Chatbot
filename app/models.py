from sqlalchemy import Column, String, Date, ForeignKey, Enum, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
import uuid
from database import Base


# Enumerations for statuses
class AssetStatus(enum.Enum):
    IN_USE = "In Use"
    UNDER_MAINTENANCE = "Under Maintenance"
    RETIRED = "Retired"


class MaintenanceStatus(enum.Enum):
    REPORTED = "Reported"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"


# Departments Table
class Department(Base):
    __tablename__ = "departments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    head_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"))
    head = relationship("Employee", foreign_keys=[head_id], back_populates="headed_department")
    employees = relationship("Employee", back_populates="department")


# Employees Table
class Employee(Base):
    __tablename__ = "employees"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    designation = Column(String)
    date_joined = Column(Date)
    department = relationship("Department", back_populates="employees")
    headed_department = relationship("Department", uselist=False, back_populates="head")


# Assets Table
class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_tag = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String)
    location = Column(String)
    purchase_date = Column(Date)
    warranty_until = Column(Date)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("employees.id"))
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"))
    status = Column(Enum(AssetStatus), nullable=False)
    assigned_employee = relationship("Employee")
    department = relationship("Department")


# Maintenance Logs Table
class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    reported_by = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(MaintenanceStatus), nullable=False)
    assigned_technician = Column(UUID(as_uuid=True), ForeignKey("employees.id"))
    resolved_date = Column(Date)
    asset = relationship("Asset", back_populates="maintenance_logs")
    reporter = relationship("Employee", foreign_keys=[reported_by])
    technician = relationship("Employee", foreign_keys=[assigned_technician])


# Vendors Table
class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact_person = Column(String)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    address = Column(String)


# Asset Vendor Link Table
class AssetVendorLink(Base):
    __tablename__ = "asset_vendor_link"
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    service_type = Column(String)
    last_service_date = Column(Date)
    asset = relationship("Asset", back_populates="vendor_links")
    vendor = relationship("Vendor", back_populates="asset_links")


# Relationships Backpopulates
Asset.maintenance_logs = relationship("MaintenanceLog", back_populates="asset")
Asset.vendor_links = relationship("AssetVendorLink", back_populates="asset")
Vendor.asset_links = relationship("AssetVendorLink", back_populates="vendor")
