from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models


# 学生方法
# 增加学生签到记录
def stu_vet(db: Session, student_id: str):
    db_vet = models.Attendance(student_id=student_id)
    db.add(db_vet)
    db.commit()
    db.refresh(db_vet)
    return db_vet


# 学生申请请假记录
def stu_leave(db: Session, student_id: str, reason: str):
    db_leave = models.Leave(student_id=student_id, reason=reason, status="Pending")
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave


# teacher方法
# 添加学生信息
def stu_create(db: Session, student_id: str, student_name: str):
    db_stu = models.Student(student_id=student_id, student_name=student_name)
    db.add(db_stu)
    db.commit()
    db.refresh(db_stu)
    return db_stu


# 删除学生id
def del_stu(db: Session, student_id: str):
    db_stu = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    print(db_stu)
    if not db_stu:
        return None
    db.delete(db_stu)
    db.commit()
    return db_stu


# 获取学生信息，返回学号，姓名
def get_stu(db: Session):
    stu = db.query(models.Student).all()
    return stu


# 更改学生信息
def upda_stu(db: Session, student_id: str, student_name: str):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).all()
    if len(student) == 0:
        return {
            'message': 'error'
        }
    student[0].student_name = student_name
    db.commit()
    return True


# 获取学生请假信息
def get_stu_leave(db: Session, student_id: str):
    stu_leave = db.query(models.Leave).filter(models.Leave.student_id == student_id).first()
    return stu_leave


# 获取学生所有请假信息
def get_leave_all(db: Session):
    stu_leave = db.query(models.Leave).all()
    return stu_leave


# 老师审批请假
def tea_vet(db: Session, student_id: str):
    stu_leave = db.query(models.Leave).filter(models.Leave.student_id == student_id).all()
    if not stu_leave:
        return None
    for leave in stu_leave:
        leave.status = 'success'
    db.commit()
    db.refresh(stu_leave[0])
    return stu_leave[0]


# 老师拒绝请假
def tea_novet(db: Session, student_id: str):
    stu_leave = db.query(models.Leave).filter(models.Leave.student_id == student_id).all()
    if not stu_leave:
        return None
    for leave in stu_leave:
        leave.status = 'refusal'
    db.commit()
    db.refresh(stu_leave[0])
    return stu_leave[0]


# 获取学生所有签到信息
def get_att_all(db: Session):
    stu_att = db.query(models.Attendance).all()
    return stu_att


# 确认学生签到信息列表
def get_stu_att(db: Session, student_id: str):
    stu_att = db.query(models.Attendance).filter(models.Attendance.student_id == student_id).first()
    return stu_att




