# **Health Data Analysis**  

## **Context**  
In 2022, I increased my efforts at staying active and logged 19 bike rides on my Apple watch between May and June. I wanted to analyze these rides to identify any patterns in what impacted my performance and if I had improved over my rides.  

To complete this, using the SQLAlchemy package through Python as well as assistance from CoPilot and ChatGPT, I created a MySQL database consisting of the data from my Apple Watch, specifically, my heart rate, average speed, elevation gain, and calories burned. Using this database, I was able to perform calculations using SQL commands to gather information such as my best ride times, my intensity per session, if recovery time influenced my performance, and if the longer I rode the more or less efficient I rode.  

## **Analysis**  
To track my performance and trends within my data, I used SQL queries to link contributing factors together.  

### **Time of Day vs. Speed**  
I initially believed I would find a strong link with the time of day that I rode my bike to my highest speed and I calculated this using:  
``` sql
HOUR(date_time), AVG(avg_speed);
```
This proved inconclusive as most values were extremely close, such as my best speed at 3 PM being nearly identical to 10 AM.

Ride Intensity vs. Distance
Looking at other potential links, Ride Intensity (calculated earlier to standardize effort to not introduce categorical bias with higher totals such as elevation gain) was selected with distance to reveal a link between more intense rides and longer distances.

This gave my most concrete performance link, however, this was not indicative of a performance gain over time as data showed that my first ride was my most intense.

### Speed vs. Duration
This led me to change my expectations and search for a link between speed and duration of my ride which was done using:
```sql 
AVG(avg_speed) GROUP BY duration;
```
This new hypothesis proved faulty as well. Although several of my shorter rides were ranked at the top, the data was inconclusive as the middle section showed no link.

### Recovery Time vs. Performance

Lastly, I looked at my ride dates and determined that there must be a link between time between rides. Unfortunately, after running the query:
```sql
AVG(avg_speed) GROUP BY hours_since_last_ride;
```
This showed no correlation between the two leading me to believe that my performance was not impacted by anything other than external factors such as my psychological state or the weather.