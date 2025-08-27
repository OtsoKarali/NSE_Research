#!/usr/bin/env python3
"""
Debug script to understand nsepython data structure
"""

import nsepython as nse
import json

def debug_nifty_structure():
    """Debug the actual structure of NIFTY options data"""
    print("🔍 Debugging NIFTY Options Data Structure...")
    print("=" * 60)
    
    try:
        # Get NIFTY options
        nifty_options = nse.nse_optionchain_scrapper('NIFTY')
        
        print(f"Type of nifty_options: {type(nifty_options)}")
        print(f"Length: {len(nifty_options) if hasattr(nifty_options, '__len__') else 'N/A'}")
        
        if isinstance(nifty_options, list):
            print("\nIt's a list. First few items:")
            for i, item in enumerate(nifty_options[:3]):
                print(f"Item {i}: {type(item)} - {item}")
                
        elif isinstance(nifty_options, dict):
            print("\nIt's a dict. Keys:")
            for key in nifty_options.keys():
                print(f"  {key}: {type(nifty_options[key])}")
                
                if isinstance(nifty_options[key], dict):
                    print(f"    Sub-keys: {list(nifty_options[key].keys())}")
                elif isinstance(nifty_options[key], list):
                    print(f"    List length: {len(nifty_options[key])}")
                    if len(nifty_options[key]) > 0:
                        print(f"    First item type: {type(nifty_options[key][0])}")
        
        # Try to find the actual options data
        print("\n🔍 Searching for options data...")
        
        def search_for_options(obj, path=""):
            """Recursively search for options data"""
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if key.lower() in ['ce', 'pe', 'call', 'put', 'options']:
                        print(f"Found potential options key: {current_path}")
                        print(f"  Type: {type(value)}")
                        if isinstance(value, list) and len(value) > 0:
                            print(f"  Length: {len(value)}")
                            print(f"  Sample: {value[0]}")
                    search_for_options(value, current_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj[:2]):  # Only check first 2 items
                    search_for_options(item, f"{path}[{i}]")
        
        search_for_options(nifty_options)
        
        # Save raw data for inspection
        with open('nifty_raw_data.json', 'w') as f:
            json.dump(nifty_options, f, indent=2, default=str)
        print(f"\n💾 Raw data saved to: nifty_raw_data.json")
        
    except Exception as e:
        print(f"❌ Debug error: {e}")

def main():
    """Main debug function"""
    print("🚀 NSE Python Data Structure Debug")
    print("=" * 60)
    
    debug_nifty_structure()
    
    print("\n" + "=" * 60)
    print("DEBUG COMPLETED")

if __name__ == "__main__":
    main()
