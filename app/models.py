import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base, SessionLocal

class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    student_name = Column(String, nullable=False)
    student_id = Column(String(20), nullable=False, unique=True)

    attendances = relationship("Attendance", back_populates="student")
    leaves = relationship("Leave", back_populates="student")

    # relationship 建立时需要主表和外表同时指向一个属性，
    # 例如Attendance的student_id设置属性ForeignKey('student.student_id'))
    # student表的attendances属性(back_populates="student") 和 Attendance表的student属性(back_populates="attendances)是依依对应的


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=func.now())

    student_id = Column(String(20), ForeignKey('student.student_id'))
    student = relationship("Student", back_populates="attendances")

# attendance.student.student_name

class Leave(Base):
    __tablename__ = "leave"

    id = Column(Integer, primary_key=True, index=True)
    reason = Column(String(100))
    status = Column(String, default="Pending")

    student_id = Column(String(20), ForeignKey('student.student_id'))
    student = relationship("Student", back_populates="leaves")
