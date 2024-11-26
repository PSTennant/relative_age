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

ui.page_opts(title="Relative Age Effect Adjustment)",theme=theme.spacelab)

with ui.sidebar():
    # Page Title
    ui.panel_title("Inputs", "RAE Adjustment")

    # Child name
    ui.input_text("child_name", "Child's Name")

    # Date Inputs
    ui.input_date("test_date", "Date of Assessment")
    ui.input_date("child_bday", "Birthdate of Child", value = date.today()-timedelta(days=730))
    ui.input_date("oldest_bday", "Birthdate of the Oldest Child in Cohort", value = date.today()-timedelta(days=1000))

    # Score Inputs
    ui.input_numeric("child_score", "Assessment Score of Child", value = None, min = 0, max = 100)
    ui.input_numeric("max_score", "Maximum Possible Assessment Score", value = None, min = 0, max = 100)

with ui.navset_pill(id="tab"):  
    with ui.nav_panel("Introduction"):
        ui.HTML("""
        The Relative Age Effect (RAE) is a phenomenon whereby older children in a given age cohort (e.g., those born earlier in a school year) tend to outperform their younger classmates in the same cohort. This effect, first noticed in sports, is now recognized as a significant factor in education.
        <br>
        <br>
        Most school systems group children by birth year or academic year. This creates age gaps within a single grade — the oldest children in a cohort can be nearly a year older than the youngest in their cohort – that can significantly impact their development and performance. The oldest children in a given cohort often score higher on assessments and tests, are more likely to be labeled as gifted, and less likely to be diagnosed with learning disabilities. This advantage is most noticeable in young children, but the effects of this gap can persist throughout a student's education and life, particularly if children are set into academic tracks (e.g., a gifted and talented track) based on their assessment scores during early childhood. 
        <br>
        <br>
        <b>Several factors contribute to RAE:</b>
        <br>
        <ul>
            <li>Older students may be more cognitively, physically, and emotionally developed.</li>           <li>They've had more time to learn and experience the world.</li>
            <li>Teachers might have higher expectations for older students.</li>
            <li>Early successes can boost confidence and motivation.</li>
        </ul>
        While RAE's impact lessens over time (as a single year of age differences becomes a smaller proportional difference in the age of individuals in the same cohort), its early influence can affect a student's self-image, educational choices and opportunities, and even career path. This long-term effect highlights the need for a more nuanced approach to academic assessment, especially in early education. Current standardized tests don't account for these age differences within grades. This oversight can lead to younger students being unfairly labeled as underperforming, while older students may be overestimated. To address this issue, we need age-adjust test and assessment scores. This approach would consider a student's exact age when testing, allowing for fairer comparisons within a cohort. By adjusting scores based on relative age, educators can make better decisions about student placement, support, and interventions. Implementing age-adjusted scoring would level the playing field, ensuring younger students aren't unfairly disadvantaged and older students are appropriately challenged. It could also lead to more effective teaching strategies, tailored to students' actual developmental needs rather than their relative age in their cohort.
        <br>
        <br>
        This adjustment calculator provides a simple and direct method of adjusting a child's assessment score based on their relative age. The linear adjustment in this application is one of many possible methods for addressing this concern, but is preferred here because of its intuitive interpretation and ease of implementation. That said, other methods could be developed for relative age adjustment and may be preferrable in certain cases. Regardless, the the need to adjust scores in some fashion is clear.
        """)

    with ui.nav_panel("Methods"):
        ui.HTML("""
        The function used here adjusts a child's assessment score to account for the relative age effect. The method uses a linear adjustment with hard capping to ensure that the adjusted score remains within the valid range.
        <br>
        <br>
        <b>Required Inputs:</b>
        <br>
        <ul>
            <li>Date of Assessment: The date when the test or assessment was conducted.</li>
            <li>Birthday of Child: The birthdate of the child whose score is being adjusted.</li>
            <li>Birthdate of the Oldest Child in Cohort: The birthdate of the oldest student in the cohort.</li>
            <li>Child Assessment Score: The original score of the child on the assessment or test.</li>
            <li>Maximum Possible Assessment Score: The maximum possible score on the assessment or test.</li>
        </ul>
        <b>Adjustment Method:</b>
        <br>
        <ol>
            <li>Calculate Time Differences: Calculate the number of days between the test date and the birthdate of the oldest student, and the number of days between the test date and the birthdate of the child whose score is being adjusted.
            <li>Compute Inflation Factor: The inflation factor is the ratio of age (in days) of oldest child in the cohort to the age (in days) of the focal child.
            <li>Adjust Score: Multiply the child's original test score by the Inflation Factor to get the adjusted score, then round the adjusted score to the nearest integer.</li>
            <li>Cap Score: If the adjusted score exceeds the maximum possible score, set the adjusted score to maximum possible score.</li>
        </ol>
        <b>Expected Output:</b>
        <br>
        <ul> 
            <li>Adjusted score: The adjusted test score, which is rounded and capped within the valid score range.</li>
        </ul>
        """)

    with ui.nav_panel("Results"):
        
        # Add CSS for spacing
        ui.HTML("""
        <style>
            .section { margin-top: 20px; }
            .plot-container { width: 100%; max-width: 600px; margin: 0 auto; }
        </style>
        """)
        
        # Header for age comparison
        ui.HTML("<h4 class='section'>Age Comparison</h3>")

        @render.text
        def age_comparison_val():
            child_age_on_testdate = input.test_date() - input.child_bday()
            oldest_age_on_testdate = input.test_date() - input.oldest_bday()
            age_ratio = oldest_age_on_testdate.days / child_age_on_testdate.days
            percent_older = (age_ratio - 1) * 100
            if input.child_name() == "":
                return f"On the test date, the oldest child in the cohort was {percent_older:.0f}% older than your child."
            if input.child_name() is not None:
                return f"On the test date, the oldest child in the cohort was {percent_older:.0f}% older than {input.child_name()}."

        # Header for adjusted score
        ui.HTML("<h4 class='section'>Adjusted Score</h3>")

        @render.text
        def adjusted_score_val():
            if input.test_date() is None or input.child_bday() is None or input.oldest_bday() is None or input.child_score() is None or input.max_score() is None:
                if input.child_name() == "":
                    return "Please fill out all input fields to see your child's adjusted score."
                if input.child_name() is not None:
                    return f"Please fill out all input fields to see {input.child_name()}'s adjusted score."
            if input.child_name() == "":
                return f"Your child's age adjusted score: {relative_age_adjustment_linear(input.test_date(), input.child_bday(), input.oldest_bday(), input.child_score(), input.max_score())}"
            if input.child_name() is not None:
                return f"{input.child_name()}'s age adjusted score: {relative_age_adjustment_linear(input.test_date(), input.child_bday(), input.oldest_bday(), input.child_score(), input.max_score())}"
        
        # Header for the plot
        ui.HTML("<h4 class='section'>Score Visualization</h3>")

        @render.plot(width=800)
        def my_plot():
            # Calculate the adjusted score once
            test_date = input.test_date()
            child_bday = input.child_bday()
            oldest_bday = input.oldest_bday()
            child_score = input.child_score()
            max_score = input.max_score()
            # Make sure all 5 inputs are available before calculating the adjusted score
            if None in [test_date, child_bday, oldest_bday, child_score, max_score]:
                return None  # Return nothing if inputs are missing
            # Calculate the adjusted score
            adjusted_score = relative_age_adjustment_linear(test_date, child_bday, oldest_bday, child_score, max_score)
            # Prepare the data for stacked bar plot
            data = pd.DataFrame({
                'Category': pd.Categorical(['RAE Score Adjustment', 'Original Score'],
                                            categories=['RAE Score Adjustment', 'Original Score'], 
                                            ordered=True),
                'Score': [adjusted_score - child_score, child_score]  # Adjusted minus original for the top part
            })
            # Create the stacked bar plot
            plot = (
                p9.ggplot(data, p9.aes(x='1', y='Score', fill='Category')) +
                p9.geom_bar(stat='identity', position='stack', width=0.5) +
                p9.scale_fill_manual(values=['#0ecbff', '#0d3958']) +
                p9.labs(title="Original and RAE Adjusted Score",
                        x="",
                        y="Score") +
                p9.ylim(0, max_score) +
                p9.scale_x_continuous(limits=(0, 2)) + 
                p9.theme_classic() +
                p9.theme(
                    axis_text_x=p9.element_blank(),
                    axis_ticks_major_x=p9.element_blank(),
                    plot_title=p9.element_text(size=14, weight='bold'),
                    legend_title=p9.element_text(size=12, family="Arial"),
                    text=p9.element_text(size=12, family="Arial"),
                    legend_position='right')
            )
            return plot
    with ui.nav_panel("References"):
        ui.HTML("""
        <b>References:</b>
        <br>
        <ul>
            <li>Delorme, N., & Champely, S. (2015). Relative Age Effect and chi-squared statistics. International Review for the Sociology of Sport, 50(6), 740–746. https://doi.org/10.1177/1012690213493104</li>
            <li>Holland, J., & Sayal, K. (2019). Relative age and ADHD symptoms, diagnosis and medication: A systematic review. European Child & Adolescent Psychiatry, 28(11), 1417–1429. https://doi.org/10.1007/s00787-018-1229-6</li>
            <li>Musch, J., & Grondin, S. (2001). Unequal Competition as an Impediment to Personal Development: A Review of the Relative Age Effect in Sport. Developmental Review, 21(2), 147–167. https://doi.org/10.1006/drev.2000.0516</li>
            <li>Navarro, J., García-Rubio, J., & Olivares, P. R. (2015). The Relative Age Effect and Its Influence on Academic Performance. PLOS ONE, 10(10), e0141895. https://doi.org/10.1371/journal.pone.0141895</li>
            <li>Smith, K. L., Weir, P. L., Till, K., Romann, M., & Cobley, S. (2018). Relative Age Effects Across and Within Female Sport Contexts: A Systematic Review and Meta-Analysis. Sports Medicine, 48(6), 1451–1478. https://doi.org/10.1007/s40279-018-0890-8</li>
        </ul>
        """)


