import requests
import re
from urllib.parse import quote
import json
config = json.load(open("config.json"))

OMDB_API_KEY = config["OMDB_API_KEY"]

def clean_title(title):
    title = re.sub(r"\s*\(\d{4}\)", "", title)  # Remove year like (2009)
    title = re.sub(r"[^a-zA-Z0-9\s']", "", title)  # Remove special chars except apostrophes
    return title.strip()

def get_movie_details(title):
    title = clean_title(title)
    encoded_title = quote(title)

    # Try direct title match
    url = f"http://www.omdbapi.com/?t={encoded_title}&plot=full&apikey={OMDB_API_KEY}"
    res = requests.get(url).json()

    if res.get("Response") == "True":
        return res.get("Plot", "N/A"), res.get("Poster", "N/A")

    # Try fallback search
    search_url = f"http://www.omdbapi.com/?s={encoded_title}&apikey={OMDB_API_KEY}"
    search_res = requests.get(search_url).json()
    if search_res.get("Response") == "True":
        try:
            first_result = search_res["Search"][0]
            new_title = first_result["Title"]
            new_url = f"http://www.omdbapi.com/?t={quote(new_title)}&plot=full&apikey={OMDB_API_KEY}"
            final_res = requests.get(new_url).json()
            if final_res.get("Response") == "True":
                return final_res.get("Plot", "N/A"), final_res.get("Poster", "N/A")
        except:
            pass

    return "N/A", "N/A"
