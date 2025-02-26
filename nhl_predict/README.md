# NHL Prediction Model

## Technology
- Python
- MongoDB
- MySQL
- Excel  

## Skills Used 
- Machine Learning
- Database Management
- API Calling
- Data Cleaning
- Statistics  

## Context  
As many avid hockey fans are familiar with, there are 32 teams in the NHL with 82 regular season games for each team to play. While watching each NHL season, I noticed that it is not uncommon for the last-place team to beat out the first-place team, and predictions were often incorrect. The inconsistency of predictions I witnessed made me wonder why game predictions seemed so unreliable.  

To explore this, I built a prediction model using the NHL API for historical team and player data. I utilized MongoDB to extract and store data as JSON, SQL to build a database from the data, and most importantly Python with assistance from CoPilot and ChatGPT to build a prediction model. This model leverages historic team and player data to determine if predictions align with the actual results of the 2023-2024 season or if the outcomes are truly unpredictable.  

## Results  
When testing my model against the 2023-2024 NHL season, my hypothesis appears correct as my model was only able to predict the correct winner 56% of the time; however, this led me to wonder where the inaccuracy arose from leading me to dig deeper into the metrics.  

### Model Performance Metrics  

| Metric | Accuracy |
|------------------------------------------------|------------|
| Overall Model Accuracy (Pct of Correct Predictions) | 56% |
| Home Goals (Prediction and Reality Error Mean) | 1.92 MAE |
| Away Goals (Prediction and Reality Error Mean) | 2.05 MAE |
| Home Goals (Correlation Score to Model Pct) | 90% |
| Away Goals (Correlation Score to Model Pct) | 40% |

Looking at my results, my model was shown to correctly predict the winner of games 56% of the time.
```excel 
=COUNTIF(P2:P1313, "Correct") / COUNTA(P2:P1313)
```
While this is slightly above half, this is more likely due to a small sample size to predict on (82-game season) than assured correct predictions.  

When comparing the home and away goals fit in the model, there is an interesting phenomenon occurring. Although the MAE (Mean Absolute Error) of home goals: 

```excel 
=AVERAGE(R2:R1313) 
``` 
And away goals: 

```excel
=AVERAGE(S2:S1313)
```
Were close to one another, the away goals were a staggering 50% lower fit to the model than home goals according to correlation caluculations.

Home: 
```excel 
=CORREL(D2:D1313, M2:M1313)
```

Away: 
```excel 
=CORREL(H2:D1313, N2:M1313)
``` 
This is a result of how the goals are related situationally rather than raw integers. While the integer values may be close, the impact of integer changes for home goals did not impact the prediction accuracy as significantly as the away goals.  
