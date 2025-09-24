#!/usr/bin/env python3
"""
Circle of Care Platform - Comprehensive Backend API Testing
Testing all critical features after major fixes implementation
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Any

class CircleOfCareAPITester:
    def __init__(self, base_url="https://traumabridge.preview.emergentagent.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 30  # 30 second timeout
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        
    def log_test(self, name: str, success: bool, details: str = "", response_time: float = 0):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            
        result = {
            "test_name": name,
            "success": success,
            "details": details,
            "response_time_ms": round(response_time * 1000, 2),
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {name} | {details} | {result['response_time_ms']}ms")
        
    def test_health_endpoints(self):
        """Test basic health and info endpoints"""
        print("\n🔍 Testing Health & Info Endpoints...")
        
        # Test root endpoint
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/")
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Root API Endpoint", True, 
                            f"Status: {data.get('status', 'unknown')}", response_time)
            else:
                self.log_test("Root API Endpoint", False, 
                            f"Status: {response.status_code}", response_time)
        except Exception as e:
            self.log_test("Root API Endpoint", False, f"Error: {str(e)}")
            
        # Test health endpoint
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/health")
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", True, 
                            f"Status: {data.get('status', 'unknown')}", response_time)
            else:
                self.log_test("Health Check", False, 
                            f"Status: {response.status_code}", response_time)
        except Exception as e:
            self.log_test("Health Check", False, f"Error: {str(e)}")
            
        # Test contact info
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/contact-info")
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                expected_fields = ['creator', 'email', 'phone']
                has_fields = all(field in data for field in expected_fields)
                self.log_test("Contact Info", has_fields, 
                            f"Fields present: {has_fields}", response_time)
            else:
                self.log_test("Contact Info", False, 
                            f"Status: {response.status_code}", response_time)
        except Exception as e:
            self.log_test("Contact Info", False, f"Error: {str(e)}")

        # Test health check
        try:
            response = requests.get(f"{self.api_url}/health", timeout=10)
            success = response.status_code == 200 and "healthy" in response.text
            self.log_test("Health check", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Health check", False, f"Error: {str(e)}")

    def test_auth_endpoints(self):
        """Test authentication endpoints"""
        print("\n🔍 Testing Authentication Endpoints...")
        
        # Test session endpoint without session ID (should fail)
        try:
            response = requests.post(f"{self.api_url}/auth/session", timeout=10)
            success = response.status_code == 400
            self.log_test("Session without X-Session-ID", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Session without X-Session-ID", False, f"Error: {str(e)}")

        # Test session endpoint with invalid session ID
        try:
            headers = {"X-Session-ID": "invalid_session_id"}
            response = requests.post(f"{self.api_url}/auth/session", headers=headers, timeout=10)
            success = response.status_code == 400
            self.log_test("Session with invalid ID", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Session with invalid ID", False, f"Error: {str(e)}")

        # Test /auth/me without authentication (should fail)
        try:
            response = requests.get(f"{self.api_url}/auth/me", timeout=10)
            success = response.status_code == 401
            self.log_test("Get user info without auth", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get user info without auth", False, f"Error: {str(e)}")

        # Test logout endpoint
        try:
            response = requests.post(f"{self.api_url}/auth/logout", timeout=10)
            success = response.status_code == 200
            self.log_test("Logout endpoint", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Logout endpoint", False, f"Error: {str(e)}")

    def test_communities_endpoints(self):
        """Test communities endpoints"""
        print("\n🔍 Testing Communities Endpoints...")
        
        # Test get communities (should work without auth for public communities)
        try:
            response = requests.get(f"{self.api_url}/communities", timeout=10)
            success = response.status_code == 200
            communities_data = response.json() if success else []
            self.log_test("Get communities", success, f"Status: {response.status_code}, Count: {len(communities_data)}")
        except Exception as e:
            self.log_test("Get communities", False, f"Error: {str(e)}")

        # Test create community without auth (should fail)
        try:
            community_data = {
                "name": "Test Community",
                "description": "Test description",
                "category": "test"
            }
            response = requests.post(f"{self.api_url}/communities", json=community_data, timeout=10)
            success = response.status_code == 401
            self.log_test("Create community without auth", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Create community without auth", False, f"Error: {str(e)}")

    def test_ai_endpoints(self):
        """Test AI companion endpoints"""
        print("\n🔍 Testing AI Companion Endpoints...")
        
        # Test AI chat without auth (should fail)
        try:
            chat_data = {"message": "Hello", "is_panic": False}
            response = requests.post(f"{self.api_url}/ai/chat", json=chat_data, timeout=10)
            success = response.status_code == 401
            self.log_test("AI chat without auth", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("AI chat without auth", False, f"Error: {str(e)}")

        # Test panic button endpoint
        try:
            panic_data = {"user_id": "test_user", "severity": "moderate"}
            response = requests.post(f"{self.api_url}/ai/panic-button", json=panic_data, timeout=15)
            success = response.status_code in [200, 401]  # Either works or needs auth
            self.log_test("Panic button endpoint", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Panic button endpoint", False, f"Error: {str(e)}")

    def test_profile_endpoints(self):
        """Test user profile endpoints"""
        print("\n🔍 Testing Profile Endpoints...")
        
        # Test get profile without auth (should fail)
        try:
            response = requests.get(f"{self.api_url}/profile", timeout=10)
            success = response.status_code == 401
            self.log_test("Get profile without auth", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get profile without auth", False, f"Error: {str(e)}")

        # Test update profile without auth (should fail)
        try:
            profile_data = {"display_name": "Test User"}
            response = requests.patch(f"{self.api_url}/profile", json=profile_data, timeout=10)
            success = response.status_code == 401
            self.log_test("Update profile without auth", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Update profile without auth", False, f"Error: {str(e)}")

    def test_cors_and_headers(self):
        """Test CORS and header handling"""
        print("\n🔍 Testing CORS and Headers...")
        
        try:
            # Test OPTIONS request for CORS
            response = requests.options(f"{self.api_url}/health", timeout=10)
            success = response.status_code in [200, 204]
            self.log_test("CORS OPTIONS request", success, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("CORS OPTIONS request", False, f"Error: {str(e)}")

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Circle of Care API Testing Suite")
        print(f"📍 Testing against: {self.base_url}")
        print("=" * 60)

        # Run all test suites
        self.test_health_endpoints()
        self.test_auth_endpoints()
        self.test_communities_endpoints()
        self.test_ai_endpoints()
        self.test_profile_endpoints()
        self.test_cors_and_headers()

        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate < 70:
            print("⚠️  Warning: Low success rate detected")
        elif success_rate >= 90:
            print("🎉 Excellent! Most tests are passing")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = CircleOfCareAPITester()
    
    try:
        success = tester.run_all_tests()
        
        # Save detailed results
        results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": tester.base_url,
            "total_tests": tester.tests_run,
            "passed_tests": tester.tests_passed,
            "success_rate": (tester.tests_passed / tester.tests_run * 100) if tester.tests_run > 0 else 0,
            "test_details": tester.test_results
        }
        
        with open("/app/test_reports/backend_api_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: /app/test_reports/backend_api_results.json")
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())