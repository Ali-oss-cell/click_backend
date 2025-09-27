#!/usr/bin/env python3
"""
Simple test script for ClickExpress API
Run this to test the API endpoints
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # Change this to your admin password

def test_api():
    print("🚀 Testing ClickExpress API")
    print("=" * 50)
    
    # Test 1: Admin Login
    print("\n1. Testing Admin Login...")
    login_data = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"   User: {data['user']['username']}")
            print(f"   Token: {data['token'][:50]}...")
            
            # Store token for other requests
            access_token = data['token']
            headers = {"Authorization": f"Bearer {access_token}"}
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test 2: Verify Token
    print("\n2. Testing Token Verification...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/verify", headers=headers)
        if response.status_code == 200:
            print("✅ Token verification successful!")
        else:
            print(f"❌ Token verification failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Token verification error: {e}")
    
    # Test 3: Get Blog Posts (Public)
    print("\n3. Testing Get Blog Posts (Public)...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/blog-posts/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Blog posts retrieved: {data['total']} posts")
        else:
            print(f"❌ Get blog posts failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get blog posts error: {e}")
    
    # Test 4: Get Gallery Images (Public)
    print("\n4. Testing Get Gallery Images (Public)...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/gallery-images/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Gallery images retrieved: {data['total']} images")
        else:
            print(f"❌ Get gallery images failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get gallery images error: {e}")
    
    # Test 5: Create Blog Post (Admin)
    print("\n5. Testing Create Blog Post (Admin)...")
    blog_data = {
        "title": "Test Blog Post",
        "excerpt": "This is a test blog post created via API",
        "content": "This is the full content of the test blog post. It demonstrates the API functionality.",
        "featured_image": "/images/test-blog.jpg"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/blog-posts/create/", 
                               json=blog_data, headers=headers)
        if response.status_code == 201:
            data = response.json()
            print("✅ Blog post created successfully!")
            print(f"   Post ID: {data['data']['id']}")
            print(f"   Title: {data['data']['title']}")
        else:
            print(f"❌ Create blog post failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Create blog post error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print("\nNext steps:")
    print("1. Import the Postman collection: ClickExpress_API.postman_collection.json")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Access Django admin: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    test_api()
