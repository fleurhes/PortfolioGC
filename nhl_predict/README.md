# NHL Prediction Model

## Context  
As many avid hockey fans are familiar with, there are 32 teams in the NHL with 82 regular season games for each team to play. While watching each NHL season, I noticed that it is not uncommon for the last-place team to beat out the first-place team, and predictions were often incorrect. The inconsistency of predictions I witnessed made me wonder why game predictions seemed so unreliable.  

To explore this, I built a prediction model using the NHL API for historical team and player data. I utilized MongoDB to extract and store data as JSON, SQL to build a database from the data, and most importantly Python with assistance from CoPilot and ChatGPT to build a prediction model. This model leverages historic team and player data to determine if predictions align with the actual results of the 2023-2024 season or if the outcomes are truly unpredictable.  

## Results  
When testing my model against the 2023-2024 NHL season, my hypothesis appears correct as my model was only able to predict the correct winner 56% of the time; however, this led me to wonder where the inaccuracy arose from.  

### Model Performance Metrics  

| Metric | Accuracy |
|------------------------------------------------|------------|
| Overall Model Accuracy (Pct of Correct Predictions) | 56% |
| Home Goals (Prediction and Reality Error Mean) | 1.92 |
| Away Goals (Prediction and Reality Error Mean) | 2.05 |
| Home Goals (Correlation Score to Model Pct) | 90% |
| Away Goals (Correlation Score to Model Pct) | 40% |

Looking at my results, my model was shown to correctly predict the winner of games 56% of the time. While this is slightly above half, this is more likely due to a small sample size to predict on (82-game season) than assured correct predictions.  

When comparing the home and away goals fit in the model, there is an interesting phenomenon occurring. Although the MAE (Mean Absolute Error) of home and away goals were close to one another, the away goals were a staggering 50% lower fit to the model than home goals. This is a result of how the goals are related situationally rather than raw integers. While the integer values may be close, the impact of integer changes for home goals did not impact the prediction accuracy as significantly as the away goals.  
