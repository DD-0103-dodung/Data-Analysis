import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import re
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
warnings.filterwarnings('ignore')

# Nguồn dữ liệu
df = pd.read_csv('../stg/linkedin_jobs.csv')
df_cleaned = df.drop_duplicates(subset=["job_url"])

# Khai báo mapping
crawl_date = "2025-12-27"
level_map = {
            "manager": "Manager",
            "lead": "Manager",
            "senior": "Senior",
            "junior": "Junior",
            "intern": "Intern"
        }
role_map = {
            "data engineer": "DE",
            "software": "Dev",
            "python": "Dev",
            "data analyst": "DA",
            "intelligence": "DA",
            "data analysis": "DA",
            "data analytics": "DA",
            "data operation": "DA",
            "insight": "DA",
            "analytic": "DA",
            "business analyst": "BA",
            "data scientist": "DS",
            "ai": "AI/ML",
            "llm": "AI/ML",
            "ml": "AI/ML",
            "finan": "Finance",
            "research": "Research"
        }
remote_map = {
            "remote": "Remote",
            "work from home": "Remote",
            "wfh": "Remote",
            "telecommute": "Remote",
            "hybrid": "Hybrid",
            "onsite": "Onsite",
            "in-office": "Onsite",
            "office-based": "Onsite"
}

job_map = {
            "contract": "Contract",
            "part-time": "Part-time",
            "internship": "Internship"
        }

time_units = {
        'day': 'days',
        'days': 'days',
        'week': 'weeks',
        'weeks': 'weeks',
        'month': 'months',
        'months': 'months',
        'year': 'years',
        'years': 'years',
        'hour': 'hours',
        'hours': 'hours',
        'minute': 'minutes',
        'minutes': 'minutes',
        'second': 'seconds',
        'seconds': 'seconds',
        'sec': 'seconds'
    }
skill_set = {
    "Python" : ["python"],
    "SQL": ["sql","postgres","mysql","oracle","plsql"],
    "Excel": ["excel","spreadsheet"],
    "Visualization": ["power bi","powerbi","tableau","qlik","looker","qlik"],
    "Statistics": ["statistics","statistical","math","mathematic"],
    "Machine Learning": ["machine learning","ml"],
    "ETL": ["etl"," data pipeline","crawl"],
    "Cloud": ["aws","gcp","azure"]
}
# Get thông tin về kinh nghiệm, loại hình làm việc, loại công việc (full time, contract,..), nhóm kỹ năng yêu cầu và thời gian post job
def extract_info(source, info_type):
    if not source:
        return {
            "experience_level": "n/a",
            "remote_group": False,
            "remote": "Onsite",
            "job_type": "n/a",
            "position":"n/a"
        }.get(info_type)

    t = str(source).lower()

    if info_type == "experience_level":
        level = level_map
        for k, v in level.items():
            if k in t:
                return v
        return "Mid-level"

    if info_type == "position":
        role = role_map
        for k, v in role.items():
            if k in t:
                return v
        return "Other"

    if info_type == "remote_group":
        return any(k in t for k in ["remote", "work from home", "hybrid"])

    if info_type == "remote":
        remote = remote_map
        for k, v in remote.items():
            if k in t:
                return v
        return "Onsite"

    if info_type == "job_type":
        job = job_map
        for k, v in job.items():
            if k in t:
                return v
        return "Full-time"

def extract_skill_set(source):
    if pd.isna(source):
        return ""
    t = str(source).lower()
    found = []
    for skill, keywords in skill_set.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', t):
                found.append(skill)
                break
    return ", ".join(sorted(set(found)))
def get_actual_post_date(posted_time, crawl_date=None):
    if pd.isna(posted_time):
        return None
    try:
        crawl_date = datetime.strptime(str(crawl_date), '%Y-%m-%d')
    except:
        crawl_date = datetime.now() - timedelta(days=1)

    text = str(posted_time).lower().strip()

    # Pattern: số + đơn vị + ago
    pattern = r'(\d+)\s+(week|weeks|month|months|day|days|hour|hours)\s+ago'
    match = re.search(pattern, text)
    if not match:
        return None
    number = int(match.group(1))
    unit = match.group(2)

    # Tính ngày post thực tế
    if unit in ['day', 'days']:
        post_date = crawl_date - timedelta(days=number)
    elif unit in ['week', 'weeks']:
        post_date = crawl_date - timedelta(weeks=number)
    elif unit in ['month', 'months']:
        post_date = crawl_date - timedelta(days=number * 30)
    elif unit in ['hour', 'hours']:
        post_date = crawl_date - timedelta(hours=number)
    else:
        return None
    return post_date.date()

df_cleaned["experience_level"] = df_cleaned["job_title"].apply(lambda x: extract_info(x,"experience_level"))
df_cleaned["remote_group"] = df_cleaned["job_description"].apply(lambda x: extract_info(x,"remote_group"))
df_cleaned["remote"] = df_cleaned["job_description"].apply(lambda x: extract_info(x,"remote"))
df_cleaned["job_type"] = df_cleaned["job_description"].apply(lambda x: extract_info(x,"job_type"))
df_cleaned["skills"] = df_cleaned["job_description"].apply(extract_skill_set)
df_cleaned["posted_date"] = df_cleaned["posted_time"].apply(lambda x: get_actual_post_date(x,crawl_date))
df_cleaned["position"] = df_cleaned["job_title"].apply(lambda x: extract_info(x,'position'))
# print(df_cleaned[df_cleaned['position'] == 'Other']['job_title'].value_counts())
#
# print("="*80)
# print("📊 PHÂN TÍCH TỔNG QUAN DATASET")
# print("="*80)
#
# # 1. Thông tin cơ bản
# print("\n1. 📋 THÔNG TIN CƠ BẢN:")
# print(f"   • Tổng số bản ghi: {len(df_cleaned):,}")
# print(f"   • Số cột: {len(df_cleaned.columns)}")
#
# # 2. Kiểm tra missing values
# print("\n2. ⚠️  KIỂM TRA MISSING VALUES:")
# missing_data = df_cleaned.isnull().sum()
# missing_pct = (missing_data / len(df_cleaned)) * 100
#
# missing_df = pd.DataFrame({
#     'Missing Values': missing_data,
#     'Percentage (%)': missing_pct.round(2)
# })

# 3. Phân tích cơ bản
print("\n3. Phân tích cơ bản")
column_name = 'position'
df_group = df_cleaned[column_name].value_counts().reset_index()
df_group['remote'] = df_cleaned[df_cleaned['remote_group'] == True][column_name].values_counts()

print(df_group.head())
#
# df_group.columns = [column_name,'count']
# plt.figure(figsize = (10,6))
# plt.bar(df_group[column_name],df_group['count'],color = '#808080')
# plt.ylabel('Number of jobs')
# plt.title('Number of jobs by '+ column_name)
# plt.show()




# # Chỉ hiển thị cột có missing
# missing_df = missing_df[missing_df['Missing Values'] > 0]
# if len(missing_df) > 0:
#     print(missing_df)
# else:
#     print("   ✅ Không có missing values!")
#
# # 3. Phân tích từng trường đã làm sạch
# print("\n3. 🔍 PHÂN TÍCH CHI TIẾT TỪNG TRƯỜNG:")
#
#
# def analyze_column(df, column_name, title):
#     """Phân tích một cột cụ thể"""
#     print(f"\n   📈 {title}:")
#     print(f"   {'─' * 40}")
#
#     if column_name in df.columns:
#         # Thống kê cơ bản
#         unique_count = df[column_name].nunique()
#         print(f"   • Số giá trị duy nhất: {unique_count}")
#
#         # Top values
#         top_values = df[column_name].value_counts().head(10)
#         total = len(df)
#
#         print(f"   • Top 10 giá trị phổ biến:")
#         for value, count in top_values.items():
#             percentage = (count / total) * 100
#             print(f"     {value}: {count} ({percentage:.1f}%)")
#
#         # Nếu là categorical, hiển thị distribution
#         if unique_count <= 20:
#             value_counts = df[column_name].value_counts()
#             print(f"   • Phân phối đầy đủ:")
#             for value, count in value_counts.items():
#                 percentage = (count / total) * 100
#                 print(f"     {value}: {count} ({percentage:.1f}%)")
#
#         return top_values
#     else:
#         print(f"   ❌ Cột '{column_name}' không tồn tại")
#         return None
#
#
# # Phân tích từng trường
# analyze_column(df_cleaned, 'experience_level', 'EXPERIENCE LEVEL')
# analyze_column(df_cleaned, 'remote', 'REMOTE TYPE')
# analyze_column(df_cleaned, 'job_type', 'JOB TYPE')
# analyze_column(df_cleaned, 'skills', 'SKILLS SET')
# analyze_column(df_cleaned, 'posted_date', 'POSTED DATE')
#
# # Tạo báo cáo phân tích mối quan hệ
# print("\n" + "=" * 80)
# print("🔗 PHÂN TÍCH MỐI QUAN HỆ GIỮA CÁC TRƯỜNG")
# print("=" * 80)
#
# # 1. Experience Level vs Remote Type
# if all(col in df_cleaned.columns for col in ['experience_level', 'remote_type']):
#     print("\n1. 🎯 EXPERIENCE LEVEL vs REMOTE TYPE:")
#     cross_exp_remote = pd.crosstab(df_cleaned['experience_level'],
#                                    df_cleaned['remote_type'],
#                                    normalize='index') * 100
#     print(cross_exp_remote.round(1))
#
#     # Heatmap visualization
#     plt.figure(figsize=(10, 6))
#     sns.heatmap(cross_exp_remote, annot=True, fmt='.1f', cmap='YlOrRd')
#     plt.title('Experience Level vs Remote Type (%)')
#     plt.tight_layout()
#     plt.savefig('exp_vs_remote.png', dpi=300, bbox_inches='tight')
#     print("   💾 Đã lưu heatmap: exp_vs_remote.png")
#
# # 2. Skills Analysis
# if 'skills_set' in df_cleaned.columns:
#     print("\n2. 🛠️  PHÂN TÍCH SKILLS:")
#
#     # Tách skills thành list
#     df_cleaned['skills_list'] = df_cleaned['skills_set'].apply(
#         lambda x: [s.strip() for s in str(x).split(',')] if pd.notna(x) and x != '' else []
#     )
#
#     # Đếm số skills mỗi job
#     df_cleaned['num_skills'] = df_cleaned['skills_list'].apply(len)
#
#     print(f"   • Trung bình skills mỗi job: {df_cleaned['num_skills'].mean():.2f}")
#     print(f"   • Min skills: {df_cleaned['num_skills'].min()}")
#     print(f"   • Max skills: {df_cleaned['num_skills'].max()}")
#
#     # Tìm skills phổ biến nhất
#     from collections import Counter
#
#     all_skills = []
#     for skills in df_cleaned['skills_list']:
#         all_skills.extend(skills)
#
#     skill_counter = Counter(all_skills)
#
#     print(f"\n   • Top 10 skills phổ biến nhất:")
#     for skill, count in skill_counter.most_common(10):
#         percentage = (count / len(df_cleaned)) * 100
#         print(f"     {skill}: {count} jobs ({percentage:.1f}%)")
#
#     # Skills vs Experience Level
#     if 'experience_level' in df_cleaned.columns:
#         print(f"\n   • Skills phổ biến theo experience level:")
#         exp_levels = df_cleaned['experience_level'].unique()
#         for level in exp_levels:
#             if pd.notna(level):
#                 level_skills = []
#                 mask = df_cleaned['experience_level'] == level
#                 for skills in df_cleaned.loc[mask, 'skills_list']:
#                     level_skills.extend(skills)
#
#                 if level_skills:
#                     top_skill = Counter(level_skills).most_common(1)[0]
#                     print(f"     {level}: {top_skill[0]} ({top_skill[1]} jobs)")
#
# # 3. Time Analysis (posted_date)
# if 'posted_date' in df_cleaned.columns:
#     print("\n3. 📅 PHÂN TÍCH THEO THỜI GIAN:")
#
#     # Convert to datetime
#     df_cleaned['posted_date_dt'] = pd.to_datetime(df_cleaned['posted_date'], errors='coerce')
#
#     # Filter valid dates
#     valid_dates = df_cleaned['posted_date_dt'].dropna()
#
#     if len(valid_dates) > 0:
#         print(f"   • Ngày post sớm nhất: {valid_dates.min().strftime('%Y-%m-%d')}")
#         print(f"   • Ngày post mới nhất: {valid_dates.max().strftime('%Y-%m-%d')}")
#         print(f"   • Số ngày phân phối: {(valid_dates.max() - valid_dates.min()).days} ngày")
#
#         # Phân bố theo tuần
#         df_cleaned['post_week'] = df_cleaned['posted_date_dt'].dt.isocalendar().week
#         weekly_counts = df_cleaned.groupby('post_week').size()
#
#         print(f"\n   • Phân bố jobs theo tuần:")
#         for week, count in weekly_counts.sort_index().items():
#             if pd.notna(week):
#                 print(f"     Tuần {week}: {count} jobs")
#
#         # Jobs theo remote type qua thời gian
#         if 'remote_type' in df_cleaned.columns:
#             time_remote = pd.crosstab(df_cleaned['post_week'],
#                                       df_cleaned['remote_type'],
#                                       normalize='index') * 100
#             print(f"\n   • Xu hướng Remote vs Onsite theo tuần:")
#             print(time_remote.round(1).tail())