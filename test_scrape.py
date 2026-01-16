import instaloader

def get_profile_data(username):
    L = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        
        print(f"Username: {profile.username}")
        print(f"Followers: {profile.followers}")
        
        # Calculate engagement from last 3 posts
        posts = profile.get_posts()
        likes = 0
        comments = 0
        count = 0
        
        for post in posts:
            if count >= 3:
                break
            likes += post.likes
            comments += post.comments
            count += 1
            
        print(f"Avg Likes (Last 3): {likes // 3}")
        print(f"Avg Comments (Last 3): {comments // 3}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test with a public profile (e.g. instagram itself or a celebrity)
    get_profile_data("instagram")
