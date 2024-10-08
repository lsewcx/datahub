from fastapi import FastAPI
from utils.yolo import export_to_yolo_format, progress_callback
app = FastAPI()

@app.post("/yolo/export")
def export_to_yolo(dataset_path: str, train_ratio: float, val_ratio: float, test_ratio: float, output_path: str):
    return export_to_yolo_format(
        dataset_path=dataset_path,
        train_ratio=train_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        output_path=output_path,
        callback=progress_callback
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)