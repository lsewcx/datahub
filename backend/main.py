from typing import List
from fastapi import FastAPI, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from loguru import logger
from views.index import create_project, Project
from database.sql import get_db, Base, engine
from utils.file import FileUtils
import os
import shutil
import tempfile

logger.add("logs/app_{time:YYYY-MM-DD}.log", rotation="00:00")  # 每天午夜轮换日志文件

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.post("/projects/create")
def create_new_project(
    name: str = Form(...),
    badge: str = Form(...),
    date: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:
        logger.info(f"Creating new project: {name}")
        
        # 创建临时文件夹
        with tempfile.TemporaryDirectory() as tmpdirname:
            temp_file_path = os.path.join(tmpdirname, file.filename)
            
            # 将上传的文件保存到临时文件
            with open(temp_file_path, "wb") as temp_file:
                shutil.copyfileobj(file.file, temp_file)
            
            output_path = f"datasets/{name}/original"
            FileUtils.unzip_file(upload_path=temp_file_path, output_path=output_path)
        
        return create_project(db, name, badge, date, output_path, description)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/projects")
def get_projects(db: Session = Depends(get_db), page: int = 1, size: int = 10):
    try:
        offset = (page - 1) * size
        projects = db.query(Project).offset(offset).limit(size).all()
        
        total_projects = db.query(Project).count()
        total_pages = (total_projects + size - 1) // size  # 计算总页数
        
        return {
            "data": projects,
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "total_projects": total_projects
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)