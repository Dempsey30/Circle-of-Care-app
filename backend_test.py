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
    
    def test_communities_functionality(self):
        """Test communities endpoints - critical for the platform"""
        print("\n🏘️ Testing Communities Functionality...")
        
        # Test get all communities
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/communities")
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                communities = response.json()
                community_count = len(communities)
                
                # Check if we have the expected 6 communities
                expected_communities = [
                    "PTSD Recovery Room", "Chronic Pain Warriors", "Cancer Fighters & Survivors",
                    "Veterans Support Network", "Anxiety & Depression Support", "General Wellness Circle"
                ]
                
                found_communities = [c.get('name', '') for c in communities]
                all_present = all(name in found_communities for name in expected_communities)
                
                self.log_test("Get All Communities", True, 
                            f"Found {community_count} communities, all 6 expected: {all_present}", response_time)
                
                # Store communities for later tests
                self.communities = communities
                
                # Test community structure
                if communities:
                    first_community = communities[0]
                    required_fields = ['id', 'name', 'description', 'category', 'rules']
                    has_required_fields = all(field in first_community for field in required_fields)
                    self.log_test("Community Structure", has_required_fields,
                                f"Required fields present: {has_required_fields}", 0)
                    
                    # Test community rules (important for guidelines)
                    rules = first_community.get('rules', [])
                    has_rules = len(rules) > 0
                    self.log_test("Community Guidelines", has_rules,
                                f"Rules count: {len(rules)}", 0)
                
            else:
                self.log_test("Get All Communities", False, 
                            f"Status: {response.status_code}", response_time)
                self.communities = []
        except Exception as e:
            self.log_test("Get All Communities", False, f"Error: {str(e)}")
            self.communities = []
    
    def test_anonymous_posting(self):
        """Test anonymous posting functionality - major fix implemented"""
        print("\n📝 Testing Anonymous Posting Functionality...")
        
        if not hasattr(self, 'communities') or not self.communities:
            self.log_test("Anonymous Posting Setup", False, "No communities available for testing")
            return
            
        # Test posting to first community without authentication
        test_community = self.communities[0]
        community_id = test_community['id']
        
        post_data = {
            "title": "Test Anonymous Post",
            "content": "This is a test post to verify anonymous posting works correctly.",
            "is_anonymous": True,
            "support_type": "general"
        }
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/api/communities/{community_id}/posts",
                json=post_data,
                headers={"Content-Type": "application/json"}
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200 or response.status_code == 201:
                post_response = response.json()
                self.log_test("Anonymous Post Creation", True,
                            f"Post ID: {post_response.get('id', 'unknown')}", response_time)
                
                # Store post ID for later verification
                self.test_post_id = post_response.get('id')
            else:
                self.log_test("Anonymous Post Creation", False,
                            f"Status: {response.status_code}, Response: {response.text[:100]}", response_time)
        except Exception as e:
            self.log_test("Anonymous Post Creation", False, f"Error: {str(e)}")
    
    def test_community_posts_viewing(self):
        """Test viewing posts in communities"""
        print("\n👀 Testing Community Posts Viewing...")
        
        if not hasattr(self, 'communities') or not self.communities:
            self.log_test("Posts Viewing Setup", False, "No communities available for testing")
            return
            
        # Test getting posts from first community
        test_community = self.communities[0]
        community_id = test_community['id']
        
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/api/communities/{community_id}/posts")
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                posts = response.json()
                posts_count = len(posts)
                
                self.log_test("Get Community Posts", True,
                            f"Found {posts_count} posts in {test_community['name']}", response_time)
                
                # Check if posts have required structure
                if posts:
                    first_post = posts[0]
                    required_fields = ['id', 'title', 'content', 'created_at', 'author_id']
                    has_required_fields = all(field in first_post for field in required_fields)
                    self.log_test("Post Structure", has_required_fields,
                                f"Required fields present: {has_required_fields}", 0)
                else:
                    self.log_test("Post Structure", True, "No posts to verify structure", 0)
                    
            else:
                self.log_test("Get Community Posts", False,
                            f"Status: {response.status_code}", response_time)
        except Exception as e:
            self.log_test("Get Community Posts", False, f"Error: {str(e)}")
    
    def test_ai_endpoints_basic(self):
        """Test AI endpoints with basic functionality (previous issue area)"""
        print("\n🤖 Testing AI Endpoints (Previous Issue Area)...")
        
        # Test panic button endpoint (was completely broken before)
        panic_data = {
            "user_id": "test_user_123",
            "severity": "moderate",
            "trigger_description": "Testing panic button functionality"
        }
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{self.base_url}/api/ai/panic-button",
                json=panic_data,
                headers={"Content-Type": "application/json"},
                timeout=10  # Shorter timeout to detect if still hanging
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                panic_response = response.json()
                has_required_fields = all(field in panic_response for field in 
                                        ['immediate_response', 'emergency_contacts'])
                self.log_test("AI Panic Button", has_required_fields,
                            f"Response received with required fields: {has_required_fields}", response_time)
            else:
                self.log_test("AI Panic Button", False,
                            f"Status: {response.status_code}", response_time)
        except requests.exceptions.Timeout:
            self.log_test("AI Panic Button", False, "Request timed out (still broken)")
        except Exception as e:
            self.log_test("AI Panic Button", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Circle of Care Backend API Testing...")
        print(f"📍 Testing against: {self.base_url}")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Run all test suites
        self.test_health_endpoints()
        self.test_communities_functionality()
        self.test_anonymous_posting()
        self.test_community_posts_viewing()
        self.test_ai_endpoints_basic()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"📈 Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        print(f"⏱️  Total Tests: {self.tests_run}")
        
        # Save detailed results
        results_file = f"/app/test_reports/backend_api_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                "test_summary": {
                    "total_tests": self.tests_run,
                    "passed_tests": self.tests_passed,
                    "failed_tests": self.tests_run - self.tests_passed,
                    "success_rate": f"{(self.tests_passed/self.tests_run)*100:.1f}%",
                    "test_timestamp": datetime.now().isoformat()
                },
                "detailed_results": self.test_results
            }, indent=2)
        
        print(f"\n📄 Detailed results saved to: {results_file}")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = CircleOfCareAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Backend is functioning correctly.")
        return 0
    else:
        print(f"\n⚠️  Some tests failed. Check results above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())