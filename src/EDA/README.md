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

Categorical input of 7 levels. We created 7 dummy_variables : grade_A,...grade_H for the reason below :...


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

categorical variable on 5 levels, but the level HOME_NONE appears only 3 times... we will remove these entries to get a 4-level dummy variables. Only 3 dummies are created in order to avoid colinearity : Mortgage, Own and Other. **NOTE, we should also remove HOME_OTHER which appears <100 times**


- verification_status

Categorical variable. Create dummy variable on 3 levels (Income_Verified, Income_NotVerified, and Income_SourceVerified)
We will use only 2 variables to avoid colinearity : Income_Verified and Income_SourceVerified


**- issue_d**

date, I embedded it using issue_d_day and issue_d_month. The issue_d_year should be added depending on the data source...



- loan_status

Categorical variable of 2 levels : FullyPaid : 0, ChargedOFf :1


- payment_plan

Constant variable, we will remove it


- desc

natural language text, for  now we remove it but we will may use NLP techniques


- purpose

Categorical variable of 14 levels, we will embed it using 13 dummies. the 0 is for `purpose_debt_consolidation`


- title

Similar to desc, we will remove it


- zip_code

zip_code prefix, only 3 numbers. We used a simple replace() embedding. Integers go from 0 to 822, the mapping to real zip prefixes is stored in categories_zip_code


- addr_state

Same as zip_code, we will use replace() with 50 different states


**- earliest_cr_line**

Not sure about how to deal with it. it is a date with ~10 000 wrong entries...


- revol_util

Percentage, we will convert it to float. 50 missing values. indexes stored in revol_util_missing


- initial_list_status

categorical variable 0 for F, 1 for W


**- last_pymnt_d**

Date, I don't know yet how to handle it


**- last_credit_pull_d**

Date, I don't know yet how to handle it


- application_type

categorical variable 0 for individual, 1 for joint


- verification_status_joint

Categorical variable of 3 levels, we will introduce 2 dummies : jointIncome_Verified and jointIncome_SourceVerified


**- sec_app_earliest_cr_line**

Date, I don't know how to handle those yet


- hardship_flag

constant variable, we will remove it (only one exception)


- hardship_type

constant variable, we will remove it (only one exception)


- hardship_reason

constant variable, we will remove it (only one exception)


- hardship_status

constant variable, we will remove it (only one exception)


- hardship_start_date

constant variable, we will remove it (only one exception)


- hardship_end_date

constant variable, we will remove it (only one exception)



- payment_plan_start_date

constant variable, we will remove it (only one exception)


- disbursement_method

Binary categorical variable, 0 is Cash , 1 is direct pay


- debt_settlement_flag

Binary categorical variable, 0 is No , 1 is direct Yes (very little data points)


**- debt_settlement_flag_date**

Date attribute, we will look at it after


- settlement_status

3 level categorical variable, we will use 2 dummies. 



**- settlement_date**

Dates not handled yet






**Add boolean column for max value:**
- Loan amount (named loan_amnt_is_max)
- funded_amnt (named funded_amnt_is_max)
- open_acc (named first_acc)

**Add boolean column for min value:**
- Loan amount (named loan_amnt_is_max)
- funded_amnt (named funded_amnt_is_max)

**Add boolean column for 0's:**
- funded_amnt_inv (named first_inv_for_loan)
- delinq_2yrs (named no_delinq_2yrs)
- mths_since_last_delinq (named delinq_this_month)
- mths_since_last_record (named record_this_month)
- revol_bal (named no_revolving_credit)

**Dropped columns:**
- out_prncp (only 0 or missing values)
- out_prncp_inv (only 0 or missing)
