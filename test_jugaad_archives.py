#!/usr/bin/env python3
"""
Test jugaad-data archives for historical F&O data
This should actually work!
"""

from jugaad_data import nse
import pandas as pd
from datetime import datetime, date, timedelta
import os

def test_bhavcopy_fo():
    """Test downloading F&O bhavcopy data"""
    print("🔍 Testing jugaad-data Archives for F&O Data...")
    print("=" * 60)
    
    try:
        print("✅ jugaad-data imported successfully")
        
        # Create archives object
        archives = nse.archives.NSEArchives()
        print(f"✅ NSEArchives created: {type(archives)}")
        
        # Test downloading today's F&O data
        today = date.today()
        print(f"\n📅 Testing date: {today}")
        
        # Create output directory
        output_dir = "jugaad_fo_data"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"📁 Created output directory: {output_dir}")
        
        # Test 1: Download today's F&O bhavcopy
        print("\n1. Testing F&O bhavcopy download...")
        try:
            archives.bhavcopy_fo_save(today, output_dir)
            print(f"   ✅ F&O bhavcopy downloaded for {today}")
            
            # Check what files were created
            files = os.listdir(output_dir)
            print(f"   📁 Files created: {files}")
            
        except Exception as e:
            print(f"   ❌ F&O bhavcopy error: {e}")
        
        # Test 2: Download yesterday's data
        print("\n2. Testing yesterday's data...")
        try:
            yesterday = today - timedelta(days=1)
            archives.bhavcopy_fo_save(yesterday, output_dir)
            print(f"   ✅ F&O bhavcopy downloaded for {yesterday}")
            
            # Check updated files
            files = os.listdir(output_dir)
            print(f"   📁 Total files: {files}")
            
        except Exception as e:
            print(f"   ❌ Yesterday's data error: {e}")
        
        # Test 3: Download last week's data
        print("\n3. Testing last week's data...")
        try:
            last_week = today - timedelta(days=7)
            archives.bhavcopy_fo_save(last_week, output_dir)
            print(f"   ✅ F&O bhavcopy downloaded for {last_week}")
            
        except Exception as e:
            print(f"   ❌ Last week's data error: {e}")
        
        # Test 4: Download last month's data
        print("\n4. Testing last month's data...")
        try:
            last_month = today - timedelta(days=30)
            archives.bhavcopy_fo_save(last_month, output_dir)
            print(f"   ✅ F&O bhavcopy downloaded for {last_month}")
            
        except Exception as e:
            print(f"   ❌ Last month's data error: {e}")
        
        # Show final results
        final_files = os.listdir(output_dir)
        print(f"\n📊 Final Results:")
        print(f"   Total files downloaded: {len(final_files)}")
        print(f"   Files: {final_files}")
        
        return True
        
    except Exception as e:
        print(f"❌ Archives test error: {e}")
        return False

def test_index_bhavcopy():
    """Test downloading index bhavcopy data"""
    print("\n📈 Testing Index Bhavcopy...")
    print("=" * 60)
    
    try:
        # Create indices archives object
        indices_archives = nse.archives.NSEIndicesArchives()
        print(f"✅ NSEIndicesArchives created: {type(indices_archives)}")
        
        # Test downloading index data
        today = date.today()
        output_dir = "jugaad_index_data"
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"📅 Testing index data for: {today}")
        
        try:
            indices_archives.bhavcopy_index_save(today, output_dir)
            print(f"   ✅ Index bhavcopy downloaded for {today}")
            
            # Check files
            files = os.listdir(output_dir)
            print(f"   📁 Index files: {files}")
            
        except Exception as e:
            print(f"   ❌ Index data error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Index test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Jugaad-Data Archives Test for Historical F&O Data")
    print("=" * 60)
    
    # Test 1: F&O bhavcopy
    fo_success = test_bhavcopy_fo()
    
    # Test 2: Index bhavcopy
    index_success = test_index_bhavcopy()
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"F&O Bhavcopy: {'✅ PASS' if fo_success else '❌ FAIL'}")
    print(f"Index Bhavcopy: {'✅ PASS' if index_success else '❌ FAIL'}")
    
    if fo_success:
        print("\n🎉 SUCCESS! We can now download historical F&O data!")
        print("This will give you the 1+ year of options data you need!")
        print("\nNext steps:")
        print("1. Download data for multiple dates")
        print("2. Parse and combine the data")
        print("3. Build your analysis framework")
    else:
        print("\n❌ F&O download failed. We need to investigate further.")

if __name__ == "__main__":
    main()
