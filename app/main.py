from fastapi import Depends, FastAPI, HTTPException, Response ,status
from sqlalchemy.orm import Session, relationship
from starlette import schemas

from app import models, crud, schema
from app.database import SessionLocal, engine

from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# student传入模型
class studentModel(BaseModel):
    id: str
    name: str | None = None


# attendance传入模型
class attendanceModel(BaseModel):
    id: str


# leave传入模型
class leaveModel(BaseModel):
    id: str
    reason: str | None = None


# 添加学生信息
@app.post("/teacher/add")
def teacher_create_student(selection: studentModel, db: Session = Depends(get_db)):
    db_stu = crud.stu_create(db, selection.id, selection.name)
    if db_stu:
        return {
            'payload': db_stu,
            'status_code': 200
        }


# 删除单个学生信息
@app.post('/teacher/delete')
def teacher_delete_student(selection: studentModel, db: Session = Depends(get_db)):
    db_del = crud.del_stu(db, selection.id)
    if db_del:
        return {
            'payload': db_del,
            'status_code': 200
        }


# 更改用户信息
@app.post('/teacher/update')
def teacher_update_student(selection: studentModel, db: Session = Depends(get_db)):
    db_upda = crud.upda_stu(db, selection.id, selection.name)
    if db_upda:
        return {
            'payload': db_upda,
            'status_code': 404
        }


# 查询用户列表
@app.post('/teacher/select')
def teacher_select_student(db: Session = Depends(get_db)):
    db_bzd = crud.get_stu(db)
    if db_bzd:
        return db_bzd


# 学生签到请求
@app.post('/student/attendance')
def student_attendance(selection: attendanceModel, db: Session = Depends(get_db)):
    stu_att = crud.get_stu_att(db, selection.id)
    if stu_att:
       return {
            'payload': stu_att,
            'status_code': 200,
            'type:': type(stu_att)
        }
    else:
        vet = crud.stu_vet(db, selection.id)
        return {
            'payload': vet,
            'status_code': 200
        }


# 学生请假请求
@app.post('/student/leave')
def student_leave_application(selection: leaveModel, db: Session = Depends(get_db)):
    stu_leave = crud.stu_leave(db, selection.id, selection.reason)
    if stu_leave:
       return {
            'payload': stu_leave,
            'status_code': 200,
        }


# 查询某个学生签到记录
@app.post('/teacher/attendance_one')
def teacher_select_attendance(selection: attendanceModel, db: Session = Depends(get_db)):
    stu_att = crud.get_stu_att(db, selection.id)
    att_name = crud.get_stu(db, selection.id)
    return {
        'message': 'Student name - %s' % stu_att.timestamp+" "+att_name.student_name,
    }


# 查询全部学生签到记录
@app.post('/teacher/attendance_all')
def teacher_select_attendance(db: Session = Depends(get_db)):
    add_all = crud.get_att_all(db)
    if add_all:
        return add_all


# 老师查询单条学生请假信息
@app.post('/teacher/leave')
def teacher_leave(selection: leaveModel, db: Session = Depends(get_db)):
    get_leave = crud.get_stu_leave(db, selection.id)
    if get_leave:
        return {
            'payload': get_leave,
            'status_code': 200
        }


# 默认查询所有请假信息
@app.post('/teacher/leave/all')
def teacher_select_leave(db: Session = Depends(get_db)):
    leave_all = crud.get_leave_all(db)
    if leave_all:
        return leave_all
        # return {
        #     '学号': leave_all.student_id,
        #     '请假理由': leave_all.reason,
        #     '请假状态': leave_all.status,
        #     'id': leave_all.id,
        # }


# 老师审批请假信息,驳回
@app.post('/teacher/leave/false')
def teacher_vetting_false(selection: leaveModel, db: Session = Depends(get_db)):
    vet = crud.tea_novet(db, selection.id)
    if vet:
        return {
            'payload': vet,
            'status_code': 200
        }


# 老师审批请假信息,通过
@app.post('/teacher/leave/true')
def teacher_vetting_true(selection: leaveModel, db: Session = Depends(get_db)):
    vet = crud.tea_vet(db, selection.id)
    if vet:
        return {
            'payload': vet,
            'status_code': 200
        }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
