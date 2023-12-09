import requests

url = "https://api.zoom.us/v2/posts"  # Example URL, you should replace it with your actual URL

# Example payload, you should replace it with the data you want to post
data_to_post = {
    "title": "foo",
    "body": "bar",
    "userId": 1
}

response = requests.post(url, json=data_to_post)

if response.status_code == 201:
    created_data = response.json()
    print("POST Request Response:")
    print(created_data)
else:
    print(f"Failed to post data. Status code: {response.status_code}")
