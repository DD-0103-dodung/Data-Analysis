# Linkedin Data-Analysis
1. 📌  Problem statement
- Crawl/ scrape data related to HR from public sources
- Analyze job market trending: required skill sets, location, job demands,.. in every sector
- Build dataset to support analyzing and to provide actionable decision
2. 🔍 Data source
- Public Linkedin job postings search as not be violated to its terms and conditions.
- Every keyword in this task is crawled with maximum of 10 pages (each page showed 25 jobs posted as Linkedin policy)
- Cannot crawl all job posted as Linkedin' bot detection
3. Data collection
- Endpoint identification via browser Network tab
- Add delay time in each crawl action like user-acting to prevent block
4. Data schema
- All data after crawling will be appended into tables with some informations: keyword,job_title,company,location,posted_time,job_url,job_description
5. Data cleaning
- Clean data, remove duplicates based on job_url
- Standardize columns by extracting information and grouping, regex: remote, job_type, experience_level, posted_date, skills
- Missing handle: Handle missing
6. 📊 EDA
- Job posting distribution by location, time, experiment_level, job_type, remote
- Most technical skill sets required
7. 🎯 Key findings
8. 🚫 Limitation
- Only ~500 records crawled as Linkedin pagination detection
- Can not be representative for job market trending and demands
- Can not get some relevant information related to company info as being blocked
- If possible, I would like to structured into dim, fact separately. In which, dim tables contain master data: company infor (name, size, location, followers), job_list, location, date (year, month, week, date),
experiment_level and salary_range. Fact tables contains records for job postings in detail
9. 🔮 Future improvement
- Get info from various source: Vietnamwork, CareerBuilder, TopCV, Indeed,... not just based on only Linkedin to see which platform is appeal to candidates, which one can be highest converted,...
- Analyze competitors in HR recruitment and predict salary range based on location, title,..
