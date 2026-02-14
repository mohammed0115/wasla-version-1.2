#!/usr/bin/env python3
"""
Wasla Django Dashboard Backend API Testing
Tests authentication, dashboard views, and tenant context functionality
"""

import requests
import sys
from datetime import datetime
import json

class WaslaDashboardTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.tests_run = 0
        self.tests_passed = 0
        self.csrf_token = None
        
    def get_csrf_token(self):
        """Get CSRF token from auth page"""
        try:
            response = self.session.get(f"{self.base_url}/auth/?tab=login")
            if response.status_code == 200:
                # Extract CSRF token from cookies
                self.csrf_token = self.session.cookies.get('csrftoken')
                return True
        except Exception as e:
            print(f"❌ Failed to get CSRF token: {e}")
        return False

    def run_test(self, name, method, endpoint, expected_status, data=None, follow_redirects=True):
        """Run a single test"""
        url = f"{self.base_url}{endpoint}"
        headers = {}
        
        if data and self.csrf_token:
            data['csrfmiddlewaretoken'] = self.csrf_token
            headers['X-CSRFToken'] = self.csrf_token
            headers['Referer'] = url

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = self.session.get(url, allow_redirects=follow_redirects)
            elif method == 'POST':
                response = self.session.post(url, data=data, headers=headers, allow_redirects=follow_redirects)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                if response.history:
                    print(f"   Redirected from: {[r.url for r in response.history]}")
                    print(f"   Final URL: {response.url}")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Final URL: {response.url}")
                if response.text and len(response.text) < 500:
                    print(f"   Response: {response.text[:200]}...")

            return success, response

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, None

    def test_login(self, email, password):
        """Test login functionality"""
        print(f"\n🔐 Testing login with {email}")
        
        # Get CSRF token first
        if not self.get_csrf_token():
            return False
            
        login_data = {
            'action': 'login',
            'login-email': email,
            'login-password': password,
        }
        
        success, response = self.run_test(
            "User Login",
            "POST", 
            "/auth/?tab=login",
            302,  # Expect redirect after successful login
            data=login_data
        )
        
        if success and response:
            # Check if we're redirected to dashboard or setup
            final_url = response.url
            if '/dashboard/' in final_url or '/store/' in final_url:
                print(f"✅ Login successful, redirected to: {final_url}")
                return True
            else:
                print(f"❌ Login failed, unexpected redirect to: {final_url}")
        
        return False

    def test_dashboard_authentication(self):
        """Test dashboard pages require authentication"""
        print(f"\n🔒 Testing Dashboard Authentication Requirements")
        
        # Test dashboard home without authentication
        success, response = self.run_test(
            "Dashboard Home (Unauthenticated)",
            "GET",
            "/dashboard/",
            302  # Should redirect to login
        )
        
        if success and response and '/accounts/login/' in response.url:
            print("✅ Dashboard correctly redirects unauthenticated users to login")
            return True
        else:
            print("❌ Dashboard authentication check failed")
            return False

    def test_dashboard_pages(self):
        """Test all dashboard pages when authenticated"""
        dashboard_pages = [
            ("/dashboard/", "Dashboard Home"),
            ("/dashboard/overview", "Dashboard Overview"),
            ("/dashboard/orders", "Dashboard Orders"),
            ("/dashboard/products", "Dashboard Products"),
            ("/dashboard/ai/tools", "AI Tools"),
            ("/dashboard/store/info", "Store Settings"),
            ("/dashboard/settlements", "Settlements"),
        ]
        
        print(f"\n📊 Testing Dashboard Pages (Authenticated)")
        
        all_passed = True
        for endpoint, name in dashboard_pages:
            success, response = self.run_test(
                name,
                "GET",
                endpoint,
                200  # Should load successfully
            )
            
            if not success:
                all_passed = False
                
            # Check for key elements in response
            if success and response:
                content = response.text.lower()
                if 'dashboard' in content and 'sidebar' in content:
                    print(f"   ✅ Page contains expected dashboard elements")
                else:
                    print(f"   ⚠️  Page may be missing dashboard elements")
        
        return all_passed

    def test_language_switching(self):
        """Test language switching functionality"""
        print(f"\n🌐 Testing Language Switching")
        
        # Test language switch endpoint
        success, response = self.run_test(
            "Language Switch (POST)",
            "POST",
            "/i18n/setlang/",
            302,  # Should redirect
            data={'language': 'en', 'next': '/dashboard/overview'}
        )
        
        return success

    def test_tenant_context(self):
        """Test tenant context is properly set"""
        print(f"\n🏪 Testing Tenant Context")
        
        # Test a page that requires tenant context
        success, response = self.run_test(
            "Store Settings (Tenant Required)",
            "GET",
            "/dashboard/store/info",
            200
        )
        
        if success and response:
            content = response.text
            if 'tenant' in content.lower() or 'store' in content.lower():
                print("   ✅ Tenant context appears to be working")
                return True
            else:
                print("   ⚠️  Tenant context may not be properly set")
        
        return success

def main():
    """Main test execution"""
    print("🚀 Starting Wasla Dashboard Backend Tests")
    print("=" * 50)
    
    tester = WaslaDashboardTester("http://localhost:8000")
    
    # Test 1: Dashboard authentication (unauthenticated)
    auth_test_passed = tester.test_dashboard_authentication()
    
    # Test 2: Login with test credentials
    login_success = tester.test_login("merchant@test.com", "test1234")
    
    if not login_success:
        print("\n❌ Login failed - cannot proceed with authenticated tests")
        print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
        return 1
    
    # Test 3: Dashboard pages (authenticated)
    dashboard_test_passed = tester.test_dashboard_pages()
    
    # Test 4: Language switching
    lang_test_passed = tester.test_language_switching()
    
    # Test 5: Tenant context
    tenant_test_passed = tester.test_tenant_context()
    
    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())