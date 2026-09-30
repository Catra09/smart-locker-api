from pydantic import BaseModel

class UserResponse(BaseModel):
    user_id: int
    student_id: str
    full_name: str
    email: str

    class Config:
        from_attributes = True

class LockerResponse(BaseModel):
    locker_id: int
    locker_number: str
    status: str

    class Config:
        from_attributes = True

class LockerUpdate(BaseModel):
    status: str

class PackageResponse(BaseModel):
    package_id: int
    tracking_code: str
    status: str

    class Config:
        from_attributes = True

class DeliveryResponse(BaseModel):
    delivery_id: int
    package_id: int
    locker_id: int

    class Config:
        from_attributes = True