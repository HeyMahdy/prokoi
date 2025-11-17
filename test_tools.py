from src.ai.tool import get_user_profile, get_user_resource_progress, get_user_skill_tests

# Test with a dummy user ID to see what happens
def test_tools():
    print("Testing get_user_profile...")
    try:
        result = get_user_profile.invoke({"user_id": "dummy-user-id"})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nTesting get_user_resource_progress...")
    try:
        result = get_user_resource_progress.invoke({"user_id": "dummy-user-id", "limit": 100})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nTesting get_user_skill_tests...")
    try:
        result = get_user_skill_tests.invoke({"user_id": "dummy-user-id", "limit": 50})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_tools()