from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import instaloader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Vercel URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

loader = instaloader.Instaloader()

@app.get("/profile-pic")
def get_profile_pic(username: str = Query(...)):
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        return {"profile_pic_url": profile.profile_pic_url}
    except Exception as e:
        return {"error": str(e)}

@app.get("/latest-post")
def get_latest_post(username: str = Query(...)):
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        posts = profile.get_posts()
        post = next(posts)
        return {"post_url": post.url}
    except Exception as e:
        return {"error": str(e)}

@app.get("/stories")
def get_stories(username: str = Query(...)):
    return {"error": "Stories require Instagram login. Not available in anonymous mode."}
  
