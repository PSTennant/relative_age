# Exploring and comparing various versions of the RAE adjustment

# Libraries
from datetime import date
import math
import matplotlib.pyplot as plt

# ================================================== Inputs ============================================================
child_bday = date.fromisoformat("2021-07-18")
oldest_in_cohort = date.fromisoformat("2020-09-01")
test_date = date.fromisoformat("2024-01-15")
child_test_score = 70
max_test_score = 100

# ============================================ Minimum Viable Prototype ============================================================

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


# ========================================== Complex Adjustment from Claude ================================================

def relative_age_adjustment(child_test_score, child_bday, max_test_score, oldest_in_cohort, k=1, a=2):
    """
    Adjusts a test score to account for the relative age effect using a logistic function with soft capping.
    
    Args:
        test_date (date): The date of the assessment or exam
        child_test_score (float): The original test score.
        child_bday (date): The birtday of the focal student.
        max_test_score (float): The maximum possible score on the test.
        oldest_in_cohort (date): The birthdate of the oldest student in the cohort
        k (float): The steepness constant for the logistic adjustment function.
        a (float): The steepness constant for the soft capping scaling function.
    
    Returns:
        float: The adjusted test score, capped smoothly within the valid score range.
    """
    # Calculate the relative age as a percentage of the cohort age range
    relative_age = (test_date - oldest_in_cohort)/(test_date - child_bday)
    
    # Apply the logistic adjustment function
    adjustment_factor = 1 / (1 + math.exp(-k * (relative_age - 0.5)))
    
    # Apply the soft capping scaling function
    adjusted_score = max_test_score * (1 - math.exp(-a * (child_test_score / adjustment_factor) / max_test_score))
    
    return adjusted_score

relative_age_adjustment(child_test_score, child_bday, max_test_score, oldest_in_cohort)

# ========================================== Comparing Adjustments ================================================

for i in range(100):
    print(relative_age_adjustment(i, child_bday, max_test_score, oldest_in_cohort))



# How to add a plot to the loop above? 
# Sample array of numbers
numbers = [3, 7, 2, 9, 4, 1, 8, 5]
# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(numbers, marker='o')  # Line plot with dots at each point
# Customize the plot
plt.title('Array Values vs. Index')
plt.xlabel('Index')
plt.ylabel('Value')
plt.grid(True)
# Show the plot
plt.show()
