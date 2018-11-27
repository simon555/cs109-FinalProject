This folder will contain the scripts for : 
- data cleaning
- feature engineering


## Data Cleaning Summary
- id
empty attribute, we removed it

- term

Convert into a categorical attribute. 0 for 36 months, 1 for 60 months

- int_rate

Convert into a float attribute

- grade

Categorical input of 7 levels. We created 7 dummy_variables : grade_A,...grade_G

- sub_grade

Every grade can be declined in 5 different sub-grades. We could create 35 different dummy variables (sub_grade_A1, ..., sub_grade_G5) but we decided to embed the sub_grade in the grade. Namely we will use this convention  :

```
sub_grade = A1 --> grade_A=1
sub_grade = D4 --> grade_D=4
sub_grade = A3 --> grade_A=2
```
