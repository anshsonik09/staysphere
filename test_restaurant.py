#!/usr/bin/env python
"""
Enhanced test script to verify StaySphere Restaurant functionality
"""

import os
import sys
import django

# Add the project path
sys.path.append(r'c:\Users\Win11 Pro\Desktop\staysphere')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'staysphere.settings')
django.setup()

from restaurant.models import MenuCategory, FoodItem, Table, Order, TableReservation
from django.test import Client
from django.urls import reverse

def test_restaurant_models():
    """Test restaurant models are working"""
    print("Testing Restaurant Models...")
    
    try:
        # Test MenuCategory
        categories = MenuCategory.objects.all()
        print(f"[PASS] Menu Categories: {categories.count()} found")
        if categories.count() > 0:
            for category in categories[:3]:  # Show first 3 categories
                print(f"   - {category.name}")
        
        # Test FoodItem
        food_items = FoodItem.objects.all()
        print(f"[PASS] Food Items: {food_items.count()} found")
        if food_items.count() > 0:
            for item in food_items[:3]:  # Show first 3 items
                print(f"   - {item.name} (Rs.{item.price})")
        
        # Test Tables
        tables = Table.objects.all()
        print(f"[PASS] Tables: {tables.count()} found")
        if tables.count() > 0:
            for table in tables[:3]:  # Show first 3 tables
                print(f"   - {table.table_number} (Capacity: {table.capacity})")
        
        # Test Orders
        orders = Order.objects.all()
        print(f"[PASS] Orders: {orders.count()} found")
        
        # Test Table Reservations
        reservations = TableReservation.objects.all()
        print(f"[PASS] Table Reservations: {reservations.count()} found")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Model test failed: {e}")
        return False

def test_restaurant_views():
    """Test restaurant views are accessible"""
    print("\nTesting Restaurant Views...")
    
    client = Client()
    success_count = 0
    total_tests = 0
    
    # Test restaurant home
    try:
        total_tests += 1
        response = client.get('/restaurant/')
        if response.status_code == 200:
            print("[PASS] Restaurant Home: Working (200)")
            success_count += 1
        else:
            print(f"[FAIL] Restaurant Home: Status {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Restaurant Home: Error - {e}")
    
    # Test menu page
    try:
        total_tests += 1
        response = client.get('/restaurant/menu/')
        if response.status_code == 200:
            print("[PASS] Restaurant Menu: Working (200)")
            success_count += 1
        else:
            print(f"[FAIL] Restaurant Menu: Status {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Restaurant Menu: Error - {e}")
    
    # Test cart page (should redirect to login for unauthenticated users)
    try:
        total_tests += 1
        response = client.get('/restaurant/cart/')
        if response.status_code in [200, 302]:
            print(f"[PASS] Restaurant Cart: Working ({response.status_code})")
            success_count += 1
        else:
            print(f"[FAIL] Restaurant Cart: Status {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Restaurant Cart: Error - {e}")
    
    # Test order page
    try:
        total_tests += 1
        response = client.get('/restaurant/order/')
        if response.status_code in [200, 302]:
            print(f"[PASS] Restaurant Order: Working ({response.status_code})")
            success_count += 1
        else:
            print(f"[FAIL] Restaurant Order: Status {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Restaurant Order: Error - {e}")
    
    # Test table reservation page
    try:
        total_tests += 1
        response = client.get('/restaurant/table-reservation/')
        if response.status_code in [200, 302]:
            print(f"[PASS] Table Reservation: Working ({response.status_code})")
            success_count += 1
        else:
            print(f"[FAIL] Table Reservation: Status {response.status_code}")
    except Exception as e:
        print(f"[FAIL] Table Reservation: Error - {e}")
    
    print(f"\nViews Test Results: {success_count}/{total_tests} passed")
    return success_count == total_tests

def test_restaurant_urls():
    """Test restaurant URL patterns"""
    print("\nTesting Restaurant URLs...")
    
    try:
        from django.urls import resolve
        from restaurant.urls import urlpatterns
        
        print(f"[PASS] URL patterns found: {len(urlpatterns)}")
        
        # Test URL resolution
        urls_to_test = [
            '/restaurant/',
            '/restaurant/menu/',
            '/restaurant/cart/',
            '/restaurant/order/',
            '/restaurant/table-reservation/',
        ]
        
        for url in urls_to_test:
            try:
                resolve(url)
                print(f"[PASS] URL resolves: {url}")
            except Exception as e:
                print(f"[FAIL] URL resolution failed: {url} - {e}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] URL test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("StaySphere Restaurant Test Suite - Enhanced")
    print("=" * 60)
    
    test_results = []
    
    try:
        # Test models
        print("Initializing model tests...")
        model_result = test_restaurant_models()
        test_results.append(("Models", model_result))
        
        # Test views
        print("Initializing view tests...")
        view_result = test_restaurant_views()
        test_results.append(("Views", view_result))
        
        # Test URLs
        print("Initializing URL tests...")
        url_result = test_restaurant_urls()
        test_results.append(("URLs", url_result))
        
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Test initialization failed: {e}")
        print("Please check your Django setup and database connection.")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed_tests = sum(1 for _, result in test_results if result)
    total_tests = len(test_results)
    
    for test_name, result in test_results:
        status = "PASSED" if result else "FAILED"
        print(f"{test_name:15} : {status}")
    
    print(f"\nOverall Result: {passed_tests}/{total_tests} test groups passed")
    
    if passed_tests == total_tests:
        print("\nALL TESTS PASSED!")
        print("\nRestaurant is accessible at:")
        print("   - Home: http://127.0.0.1:8000/restaurant/")
        print("   - Menu: http://127.0.0.1:8000/restaurant/menu/")
        print("   - Cart: http://127.0.0.1:8000/restaurant/cart/")
        print("   - Order: http://127.0.0.1:8000/restaurant/order/")
        print("   - Table Reservation: http://127.0.0.1:8000/restaurant/table-reservation/")
        print("\nRestaurant system is ready for use!")
        return True
    else:
        print(f"\n{total_tests - passed_tests} test group(s) failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
