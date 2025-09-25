#!/usr/bin/env python3
"""
Live Chat Backend API Testing - HTTP-based Chat System
Testing the new HTTP-based live chat implementation that replaced WebSocket
"""

import requests
import json
import time
import sys
from datetime import datetime

class LiveChatTester:
    def __init__(self, base_url="https://traumabridge.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.communities = []
        
    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED")
        if details:
            print(f"   Details: {details}")
        print()

    def test_get_communities(self):
        """Get all communities to test chat across them"""
        try:
            response = requests.get(f"{self.base_url}/api/communities", timeout=10)
            success = response.status_code == 200
            
            if success:
                self.communities = response.json()
                details = f"Found {len(self.communities)} communities: {[c['name'] for c in self.communities[:3]]}"
            else:
                details = f"Status: {response.status_code}"
                
            self.log_test("Get Communities for Chat Testing", success, details)
            return success
            
        except Exception as e:
            self.log_test("Get Communities for Chat Testing", False, f"Error: {str(e)}")
            return False

    def test_send_chat_message(self, community_id, community_name, message_text, user_name="TestUser"):
        """Test sending a chat message to a community"""
        try:
            message_data = {
                "message": message_text,
                "user_name": user_name,
                "is_anonymous": True
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat/{community_id}/send",
                json=message_data,
                timeout=10
            )
            
            success = response.status_code == 200
            
            if success:
                result = response.json()
                details = f"Message sent to {community_name}. ID: {result.get('message_id', 'N/A')}, Status: {result.get('status', 'N/A')}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:100]}"
                
            self.log_test(f"Send Chat Message to {community_name}", success, details)
            return success, response.json() if success else {}
            
        except Exception as e:
            self.log_test(f"Send Chat Message to {community_name}", False, f"Error: {str(e)}")
            return False, {}

    def test_get_chat_messages(self, community_id, community_name, expected_count=None):
        """Test retrieving chat messages from a community"""
        try:
            response = requests.get(
                f"{self.base_url}/api/chat/{community_id}/messages?limit=20",
                timeout=10
            )
            
            success = response.status_code == 200
            
            if success:
                messages = response.json()
                details = f"Retrieved {len(messages)} messages from {community_name}"
                if expected_count is not None:
                    if len(messages) >= expected_count:
                        details += f" (Expected at least {expected_count} ✓)"
                    else:
                        details += f" (Expected at least {expected_count} ❌)"
                        success = False
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:100]}"
                
            self.log_test(f"Get Chat Messages from {community_name}", success, details)
            return success, response.json() if success else []
            
        except Exception as e:
            self.log_test(f"Get Chat Messages from {community_name}", False, f"Error: {str(e)}")
            return False, []

    def test_content_filtering(self, community_id, community_name):
        """Test content filtering blocks inappropriate content"""
        blocked_messages = [
            "Let's talk about politics and Trump",
            "Biden is terrible for this country", 
            "This government sucks",
            "Fuck this shit damn"
        ]
        
        blocked_count = 0
        for message in blocked_messages:
            try:
                message_data = {
                    "message": message,
                    "user_name": "FilterTester",
                    "is_anonymous": True
                }
                
                response = requests.post(
                    f"{self.base_url}/api/chat/{community_id}/send",
                    json=message_data,
                    timeout=10
                )
                
                if response.status_code == 400:  # Should be blocked
                    blocked_count += 1
                    print(f"   ✓ Blocked: '{message[:30]}...'")
                else:
                    print(f"   ❌ Not blocked: '{message[:30]}...' (Status: {response.status_code})")
                    
            except Exception as e:
                print(f"   Error testing filter for '{message[:20]}...': {e}")
        
        success = blocked_count >= 2  # At least 2 should be blocked
        details = f"Blocked {blocked_count}/{len(blocked_messages)} inappropriate messages"
        self.log_test(f"Content Filtering in {community_name}", success, details)
        return success

    def test_message_persistence(self, community_id, community_name):
        """Test that messages persist and can be retrieved"""
        # Send a unique test message
        timestamp = int(time.time())
        test_message = f"Persistence test message {timestamp}"
        
        # Send message
        send_success, send_result = self.test_send_chat_message(
            community_id, community_name, test_message, "PersistenceTest"
        )
        
        if not send_success:
            return False
            
        # Wait a moment
        time.sleep(2)
        
        # Retrieve messages and check if our message is there
        get_success, messages = self.test_get_chat_messages(community_id, community_name)
        
        if not get_success:
            return False
            
        # Look for our test message
        found_message = False
        for msg in messages:
            if test_message in msg.get('message', ''):
                found_message = True
                break
                
        success = found_message
        details = f"Test message {'found' if found_message else 'not found'} in retrieved messages"
        self.log_test(f"Message Persistence in {community_name}", success, details)
        return success

    def test_anonymous_vs_named_messaging(self, community_id, community_name):
        """Test both anonymous and named user messaging"""
        # Test anonymous message
        anon_success, anon_result = self.test_send_chat_message(
            community_id, community_name, "Anonymous test message", "AnonymousUser"
        )
        
        # Test named message  
        named_success, named_result = self.test_send_chat_message(
            community_id, community_name, "Named user test message", "NamedUser"
        )
        
        success = anon_success and named_success
        details = f"Anonymous: {'✓' if anon_success else '❌'}, Named: {'✓' if named_success else '❌'}"
        self.log_test(f"Anonymous vs Named Messaging in {community_name}", success, details)
        return success

    def test_empty_message_validation(self, community_id, community_name):
        """Test that empty messages are rejected"""
        try:
            message_data = {
                "message": "",  # Empty message
                "user_name": "EmptyTester",
                "is_anonymous": True
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat/{community_id}/send",
                json=message_data,
                timeout=10
            )
            
            # Should return 400 for empty message
            success = response.status_code == 400
            details = f"Empty message validation: Status {response.status_code} ({'✓' if success else '❌'})"
            self.log_test(f"Empty Message Validation in {community_name}", success, details)
            return success
            
        except Exception as e:
            self.log_test(f"Empty Message Validation in {community_name}", False, f"Error: {str(e)}")
            return False

    def run_comprehensive_chat_tests(self):
        """Run all live chat tests across communities"""
        print("🚀 Starting Comprehensive Live Chat Backend Testing")
        print("=" * 60)
        
        # Get communities first
        if not self.test_get_communities():
            print("❌ Cannot proceed without communities")
            return False
            
        if len(self.communities) == 0:
            print("❌ No communities found")
            return False
            
        print(f"📋 Testing chat functionality across {len(self.communities)} communities")
        print()
        
        # Test core functionality on first 3 communities (to save time)
        test_communities = self.communities[:3]
        
        for community in test_communities:
            community_id = community['id']
            community_name = community['name']
            
            print(f"🏥 Testing {community_name}")
            print("-" * 40)
            
            # Core chat functionality tests
            self.test_send_chat_message(community_id, community_name, "Hello from test suite!")
            self.test_get_chat_messages(community_id, community_name)
            self.test_content_filtering(community_id, community_name)
            self.test_message_persistence(community_id, community_name)
            self.test_anonymous_vs_named_messaging(community_id, community_name)
            self.test_empty_message_validation(community_id, community_name)
            
            print()
        
        # Test basic send/receive on remaining communities
        remaining_communities = self.communities[3:]
        if remaining_communities:
            print("🔄 Quick tests on remaining communities")
            print("-" * 40)
            
            for community in remaining_communities:
                community_id = community['id']
                community_name = community['name']
                
                self.test_send_chat_message(community_id, community_name, f"Quick test in {community_name}")
                self.test_get_chat_messages(community_id, community_name, expected_count=1)
        
        return True

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 LIVE CHAT BACKEND TEST SUMMARY")
        print("=" * 60)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED - Live Chat Backend is Working!")
        elif self.tests_passed >= self.tests_run * 0.8:
            print("✅ MOSTLY WORKING - Minor issues detected")
        else:
            print("❌ SIGNIFICANT ISSUES - Live Chat needs attention")
            
        return self.tests_passed >= self.tests_run * 0.8

def main():
    tester = LiveChatTester()
    
    try:
        success = tester.run_comprehensive_chat_tests()
        tester.print_summary()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Critical error during testing: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())