#!/usr/bin/env python3
"""
VLOOKUP Script for HANWASH Indicators (Fixed Version)
Performs VLOOKUP between merged_indicators and HANWASH_IndicatorFrameworkRevised_July_11_2025
Uses ID column as the matching key to fill empty columns in the HANWASH file.
Handles data type inconsistencies (int vs string IDs).
"""

import pandas as pd
import os
from pathlib import Path

def perform_vlookup():
    """
    Perform VLOOKUP between merged_indicators and HANWASH indicator framework
    """
    
    # Define file paths
    base_dir = Path("/home/alexandrod/Desktop/Hanwash.mwater.dev/indicators")
    merged_indicators_file = base_dir / "output/merged_indicators.xlsx"
    hanwash_file = base_dir / "HANWASH_IndicatorFrameworkRevised_July_11_2025.xlsx"
    
    print("🔍 Starting VLOOKUP operation...")
    print(f"Source file (old data): {merged_indicators_file}")
    print(f"Target file (new framework): {hanwash_file}")
    
    # Read the merged indicators file (old source of truth)
    print("\n📖 Reading merged_indicators.xlsx...")
    merged_df = pd.read_excel(merged_indicators_file, sheet_name='Sheet1')
    print(f"Loaded {len(merged_df)} rows from merged_indicators")
    
    # Read the HANWASH framework file (new source of truth)
    print("\n📖 Reading HANWASH_IndicatorFrameworkRevised_July_11_2025.xlsx...")
    hanwash_df = pd.read_excel(hanwash_file, sheet_name='Sheet1')
    print(f"Loaded {len(hanwash_df)} rows from HANWASH framework")
    
    # Convert ID columns to string for consistent matching
    print("\n🔧 Converting ID columns to strings for consistent matching...")
    merged_df['ID'] = merged_df['ID'].astype(str)
    hanwash_df['ID'] = hanwash_df['ID'].astype(str)
    
    print(f"📊 merged_indicators ID types after conversion: {merged_df['ID'].dtype}")
    print(f"📊 hanwash ID types after conversion: {hanwash_df['ID'].dtype}")
    
    # Define the columns to update in HANWASH file with data from merged_indicators
    columns_to_update = [
        'Indicator group', 
        'Units', 
        'Baseline Value', 
        'Planned Value', 
        'current_value', 
        'Indicator Type'
    ]
    
    print(f"\n📋 Columns to update: {columns_to_update}")
    
    # Check which columns exist in both dataframes
    available_columns = [col for col in columns_to_update if col in merged_df.columns and col in hanwash_df.columns]
    print(f"✅ Available columns for update: {available_columns}")
    
    # Show current state - all should be null
    print("\n📊 Current state of target columns in HANWASH file:")
    for col in available_columns:
        null_count = hanwash_df[col].isnull().sum()
        print(f"  {col}: {null_count}/{len(hanwash_df)} null values")
    
    # Perform the merge (VLOOKUP equivalent)
    print(f"\n🔗 Performing VLOOKUP on ID column...")
    
    # Create a lookup dictionary from merged_indicators (using string IDs)
    lookup_dict = {}
    for _, row in merged_df.iterrows():
        row_id = str(row['ID'])
        lookup_dict[row_id] = {}
        for col in available_columns:
            lookup_dict[row_id][col] = row[col]
    
    print(f"Created lookup dictionary with {len(lookup_dict)} ID entries")
    
    # Update hanwash_df with data from lookup dictionary
    updates_made = 0
    matches_found = 0
    for idx, row in hanwash_df.iterrows():
        row_id = str(row['ID'])
        if row_id in lookup_dict:
            matches_found += 1
            for col in available_columns:
                # Only update if the target cell is null and source has data
                if pd.isnull(row[col]) and not pd.isnull(lookup_dict[row_id][col]):
                    hanwash_df.at[idx, col] = lookup_dict[row_id][col]
                    updates_made += 1
    
    print(f"\n✅ Made {updates_made} field updates")
    print(f"🎯 Found matches for {matches_found} out of {len(hanwash_df)} rows")
    
    # Show final state after updates
    print("\n📊 Final state of target columns in HANWASH file:")
    for col in available_columns:
        null_count = hanwash_df[col].isnull().sum()
        filled_count = len(hanwash_df) - null_count
        print(f"  {col}: {filled_count}/{len(hanwash_df)} filled, {null_count} null")
    
    # Create output file path
    output_file = base_dir / "HANWASH_IndicatorFrameworkRevised_July_11_2025_UPDATED.xlsx"
    
    # Backup original file if it exists
    if output_file.exists():
        backup_file = base_dir / f"HANWASH_IndicatorFrameworkRevised_July_11_2025_UPDATED_backup.xlsx"
        print(f"\n💾 Creating backup: {backup_file}")
        output_file.rename(backup_file)
    
    # Save the updated HANWASH file
    print(f"\n💾 Saving updated file: {output_file}")
    
    # Read all sheets from original file to preserve them
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Read all sheets from original
        original_xl = pd.ExcelFile(hanwash_file)
        for sheet_name in original_xl.sheet_names:
            if sheet_name == 'Sheet1':
                # Write the updated Sheet1
                hanwash_df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"  ✅ Saved updated {sheet_name}")
            else:
                # Copy other sheets as-is
                original_sheet = pd.read_excel(hanwash_file, sheet_name=sheet_name)
                original_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"  📋 Copied {sheet_name}")
    
    print(f"\n🎉 VLOOKUP operation completed successfully!")
    print(f"📄 Updated file saved as: {output_file}")
    
    # Show summary of matches
    hanwash_ids = set(hanwash_df['ID'].astype(str))
    merged_ids = set(merged_df['ID'].astype(str))
    matched_ids = hanwash_ids.intersection(merged_ids)
    unmatched_ids = hanwash_ids - merged_ids
    
    print(f"\n📈 Matching Summary:")
    print(f"  📊 Total IDs in HANWASH file: {len(hanwash_ids)}")
    print(f"  📊 Total IDs in merged_indicators: {len(merged_ids)}")
    print(f"  ✅ Matched IDs: {len(matched_ids)}")
    print(f"  ❌ Unmatched IDs in HANWASH: {len(unmatched_ids)}")
    
    if unmatched_ids:
        print(f"  📝 Unmatched ID examples: {list(unmatched_ids)[:5]}")
        print(f"  💡 These IDs exist in HANWASH but not in merged_indicators")
    
    return output_file

if __name__ == "__main__":
    try:
        output_file = perform_vlookup()
        print(f"\n✨ Script completed successfully!")
        print(f"📂 Check the updated file: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
