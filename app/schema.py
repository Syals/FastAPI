from pydantic import BaseModel


class StudentBase(BaseModel):
    Student_name: str
    Student_id: str


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True


class AttendanceBase(BaseModel):
    Student_id: str
    timeStamp: str


class AttendanceCreate(AttendanceBase):

    pass


class Attendance(AttendanceBase):
    id: int

    class Config:
        orm_mode = True


class LeaveBase(BaseModel):
    Student_id: str
    reason: str
    status: str = "Pending"


class LeaveCreate(LeaveBase):
    pass


class Leave(LeaveBase):
    id: int

    class Config:
        orm_mode = True
