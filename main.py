from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import instaloader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

loader = instaloader.Instaloader()

# Function to login
def login_instagram():
    # Enter your Instagram username and password here
    username = "your-username"  # Replace with your Instagram username
    password = "your-password"  # Replace with your Instagram password

    try:
        loader.context.log("Logging in...")
        loader.load_session_from_file(username)  # Check if session is saved
        if not loader.context.is_logged_in:
            loader.context.login(username, password)  # Log in if not already
            loader.save_session_to_file(username)  # Save session for future use
        return True
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return False

@app.get("/profile-pic")
def get_profile_pic(username: str = Query(...)):
    if not login_instagram():
        return {"error": "Login failed, please check your credentials."}

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        return {"profile_pic_url": profile.profile_pic_url}
    except Exception as e:
        return {"error": str(e)}

@app.get("/latest-post")
def get_latest_post(username: str = Query(...)):
    if not login_instagram():
        return {"error": "Login failed, please check your credentials."}

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        posts = profile.get_posts()
        post = next(posts)
        return {"post_url": post.url}
    except Exception as e:
        return {"error": str(e)}

@app.get("/stories")
def get_stories(username: str = Query(...)):
    if not login_instagram():
        return {"error": "Login failed, please check your credentials."}

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        return {"error": "Story downloading requires login and follow access."}
    except Exception as e:
        return {"error": str(e)}
        
