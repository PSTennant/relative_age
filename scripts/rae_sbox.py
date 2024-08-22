# Exploring and comparing various versions of the RAE adjustment

# Libraries
from datetime import date
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from plotnine import ggplot, aes, geom_line, facet_grid, theme_minimal, scale_color_discrete, scale_linetype_discrete, labs


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

def relative_age_adjustment_linear(test_date, child_test_score, max_test_score, child_bday, oldest_in_cohort):
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

relative_age_adjustment_linear(test_date, child_test_score, max_test_score, child_bday, oldest_in_cohort)

# ================================= Complex Adjustment from Claude  ==============================

def relative_age_adjustment_exp(test_date, child_test_score, max_test_score, child_bday, oldest_in_cohort, k=1, a=2):
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

# ========================================== Understand Exp Adjustment ==========================================

print('Relative age is:', f'{(test_date - child_bday)/(test_date - oldest_in_cohort)}.',
     'On the test date, the child was this proportion as old as the oldest child')
print('Adjustment factor is:', f'{1 / (1 + math.exp(-1 * (.74 - 0.5)))}')
# Adjustment factor will be less than 1.
print('Adjustment factor is when the age gap is quite small:', f'{1 / (1 + math.exp(-1 * (.99 - 0.5)))}')
print('Adjustment factor is the age gap is quite large:', f'{1 / (1 + math.exp(-1 * (.01 - 0.5)))}')
# So at k = 1, the adjustment ranges from .38 to .62

# But what if we adjust k?
print('Adjustment factor is when the age gap is quite small:', f'{1 / (1 + math.exp(-3 * (.99 - 0.5)))}')
print('Adjustment factor is the age gap is quite large:', f'{1 / (1 + math.exp(-3 * (.01 - 0.5)))}')
# So at these levels of k and a, the adjustment ranges from .38 to .62

# and how does the adjustment factor play into the score multiplier? 
print('Score multiplier is:', f'{(1 - math.exp(-2 * (child_test_score / .56) / max_test_score))}')
print('Score multiplier is for smallest age gap:', f'{(1 - math.exp(-2 * (child_test_score / .81) / max_test_score))}')
print('Score multiplier is for largest age gap:', f'{(1 - math.exp(-2 * (child_test_score / .187) / max_test_score))}')

# And what if we adjust a? 
print('Score multiplier is:', f'{(1 - math.exp(-2 * (child_test_score / .56) / max_test_score))}')
print('Score multiplier is for smallest age gap:', f'{(1 - math.exp(-1.44 * (child_test_score / .81) / max_test_score))}')
print('Score multiplier is for largest age gap:', f'{(1 - math.exp(-1.44 * (child_test_score / .187) / max_test_score))}')


# So maybe k of 2 and a of 1.44? Is this just tuned to this exact birthday and test date combination? 

# ========================================== Comparing Adjustments =====================================

# Realistic pressure testing
# Small age gap, big score difference
relative_age_adjustment_linear(test_date=date.fromisoformat("2024-01-15"), child_bday=date.fromisoformat("2022-09-15"), child_test_score=55, max_test_score=100, oldest_in_cohort=date.fromisoformat("2022-09-01"))
# large age gap, big score difference
relative_age_adjustment_linear(test_date=date.fromisoformat("2024-01-15"), child_bday=date.fromisoformat("2021-08-30"), child_test_score=55, max_test_score=100, oldest_in_cohort=date.fromisoformat("2020-09-01"))


# Quick print version of different scores
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
testdays = [date.fromisoformat("2023-01-01"), date.fromisoformat("2024-01-01"), 
            date.fromisoformat("2025-01-01"), date.fromisoformat("2026-01-01"), 
            date.fromisoformat("2027-01-01")]
# Initialize a DataFrame to store the results
data = pd.DataFrame()
# Looping over k against different birth and test dates
for k in [.1, 1, 2, 3, 5]:
    for testday in testdays:
        for child_bday in bdays:
            lin_list = [relative_age_adjustment_linear(child_test_score = i, test_date=testday, max_test_score=max_test_score, child_bday=child_bday, oldest_in_cohort=oldest_in_cohort) for i in range(100)]
            exp_list = [relative_age_adjustment_exp(child_test_score = i, test_date=testday, max_test_score=max_test_score, child_bday=child_bday, oldest_in_cohort=oldest_in_cohort, 
            k = k) for i in range(100)]
            df = pd.DataFrame({'score': range(100), 'lin_value': lin_list, 
                            'exp_value': exp_list, 'Child_Bday': child_bday, 'test_date': testday,
                            'k': k})
            data = pd.concat([data, df], ignore_index=True)
# And reshaping to long form    
data = data.melt(id_vars=['score', 'Child_Bday', 'test_date','k'], var_name='adj_method',
                 value_vars=['lin_value', 'exp_value'], value_name="adjusted_score")

# Plot the data
plt.figure(figsize=(12, 8))
sns.lineplot(x='score', y='adjusted_score', hue='Child_Bday', style='variable', data=data, palette='tab10')
plt.title('Comparison of relative_age_adjustment across different Child_Bday values')
plt.xlabel('Original Score')
plt.ylabel('Adjusted Score')
plt.legend(title='Child Birthday and Adjustment Method')
plt.savefig("out/comp_list_4D.png")

# Faceted plot
g = sns.FacetGrid(data, col="k", row="a", hue="Child_Bday")
g.map(sns.lineplot, 'score', 'adjusted_score')
plt.savefig("out/comp_list_4D.png")

# # Create the plot
# ggplot(data, aes(x='score', y='adjusted_score', color='Child_Bday', linetype='adj_method')) +
#     geom_line()
#      +
#     facet_grid('k ~ test_date') #+
#     # scale_color_discrete(name="Child_Bday") +
#     # scale_linetype_discrete(name="Adjustment Type") +
#     # labs(
#     #     title="Faceted Line Graph",
#     #     x="Test Date",
#     #     y="Value"
#     # ) +
#     # theme_minimal()
# )
# print(plot)



# from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap
# from plotnine.data import mtcars

# (
#     ggplot(mtcars, aes("wt", "mpg", color="factor(gear)"))
#     + geom_point()
#     + stat_smooth(method="lm")
#     + facet_wrap("gear")
# )
