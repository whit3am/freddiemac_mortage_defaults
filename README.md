# Freddie Mac Late Payment Predictions.
This repo predicts if a 15-year mortgage will ever go past 89 days late using loan level data
from Freddie Mac. The data dictionary can be found here: http://www.freddiemac.com/fmac-resources/research/pdf/user_guide.pdf

## Organization
The repo is organized as follows.
1. data_builder: downloads data from Freddie Mac and builds the
data directory.
2. eda: explores and preprocesses the data.
3. modeling: stores notebooks to build models. 

Below explains the problem setup, results, and methods.

## Problem set up
I wanted to see if loan level data from 1999-2001 could be used to
predict late payments for years outside that range. The goal is to
predict if a loan has ever been over 89 days late or not.

## Results

The metric used was f1 score as both recall and precision are
important here. Accuracy would be useless as the dataset is
imbalanced. 

The first set of models were trained on the following variables:

    original_combined_loan-to-value_(cltv) 
    original_debt-to-income_(dti)_ratio      
    original_upb                             
    original_loan-to-value_(ltv)             
    credit_score                        
    number_of_units                     
    original_interest_rate               
    number_of_borrowers 

These were already in numeric format with no nulls,
so they were easy to throw into a model.

### Test Error (1999-2001)

| f-1 Scores          | No Pre-Processing (Top 8) | Pre-Processed (All) |
|---------------------|---------------------------|---------------------|
| Baseline            | 0.1627                    | 0.1627              |
| Naive Bayes         | 0.2734                    | 0.2660              |
| Random Forest       | 0.3302                    | 0.3650              |
| Logistic Regression | 0.2793                    | 0.2783              |


### 2005 Error

| f-1 Scores          | No Pre-Processing (Top 8) | Pre-Processed (All) |
|---------------------|---------------------------|---------------------|
| Baseline            | 0.1059                    | 0.1059              |
| Naive Bayes         | To Be Calculated          | To Be Calculated    |
| Random Forest       | To Be Calculated          | 0.1270              |
| Logistic Regression | To Be Calculated          | To Be Calculated    |




From the charts above it is clear that the models were unable to
generalize beyond the years their training data encompassed.

## Methods
   To be added...
### Quick No Preprocessing Models
   To be added...
### Preprocessing
   To be added...
### Imbalanced Data
   To be added...
## Future Work

1. Dimensionality Reduction
2. Custom Balancing
3. Use all the other classification methods (boosted trees, neural nets
   , etc)
4. Reframe solution to predict next quarter's/year's loans that will 
   be late and roll that forward after each time period. This would 
   allow more data to flow into the model via added exogenous 
   variables like forecasted GDP increases and the previous payment
   history on the loan. This model may be more useful business wise
   as well because it could be used to regrade loans within a mortgage
   backed security throughout the life span of the loan. 
   