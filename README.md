# AO3_Analytics
Analyze AO3 User Data

to start the virtual enviorment run `.\env\Scripts\activate.bat `

to run against history page `python ao3_scrape.py`
- For testing only scrapes the first 10 pages and displays limited info


## TODO
- [X] Fix Dependencies file (convert to requirements.txt)
- [X] Integrate a Database (no sql) - JSON Files
- Handle specific errors when getting works
  - [X] hidden works
  - [X] deleted works
- Create a UI
  - [X] Base UI
  - [X] Print CMD line output
  - [X] Create Result Tabs
  - [X] display results in Tabs
  - [X] Add new metrics to the UI
- Analyze tags to get
  - [X] get top 10 trope tag
  - [X] get top 10 relashionship tags
- [ ] Display analytics in charts
- [X] Add Wordcloud Generation
- [X] add recs page/favorites
- [ ] pull the number of times visiting a story into data 
- [X] Pull if part of collection or series/multiple series
- [X] Handle bad login
- [X] Get Rating
- [ ] Add fandom to character and relashionship tags, freeforms dont need it
- [ ] Add fandom to works table
- [X] Add wordcloud
- Bookbinding Resources
  - [ ] Keep track of a to-bind list
  - [ ] Keep track of which works have been bound
  - [ ] Utility to store typest metrics based on pdf
  - [ ] Utility to estimate size of spine
