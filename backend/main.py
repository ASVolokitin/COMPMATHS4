# TODO

# добавить вывод в файл

# отладить и унифицировать обработку ошибок
# для логарифма понять почему он не может просчитать точки для графика

# добавить комментарий к коэффициенту детерминации
# понять почему окошко с графиком уменьшается вместе с таблицей


from typing import Dict, Union

from backend.utils.http_entities import DataInput, LinearResultOutput, ResultOutput
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

ResponseUnion = Union[ResultOutput, LinearResultOutput]

@app.post("/approximate", response_model=Dict[str, ResponseUnion])
async def approximate(data: DataInput):
    result = solve_approximation(data)
    return result