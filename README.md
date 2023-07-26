# AO3_Analytics
Analyze AO3 User Data

to start the virtual enviorment run `.\env\Scripts\activate.bat `

to run against history page `python ao3_scrape.py`
- For testing only scrapes the first 10 pages and displays limited info


## TODO
- [X] Integrate a Database (no sql) - JSON Files
- Handle specific errors when getting works
  - [X] hidden works
  - [X] deleted works
- Create a UI
  - [X] Base UI
  - [X] Print CMD line output
  - [X] Create Result Tabs
  - [ ] display results in Tabs
- Analyze tags to get
  - [ ] get top 10 trope tag
  - [ ] get top 10 relashionship tags
- [ ] Display analytics in charts
- [ ] pull the number of times visiting a story into data 
- [X] Handle bad login
- [ ] Get Rating