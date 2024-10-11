import pandas as pd
import os
import matplotlib.pyplot as plt

# Load the dataset (assuming it has already been cleaned and merged as 'user_mwater_data.xlsx')
file_path = './mWater_usage/reports/user_mwater_data.xlsx'
complete_data = pd.read_excel(file_path)

# Create a clean_data dataset by deduplicating based on 'user_ID'
clean_data = complete_data.drop_duplicates(subset='user_ID', keep='first')

# Convert 'Last Activity' to naive datetime (without timezone) for consistency
clean_data['Last Activity'] = pd.to_datetime(clean_data['Last Activity'], errors='coerce').dt.tz_localize(None)

# Define the 12-month cutoff using naive datetime for consistency
cutoff_date = pd.Timestamp.now().tz_localize(None) - pd.DateOffset(months=12)
active_users_12_months = clean_data[clean_data['Last Activity'] >= cutoff_date]
num_active_users_12_months = len(active_users_12_months)

# Corrected calculation for active users in the portal and app (instead of summing the activity)
total_portal_active_users = clean_data[clean_data['Portal Activity 7 days'] > 0].shape[0]
total_app_active_users = clean_data[clean_data['App Activity 7 days'] > 0].shape[0]

# Total unique active users (either app or portal)
total_active_users = len(clean_data[(clean_data['Portal Activity 7 days'] > 0) | (clean_data['App Activity 7 days'] > 0)])

# Calculate percentages
portal_usage_percentage = (total_portal_active_users / total_active_users) * 100 if total_active_users > 0 else 0
app_usage_percentage = (total_app_active_users / total_active_users) * 100 if total_active_users > 0 else 0

# Number of inactive users overall (users with no activity in both app and portal)
inactive_users = clean_data[(clean_data['App Activity 7 days'] == 0) & (clean_data['Portal Activity 7 days'] == 0)]
num_inactive_users = len(inactive_users)

# Exclude the 'HANWASH' column from the committee analysis
committee_columns_no_hanwash = [
    'Ambassadors', 'Champion Partnerships', 'D7020 Engagement', 'Executive', 'Finance Legal and Admin',
    'Haiti Liaison', 'MAGEPA', 'Marketing and Donor Relations', 'Monitoring and Evaluation',
    'Projects Support Subcommittee', 'Steering Committee'
]

# Active and inactive users by committee (excluding HANWASH)
active_users_by_committee_no_hanwash = active_users_12_months[committee_columns_no_hanwash].apply(lambda col: (col == 'Yes').sum())
inactive_users_by_committee_no_hanwash = inactive_users[committee_columns_no_hanwash].apply(lambda col: (col == 'Yes').sum())

# Calculate the percentage of active users in each committee (excluding HANWASH)
active_users_percentage_by_committee_no_hanwash = (active_users_by_committee_no_hanwash / active_users_12_months.shape[0]) * 100

# Ensure that the 'reports' directory exists
output_dir = './mWater_usage/reports'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create a Bar Chart for the percentage of active users by committee (excluding HANWASH)
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(committee_columns_no_hanwash, active_users_percentage_by_committee_no_hanwash, color='#1f77b4')
ax.set_xlabel('Percentage of Active Users (%)')
ax.set_title('Percentage of Active Users by Committee (Excluding HANWASH)')

# Save the updated percentage bar chart (excluding HANWASH)
percentage_bar_chart_image_no_hanwash = os.path.join(output_dir, 'percentage_active_committee_chart_no_hanwash.png')
plt.savefig(percentage_bar_chart_image_no_hanwash, bbox_inches='tight')

# Calculate total unique users and percentage of active users in the past 12 months over total users
total_unique_users = clean_data.shape[0]
active_users_percentage_overall = (num_active_users_12_months / total_unique_users) * 100

# Create a pie chart showing active users vs. total users
fig, ax = plt.subplots()
ax.pie([num_active_users_12_months, total_unique_users - num_active_users_12_months],
       labels=['Active Users (12 months)', 'Inactive/Other Users'], autopct='%1.1f%%', startangle=90, colors=['#1f77b4', '#ff7f0e'])
ax.set_title('Active Users vs Total Users on Platform')

# Save the overall pie chart
overall_pie_chart_image = os.path.join(output_dir, 'overall_active_users_pie.png')
plt.savefig(overall_pie_chart_image, bbox_inches='tight')

# Now update the report by removing HANWASH from all committee analyses and charts
output_file_excluding_hanwash = os.path.join(output_dir, 'mWater_usage_reports_final_excluding_hanwash.xlsx')

with pd.ExcelWriter(output_file_excluding_hanwash, engine='xlsxwriter') as writer:
    # Write clean_data with deduplication summary
    clean_data.to_excel(writer, sheet_name='Clean Data', index=False)

    # Write active user analysis to a sheet
    pd.DataFrame({
        'Metric': ['Number of Active Users in 12 months', 'Number of Active Portal Users', 'Number of Active App Users', 'Portal Usage Percentage', 'App Usage Percentage', 'Number of Inactive Users'],
        'Value': [num_active_users_12_months, total_portal_active_users, total_app_active_users, portal_usage_percentage, app_usage_percentage, num_inactive_users]
    }).to_excel(writer, sheet_name='Usage Summary', index=False)

    # Write committee analysis excluding HANWASH
    active_users_by_committee_no_hanwash.to_frame(name='Active Users Count').to_excel(writer, sheet_name='Active Users Committees', index=True)
    inactive_users_by_committee_no_hanwash.to_frame(name='Inactive Users Count').to_excel(writer, sheet_name='Inactive Users Committees', index=True)

    # Insert the updated percentage bar chart excluding HANWASH
    worksheet_percentage_bar_chart_no_hanwash = writer.book.add_worksheet('Percentage Active Excl HANWASH')
    worksheet_percentage_bar_chart_no_hanwash.insert_image('B2', percentage_bar_chart_image_no_hanwash)

    # Insert the overall pie chart for active users vs total users
    worksheet_overall_pie_chart = writer.book.add_worksheet('Active vs Total Pie Chart')
    worksheet_overall_pie_chart.insert_image('B2', overall_pie_chart_image)

print(f"Final report (excluding HANWASH) generated at: {output_file_excluding_hanwash}")
