from typing import Optional, Dict
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from datetime import datetime
import uvicorn
import glob
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

BASE_DICOM_DIR = "./backend/dicom"

@app.get("/")
def read_root():
    return "This is slice-match-annotator API server"

@app.get("/patients")
def get_patients():
    PREFIX_LEN = len(BASE_DICOM_DIR.split('/'))
    fdict = {}
    for f in glob.glob(BASE_DICOM_DIR + "/**/*.DCM", recursive=True):
        f = f.split('/')
        patient, date, fname = f[PREFIX_LEN:]
        if patient not in fdict: fdict[patient] = {}
        if date not in fdict[patient]: fdict[patient][date] = []
        fdict[patient][date].append(fname)
    return fdict

@app.get("/slice/{patient_id}/{date}/{slice_id}")
def get_slice(patient_id: str, date: str, slice_id: str):
    slice_id = "%s/%s/%s/%s" % (BASE_DICOM_DIR, patient_id, date, slice_id) 
    return FileResponse(slice_id)

@app.put("/answer")
def answer(data: Dict[str, Dict]):
    now = datetime.now()
    fname = now.strftime("backend/annotated/%Y%m%d-%H%M%S_GROUNDTRUTH.json")
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return "データを保存しました！\nご協力ありがとうございました．"

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True, log_level="info")