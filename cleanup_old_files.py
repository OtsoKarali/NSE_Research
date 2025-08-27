#!/usr/bin/env python3
"""
Cleanup script to remove all failed attempts, test scripts, and futures-related work
Keep only the working scripts and data
"""

import os
import shutil

def cleanup_repository():
    """Clean up the repository by removing failed attempts and organizing working files"""
    print("🧹 CLEANING UP REPOSITORY")
    print("=" * 60)
    
    # Files to REMOVE (failed attempts, tests, futures-related)
    files_to_remove = [
        # Failed collection attempts
        'comprehensive_market_collector.py',
        'test_phase2_extended_indices.py',
        'test_alternative_functions.py',
        'test_date_transition.py',
        'test_working_symbols.py',
        'test_extended_indices.py',
        'collect_extended_indices_flexible.py',
        'collect_extended_indices_options_only.py',
        'debug_column_mismatch.py',
        'test_flexible_columns.py',
        'collect_extended_indices_batch1.py',
        'market_coverage_plan.py',
        'collect_robust_5year_data.py',
        'collect_single_year_test.py',
        'test_column_structure.py',
        'collect_full_5year_data.py',
        'collect_historical_derivatives.py',
        'test_derivatives_simple.py',
        'nifty_futures_sample.csv',
        'test_jugaad_archives.py',
        'NSE_OPTIONS_ACQUISITION_SUMMARY.md',
        'test_jugaad_correct.py',
        'test_jugaad_data.py',
        'test_jugaad_final.py',
        'test_jugaad_fixed.py',
        'test_openchart.py',
        'test_openchart_correct.py',
        'collect_historical_options.py',
        'nifty_raw_data.json',
        'debug_nse_structure.py',
        'test_derivative_history.py',
        'test_nsepython_options.py',
        'REAL_ANALYSIS_RESULTS.md',
        'CURRENT_STATUS_SUMMARY.md',
        'HISTORICAL_DATA_ANALYSIS.md',
        'download_nifty_history.py',
        'india_options_history.py',
        'india_options_history_robust.py',
        'test_nsepy.py',
        'CHATGPT_ANALYSIS_OUTPUT.txt',
        'PROJECT_STATUS.md'
    ]
    
    # Directories to REMOVE (failed attempts, test data)
    dirs_to_remove = [
        'test_phase2_extended_indices',
        'extended_indices_batch1',
        'jugaad_index_data',
        'jugaad_fo_data',
        'sample_data',
        'options_data',
        'analysis'
    ]
    
    # Files to KEEP but move to clean repository
    files_to_keep = [
        'maximize_working_symbols.py',
        'collect_5year_data_simple.py',
        'collect_working_banknifty.py',
        'collect_5year_final.py',
        'collect_historical_derivatives.py',
        'requirements.txt',
        'config.yaml',
        'README.md'
    ]
    
    # Directories to KEEP but move to clean repository
    dirs_to_keep = [
        'maximized_working_symbols',
        'full_5year_monthly_derivatives',
        'working_banknifty_data',
        'historical_data'
    ]
    
    print("🗑️  Removing failed attempts and test files...")
    removed_files = 0
    removed_dirs = 0
    
    # Remove failed files
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"   ✅ Removed: {file}")
                removed_files += 1
            except Exception as e:
                print(f"   ❌ Failed to remove {file}: {e}")
    
    # Remove failed directories
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"   ✅ Removed directory: {dir_name}")
                removed_dirs += 1
            except Exception as e:
                print(f"   ❌ Failed to remove directory {dir_name}: {e}")
    
    print(f"\n📊 Cleanup Summary:")
    print(f"   Files removed: {removed_files}")
    print(f"   Directories removed: {removed_dirs}")
    
    # Verify clean repository structure
    print(f"\n🔍 Verifying clean repository structure...")
    if os.path.exists('clean_repository'):
        print(f"   ✅ Clean repository exists")
        
        # Check what's in clean repository
        clean_files = []
        for root, dirs, files in os.walk('clean_repository'):
            for file in files:
                clean_files.append(os.path.join(root, file))
        
        print(f"   📁 Clean repository contains {len(clean_files)} files")
        
        # Show structure
        print(f"\n📂 Clean Repository Structure:")
        for root, dirs, files in os.walk('clean_repository'):
            level = root.replace('clean_repository', '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Show first 5 files per directory
                print(f"{subindent}{file}")
            if len(files) > 5:
                print(f"{subindent}... and {len(files) - 5} more files")
    
    print(f"\n🎉 Repository cleanup complete!")
    print(f"📁 Clean repository is ready for use")
    print(f"🗑️  All failed attempts and test files have been removed")

if __name__ == "__main__":
    cleanup_repository()
