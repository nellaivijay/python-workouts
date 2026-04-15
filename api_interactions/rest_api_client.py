"""
API Interactions - Working with REST APIs
"""

import requests
import json
from typing import Dict, Any, Optional

def get_request(url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Make a GET request to an API endpoint
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"GET request failed: {e}")
        return {}

def post_request(url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Make a POST request to an API endpoint
    """
    try:
        response = requests.post(url, data=data, json=json_data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"POST request failed: {e}")
        return {}

def put_request(url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Make a PUT request to an API endpoint
    """
    try:
        response = requests.put(url, data=data, json=json_data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"PUT request failed: {e}")
        return {}

def delete_request(url: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Make a DELETE request to an API endpoint
    """
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json() if response.content else {}
    except requests.RequestException as e:
        print(f"DELETE request failed: {e}")
        return {}

def test_json_placeholder():
    """Test API using JSONPlaceholder (free fake API for testing)"""
    base_url = "https://jsonplaceholder.typicode.com"
    
    print("Testing JSONPlaceholder API\n")
    print("=" * 50)
    
    # GET request - Get all posts
    print("\n1. GET all posts:")
    posts = get_request(f"{base_url}/posts")
    print(f"   Retrieved {len(posts)} posts")
    if posts:
        print(f"   First post: {posts[0]['title'][:50]}...")
    
    # GET request - Get specific post
    print("\n2. GET specific post (ID=1):")
    post = get_request(f"{base_url}/posts/1")
    print(f"   Title: {post.get('title', 'N/A')}")
    
    # GET request - Get posts for specific user
    print("\n3. GET posts for user ID=1:")
    user_posts = get_request(f"{base_url}/posts", params={'userId': 1})
    print(f"   Found {len(user_posts)} posts for user 1")
    
    # POST request - Create new post
    print("\n4. POST new post:")
    new_post = {
        'title': 'Test Post',
        'body': 'This is a test post created via API',
        'userId': 1
    }
    created_post = post_request(f"{base_url}/posts", json_data=new_post)
    print(f"   Created post with ID: {created_post.get('id', 'N/A')}")
    
    # PUT request - Update post
    print("\n5. PUT update post (ID=1):")
    updated_data = {
        'id': 1,
        'title': 'Updated Title',
        'body': 'Updated body content',
        'userId': 1
    }
    updated_post = put_request(f"{base_url}/posts/1", json_data=updated_data)
    print(f"   Updated title: {updated_post.get('title', 'N/A')}")

def test_random_user_api():
    """Test Random User API"""
    url = "https://randomuser.me/api/"
    
    print("\n" + "=" * 50)
    print("\nTesting Random User API\n")
    
    # Get random user
    user_data = get_request(url)
    if user_data and 'results' in user_data:
        user = user_data['results'][0]
        print(f"Name: {user['name']['first']} {user['name']['last']}")
        print(f"Email: {user['email']}")
        print(f"Location: {user['location']['city']}, {user['location']['country']}")

def add_custom_headers():
    """Example of adding custom headers to requests"""
    headers = {
        'User-Agent': 'MyPythonApp/1.0',
        'Accept': 'application/json',
        'Authorization': 'Bearer YOUR_TOKEN_HERE'  # Replace with actual token
    }
    print("\nExample headers configuration:")
    for key, value in headers.items():
        print(f"  {key}: {value}")

def handle_api_errors():
    """Example of handling different API errors"""
    print("\n" + "=" * 50)
    print("\nAPI Error Handling Examples:")
    
    # Test with invalid URL
    result = get_request("https://api.example.com/invalid")
    if not result:
        print("  ✓ Handled invalid URL gracefully")
    
    # Test with valid endpoint but potential errors
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts/99999")
        if response.status_code == 404:
            print("  ✓ Handled 404 Not Found error")
    except requests.RequestException as e:
        print(f"  ✓ Handled request exception: {e}")

def main():
    """Main function to run API examples"""
    print("API Interaction Examples")
    print("=" * 50)
    
    # Test various APIs
    test_json_placeholder()
    test_random_user_api()
    add_custom_headers()
    handle_api_errors()
    
    print("\n" + "=" * 50)
    print("\nKey Takeaways:")
    print("1. Always handle exceptions when making API requests")
    print("2. Check status codes and response content")
    print("3. Use appropriate headers (User-Agent, Authorization)")
    print("4. Respect rate limits and API terms of service")
    print("5. Consider using session objects for multiple requests")
    print("6. Implement proper error handling and logging")

if __name__ == "__main__":
    main()