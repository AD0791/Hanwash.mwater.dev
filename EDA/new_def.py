
# HANWASH Indicators Dictionary and Utility Functions

hanwash_indicators_dict = {
    'Code_index': ['-',
                   '-',
                   '1100a',
                   '1100b',
                   '1110a',
                   '1110b',
                   '1120a',
                   '1120b',
                   '1120c',
                   '1120d',
                   '1200a',
                   '1210a',
                   '1220a',
                   '1300a',
                   '1300b',
                   '1300c',
                   '1310a',
                   '1310b',
                   '1310c',
                   '-',
                   '2100a',
                   '2100b',
                   '2100c',
                   '2100d',
                   '2110a',
                   '2110b',
                   '2110c',
                   '2120a',
                   '2120c',
                   '2120b',
                   '2200a',
                   '2200b',
                   '2200c',
                   '2210a',
                   '2210b',
                   '2220a',
                   '2230a',
                   '2300a',
                   '2300b',
                   '2310a',
                   '2310b',
                   '2320a',
                   '2400a',
                   '2400b',
                   '2410a',
                   '2410b',
                   '2420a',
                   '2420b',
                   '2430a',
                   '2430b',
                   '-',
                   '3100a',
                   '3100b',
                   '3110a',
                   '3120a',
                   '3200a',
                   '3210a',
                   '3220a'],
    'New_Definitions': [
        '-',
        '-',
        'Percentage of commune-level WASH events that have active Rotarian participation, measured as a proportion of total reported events.',
        'Percentage of commune-level WASH events led by trained HANWASH Ambassadors and Coordinators to communicate WASH messages and advocate for HANWASH goals, measured as a proportion of total reported events.',
        'Average number of volunteer hours per month spent by Rotarians in WASH events, calculated per Rotary club.',
        'Total number of individuals reached through WASH events and advocacy efforts led by HANWASH Ambassadors, Coordinators, and Rotarians in the commune.',
        'Total number of HANWASH Ambassadors who have successfully completed the required training program.',
        'Total number of HANWASH Coordinators who have successfully completed the required training program.',
        'Number of training materials developed that align with HANWASH\'s three pillars and core values.',
        'Cumulative number of training hours received by HANWASH Ambassadors, Coordinators, and their committees throughout the Caribbean region.',
        'Percentage of implemented interventions that align with approved Commune Action Plans, indicating adherence to local priorities and needs.',
        'Number of communes with comprehensive action plans that explicitly address all four WASH aspects: Water, Sanitation, Hygiene, and Water Resources Management.',
        'Number of WASH planning and coordination events conducted with DINEPA and municipal officials per month, fostering collaboration and alignment.',
        'Percentage of service providers under the HANWASH initiative that are monitored according to national guidelines, ensuring compliance and quality.',
        'Percentage of intervention service providers that have established accountability structures, promoting transparency and community engagement.',
        'Percentage of users expressing satisfaction with the quality, affordability, and reliability of WASH services provided, based on household surveys.',
        'Number of intervention water systems that consistently report data on a regular basis, demonstrating operational transparency.',
        'Percentage of customer complaints resolved during the month, calculated as (number of resolved complaints / total number of complaints) * 100.',
        'Average number of days taken to resolve customer complaints, indicating responsiveness and service quality.',
        '-',
        'Percentage of intervention water points that are both functioning and providing potable water, ensuring access to safe drinking water.',
        'Percentage of population in intervention communes with access to at least basic drinking water service, defined as an improved water source within 30 minutes round trip.',
        'Percentage of population in intervention communes with access to safely managed drinking water service, defined as an improved water source on premises, available when needed, and free from contamination.',
        'Percentage of intervention water points that are functioning, potable, and financially sustainable (balanced or surplus budget) after 2 years of operation.',
        'Number of people in intervention communes gaining access to basic drinking water service through community-managed water points.',
        'Number of new community-managed water points created, with signed CPE statutes with DINEPA.',
        'Percentage of newly created community-managed water points that submit monthly reports to local authorities, promoting accountability.',
        'Number of people newly provided with safely managed drinking water service, meeting WHO/UNICEF Joint Monitoring Programme (JMP) criteria.',
        'Number of professionally managed piped water systems rehabilitated in the intervention communes, improving existing infrastructure.',
        'Number of new professionally managed piped water systems created in the intervention communes, expanding water service coverage.',
        'Percentage of intervention communities verified as Open Defecation Free (ODF), meeting all criteria set by the commune WASH committee.',
        'Percentage of population in intervention communes with access to at least basic sanitation service, defined as improved and unshared facilities.',
        'Percentage of population in intervention communes with access to safely managed sanitation service, meeting WHO/UNICEF JMP criteria.',
        'Number of people newly provided with access to basic sanitation service in the intervention communes.',
        'Number of intervention communities that have been verified as Open Defecation Free (ODF) by the commune WASH committee.',
        'Number of intervention communities that have been certified as Open Defecation Free (ODF), maintaining verified ODF status for at least one year.',
        'Number of public latrines constructed, improving sanitation access in communal areas.',
        'Percentage of population in intervention communes with access to at least basic hygiene service, defined as presence of a handwashing facility with soap and water on premises.',
        'Percentage of population in intervention communes with access to basic hygiene service, as defined by WHO/UNICEF JMP criteria.',
        'Number of community animators trained to provide hygiene education and community mobilization.',
        'Cumulative number of hours of hygiene training and community mobilization provided by trained community animators.',
        'Number of people newly provided with access to basic hygiene service in intervention areas.',
        'Percentage of schools in intervention areas with basic drinking water, sanitation, and hygiene services, meeting WHO/UNICEF JMP criteria for schools.',
        'Percentage of healthcare facilities in intervention areas with basic drinking water, sanitation, and hygiene services, meeting WHO/UNICEF JMP criteria for healthcare facilities.',
        'Number of schools newly provided with basic drinking water services in intervention areas.',
        'Number of healthcare facilities newly provided with basic drinking water services in intervention areas.',
        'Number of schools newly provided with basic sanitation services in intervention areas.',
        'Number of healthcare facilities newly provided with basic sanitation services in intervention areas.',
        'Number of schools newly provided with basic hygiene services in intervention areas.',
        'Number of healthcare facilities newly provided with basic hygiene services in intervention areas.',
        '-',
        'Cumulative amount of money (in USD) committed to projects aligned with HANWASH Core Values, including local leadership, collaboration, systematic approach, impact, and commitment.',
        'Percentage of committed funds that have been spent, calculated as (Cumulative_amount_spent / Cumulative_amount_committed) * 100.',
        'Amount of money (in USD) spent by external actors within HANWASH project areas, aligned with HANWASH Core Values.',
        'Amount of money (in USD) spent by external actors beyond HANWASH project areas but still aligned with HANWASH Core Values, extending impact.',
        'Percentage of implementing partners in HANWASH program areas who have signed the DINEPA Accord Cadre, ensuring alignment with national standards.',
        'Number of DINEPA personnel who have completed leadership training, building capacity within the national water authority.',
        'Number of technical trainings provided for DINEPA priority areas, focusing on key topics such as unified national tariff methodology and ODF certification.'
    ]
}


 
def get_definition(code_index):
    """
    Get the new definition for a given Code_index.
    
    Args:
    code_index (str): The Code_index to look up.
    
    Returns:
    str: The corresponding new definition, or None if not found.
    """
    try:
        index = hanwash_indicators['Code_index'].index(code_index)
        return hanwash_indicators['New_Definitions'][index]
    except ValueError:
        return None

def print_all_definitions():
    """
    Print all Code_index values and their corresponding new definitions.
    """
    for code, definition in zip(hanwash_indicators['Code_index'], hanwash_indicators['New_Definitions']):
        print(f"Code_index: {code}")
        print(f"Definition: {definition}")
        print("-" * 50)
