from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.models import DataInput, ResultOutput
from backend.solver import solve_approximation

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_index():
    return FileResponse("frontend/index.html")

@app.post("/approximate", response_model=ResultOutput)
async def approximate(data: DataInput):
    result = solve_approximation(data.x, data.y)
    return result