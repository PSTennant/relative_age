from shiny.express import input, render, ui

ui.input_date("test_date", "Date of Assessment", )

@render.text
def test_date_val():
    return f"Test Date: {input.test_date()}"