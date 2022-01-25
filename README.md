# Storms Prediction
In our Storm Prediction <br>
1. we tried to predict the strength of the wind.<br>
2. We tried to predict the probability of a storm intensity according to Beaufort scale.
## To install our program
```
git clone <web URL>
pip install selenium
pip install plotly==5.5.0
```
 Download chrome driver: [Click here to download chromedriver](https://chromedriver.chromium.org/downloads)

## Data Acquisition
We scraping our data from [Wunderground](https://www.wunderground.com/hurricane/archive) .<br>
We used Selenium and Beautiful Soup libraries.<br>
We export our data to CSV file using Pandas library.<br>
- Open Acquisition.ipynb 
- Paste your chromedriver path in chromeDriverPath
- Run the program

## Data Cleaning
We clean our data using Pandas library.<br>
- Open data_cleaning
- Import storms.csv
- Run the program

## EDA & Visualization
We visualize our data with Plotly, Matplotlib and Seaborn libraies.<br>
- Open visualizaation.ipynb
- Import cleaningDF.csv
- Run the program

## Machine Learning
We builded our model using Sklearn library.<br>
- Open ML.ipynb
- Import cleaningDF.csv
- Run the program
- Enter your requested predict values

### Model Evaluation
- Linear Regression:<br>
![Screenshot (321)](https://user-images.githubusercontent.com/68068799/151043826-b3e3ea99-a3e1-470f-a2f8-b80437c71665.png)

- Logistic Regression:<br>
![Screenshot (318)](https://user-images.githubusercontent.com/68068799/151043932-4b2ff83b-798f-46f5-85d7-10c9244ad495.png)


