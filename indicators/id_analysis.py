import pandas as pd
import os
import re
from fuzzywuzzy import fuzz, process

def normalize_string(s):
    """
    Normalize a string by:
    1. Stripping leading/trailing whitespace
    2. Removing extra internal whitespace
    3. Standardizing percentage/number representations
    """
    if not isinstance(s, str):
        return s
    
    # Strip leading/trailing whitespace and normalize internal whitespace
    normalized = ' '.join(s.strip().split())
    
    # Standardize percentage representations
    normalized = re.sub(r'\bpercent\b', '%', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\bpercentage\b', '%', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\b%\b', '%', normalized)
    
    # Standardize number representations
    normalized = re.sub(r'\b#\b', 'number', normalized)
    normalized = re.sub(r'\bnum\b', 'number', normalized, flags=re.IGNORECASE)
    normalized = re.sub(r'\bno\.\b', 'number', normalized, flags=re.IGNORECASE)
    
    # Remove extra spaces around punctuation
    normalized = re.sub(r'\s+\.\s*', '. ', normalized)
    normalized = re.sub(r'\s+,', ',', normalized)
    normalized = re.sub(r',\s+', ', ', normalized)
    normalized = re.sub(r'\s+\(', '(', normalized)
    normalized = re.sub(r'\)\s+', ') ', normalized)
    
    # Final whitespace cleanup
    normalized = ' '.join(normalized.split())
    
    return normalized

def create_comprehensive_analysis():
    """
    Create a comprehensive analysis with all outputs in one master file.
    """
    
    # File paths
    translated_file = "indicateur_interim_translated.xlsx"
    merged_file = "output/merged_indicators.xlsx"
    master_output_file = "id_master_analysis.xlsx"
    
    print("🔍 Starting comprehensive analysis...")
    
    # Read the files
    print("📖 Reading input files...")
    
    # Read the translated file (French + English)
    df_translated = pd.read_excel(translated_file, sheet_name='Sheet1')
    print(f"   Translated file: {len(df_translated)} indicators")
    
    # Read the merged indicators (source of truth)
    df_merged = pd.read_excel(merged_file, sheet_name='Sheet1')
    print(f"   Merged file: {len(df_merged)} rows")
    
    # Filter merged dataframe to only rows with indicators (exclude header/empty rows)
    df_merged_indicators = df_merged[df_merged['Indicator'].notna() & (df_merged['Indicator'] != '')]
    print(f"   Merged file with indicators: {len(df_merged_indicators)} indicators")
    
    # Normalize the indicator strings in both dataframes
    print("\n🔄 Normalizing indicator strings...")
    
    df_translated['indicator_normalized'] = df_translated['indicators_translated'].apply(normalize_string)
    df_merged_indicators['indicator_normalized'] = df_merged_indicators['Indicator'].apply(normalize_string)
    
    # Create lists of normalized indicators for fuzzy matching
    translated_indicators = df_translated['indicator_normalized'].tolist()
    merged_indicators = df_merged_indicators['indicator_normalized'].tolist()
    
    # Create mapping from normalized to original French
    normalized_to_french = {}
    for idx, row in df_translated.iterrows():
        if pd.notna(row['indicator_normalized']) and row['indicator_normalized']:
            normalized_to_french[row['indicator_normalized']] = {
                'french_original': row['Indicator'],
                'english_translated': row['indicators_translated']
            }
    
    print(f"   Created mapping for {len(normalized_to_french)} French indicators")
    
    # PHASE 1: Perform fuzzy matching from merged to translated
    print("\n🔍 Performing fuzzy matching (Merged → Translated)...")
    
    # Match thresholds
    HIGH_MATCH = 85
    MEDIUM_MATCH = 70
    LOW_MATCH = 50
    
    results = []
    
    high_matches = 0
    medium_matches = 0
    low_matches = 0
    no_matches = 0
    
    for idx, row in df_merged_indicators.iterrows():
        merged_indicator = row['Indicator']
        normalized_merged = row['indicator_normalized']
        category_code = row['Category_code']
        indicator_id = row['ID']
        indicator_group = row['Indicator group']
        category = row['Category']
        
        # Use fuzzywuzzy to find the best match
        match_result = process.extractOne(
            normalized_merged, 
            translated_indicators, 
            scorer=fuzz.token_sort_ratio
        )
        
        french_indicator = None
        match_type = "no_match"
        best_score = 0
        best_match = None
        match_details = None
        
        if match_result:
            best_match, best_score = match_result
            match_details = normalized_to_french.get(best_match)
        
        if best_score >= HIGH_MATCH:
            french_indicator = match_details['french_original'] if match_details else None
            match_type = f"high_match"
            high_matches += 1
        elif best_score >= MEDIUM_MATCH:
            french_indicator = match_details['french_original'] if match_details else None
            match_type = f"medium_match"
            medium_matches += 1
        elif best_score >= LOW_MATCH:
            french_indicator = match_details['french_original'] if match_details else None
            match_type = f"low_match"
            low_matches += 1
        else:
            no_matches += 1
            match_type = f"no_match"
        
        results.append({
            'ID': indicator_id,
            'Category_code': category_code,
            'Indicator_group': indicator_group,
            'Category': category,
            'indicator_french': french_indicator,
            'indicator_english_source': merged_indicator,
            'indicator_source': match_type,
            'match_score': best_score,
            'best_match_english': best_match if best_score >= LOW_MATCH else None,
            'match_status': 'MATCHED' if best_score >= LOW_MATCH else 'NOT_MATCHED'
        })
    
    # Create the main analysis dataframe
    df_analysis = pd.DataFrame(results)
    
    print(f"\n📊 Fuzzy Matching Results (Merged → Translated):")
    print(f"   High matches (≥{HIGH_MATCH}%): {high_matches}")
    print(f"   Medium matches (≥{MEDIUM_MATCH}%): {medium_matches}")
    print(f"   Low matches (≥{LOW_MATCH}%): {low_matches}")
    print(f"   No matches (<{LOW_MATCH}%): {no_matches}")
    print(f"   Total processed: {len(df_analysis)}")
    
    # PHASE 2: Update the translated file with match information
    print("\n🔄 Updating translated file with match information...")
    
    # Create a reverse mapping from French indicators to their matches
    french_to_matches = {}
    for _, row in df_analysis.iterrows():
        if row['indicator_french'] and pd.notna(row['indicator_french']):
            if row['indicator_french'] not in french_to_matches:
                french_to_matches[row['indicator_french']] = []
            french_to_matches[row['indicator_french']].append({
                'ID': row['ID'],
                'Category_code': row['Category_code'],
                'match_score': row['match_score'],
                'indicator_english_source': row['indicator_english_source'],
                'match_type': row['indicator_source']
            })
    
    # Add match information to translated dataframe
    df_translated_enhanced = df_translated.copy()
    df_translated_enhanced['matched_ids'] = ''
    df_translated_enhanced['matched_category_codes'] = ''
    df_translated_enhanced['best_match_score'] = 0
    df_translated_enhanced['match_status'] = 'NOT_MATCHED'
    df_translated_enhanced['matching_english_indicators'] = ''
    
    for idx, row in df_translated_enhanced.iterrows():
        french_indicator = row['Indicator']
        if french_indicator in french_to_matches:
            matches = french_to_matches[french_indicator]
            # Get best match score
            best_score = max(match['match_score'] for match in matches)
            # Get all IDs and category codes
            ids = ', '.join(str(match['ID']) for match in matches)
            category_codes = ', '.join(str(match['Category_code']) for match in matches)
            english_indicators = ' | '.join(match['indicator_english_source'] for match in matches)
            
            df_translated_enhanced.at[idx, 'matched_ids'] = ids
            df_translated_enhanced.at[idx, 'matched_category_codes'] = category_codes
            df_translated_enhanced.at[idx, 'best_match_score'] = best_score
            df_translated_enhanced.at[idx, 'match_status'] = 'MATCHED'
            df_translated_enhanced.at[idx, 'matching_english_indicators'] = english_indicators
    
    # PHASE 3: Create detailed breakdowns
    print("\n📈 Creating detailed breakdowns...")
    
    # Match breakdown by confidence level
    high_match_df = df_analysis[df_analysis['match_score'] >= HIGH_MATCH]
    medium_match_df = df_analysis[(df_analysis['match_score'] >= MEDIUM_MATCH) & (df_analysis['match_score'] < HIGH_MATCH)]
    low_match_df = df_analysis[(df_analysis['match_score'] >= LOW_MATCH) & (df_analysis['match_score'] < MEDIUM_MATCH)]
    no_match_df = df_analysis[df_analysis['match_score'] < LOW_MATCH]
    
    # Matched vs Unmatched summary
    matched_summary = df_analysis.groupby('match_status').agg({
        'ID': 'count',
        'match_score': 'mean'
    }).rename(columns={'ID': 'count', 'match_score': 'avg_score'}).reset_index()
    
    # Category code analysis
    category_analysis = df_analysis.groupby('Category_code').agg({
        'ID': 'count',
        'match_score': 'mean',
        'match_status': lambda x: (x == 'MATCHED').sum()
    }).rename(columns={
        'ID': 'total_indicators', 
        'match_score': 'avg_match_score',
        'match_status': 'matched_indicators'
    }).reset_index()
    category_analysis['match_rate'] = (category_analysis['matched_indicators'] / category_analysis['total_indicators'] * 100).round(1)
    
    # PHASE 4: Create master analysis file
    print(f"\n💾 Creating master analysis file: {master_output_file}...")
    
    with pd.ExcelWriter(master_output_file, engine='openpyxl') as writer:
        # 1. Main Analysis Sheet
        df_analysis.to_excel(writer, sheet_name='id_analysis', index=False)
        
        # 2. Enhanced Translated Indicators
        df_translated_enhanced.to_excel(writer, sheet_name='indicator_interim_translated_enhanced', index=False)
        
        # 3. Summary Statistics
        summary_data = {
            'Metric': [
                'Total Merged Indicators',
                'Total Translated Indicators', 
                'High Confidence Matches (≥85%)',
                'Medium Confidence Matches (≥70%)',
                'Low Confidence Matches (≥50%)',
                'No Matches (<50%)',
                'Overall Match Rate (≥50%)',
                'Average Match Score',
                'Translated Indicators Matched',
                'Translated Indicators Not Matched'
            ],
            'Count': [
                len(df_analysis),
                len(df_translated_enhanced),
                len(high_match_df),
                len(medium_match_df), 
                len(low_match_df),
                len(no_match_df),
                f"{(len(high_match_df) + len(medium_match_df) + len(low_match_df)) / len(df_analysis) * 100:.1f}%",
                f"{df_analysis['match_score'].mean():.1f}%",
                len(df_translated_enhanced[df_translated_enhanced['match_status'] == 'MATCHED']),
                len(df_translated_enhanced[df_translated_enhanced['match_status'] == 'NOT_MATCHED'])
            ]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='summary_statistics', index=False)
        
        # 4. Confidence Level Breakdown
        confidence_data = {
            'Confidence Level': ['High (≥85%)', 'Medium (≥70%)', 'Low (≥50%)', 'No Match (<50%)'],
            'Count': [len(high_match_df), len(medium_match_df), len(low_match_df), len(no_match_df)],
            'Percentage': [
                f"{(len(high_match_df)/len(df_analysis)*100):.1f}%",
                f"{(len(medium_match_df)/len(df_analysis)*100):.1f}%",
                f"{(len(low_match_df)/len(df_analysis)*100):.1f}%", 
                f"{(len(no_match_df)/len(df_analysis)*100):.1f}%"
            ]
        }
        pd.DataFrame(confidence_data).to_excel(writer, sheet_name='confidence_breakdown', index=False)
        
        # 5. Detailed Match Sheets
        if len(high_match_df) > 0:
            high_match_df.to_excel(writer, sheet_name='high_confidence_matches', index=False)
        if len(medium_match_df) > 0:
            medium_match_df.to_excel(writer, sheet_name='medium_confidence_matches', index=False)
        if len(low_match_df) > 0:
            low_match_df.to_excel(writer, sheet_name='low_confidence_matches', index=False)
        if len(no_match_df) > 0:
            no_match_df.to_excel(writer, sheet_name='unmatched_indicators', index=False)
        
        # 6. Category Analysis
        category_analysis.to_excel(writer, sheet_name='category_analysis', index=False)
        
        # 7. Normalization Examples (for debugging)
        debug_data = []
        for i in range(min(15, len(df_merged_indicators))):
            row = df_merged_indicators.iloc[i]
            debug_data.append({
                'ID': row['ID'],
                'Original_English': row['Indicator'],
                'Normalized_English': row['indicator_normalized'],
                'Category_Code': row['Category_code']
            })
        pd.DataFrame(debug_data).to_excel(writer, sheet_name='normalization_examples', index=False)
    
    # Print final summary
    print(f"\n🎉 MASTER ANALYSIS COMPLETE!")
    print(f"📁 Output file: {master_output_file}")
    print(f"\n📊 FINAL SUMMARY:")
    print(f"   Merged indicators analyzed: {len(df_analysis)}")
    print(f"   Translated indicators enhanced: {len(df_translated_enhanced)}")
    print(f"   Overall match rate: {(len(high_match_df) + len(medium_match_df) + len(low_match_df)) / len(df_analysis) * 100:.1f}%")
    print(f"   Average match score: {df_analysis['match_score'].mean():.1f}%")
    print(f"   Translated indicators with matches: {len(df_translated_enhanced[df_translated_enhanced['match_status'] == 'MATCHED'])}")
    
    print(f"\n📋 SHEETS CREATED:")
    sheets = [
        'id_analysis', 'indicator_interim_translated_enhanced', 'summary_statistics',
        'confidence_breakdown', 'category_analysis', 'normalization_examples'
    ]
    if len(high_match_df) > 0: sheets.append('high_confidence_matches')
    if len(medium_match_df) > 0: sheets.append('medium_confidence_matches')
    if len(low_match_df) > 0: sheets.append('low_confidence_matches')
    if len(no_match_df) > 0: sheets.append('unmatched_indicators')
    
    for sheet in sheets:
        print(f"   ✓ {sheet}")
    
    return df_analysis, df_translated_enhanced

if __name__ == "__main__":
    try:
        # Install fuzzywuzzy if not already installed
        try:
            from fuzzywuzzy import fuzz, process
        except ImportError:
            print("Installing fuzzywuzzy...")
            import subprocess
            subprocess.check_call(["pip", "install", "fuzzywuzzy", "python-Levenshtein"])
            from fuzzywuzzy import fuzz, process
        
        df_analysis, df_translated_enhanced = create_comprehensive_analysis()
        
        # Show sample of enhanced translated file
        print(f"\n🔍 SAMPLE OF ENHANCED TRANSLATED FILE:")
        matched_samples = df_translated_enhanced[df_translated_enhanced['match_status'] == 'MATCHED'].head(2)
        for idx, row in matched_samples.iterrows():
            print(f"   French: {row['Indicator'][:60]}...")
            print(f"   English: {row['indicators_translated'][:60]}...")
            print(f"   Matched IDs: {row['matched_ids']}")
            print(f"   Match Score: {row['best_match_score']}%")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        