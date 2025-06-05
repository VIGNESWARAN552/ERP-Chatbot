from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
class ChatResponse(BaseModel):
    reply: str
class AssetRequest(BaseModel):
    asset_tag: str      
class AssetResponse(BaseModel):
    asset_tag: str
    name: str
    category: str
    location: str
    purchase_date: str
    warranty_until: str
    assigned_to: str
    department_id: str
    status: str 
class MaintenanceLogRequest(BaseModel):
    asset_id: int
    reported_by: str
    description: str
    status: str
    assigned_technician: str = None
    resolved_date: str = None   
class MaintenanceLogResponse(BaseModel):
    id: int
    asset_id: int
    reported_by: str
    description: str
    status: str
    assigned_technician: str = None
    resolved_date: str = None   
class VendorRequest(BaseModel):
    name: str
    contact_info: str
    address: str
class VendorResponse(BaseModel):
    id: int
    name: str
    contact_info: str
    address: str
class DepartmentRequest(BaseModel):
    name: str
    head_id: str    
class DepartmentResponse(BaseModel):
    id: int
    name: str
    head_id: str
    employees: list[str] = []  # List of employee names in the department   
class EmployeeRequest(BaseModel):
    name: str
    email: str
    department_id: str
    designation: str
    date_joined: str
class EmployeeResponse(BaseModel):  
    id: str
    name: str
    email: str
    department_id: str
    designation: str
    date_joined: str
    department_name: str = None  # Optional field to include department name if needed
    headed_department: bool = False  # Indicates if the employee is a department head
class NLQueryRequest(BaseModel):
    query: str      
class NLQueryResponse(BaseModel):
    result: str
