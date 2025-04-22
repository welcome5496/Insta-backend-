from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import instaloader
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

loader = instaloader.Instaloader()
session_file = "session.json"

# Function to handle login and save session
def login_instagram(username: str, password: str):
    try:
        loader.context.log("Logging in...")
        loader.load_session_from_file(username)  # Load saved session
        if not loader.context.is_logged_in:
            loader.context.login(username, password)  # Log in with credentials
            loader.save_session_to_file(username)  # Save session
        return True
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return False

@app.get("/profile-pic")
def get_profile_pic(username: str = Query(...)):
    if not os.path.exists(session_file):
        raise HTTPException(status_code=401, detail="Not logged in")
    
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        return {"profile_pic_url": profile.profile_pic_url}
    except Exception as e:
        return {"error": str(e)}

@app.get("/latest-post")
def get_latest_post(username: str = Query(...)):
    if not os.path.exists(session_file):
        raise HTTPException(status_code=401, detail="Not logged in")
    
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        posts = profile.get_posts()
        post = next(posts)
        return {"post_url": post.url}
    except Exception as e:
        return {"error": str(e)}
        
