# uvicorn app.main:app --reload --port 8001 --host 0.0.0.0
import uvicorn

from app.core.config import settings

if __name__ == "__main__":
    if settings.ENVIRONMENT == "dev":
        uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
    else:
        uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=False)
