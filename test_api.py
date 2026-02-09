"""
🧪 Test script for Data Converter API
Run: python test_api.py
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}\n")

def test_health():
    """Test health check endpoint"""
    print_section("1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print_section("2. API Info")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_formats():
    """Test formats endpoint"""
    print_section("3. Supported Formats")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/formats")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_csv_to_json():
    """Test CSV to JSON conversion"""
    print_section("4. CSV → JSON Conversion")
    try:
        # Create test CSV
        csv_data = "name,age,city\nJohn,25,NYC\nJane,28,LA"
        
        files = {'file': ('test.csv', csv_data)}
        response = requests.post(
            f"{BASE_URL}/api/v1/csv-to-json",
            files=files
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_json_to_csv():
    """Test JSON to CSV conversion"""
    print_section("5. JSON → CSV Conversion")
    try:
        json_data = json.dumps([
            {"name": "John", "age": 25, "city": "NYC"},
            {"name": "Jane", "age": 28, "city": "LA"}
        ])
        
        files = {'file': ('test.json', json_data)}
        response = requests.post(
            f"{BASE_URL}/api/v1/json-to-csv",
            files=files
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response (CSV format):")
        print(response.text)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_csv_to_sql():
    """Test CSV to SQL conversion"""
    print_section("6. CSV → SQL Conversion")
    try:
        csv_data = "name,age,city\nJohn,25,NYC\nJane,28,LA"
        
        files = {'file': ('test.csv', csv_data)}
        response = requests.post(
            f"{BASE_URL}/api/v1/csv-to-sql",
            files=files,
            params={"table_name": "users"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response (SQL format):")
        print(response.text)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_json_to_xml():
    """Test JSON to XML conversion"""
    print_section("7. JSON → XML Conversion")
    try:
        json_data = json.dumps({
            "name": "John",
            "age": 25,
            "city": "NYC"
        })
        
        files = {'file': ('test.json', json_data)}
        response = requests.post(
            f"{BASE_URL}/api/v1/json-to-xml",
            files=files
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response (XML format):")
        print(response.text)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("  🧪 Data Converter API Test Suite")
    print("="*50)
    print(f"\nTesting: {BASE_URL}")
    print("\nMake sure the API is running (python main.py)")
    
    results = {
        "Health Check": test_health(),
        "API Info": test_root(),
        "Supported Formats": test_formats(),
        "CSV → JSON": test_csv_to_json(),
        "JSON → CSV": test_json_to_csv(),
        "CSV → SQL": test_csv_to_sql(),
        "JSON → XML": test_json_to_xml(),
    }
    
    print_section("Test Results Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your API is working correctly!")
        print("\nNext steps:")
        print("1. Open http://localhost:8000/docs in your browser")
        print("2. Test endpoints using Swagger UI")
        print("3. Deploy to Render.com (see DEPLOY.md)")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("\nTroubleshooting:")
        print("- Make sure the API is running: python main.py")
        print("- Check if http://localhost:8000/health returns 200")
        print("- Check error messages above")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
