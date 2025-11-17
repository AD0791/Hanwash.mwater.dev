import pandas as pd
import re

# Translation map
WASH_TRANSLATION_MAP = {
    "Pourcentage d'interventions approuvées mises en œuvre conformément aux plans d'action des communes.": "Percentage of approved interventions implemented in accordance with commune action plans.",
    "Nombre de communes disposant de plans d'action qui incluent explicitement chaque aspect W, S, H, WRM (eau, assainissement, hygiène, gestion des ressources en eau).": "Number of communes with action plans that explicitly include all aspects: W, S, H, WRM (water, sanitation, hygiene, water resource management).",
    "Pourcentage de prestataires de services relevant de l'initiative HANWASH contrôlés conformément aux directives de la DINEPA/OREPA acceptées par le bureau du maire": "Percentage of HANWASH initiative service providers monitored in accordance with DINEPA/OREPA directives accepted by the mayor's office.",
    "Pourcentage de prestataires de services d'intervention qui sont entièrement responsables conformément aux exigences de la DINEPA/OREPA et du maire": "Percentage of intervention service providers who are fully accountable according to DINEPA/OREPA and mayor's requirements.",
    "Pourcentage d'utilisateurs satisfaits de la qualité, du caractère abordable et de la fiabilité des services WASH fournis": "Percentage of users satisfied with the quality, affordability, and reliability of WASH services provided.",
    "Nombre moyen de jours nécessaires pour résoudre les pannes des infrastructures hydrauliques": "Average number of days required to resolve water infrastructure failures.",
    "Nombre moyen de jours de service d'eau potable fournis au cours du mois par les prestataires de services": "Average number of days of drinking water service provided during the month by service providers.",
    "Taux de recouvrement des redevances d'eau (ventilé par type de prestataires de services)": "Water fee collection rate (disaggregated by type of service provider).",
    "Nombre de communes ayant organisé une évaluation annuelle des prestataires de services avec les principales parties prenantes au cours de l'année écoulée": "Number of communes that organized an annual service provider evaluation with key stakeholders during the past year.",
    "Pourcentage de la population des communes concernées bénéficiant d'un service d'approvisionnement en eau potable au moins basique.": "Percentage of the population in target communes benefiting from at least a basic drinking water service.",
    "Pourcentage de la population des communes concernées bénéficiant d'un service d'approvisionnement en eau potable géré de manière sûre.": "Percentage of the population in target communes benefiting from a safely managed drinking water service.",
    "Pourcentage des points d'eau concernés qui sont fonctionnels, potables et dont le budget est équilibré ou excédentaire après deux ans.": "Percentage of target water points that are functional, potable, and whose budget is balanced or in surplus after two years.",
    "Pourcentage de communautés d'intervention vérifiées comme étant exemptes de défécation à l'air libre (DAL)": "Percentage of intervention communities verified as Open Defecation Free (ODF).",
    "Pourcentage de communautés d'intervention certifiées comme étant exemptes de défécation à l'air libre (DAL)": "Percentage of intervention communities certified as Open Defecation Free (ODF).",
    "Pourcentage de la population des communes d'intervention bénéficiant d'au moins un service d'assainissement de base": "Percentage of the population in intervention communes benefiting from at least a basic sanitation service.",
    "Nombre de personnes bénéficiant d'un service d'assainissement de base dans les communes d'intervention": "Number of people benefiting from a basic sanitation service in intervention communes.",
    "Pourcentage d'écoles bénéficiant au moins d'un service d'eau potable, d'assainissement et d'hygiène de base": "Percentage of schools benefiting from at least basic water, sanitation, and hygiene (WASH) services.",
    "Pourcentage d'établissements de santé bénéficiant au moins d'un service d'eau potable, d'assainissement et d'hygiène de base": "Percentage of healthcare facilities benefiting from at least basic water, sanitation, and hygiene (WASH) services.",
    "Nombre d'écoles bénéficiant désormais d'un service d'eau potable de base": "Number of schools now benefiting from a basic drinking water service.",
    "Nombre d'établissements de santé bénéficiant désormais de services d'eau potable de base": "Number of healthcare facilities now benefiting from basic drinking water services.",
    "Nombre d'écoles bénéficiant désormais de services d'assainissement de base": "Number of schools now benefiting from basic sanitation services.",
    "Nombre d'établissements de santé bénéficiant désormais de services d'assainissement de base": "Number of healthcare facilities now benefiting from basic sanitation services.",
    "Nombre d'écoles bénéficiant désormais de services d'hygiène de base": "Number of schools now benefiting from basic hygiene services.",
    "Nombre d'établissements de santé bénéficiant désormais de services d'hygiène de base": "Number of healthcare facilities now benefiting from basic hygiene services.",
    "Montant cumulé des fonds engagés conformément aux valeurs fondamentales de HANWASH, sur la base d'un protocole d'accord signé avec HANWASH": "Cumulative amount of funds committed in accordance with HANWASH core values, based on a signed MOU with HANWASH.",
    "Pourcentage de partenaires de mise en œuvre dans les zones du programme HANWASH ayant signé le cadre d'accord DINEPA.": "Percentage of implementation partners in HANWASH program areas that have signed the DINEPA framework agreement."
}

def normalize_string(s):
    """
    Normalize a string by:
    1. Stripping leading/trailing whitespace
    2. Removing extra internal whitespace
    3. Standardizing punctuation (optional)
    """
    if not isinstance(s, str):
        return s
    # Strip leading/trailing whitespace and normalize internal whitespace
    normalized = ' '.join(s.strip().split())
    return normalized

def create_normalized_translation_map(translation_map):
    """Create a normalized version of the translation map for matching."""
    normalized_map = {}
    for key, value in translation_map.items():
        normalized_key = normalize_string(key)
        normalized_map[normalized_key] = value
    return normalized_map

def verify_and_fix_translations(input_file, output_file):
    """
    Verify translation map completeness and add translations with normalized matching.
    """
    
    # Read the Excel file
    df = pd.read_excel(input_file, sheet_name='Sheet1')
    
    # Create normalized translation map
    normalized_map = create_normalized_translation_map(WASH_TRANSLATION_MAP)
    
    print("🔍 Verifying translation map completeness with normalized strings...")
    
    # Normalize DataFrame indicators for comparison
    df_indicators_normalized = set(normalize_string(indicator) for indicator in df['Indicator'] if pd.notna(indicator))
    
    # Get normalized keys from translation map
    map_indicators_normalized = set(normalized_map.keys())
    
    # Find mismatches
    missing_in_map = df_indicators_normalized - map_indicators_normalized
    extra_in_map = map_indicators_normalized - df_indicators_normalized
    
    print(f"Total indicators in DataFrame: {len(df_indicators_normalized)}")
    print(f"Total keys in translation map: {len(map_indicators_normalized)}")
    
    if missing_in_map:
        print(f"\n❌ MISSING TRANSLATIONS ({len(missing_in_map)}):")
        for i, indicator in enumerate(missing_in_map, 1):
            print(f"  {i}. '{indicator}'")
        
        # Try to find close matches for missing translations
        print(f"\n🔍 Looking for close matches...")
        for missing_indicator in missing_in_map:
            close_matches = []
            for map_indicator in map_indicators_normalized:
                # Simple similarity check - you could use difflib for more sophisticated matching
                if missing_indicator in map_indicator or map_indicator in missing_indicator:
                    close_matches.append(map_indicator)
            
            if close_matches:
                print(f"  For '{missing_indicator}':")
                for match in close_matches[:3]:  # Show top 3 matches
                    print(f"    Possible match: '{match}'")
    
    if extra_in_map:
        print(f"\n⚠️  EXTRA TRANSLATIONS (not in DataFrame) ({len(extra_in_map)}):")
        for i, indicator in enumerate(extra_in_map, 1):
            print(f"  {i}. '{indicator}'")
    
    if missing_in_map:
        print(f"\n❌ Cannot proceed - {len(missing_in_map)} indicators are missing translations.")
        return None
    
    print(f"\n✅ Translation map is complete! All {len(df_indicators_normalized)} indicators have translations.")
    
    # Now perform the actual translation
    print(f"\n🔄 Adding translations to DataFrame...")
    
    translations = []
    match_types = []
    
    for index, row in df.iterrows():
        original_indicator = row['Indicator']
        normalized_indicator = normalize_string(original_indicator)
        
        if normalized_indicator in normalized_map:
            translation = normalized_map[normalized_indicator]
            translations.append(translation)
            match_types.append("normalized")
        else:
            # This should not happen if verification passed
            raise ValueError(f"Critical error: No translation found for normalized indicator: '{normalized_indicator}'")
    
    # Add translations to DataFrame
    df['indicators_translated'] = translations
    
    print(f"✅ Successfully added {len(translations)} translations")
    print(f"   - Normalized matches: {len(match_types)}")
    
    # Save the updated DataFrame
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        pd.DataFrame().to_excel(writer, sheet_name='Sheet3', index=False)
    
    print(f"\n💾 File successfully saved as: {output_file}")
    
    # Show verification of first few rows
    print(f"\n🔍 Verification (first 5 rows):")
    for i in range(min(5, len(df))):
        original = df.iloc[i]['Indicator']
        translated = df.iloc[i]['indicators_translated']
        print(f"  {i+1}. Original: '{original}'")
        print(f"     Translated: '{translated}'\n")
    
    return df

# Execute the function
if __name__ == "__main__":
    input_filename = "indicateur_interim.xlsx"
    output_filename = "indicateur_interim_translated.xlsx"
    
    try:
        result_df = verify_and_fix_translations(input_filename, output_filename)
        if result_df is not None:
            print(f"🎉 Success! All {len(result_df)} indicators have been translated and saved.")
        else:
            print("❌ Failed to complete translation due to missing translations.")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        