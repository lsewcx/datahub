from fastapi import FastAPI, Depends, File, HTTPException, UploadFile
from utils.yolo import YOLO
from loguru import logger
from sqlalchemy.orm import Session
from views.index import create_project
from database.sql import get_db, Base, engine

logger.add("logs/app_{time:YYYY-MM-DD}.log", rotation="00:00")  # 每天午夜轮换日志文件

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.post("/yolo/export")
def export_to_yolo(dataset_path: str, train_ratio: float, val_ratio: float, test_ratio: float, output_path: str):
    logger.info(f"Exporting dataset to YOLO format: {dataset_path}")
    return YOLO.export_to_yolo_format(
        dataset_path=dataset_path,
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        output_path=output_path,
    )

@app.post("/projects/create")
def create_new_project(name: str, badge: str, date: str,description: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)