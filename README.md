# Optimizing Urban Traffic Safety: A Data-Driven Analysis of NYC Road Accidents

## Project Overview
This project provides a comprehensive exploratory data analysis (EDA) of NYC road accidents from January 2021 to April 2023. By leveraging Python libraries such as Pandas, NumPy, Matplotlib, and Seaborn, the project aims to uncover temporal patterns, spatial hotspots, and key contributing factors behind traffic collisions in New York City. The analysis is designed to derive actionable insights that can inform urban planning and road safety initiatives.

## Link for downloading the dataset
https://maven-datasets.s3.amazonaws.com/NYC+Traffic+Accidents/NYC_Collisions.zip


## Project Objectives
1. **Monthly Accident Distribution Analysis:**  
   Assess the percentage of total accidents per month to identify seasonal trends and potential outliers.

2. **Temporal Pattern Decomposition:**  
   Break down accident frequencies by day of the week and hour of the day to pinpoint peak periods of incidents.

3. **Accident Hotspot Identification:**  
   Identify areas with higher concentrations of accidents using available location data (e.g., by borough and street name).

4. **Street-Specific Risk Evaluation:**  
   Determine which street experiences the highest number of accidents and calculate its share relative to the total.

5. **Contributing Factor Assessment:**  
   Analyze the most common contributing factors for all accidents, providing insights into underlying causes.

6. **Fatal Accident Causality Analysis:**  
   Isolate and analyze fatal accidents to determine the primary contributing factors in these cases.

7. **Injury Severity Profiling:**  
   Evaluate the distribution of injuries and fatalities among pedestrians, cyclists, and motorists to assess public safety risks.

8. **Vehicle Type Impact Analysis:**  
   Investigate correlations between vehicle types involved and the severity of outcomes, identifying potential risk patterns.

9. **Temporal-Spatial Correlation Exploration:**  
   Examine how temporal factors (month, day, hour) correlate with accident occurrences by borough and street name to develop targeted safety strategies.

10. **Data Quality and Outlier Management:**  
    Implement robust data cleaning and outlier detection techniques to ensure the reliability of the insights derived.

## Methodology and Steps

1. **Data Ingestion and Setup:**  
   - Import necessary Python libraries.
   - Load the NYC road accidents dataset using Pandas.
   - Convert the Date and Time columns into a unified datetime object.

2. **Data Cleaning and Preprocessing:**  
   - Handle missing values and perform data type conversions.
   - Engineer additional features such as month, day of the week, and hour from the datetime column.

3. **Exploratory Data Analysis (EDA):**  
   - Analyze monthly accident distributions to identify seasonal trends.
   - Break down accident frequencies by day of the week and hour of the day.
   - Visualize these temporal patterns using bar plots and line graphs.

4. **Spatial and Street-Level Analysis:**  
   - Analyze accident data by borough and street name to identify hotspots.
   - Determine the street with the highest number of accidents and calculate its contribution to the total.

5. **Contributing Factors and Severity Analysis:**  
   - Examine the overall frequency of contributing factors.
   - Focus on fatal accidents to isolate the top contributing factors in severe cases.
   - Profile injury severity across different user groups (pedestrians, cyclists, motorists).

6. **Advanced Temporal-Spatial Correlation:**  
   - Explore correlations between time-based factors and geographic accident data.
   - Segment data into specific time intervals (e.g., rush hours) to identify targeted patterns.

7. **Reporting and Visualization:**  
   - Document findings in a comprehensive report.
   - Combine visualizations and narrative to communicate insights clearly.

8. **Actionable Insights and Recommendations:**  
   - Summarize key findings and interpret their implications for urban traffic safety.
   - Provide actionable recommendations for policymakers and urban planners based on the analysis.
