# Exploring and comparing various versions of the RAE adjustment

# Libraries
from datetime import date
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# ================================================== Inputs =======================================
child_bday = date.fromisoformat("2021-07-18")
oldest_in_cohort = date.fromisoformat("2020-09-01")
test_date = date.fromisoformat("2024-01-15")
child_test_score = 70
max_test_score = 100

# ===================================== Minimum Viable Prototype ========================================

# Calculate the difference between the two dates
oldest_delta = test_date - oldest_in_cohort
child_delta = test_date - child_bday

# Access the number of days
inflation_factor = oldest_delta.days/child_delta.days

# New test score
child_inflated_score = round(child_test_score*inflation_factor)
if child_inflated_score > max_test_score:
    child_inflated_score = max_test_score

# printing results
print(f"The inflation factor from a test date of {test_date} for a child born {child_bday} in a cohort with",
      f"oldest member born on {oldest_in_cohort} is {inflation_factor}.", 
      f"That means the test score of {child_test_score} should actually be {child_inflated_score}")

# ===================================== MVP into Linear Function ========================================

def relative_age_adjustment_linear(child_test_score, max_test_score, child_bday, oldest_in_cohort):
    """
    Adjusts a test score to account for the relative age effect using a linear function with hard capping.
    
    Args:
        test_date (date): The date of the assessment or exam
        child_test_score (float): The original test score.
        max_test_score (float): The maximum possible score on the test.
        child_bday (date): The birtday of the focal student.
        oldest_in_cohort (date): The birthdate of the oldest student in the cohort
    
    Returns:
        float: The adjusted test score, capped within the valid score range.
    """
    # Calculate the difference between the two dates
    oldest_delta = test_date - oldest_in_cohort
    child_delta = test_date - child_bday
    # Access the number of days
    inflation_factor = oldest_delta.days/child_delta.days
    # New test score
    adjusted_score = round(child_test_score*inflation_factor)
    if adjusted_score > max_test_score:
        adjusted_score = max_test_score
    return adjusted_score

relative_age_adjustment_linear(child_test_score, max_test_score, child_bday, oldest_in_cohort)

# ================================= Complex Adjustment from Claude into Function ==============================

def relative_age_adjustment_exp(child_test_score, max_test_score, child_bday, oldest_in_cohort, k=1, a=2):
    """
    Adjusts a test score to account for the relative age effect using a logistic function with soft capping.
    
    Args:
        test_date (date): The date of the assessment or exam
        child_test_score (float): The original test score.
        max_test_score (float): The maximum possible score on the test.
        child_bday (date): The birtday of the focal student.
        oldest_in_cohort (date): The birthdate of the oldest student in the cohort
        k (float): The steepness constant for the logistic adjustment function.
        a (float): The steepness constant for the soft capping scaling function.
    
    Returns:
        float: The adjusted test score, capped smoothly within the valid score range.
    """
    # Calculate the relative age as a percentage of the cohort age range
    relative_age = (test_date - child_bday)/(test_date - oldest_in_cohort)
    # Apply the logistic adjustment function
    adjustment_factor = 1 / (1 + math.exp(-k * (relative_age - 0.5)))
    # Apply the soft capping scaling function
    adjusted_score = max_test_score * (1 - math.exp(-a * (child_test_score / adjustment_factor) / max_test_score))
    adjusted_score = round(adjusted_score)
    return adjusted_score

relative_age_adjustment_exp(child_test_score, max_test_score, child_bday, oldest_in_cohort)

# ========================================== Comparing Adjustments ================================================

# Quick print version
for i in range(100):
    print(i, 
          relative_age_adjustment_exp(i, max_test_score, child_bday, oldest_in_cohort),
          relative_age_adjustment_linear(i, max_test_score, child_bday, oldest_in_cohort))

# # Making it into a list
# comp_list = []
# for i in range(100):
#     comp_list.append(relative_age_adjustment(i, max_test_score, child_bday, oldest_in_cohort))
# Same thing as list comprehnsion
comp_list = [relative_age_adjustment_exp(i, max_test_score, child_bday, oldest_in_cohort) for i in range(100)]

# Line Plot
plt.figure(figsize=(10, 6))
sns.lineplot(x=range(len(comp_list)), y=comp_list)
plt.title('Line Plot of comp_list')
plt.xlabel('Original Score')
plt.ylabel('Adjusted Score')
# plt.show()
plt.savefig("out/comp_list_linefig.png")


# **** Multi-Dimensional Version ****

# Create the data
# List of child birthdays to cycle through
bdays = [date.fromisoformat("2020-09-01"), date.fromisoformat("2020-12-31"), 
         date.fromisoformat("2021-03-31"), date.fromisoformat("2021-07-18"), 
         date.fromisoformat("2021-08-30")]
# Initialize a DataFrame to store the results
data = pd.DataFrame()
# Calculate comp_list for each child_bday and store the results
for child_bday in bdays:
    lin_list = [relative_age_adjustment_linear(i, max_test_score, child_bday, 
                oldest_in_cohort) for i in range(100)]
    exp_list = [relative_age_adjustment_exp(i, max_test_score, child_bday, oldest_in_cohort) for i in range(100)]
    df = pd.DataFrame({'score': range(100), 'lin_value': lin_list, 
                       'exp_value': exp_list, 'Child_Bday': child_bday})
    data = pd.concat([data, df], ignore_index=True)
# And reshaping to long form    
data = data.melt(id_vars=['score', 'Child_Bday'], value_vars=['lin_value', 'exp_value'],
                 value_name="adjusted_score")

# Plot the data
plt.figure(figsize=(12, 8))
sns.lineplot(x='score', y='adjusted_score', hue='Child_Bday', style='variable', data=data, palette='tab10')
plt.title('Comparison of relative_age_adjustment across different Child_Bday values')
plt.xlabel('Original Score')
plt.ylabel('Adjusted Score')
plt.legend(title='Child Birthday and Adjustment Method')
plt.savefig("out/comp_list_2D.png")
