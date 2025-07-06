from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
client = ApifyClient("<YOUR_API_TOKEN>")

# Prepare the Actor input
run_input = {
    "hashtags": ["fyp"],
    "resultsPerPage": 100,
    "profileScrapeSections": ["videos"],
    "profileSorting": "latest",
    "excludePinnedPosts": False,
    "searchSection": "",
    "maxProfilesPerQuery": 10,
    "shouldDownloadVideos": False,
    "shouldDownloadCovers": False,
    "shouldDownloadSubtitles": False,
    "shouldDownloadSlideshowImages": False,
}

# Run the Actor and wait for it to finish
run = client.actor("OtzYfK1ndEGdwWFKQ").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
