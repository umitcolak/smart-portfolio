from fastapi import FastAPI
from backend import auth
from fastapi.middleware.cors import CORSMiddleware
from backend import auth, stocks  # add stocks
from backend import auth, stocks, realtime  # add realtime


app = FastAPI()  # ✅ Define the app first

# ✅ Then add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend origin if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include your auth router
app.include_router(auth.router)
app.include_router(stocks.router)  # include the new stocks route
app.include_router(realtime.router)


# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware






