#!/usr/bin/env python3
"""
AI Companion and Critical Features Test for Circle of Care
Tests the PRIORITY 1 AI Companion functionality and other critical features
"""

import requests
import json
import time
import sys
from datetime import datetime

class CircleOfCareAITest:
    def __init__(self, base_url="https://traumabridge.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, details, response_data=None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "response_data": response_data,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        
        if response_data and not success:
            print(f"   Response: {json.dumps(response_data, indent=2)}")
    
    def test_panic_button_functionality(self):
        """Test panic button - critical mental health feature"""
        print("\n=== TESTING PANIC BUTTON (CRITICAL FEATURE) ===")
        
        try:
            # Test panic button without authentication (should still work for crisis)
            panic_data = {
                "user_id": "test_user_crisis",
                "trigger_description": "Feeling overwhelmed and anxious",
                "severity": "moderate"
            }
            
            response = self.session.post(
                f"{self.api_url}/ai/panic-button",
                json=panic_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required crisis response fields
                required_fields = ["immediate_response", "emergency_contacts", "grounding_techniques"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    # Check if AI guidance is present
                    has_ai_guidance = "ai_guidance" in data and data["ai_guidance"]
                    
                    # Check emergency contacts
                    contacts = data.get("emergency_contacts", [])
                    has_circle_contact = any("circleofcaresupport@pm.me" in str(contact) for contact in contacts)
                    has_phone_contact = any("250-902-9869" in str(contact) for contact in contacts)
                    
                    details = f"Status: {response.status_code}, AI Guidance: {has_ai_guidance}, Circle Contact: {has_circle_contact}, Phone: {has_phone_contact}"
                    self.log_test("Panic Button Response", True, details, data)
                    
                    # Test different severity levels
                    for severity in ["mild", "severe"]:
                        panic_data["severity"] = severity
                        sev_response = self.session.post(
                            f"{self.api_url}/ai/panic-button",
                            json=panic_data,
                            timeout=10
                        )
                        
                        if sev_response.status_code == 200:
                            self.log_test(f"Panic Button - {severity} severity", True, f"Status: {sev_response.status_code}")
                        else:
                            self.log_test(f"Panic Button - {severity} severity", False, f"Status: {sev_response.status_code}")
                else:
                    self.log_test("Panic Button Response", False, f"Missing required fields: {missing_fields}", data)
            else:
                self.log_test("Panic Button Response", False, f"Status: {response.status_code}", response.text)
                
        except requests.exceptions.Timeout:
            self.log_test("Panic Button Response", False, "Request timeout - critical issue for crisis support")
        except Exception as e:
            self.log_test("Panic Button Response", False, f"Error: {str(e)}")
    
    def test_ai_chat_without_auth(self):
        """Test AI chat endpoint behavior without authentication"""
        print("\n=== TESTING AI CHAT ENDPOINT ===")
        
        try:
            chat_data = {
                "message": "I'm feeling anxious and need support",
                "is_panic": False
            }
            
            response = self.session.post(
                f"{self.api_url}/ai/chat",
                json=chat_data,
                timeout=10
            )
            
            # Should return 401 without authentication
            if response.status_code == 401:
                self.log_test("AI Chat Authentication Check", True, "Properly requires authentication (401)")
            else:
                self.log_test("AI Chat Authentication Check", False, f"Unexpected status: {response.status_code}")
                
        except Exception as e:
            self.log_test("AI Chat Authentication Check", False, f"Error: {str(e)}")
    
    def test_communities_functionality(self):
        """Test communities endpoint - should work without auth for browsing"""
        print("\n=== TESTING COMMUNITIES FUNCTIONALITY ===")
        
        try:
            response = self.session.get(f"{self.api_url}/communities", timeout=10)
            
            if response.status_code == 200:
                communities = response.json()
                
                # Check for expected communities
                expected_communities = ["PTSD", "Veterans", "Cancer", "Chronic Pain", "Mental Health", "General Wellness"]
                found_communities = []
                
                for community in communities:
                    name = community.get("name", "")
                    for expected in expected_communities:
                        if expected.lower() in name.lower():
                            found_communities.append(expected)
                            break
                
                details = f"Status: {response.status_code}, Communities found: {len(communities)}, Expected types found: {len(found_communities)}/{len(expected_communities)}"
                self.log_test("Communities Endpoint", True, details)
                
                # Test community posts endpoint
                if communities:
                    community_id = communities[0].get("id")
                    if community_id:
                        posts_response = self.session.get(
                            f"{self.api_url}/communities/{community_id}/posts",
                            timeout=10
                        )
                        
                        if posts_response.status_code == 200:
                            posts = posts_response.json()
                            self.log_test("Community Posts", True, f"Status: {posts_response.status_code}, Posts: {len(posts)}")
                        else:
                            self.log_test("Community Posts", False, f"Status: {posts_response.status_code}")
            else:
                self.log_test("Communities Endpoint", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Communities Endpoint", False, f"Error: {str(e)}")
    
    def test_contact_info_endpoint(self):
        """Test contact information endpoint"""
        print("\n=== TESTING CONTACT INFO ENDPOINT ===")
        
        try:
            response = self.session.get(f"{self.api_url}/contact-info", timeout=10)
            
            if response.status_code == 200:
                contact_info = response.json()
                
                # Check for required contact information
                has_email = "circleofcaresupport@pm.me" in str(contact_info)
                has_phone = "250-902-9869" in str(contact_info)
                has_creator = "Brent Dempsey" in str(contact_info)
                
                details = f"Status: {response.status_code}, Email: {has_email}, Phone: {has_phone}, Creator: {has_creator}"
                self.log_test("Contact Info Endpoint", True, details, contact_info)
            else:
                self.log_test("Contact Info Endpoint", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Contact Info Endpoint", False, f"Error: {str(e)}")
    
    def test_health_endpoints(self):
        """Test health and status endpoints"""
        print("\n=== TESTING HEALTH ENDPOINTS ===")
        
        endpoints = [
            ("Root Endpoint", ""),
            ("Health Check", "/health")
        ]
        
        for name, endpoint in endpoints:
            try:
                response = self.session.get(f"{self.api_url}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    self.log_test(name, True, f"Status: {response.status_code}")
                else:
                    self.log_test(name, False, f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_test(name, False, f"Error: {str(e)}")
    
    def test_authentication_endpoints(self):
        """Test authentication-related endpoints"""
        print("\n=== TESTING AUTHENTICATION ENDPOINTS ===")
        
        # Test session endpoint without X-Session-ID
        try:
            response = self.session.post(f"{self.api_url}/auth/session", timeout=10)
            
            if response.status_code == 400:
                self.log_test("Session Without Header", True, "Properly rejects missing X-Session-ID (400)")
            else:
                self.log_test("Session Without Header", False, f"Unexpected status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Session Without Header", False, f"Error: {str(e)}")
        
        # Test /auth/me without authentication
        try:
            response = self.session.get(f"{self.api_url}/auth/me", timeout=10)
            
            if response.status_code == 401:
                self.log_test("Auth Me Without Token", True, "Properly requires authentication (401)")
            else:
                self.log_test("Auth Me Without Token", False, f"Unexpected status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Auth Me Without Token", False, f"Error: {str(e)}")
    
    def test_websocket_availability(self):
        """Test if WebSocket endpoint is available (basic connectivity test)"""
        print("\n=== TESTING WEBSOCKET AVAILABILITY ===")
        
        # We can't easily test WebSocket functionality without proper auth,
        # but we can test if the endpoint exists by checking the HTTP response
        try:
            # WebSocket endpoints typically return 400 or 426 for HTTP requests
            ws_url = f"{self.base_url}/api/chat/live/test-community"
            response = self.session.get(ws_url, timeout=5)
            
            # WebSocket endpoints should not return 404
            if response.status_code != 404:
                self.log_test("WebSocket Endpoint Availability", True, f"Endpoint exists (Status: {response.status_code})")
            else:
                self.log_test("WebSocket Endpoint Availability", False, "WebSocket endpoint not found (404)")
                
        except Exception as e:
            self.log_test("WebSocket Endpoint Availability", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🔍 CIRCLE OF CARE AI COMPANION & CRITICAL FEATURES TEST")
        print("=" * 60)
        print(f"Testing against: {self.base_url}")
        print(f"Started at: {datetime.now().isoformat()}")
        print()
        
        # Run all tests
        self.test_health_endpoints()
        self.test_panic_button_functionality()  # PRIORITY 1
        self.test_ai_chat_without_auth()
        self.test_communities_functionality()
        self.test_contact_info_endpoint()
        self.test_authentication_endpoints()
        self.test_websocket_availability()
        
        # Generate summary
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print("\n" + "=" * 60)
        print("🏁 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Identify critical issues
        critical_failures = []
        for result in self.test_results:
            if not result["success"] and any(keyword in result["test"].lower() for keyword in ["panic", "ai", "crisis"]):
                critical_failures.append(result["test"])
        
        if critical_failures:
            print(f"\n🚨 CRITICAL FAILURES: {len(critical_failures)}")
            for failure in critical_failures:
                print(f"   - {failure}")
        
        # Save detailed results
        report = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": success_rate,
            "critical_failures": critical_failures,
            "test_details": self.test_results
        }
        
        with open("/app/test_reports/ai_companion_test_results.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: /app/test_reports/ai_companion_test_results.json")
        
        return success_rate >= 80  # Return True if success rate is good

if __name__ == "__main__":
    tester = CircleOfCareAITest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)