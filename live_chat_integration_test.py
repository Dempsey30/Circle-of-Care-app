#!/usr/bin/env python3
"""
Live Chat Integration Testing - Simulating Frontend Polling Behavior
Tests the complete live chat flow as the frontend would use it
"""

import requests
import json
import time
import threading
import sys
from datetime import datetime

class LiveChatIntegrationTester:
    def __init__(self, base_url="https://traumabridge.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.communities = []
        self.polling_active = False
        self.polling_results = []
        
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

    def get_communities(self):
        """Get communities for testing"""
        try:
            response = requests.get(f"{self.base_url}/api/communities", timeout=10)
            if response.status_code == 200:
                self.communities = response.json()
                return True
            return False
        except:
            return False

    def simulate_frontend_polling(self, community_id, duration_seconds=15):
        """Simulate frontend polling every 3 seconds like the real app"""
        print(f"🔄 Starting polling simulation for {duration_seconds} seconds...")
        
        self.polling_active = True
        self.polling_results = []
        start_time = time.time()
        poll_count = 0
        
        while self.polling_active and (time.time() - start_time) < duration_seconds:
            try:
                response = requests.get(
                    f"{self.base_url}/api/chat/{community_id}/messages?limit=20",
                    timeout=5
                )
                
                poll_count += 1
                if response.status_code == 200:
                    messages = response.json()
                    self.polling_results.append({
                        'poll_number': poll_count,
                        'timestamp': datetime.now().isoformat(),
                        'message_count': len(messages),
                        'success': True
                    })
                    print(f"   Poll #{poll_count}: {len(messages)} messages retrieved")
                else:
                    self.polling_results.append({
                        'poll_number': poll_count,
                        'timestamp': datetime.now().isoformat(),
                        'success': False,
                        'status_code': response.status_code
                    })
                    print(f"   Poll #{poll_count}: Failed with status {response.status_code}")
                
                time.sleep(3)  # Poll every 3 seconds like frontend
                
            except Exception as e:
                self.polling_results.append({
                    'poll_number': poll_count,
                    'timestamp': datetime.now().isoformat(),
                    'success': False,
                    'error': str(e)
                })
                print(f"   Poll #{poll_count}: Error - {e}")
                time.sleep(3)
        
        self.polling_active = False
        return poll_count

    def test_real_time_message_flow(self):
        """Test the complete real-time message flow"""
        if not self.communities:
            self.log_test("Real-time Message Flow", False, "No communities available")
            return False
            
        community = self.communities[0]  # Use first community
        community_id = community['id']
        community_name = community['name']
        
        print(f"🚀 Testing Real-time Message Flow in {community_name}")
        print("-" * 50)
        
        # Step 1: Get initial message count
        try:
            response = requests.get(f"{self.base_url}/api/chat/{community_id}/messages?limit=20")
            initial_count = len(response.json()) if response.status_code == 200 else 0
            print(f"📊 Initial message count: {initial_count}")
        except:
            initial_count = 0
        
        # Step 2: Start polling in background thread
        def background_polling():
            self.simulate_frontend_polling(community_id, duration_seconds=12)
        
        polling_thread = threading.Thread(target=background_polling)
        polling_thread.start()
        
        # Step 3: Send messages while polling is active
        time.sleep(2)  # Let polling start
        
        test_messages = [
            "Hello from integration test!",
            "Testing real-time updates",
            "This should appear in polling results"
        ]
        
        sent_messages = []
        for i, message in enumerate(test_messages):
            try:
                message_data = {
                    "message": message,
                    "user_name": f"IntegrationTester{i+1}",
                    "is_anonymous": True
                }
                
                response = requests.post(
                    f"{self.base_url}/api/chat/{community_id}/send",
                    json=message_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    sent_messages.append({
                        'message': message,
                        'message_id': result.get('message_id'),
                        'timestamp': result.get('timestamp')
                    })
                    print(f"📤 Sent: '{message}' (ID: {result.get('message_id', 'N/A')})")
                else:
                    print(f"❌ Failed to send: '{message}' (Status: {response.status_code})")
                
                time.sleep(2)  # Space out messages
                
            except Exception as e:
                print(f"❌ Error sending message '{message}': {e}")
        
        # Step 4: Wait for polling to complete
        polling_thread.join()
        
        # Step 5: Analyze results
        successful_polls = [r for r in self.polling_results if r.get('success', False)]
        total_polls = len(self.polling_results)
        
        # Check if message count increased during polling
        final_response = requests.get(f"{self.base_url}/api/chat/{community_id}/messages?limit=20")
        final_count = len(final_response.json()) if final_response.status_code == 200 else 0
        
        message_increase = final_count - initial_count
        expected_increase = len(sent_messages)
        
        success = (
            len(successful_polls) >= 3 and  # At least 3 successful polls
            message_increase >= expected_increase and  # Messages were stored
            total_polls >= 3  # Polling happened multiple times
        )
        
        details = f"Polls: {len(successful_polls)}/{total_polls} successful, Messages: {message_increase} increase (expected {expected_increase})"
        self.log_test("Real-time Message Flow Integration", success, details)
        
        return success

    def test_concurrent_users_simulation(self):
        """Simulate multiple users sending messages concurrently"""
        if not self.communities:
            self.log_test("Concurrent Users Simulation", False, "No communities available")
            return False
            
        community = self.communities[1] if len(self.communities) > 1 else self.communities[0]
        community_id = community['id']
        community_name = community['name']
        
        print(f"👥 Testing Concurrent Users in {community_name}")
        print("-" * 40)
        
        # Simulate 3 users sending messages simultaneously
        def send_user_messages(user_id, message_count=2):
            messages_sent = 0
            for i in range(message_count):
                try:
                    message_data = {
                        "message": f"Message {i+1} from User{user_id}",
                        "user_name": f"ConcurrentUser{user_id}",
                        "is_anonymous": True
                    }
                    
                    response = requests.post(
                        f"{self.base_url}/api/chat/{community_id}/send",
                        json=message_data,
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        messages_sent += 1
                        print(f"   User{user_id}: Sent message {i+1}")
                    
                    time.sleep(1)  # Small delay between messages
                    
                except Exception as e:
                    print(f"   User{user_id}: Error sending message {i+1} - {e}")
            
            return messages_sent
        
        # Get initial count
        try:
            response = requests.get(f"{self.base_url}/api/chat/{community_id}/messages?limit=20")
            initial_count = len(response.json()) if response.status_code == 200 else 0
        except:
            initial_count = 0
        
        # Start concurrent threads
        threads = []
        for user_id in range(1, 4):  # 3 users
            thread = threading.Thread(target=send_user_messages, args=(user_id, 2))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check final count
        time.sleep(2)  # Allow for processing
        try:
            response = requests.get(f"{self.base_url}/api/chat/{community_id}/messages?limit=20")
            final_count = len(response.json()) if response.status_code == 200 else 0
        except:
            final_count = initial_count
        
        messages_added = final_count - initial_count
        expected_messages = 6  # 3 users × 2 messages each
        
        success = messages_added >= expected_messages * 0.8  # Allow for some failures
        details = f"Added {messages_added} messages (expected {expected_messages})"
        self.log_test("Concurrent Users Simulation", success, details)
        
        return success

    def test_polling_reliability(self):
        """Test polling reliability over time"""
        if not self.communities:
            self.log_test("Polling Reliability", False, "No communities available")
            return False
            
        community = self.communities[0]
        community_id = community['id']
        community_name = community['name']
        
        print(f"⏱️ Testing Polling Reliability in {community_name}")
        print("-" * 40)
        
        # Perform 10 consecutive polls with 3-second intervals
        successful_polls = 0
        total_polls = 10
        response_times = []
        
        for i in range(total_polls):
            try:
                start_time = time.time()
                response = requests.get(
                    f"{self.base_url}/api/chat/{community_id}/messages?limit=20",
                    timeout=10
                )
                end_time = time.time()
                
                response_time = end_time - start_time
                response_times.append(response_time)
                
                if response.status_code == 200:
                    successful_polls += 1
                    messages = response.json()
                    print(f"   Poll {i+1}: ✓ {len(messages)} messages ({response_time:.2f}s)")
                else:
                    print(f"   Poll {i+1}: ❌ Status {response.status_code} ({response_time:.2f}s)")
                
                if i < total_polls - 1:  # Don't sleep after last poll
                    time.sleep(3)
                    
            except Exception as e:
                print(f"   Poll {i+1}: ❌ Error - {e}")
        
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        success_rate = successful_polls / total_polls
        
        success = success_rate >= 0.9 and avg_response_time < 2.0  # 90% success, under 2s avg
        details = f"Success rate: {success_rate:.1%}, Avg response time: {avg_response_time:.2f}s"
        self.log_test("Polling Reliability", success, details)
        
        return success

    def test_message_ordering(self):
        """Test that messages maintain proper chronological order"""
        if not self.communities:
            self.log_test("Message Ordering", False, "No communities available")
            return False
            
        community = self.communities[0]
        community_id = community['id']
        community_name = community['name']
        
        print(f"📅 Testing Message Ordering in {community_name}")
        print("-" * 40)
        
        # Send 3 messages with timestamps
        timestamp = int(time.time())
        test_messages = [
            f"Order test 1 - {timestamp}",
            f"Order test 2 - {timestamp}",
            f"Order test 3 - {timestamp}"
        ]
        
        sent_times = []
        for i, message in enumerate(test_messages):
            try:
                message_data = {
                    "message": message,
                    "user_name": f"OrderTester",
                    "is_anonymous": True
                }
                
                send_time = time.time()
                response = requests.post(
                    f"{self.base_url}/api/chat/{community_id}/send",
                    json=message_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    sent_times.append(send_time)
                    print(f"   Sent: '{message}'")
                
                time.sleep(1)  # 1 second between messages
                
            except Exception as e:
                print(f"   Error sending '{message}': {e}")
        
        # Retrieve messages and check order
        time.sleep(2)
        try:
            response = requests.get(f"{self.base_url}/api/chat/{community_id}/messages?limit=20")
            if response.status_code == 200:
                messages = response.json()
                
                # Find our test messages
                our_messages = [msg for msg in messages if f"Order test" in msg.get('message', '')]
                
                if len(our_messages) >= 3:
                    # Check if they're in chronological order (should be 1, 2, 3)
                    order_correct = True
                    for i in range(len(our_messages) - 1):
                        current_msg = our_messages[i]['message']
                        next_msg = our_messages[i + 1]['message']
                        
                        # Extract order numbers
                        current_order = int(current_msg.split('Order test ')[1].split(' -')[0])
                        next_order = int(next_msg.split('Order test ')[1].split(' -')[0])
                        
                        if current_order >= next_order:
                            order_correct = False
                            break
                    
                    success = order_correct
                    details = f"Found {len(our_messages)} test messages, order {'correct' if order_correct else 'incorrect'}"
                else:
                    success = False
                    details = f"Only found {len(our_messages)} of 3 test messages"
            else:
                success = False
                details = f"Failed to retrieve messages: {response.status_code}"
                
        except Exception as e:
            success = False
            details = f"Error checking message order: {e}"
        
        self.log_test("Message Ordering", success, details)
        return success

    def run_integration_tests(self):
        """Run all integration tests"""
        print("🚀 Starting Live Chat Integration Testing")
        print("=" * 60)
        
        # Get communities
        if not self.get_communities():
            print("❌ Cannot get communities - aborting tests")
            return False
        
        print(f"📋 Testing integration across {len(self.communities)} communities")
        print()
        
        # Run integration tests
        self.test_real_time_message_flow()
        self.test_concurrent_users_simulation()
        self.test_polling_reliability()
        self.test_message_ordering()
        
        return True

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 LIVE CHAT INTEGRATION TEST SUMMARY")
        print("=" * 60)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL INTEGRATION TESTS PASSED - Live Chat System Fully Working!")
        elif self.tests_passed >= self.tests_run * 0.8:
            print("✅ INTEGRATION MOSTLY WORKING - Minor issues detected")
        else:
            print("❌ INTEGRATION ISSUES - Live Chat system needs attention")
            
        return self.tests_passed >= self.tests_run * 0.8

def main():
    tester = LiveChatIntegrationTester()
    
    try:
        success = tester.run_integration_tests()
        overall_success = tester.print_summary()
        
        return 0 if overall_success else 1
        
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Critical error during integration testing: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())