from fastapi import FastAPI, UploadFile
from frontend_api import run_balancing
import shutil
import os
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/solve")
async def solve_manifest(file: UploadFile):
    
    #save the uploaded file to a temporary location
    temp_file = f"temp_{uuid.uuid4().hex}.txt"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    print("Received manifest:", temp_file)
    #process the manifest file to get the solution
    result = run_balancing(temp_file)
    
    #clean up the temporary file
    os.remove(temp_file)

    return result