This folder will contain the scripts for :
- data cleaning
- feature engineering


## Instructions
1. You should work on the small data provided on the drive in data/smallData/rawData/ 
You will download these files and put them in your own github repo (locally) at data/smallData/rawData/

2. To perform your data cleaning, you should create your own jupyter notebook EDA_[yourName].ipynb and then, for every feature you are cleaning **in the notebook** :

a. Write an outline of what you are going to do

b. Make your analysis/data modification

c. Write a Conclusion

d. Write a summary of what you did for that feature **in the README**


I will provide a template of EDA.ipynb you can use

3. When you finished your data cleaning on your features, save your cleaned dataset in data/tmp/[yourName]/ ...
                                          




## Data Cleaning Summary
- id

empty attribute, we removed it


- term

Convert into a categorical attribute. 0 for 36 months, 1 for 60 months


- int_rate

Convert into a float attribute. For now we kept it as 0-100 but maybe we should rescale it between 0 and 1 ?


- grade

Categorical input of 7 levels. We created 7 dummy_variables : grade_A,...grade_G


- sub_grade

Every grade can be declined in 5 different sub-grades. We could create 35 different dummy variables (sub_grade_A1, ..., sub_grade_G5) but we decided to embed the sub_grade in the grade. Namely we will use this convention  :

```
sub_grade = A1 --> grade_A=1
sub_grade = D4 --> grade_D=4
sub_grade = A3 --> grade_A=2
```

- emp_title

Name of the borrower'job, not useful for our analysis. We will remove this variable


- emp_length

number of missing values : 1078.
We embedded these strings ('<1 year', '4 years', '10+ years',..) as integers (0,4,10,...). The missing values have not been modified yet


- home_ownership

categorical variable on 5 levels, but the level HOME_NONE appears only 3 times... we will remove these entries to get a 4-level dummy variables. **NOTE, we should also remove HOME_OTHER which appears <100 times**


- verification_status

Did not find doc. To be continued...

Add boolean column for max value
- Loan amount (named loan_amnt_is_max)
- funded_amnt (named funded_amnt_is_max)

Add boolean column for min value
- Loan amount (named loan_amnt_is_max)
- funded_amnt (named funded_amnt_is_max)

Add boolean column for 0's
- funded_amnt_inv (named first_inv_for_loan)
- delinq_2yrs (named no_delinq_2yrs)
