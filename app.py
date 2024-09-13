# Setup and Libraries
from shiny.express import input, render, ui
from datetime import date, timedelta

# ========================================== RAE Adjusment Function ================================================

def relative_age_adjustment_linear(test_date, child_bday, oldest_in_cohort, child_test_score, max_test_score):
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

# ========================================== User Interface ================================================

# Page Title
ui.panel_title("Relative Age Effect Adjustment (Protoype)", "RAE Adjustment")

# Date Inputs
ui.input_date("test_date", "Date of Assessment")
ui.input_date("child_bday", "Birthdate of Child", value = date.today()-timedelta(days=365))
ui.input_date("oldest_bday", "Birthdate of the Oldest Child in Cohort", value = date.today()-timedelta(days=366))

# Score Inputs
ui.input_numeric("child_score", "Assessment Score of Child", value = None, min = 0, max = 100)
ui.input_numeric("max_score", "Maximum Possible Assessment Score", value = None, min = 0, max = 100)

# ========================================== Server Logic ==================================================
@render.text
def test_date_val():
    return f"Test Date: {input.test_date()}"

@render.text
def child_bday_val():
    return f"Child Birthdate: {input.child_bday()}"

@render.text
def oldest_bday_val():
    return f"Oldest in Cohort Birthdate: {input.oldest_bday()}"

@render.text
def child_score_val():
    return f"Child Assessment Score: {input.child_score()}"

@render.text
def max_score_val():
    return f"Maximum Possible Assessment Score: {input.max_score()}"

@render.text
def age_comparison_val():
    child_age_on_testdate = input.test_date() - input.child_bday()
    oldest_age_on_testdate = input.test_date() - input.oldest_bday()
    age_ratio = oldest_age_on_testdate.days/child_age_on_testdate.days
    percent_older = (age_ratio - 1)*100
    return f"\nOn the test date, the oldest child was {percent_older:.0f}% older than your child."

@render.text
def adjusted_score_val():
    if input.test_date() is None or input.child_bday() is None or input.oldest_bday() is None or input.child_score() is None or input.max_score() is None:
        return "Please fill out all fields to see your child's adjusted score."
    return f"Your child's age adjusted score: {relative_age_adjustment_linear(input.test_date(), input.child_bday(), input.oldest_bday(), input.child_score(), input.max_score())}"