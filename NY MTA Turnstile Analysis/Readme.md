# NY MTA Turnstile Data Analysis 

## Abstract

The goal of this project was to find the best place to open deli restaurant near New York MTA station. 
I worked with MTA turnstile data files that were provided in MTA website. After cleaning data, I visualized the result with the graphs.

## Design

The project was started with exploratory data analysis class from Metis data science class.
I chose to research deli-business because a few people around me are currently doing similar businesses.
Building crowd data near MTA station would help to start the business.

## Data
I used 3 months of MTA turnstile data from 7/3/21 to 10/30/21. Data has 3774102 rows and 12 columns. 
The key data I was looking were entries, exits, and dates. Some columns are very connected, so it could be ignored.

## Algorithms
- Limit the time range for the time data between 3 am to 4 pm
- Find the number of daily turnstile number
- Group the number by station
- Add entry and exit turnstile number

