# Setup and Libraries
from shiny.express import input, render, ui
from shinyswatch import theme
from datetime import date, timedelta
import pandas as pd
import plotnine as p9

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

ui.page_opts(title="Relative Age Effect Adjustment (Prototype)",theme=theme.spacelab)

with ui.sidebar():
    # Page Title
    ui.panel_title("Inputs", "RAE Adjustment")

    # Child name
    ui.input_text("child_name", "Child's Name")

    # Date Inputs
    ui.input_date("test_date", "Date of Assessment")
    ui.input_date("child_bday", "Birthdate of Child", value = date.today()-timedelta(days=365))
    ui.input_date("oldest_bday", "Birthdate of the Oldest Child in Cohort", value = date.today()-timedelta(days=366))

    # Score Inputs
    ui.input_numeric("child_score", "Assessment Score of Child", value = None, min = 0, max = 100)
    ui.input_numeric("max_score", "Maximum Possible Assessment Score", value = None, min = 0, max = 100)

with ui.navset_pill(id="tab"):  
    with ui.nav_panel("Introduction"):
        ui.HTML("""
        The Relative Age Effect (RAE) is a phenomenon where children born earlier in a school year tend to outperform their younger classmates. This effect, first noticed in sports, is now recognized as a significant factor in education.
        <br>
        <br>
        Most school systems group children by birth year or academic year. This creates age gaps within a single grade—some kids can be nearly a year older than others in their class. For young children, this age difference can significantly impact their development and performance. RAE gives older students in a grade an advantage. They often score higher on tests, are more likely to be labeled as gifted, and less likely to be diagnosed with learning disabilities. This advantage is most noticeable in early school years but can persist throughout a student's education.
        <br>
        <br>
        <b>Several factors contribute to RAE:</b>
        <br>
        <ul>
            <li>Older students may be more cognitively and physically developed.</li>
            <li>They might be more emotionally mature.</li>
            <li>They've had more time to learn and experience the world.</li>
            <li>Teachers might have higher expectations for older students.</li>
            <li>Early successes can boost confidence and motivation.</li>
        </ul>
        While RAE's impact lessens over time, its early influence can affect a student's self-image, educational choices, and even career path. This long-term effect highlights the need for a more nuanced approach to academic assessment, especially in early education. Current standardized tests don't account for these age differences within grades. This oversight can lead to younger students being unfairly labeled as underperforming, while older students may be overestimated. To address this issue, we need age-adjusted test scores. This approach would consider a student's exact age when testing, allowing for fairer comparisons within a grade. By adjusting scores based on relative age, educators can make better decisions about student placement, support, and interventions. Implementing age-adjusted scoring could significantly improve educational equity. It would level the playing field, ensuring younger students aren't unfairly disadvantaged and older students are appropriately challenged. It could also lead to more effective teaching strategies, tailored to students' actual developmental needs rather than their relative age in class.
        <br>
        <br>
        This analysis will explore current research on RAE in academic testing, examine existing age adjustment methods, and propose a framework for implementing age-adjusted test scores. Our goal is to contribute to creating fairer and more accurate assessment practices in education, supporting the success of all students, regardless of their birth month.
        """)

    with ui.nav_panel("Methods"):
        ui.HTML("""
        The function used here adjusts a test score to account for the relative age effect, which can impact the performance of younger students compared to their older peers within the same cohort. The method uses a linear adjustment with hard capping to ensure that the adjusted score remains within the valid range.
        <br>
        <br>
        <b>Required Inputs:</b>
        <br>
        <ol>
            <li>Date of Assessment: The date when the test or assessment was conducted.</li>
            <li>**child_test_score (float)**: The original score of the child on the test.</li>
            <li>**max_test_score (float)**: The maximum possible score on the test.</li>
            <li>**child_bday (date)**: The birthdate of the child whose score is being adjusted.</li>
            <li>**oldest_in_cohort (date)**: The birthdate of the oldest student in the cohort.</li>
        </ol>
        <br>
        <b>Adjustments Made:</b>
        1. **Calculate Time Differences**:
        - `oldest_delta`: The number of days between the test date and the birthdate of the oldest student.
        - `child_delta`: The number of days between the test date and the birthdate of the child whose score is being adjusted.
        2. **Compute Inflation Factor**:
        - `inflation_factor`: The ratio of `oldest_delta.days` to `child_delta.days`, representing the relative age difference.
        3. **Adjust Score**:
        - Multiply the child's original test score by the `inflation_factor` to get the adjusted score.
        - Round the adjusted score to the nearest integer.
        4. **Cap Score**:
        - If the adjusted score exceeds the maximum possible score (`max_test_score`), cap it at `max_test_score`.

        ### Expected Output:
        - **float**: The adjusted test score, which is rounded and capped within the valid score range.

        ### Edge Cases and Inaccuracies:
        1. **Division by Zero**: If `child_delta.days` is zero (i.e., the test date is the same as the child's birthday), this will cause a division by zero error.
        2. **Negative Scores**: If the adjusted score calculation results in a negative value, the function does not handle this explicitly.
        3. **Over-Adjustment**: The linear adjustment may not accurately reflect the true impact of relative age, particularly in cases where the age difference is large.
        4. **Rounding**: Rounding to the nearest integer can introduce minor inaccuracies, especially for scores that are close to the rounding threshold.

        By considering these edge cases and potential inaccuracies, users can better understand the limitations and appropriate use of the `relative_age_adjustment_linear` function.
        """)

    with ui.nav_panel("Results"):
        @render.text
        def child_name_val():
            return f"Child's Name: {input.child_name()}"

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

        @render.plot
        def my_plot():
            # Create a DataFrame from val1 and val2
            data = pd.DataFrame({
                'x': [input.inflation_factor],
                'y': [input.adjusted_score]
            })
            plot = (
                p9.ggplot(data, p9.aes('x', 'y')) +
                p9.geom_point()
            )
            return plot

