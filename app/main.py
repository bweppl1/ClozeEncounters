import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# rate limiter imports, reintegrate later for security
# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.errors import RateLimitExceeded
# from slowapi.util import get_remote_address

from .core.config import CORS_ORIGINS
from .routers import auth, user, cloze

# rate limiter before creating the FastAPI app
# limiter = Limiter(key_func=get_remote_address) # implement ratelimiter in future..
app = FastAPI(debug=True)
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

#Cross origin resources sharing - allowing react <-> fastapi communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API root"}


app.include_router(user.router)
app.include_router(auth.router, prefix="/auth")
app.include_router(cloze.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
