from fastapi import FastAPI, APIRouter

from server.api.v1 import v1


app = FastAPI()

router = APIRouter(prefix="/api")
router.include_router(v1.router)

app.include_router(router)
