import random
import json

levelDescriptions = {
  1: "Identify whether a given variable (described by context or data values) is categorical (qualitative) or quantitative (numerical).",
  2: "Explain differences between categorical and quantitative variables, including examples of each.",
  3: "Given a real data context, classify multiple variables and decide which summaries (counts vs. numerical measures) apply.",
  4: "Analyze how variable type affects data display and analysis (e.g., why computing a mean makes sense for a quantitative variable but not for a categorical one).",
  5: "Design or critique a study’s data collection plan with both variable types, including selecting measurement scales and justifying data types."
}

# --- Data Pools ---
# Each variable includes its name, type, and example data values for context.
common_variables = [
    {"name": "Age", "type": "quantitative", "examples": ["25", "30", "45"]},
    {"name": "Gender", "type": "categorical", "examples": ["Male", "Female", "Non-binary"]},
    {"name": "Income", "type": "quantitative", "examples": ["$50,000", "$75,000", "$120,000"]},
    {"name": "Education Level", "type": "categorical", "examples": ["High School", "Bachelors", "Masters", "PhD"]},
    {"name": "Height (cm)", "type": "quantitative", "examples": ["175", "162", "180"]},
    {"name": "Favorite Color", "type": "categorical", "examples": ["Blue", "Red", "Green"]},
    {"name": "Number of Pets", "type": "quantitative", "examples": ["0", "1", "3"]},
    {"name": "Zip Code", "type": "categorical", "examples": ["90210", "10001", "60601"]}, # Often treated as categorical in analysis
    {"name": "Temperature (°C)", "type": "quantitative", "examples": ["20", "25", "30"]},
    {"name": "Blood Type", "type": "categorical", "examples": ["A+", "B-", "O"]},
    {"name": "Satisfaction Rating (1-5)", "type": "quantitative", "examples": ["4", "2", "5"]}, # Ordinal, often treated as quantitative for means
    {"name": "Marital Status", "type": "categorical", "examples": ["Single", "Married", "Divorced"]},
    {"name": "Number of Children", "type": "quantitative", "examples": ["0", "1", "2"]},
    {"name": "Political Affiliation", "type": "categorical", "examples": ["Democrat", "Republican", "Independent"]},
    {"name": "Time Spent Studying (hours)", "type": "quantitative", "examples": ["2.5", "5", "1.5"]},
]

# Contexts for various studies or scenarios.
study_contexts = [
    "a survey of college students",
    "a medical research study",
    "a marketing campaign analysis",
    "an ecological survey of a forest",
    "a customer satisfaction survey",
    "a study on consumer habits",
    "a public health initiative",
    "a research project on sleep patterns",
    "an analysis of sales data"
]

# Appropriate summary measures for quantitative data.
summary_types_quantitative = ["mean", "median", "standard deviation", "range", "sum"]
# Appropriate summary measures for categorical data.
summary_types_categorical = ["count", "proportion", "mode", "frequency"]
# Appropriate display types for quantitative data.
display_types_quantitative = ["histogram", "scatter plot", "box plot"]
# Appropriate display types for categorical data.
display_types_categorical = ["bar chart", "pie chart", "frequency table"]

# --- Helper Functions ---
def get_random_variable(var_type=None):
    """
    Returns a random variable dictionary from `common_variables`,
    optionally filtered by 'categorical' or 'quantitative' type.
    """
    if var_type:
        # Filter variables by the specified type
        filtered_vars = [v for v in common_variables if v["type"] == var_type]
        return random.choice(filtered_vars) if filtered_vars else random.choice(common_variables)
    return random.choice(common_variables)

def get_variable_description(variable):
    """
    Generates a descriptive HTML string for a variable, including example data values.
    """
    # Randomly sample up to 3 example values for brevity
    examples = random.sample(variable['examples'], min(3, len(variable['examples'])))
    return f"'{variable['name']}' (e.g., data values: {', '.join(examples)})"

def shuffle_options_and_get_correct_index(options_list, correct_option_text_part):
    """
    Shuffles a list of options and returns the shuffled list along with the
    index of the option that contains the `correct_option_text_part`.
    This allows for flexible matching of the correct answer.
    """
    shuffled_options = random.sample(options_list, len(options_list))
    correct_index = -1
    for i, opt in enumerate(shuffled_options):
        # Check if the identifying part of the correct answer is within the option string
        if correct_option_text_part in opt:
            correct_index = i
            break
    return shuffled_options, correct_index

# --- Main Question Generation Function ---
def generate_question(dummy,level: int) -> dict:
    """
    Given a difficulty level (1-5), returns a new random practice question dictionary.

    Args:
        level (int): The difficulty level (1 to 5).

    Returns:
        dict: A dictionary containing:
            "question": self-contained HTML for the question.
            "options": A list of self-contained HTML strings for the answer options.
            "correctAnswer": The 0-based index of the correct option in the shuffled list.
            "explanation": A string explaining why the correct answer is correct.
    """
    question_data = {
        "question": "",
        "options": [],
        "correctAnswer": -1,
        "explanation": ""
    }

    # --- Level 1: Identify Categorical vs. Quantitative ---
    if level == 1:
        templates = [
            "Is the variable {var_desc} a categorical (qualitative) or quantitative (numerical) variable?",
            "Consider a study in {context}. If you collect data on {var_desc}, what type of variable is it?",
            "Which of the following describes a <strong>{target_type}</strong> variable?",
            "Classify the variable: {var_desc}. Is it categorical or quantitative?"
        ]
        template = random.choice(templates)

        if "target_type" in template:
            # Question asks to identify a variable of a specific type
            target_type = random.choice(["categorical", "quantitative"])
            correct_var = get_random_variable(target_type)
            # Get a distractor variable of the opposite type
            distractor_var = get_random_variable("quantitative" if target_type == "categorical" else "categorical")

            question_data["question"] = f"<p>{template.format(target_type=target_type)}</p>"
            correct_option = (
                f"<p><strong>{correct_var['name']}</strong> is {correct_var['type']} (e.g., "
                f"{', '.join(random.sample(correct_var['examples'], min(2, len(correct_var['examples']))))}).</p>"
            )
            distractor_option1 = (
                f"<p><strong>{distractor_var['name']}</strong> is {distractor_var['type']} (e.g., "
                f"{', '.join(random.sample(distractor_var['examples'], min(2, len(distractor_var['examples']))))}).</p>"
            )
            # Generic distractor options
            distractor_option2 = (
                "<p>A variable that can be measured numerically, like height.</p>" if target_type == "categorical"
                else "<p>A variable that describes qualities or categories, like eye color.</p>"
            )
            distractor_option3 = (
                "<p>A variable that can be counted, but not measured, like number of siblings.</p>" if target_type == "categorical"
                else "<p>A variable that can be categorized, but not ordered, like types of fruit.</p>"
            )

            options = [correct_option, distractor_option1, distractor_option2, distractor_option3]
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, correct_var['name'])
            question_data["explanation"] = (
                f"The question asks to identify a <strong>{target_type}</strong> variable. "
                f"'{correct_var['name']}' is {correct_var['type']} because it "
                f"{levelDescriptions[1].lower().split(' or ')[0].replace('identify whether a given variable (described by context or data values) is ', '')}. "
                f"For example, '{correct_var['name']}' values are {', '.join(random.sample(correct_var['examples'], min(2, len(correct_var['examples']))))}."
            )
        else:
            # Question asks to classify a given variable
            variable = get_random_variable()
            var_desc = get_variable_description(variable)
            context = random.choice(study_contexts)

            question_data["question"] = f"<p>{template.format(var_desc=var_desc, context=context)}</p>"
            correct_type = variable["type"]
            options = [
                f"<p>Categorical (qualitative)</p>",
                f"<p>Quantitative (numerical)</p>",
                f"<p>Both categorical and quantitative</p>",
                f"<p>Neither categorical nor quantitative</p>"
            ]
            correct_option_text = f"Categorical (qualitative)" if correct_type == "categorical" else f"Quantitative (numerical)"
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, correct_option_text)
            question_data["explanation"] = (
                f"'{variable['name']}' is a <strong>{correct_type}</strong> variable. "
                f"{'Categorical variables describe qualities or categories, like ' + ', '.join(random.sample(variable['examples'], min(2, len(variable['examples'])))) + '.' if correct_type == 'categorical' else 'Quantitative variables measure numerical quantities, like ' + ', '.join(random.sample(variable['examples'], min(2, len(variable['examples'])))) + '.'} "
                f"This aligns with the goal of {levelDescriptions[1].lower()}."
            )

    # --- Level 2: Explain Differences ---
    elif level == 2:
        templates = [
            "Which statement accurately explains the primary difference between categorical and quantitative variables?",
            "Provide an example of a categorical variable and a quantitative variable, and explain why each fits its type.",
            "Consider the variables: '{cat_var_name}' and '{quant_var_name}'. How do their fundamental characteristics differ?"
        ]
        template = random.choice(templates)

        cat_var = get_random_variable("categorical")
        quant_var = get_random_variable("quantitative")
        while cat_var['name'] == quant_var['name']: # Ensure distinct variables
            quant_var = get_random_variable("quantitative")

        if "primary difference" in template:
            question_data["question"] = f"<p>{template}</p>"
            correct_option = "<p>Categorical variables classify observations into distinct groups, while quantitative variables represent measurable quantities.</p>"
            options = [
                correct_option,
                "<p>Categorical variables are always numbers, while quantitative variables are always text.</p>",
                "<p>Quantitative variables can only be counted, while categorical variables can be measured.</p>",
                "<p>There is no significant difference; they are interchangeable terms.</p>"
            ]
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, "Categorical variables classify observations")
            question_data["explanation"] = (
                f"Categorical variables group data into categories (e.g., '{cat_var['name']}'), while quantitative variables represent numerical measurements (e.g., '{quant_var['name']}'). "
                f"This is the fundamental distinction as described in {levelDescriptions[2].lower()}."
            )
        elif "Provide an example" in template:
            context = random.choice(study_contexts)
            question_data["question"] = f"<p>{template.format(context=context)}</p>"
            correct_option = (
                f"<p>Categorical: <strong>{cat_var['name']}</strong> (e.g., {', '.join(random.sample(cat_var['examples'], min(2, len(cat_var['examples']))))}) "
                f"because it describes categories. Quantitative: <strong>{quant_var['name']}</strong> (e.g., {', '.join(random.sample(quant_var['examples'], min(2, len(quant_var['examples']))))}) "
                f"because it represents a measurable quantity.</p>"
            )
            options = [
                correct_option,
                f"<p>Categorical: <strong>{quant_var['name']}</strong>; Quantitative: <strong>{cat_var['name']}</strong>. (Incorrect variable types)</p>",
                f"<p>Both <strong>{cat_var['name']}</strong> and <strong>{quant_var['name']}</strong> are quantitative. (Incorrect classification)</p>",
                f"<p>Both <strong>{cat_var['name']}</strong> and <strong>{quant_var['name']}</strong> are categorical. (Incorrect classification)</p>"
            ]
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, cat_var['name'])
            question_data["explanation"] = (
                f"'{cat_var['name']}' is categorical as it represents categories or qualities. '{quant_var['name']}' is quantitative as it represents numerical measurements. "
                f"This directly fulfills the requirement to {levelDescriptions[2].lower()}."
            )
        else: # "Consider the variables..."
            question_data["question"] = f"<p>{template.format(cat_var_name=cat_var['name'], quant_var_name=quant_var['name'])}</p>"
            correct_option = (
                f"<p><strong>{cat_var['name']}</strong> describes qualities or groups, while <strong>{quant_var['name']}</strong> represents numerical values that can be measured or counted.</p>"
            )
            options = [
                correct_option,
                f"<p><strong>{cat_var['name']}</strong> can be used for calculations, but <strong>{quant_var['name']}</strong> cannot. (Incorrect)</p>",
                f"<p>They are both types of numerical data. (Incorrect)</p>",
                f"<p>They are both types of qualitative data. (Incorrect)</p>"
            ]
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, cat_var['name'])
            question_data["explanation"] = (
                f"'{cat_var['name']}' is a categorical variable, which means it deals with categories or groups. "
                f"'{quant_var['name']}' is a quantitative variable, meaning it deals with measurable numerical values. "
                f"This aligns with {levelDescriptions[2].lower().replace('explain differences between categorical and quantitative variables, including examples of each.', 'the explanation of differences between variable types.')}"
            )

    # --- Level 3: Classify Multiple Variables & Apply Summaries ---
    elif level == 3:
        templates = [
            "In a study on {context}, a researcher collected data on: <ul><li>{var1_name}</li><li>{var2_name}</li><li>{var3_name}</li></ul> For each variable, identify its type and an appropriate summary measure.",
            "Given the variables: '{var1_name}' and '{var2_name}'. Which type of summary (e.g., mean, count) is suitable for '{var1_name}' but not for '{var2_name}'?",
            "A survey includes questions about '{cat_var_name}' and '{quant_var_name}'. What are the most appropriate summary statistics for each?"
        ]
        template = random.choice(templates)

        var1 = get_random_variable()
        var2 = get_random_variable()
        while var2["name"] == var1["name"]: # Ensure distinct variables
            var2 = get_random_variable()
        var3 = get_random_variable()
        while var3["name"] == var1["name"] or var3["name"] == var2["name"]: # Ensure distinct variables
            var3 = get_random_variable()

        if "For each variable" in template:
            context = random.choice(study_contexts)
            question_data["question"] = f"<p>{template.format(context=context, var1_name=var1['name'], var2_name=var2['name'], var3_name=var3['name'])}</p>"

            # Determine correct summaries based on variable types
            correct_summary1 = random.choice(summary_types_categorical) if var1["type"] == "categorical" else random.choice(summary_types_quantitative)
            correct_summary2 = random.choice(summary_types_categorical) if var2["type"] == "categorical" else random.choice(summary_types_quantitative)
            correct_summary3 = random.choice(summary_types_categorical) if var3["type"] == "categorical" else random.choice(summary_types_quantitative)

            correct_option = (
                f"<p><strong>{var1['name']}</strong>: {var1['type']}, suitable summary: {correct_summary1}.<br>"
                f"<strong>{var2['name']}</strong>: {var2['type']}, suitable summary: {correct_summary2}.<br>"
                f"<strong>{var3['name']}</strong>: {var3['type']}, suitable summary: {correct_summary3}.</p>"
            )

            options = [correct_option]
            # Add distractors by swapping types or using inappropriate summaries
            options.append(
                f"<p><strong>{var1['name']}</strong>: {'quantitative' if var1['type'] == 'categorical' else 'categorical'}, suitable summary: "
                f"{random.choice(summary_types_quantitative) if var1['type'] == 'categorical' else random.choice(summary_types_categorical)}.</p>"
            )
            options.append(
                f"<p><strong>{var2['name']}</strong>: {var2['type']}, suitable summary: "
                f"{random.choice(summary_types_quantitative) if var2['type'] == 'categorical' else random.choice(summary_types_categorical)}.</p>"
            )
            options.append(f"<p>All variables are quantitative and can be summarized by the mean.</p>")

            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, var1['name'])
            question_data["explanation"] = (
                f"For each variable, its type (categorical or quantitative) dictates the appropriate summary measures. "
                f"For example, '{var1['name']}' is {var1['type']} and a {correct_summary1} is suitable. "
                f"This aligns with {levelDescriptions[3].lower().replace('given a real data context, classify multiple variables and decide which summaries (counts vs. numerical measures) apply.', 'the classification of variables and application of summary measures.')}"
            )
        elif "suitable for '{var1_name}' but not for '{var2_name}'" in template:
            # Ensure var1 is quantitative and var2 is categorical for a clear example
            var1_quant = get_random_variable("quantitative")
            var2_cat = get_random_variable("categorical")
            while var1_quant['name'] == var2_cat['name']:
                var2_cat = get_random_variable("categorical")

            question_data["question"] = f"<p>{template.format(var1_name=var1_quant['name'], var2_name=var2_cat['name'])}</p>"
            correct_summary = random.choice(summary_types_quantitative)
            distractor_summary = random.choice(summary_types_categorical)

            correct_option = f"<p>A <strong>{correct_summary}</strong> is suitable for <strong>{var1_quant['name']}</strong> but not for <strong>{var2_cat['name']}</strong>.</p>"
            options = [
                correct_option,
                f"<p>A <strong>{distractor_summary}</strong> is suitable for <strong>{var1_quant['name']}</strong> but not for <strong>{var2_cat['name']}</strong>. (Incorrect summary for quantitative)</p>",
                f"<p>Both variables can be summarized by a <strong>mean</strong>. (Incorrect, mean for categorical is inappropriate)</p>",
                f"<p>Neither variable can be summarized by a <strong>count</strong>. (Incorrect, count is appropriate for categorical)</p>"
            ]
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, correct_summary)
            question_data["explanation"] = (
                f"Quantitative variables like '{var1_quant['name']}' can be summarized by measures like the {correct_summary}, "
                f"whereas categorical variables like '{var2_cat['name']}' are better summarized by counts or proportions. "
                f"This directly addresses {levelDescriptions[3].lower().replace('given a real data context, classify multiple variables and decide which summaries (counts vs. numerical measures) apply.', 'the appropriate summary measures for different variable types.')}"
            )
        else: # "What are the most appropriate summary statistics for each?"
            cat_var = get_random_variable("categorical")
            quant_var = get_random_variable("quantitative")
            while cat_var['name'] == quant_var['name']:
                quant_var = get_random_variable("quantitative")

            question_data["question"] = f"<p>{template.format(cat_var_name=cat_var['name'], quant_var_name=quant_var['name'])}</p>"
            correct_cat_summary = random.choice(summary_types_categorical)
            correct_quant_summary = random.choice(summary_types_quantitative)

            correct_option = (
                f"<p>For <strong>{cat_var['name']}</strong>: {correct_cat_summary}; For <strong>{quant_var['name']}</strong>: {correct_quant_summary}.</p>"
            )
            options = [
                correct_option,
                f"<p>For <strong>{cat_var['name']}</strong>: {correct_quant_summary}; For <strong>{quant_var['name']}</strong>: {correct_cat_summary}. (Swapped inappropriate summaries)</p>",
                f"<p>Both can be summarized by the <strong>mean</strong>. (Incorrect for categorical)</p>",
                f"<p>Both can be summarized by the <strong>mode</strong>. (Mode is generally okay for both, but not 'most appropriate' for quantitative typically)</p>"
            ]
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, correct_cat_summary)
            question_data["explanation"] = (
                f"Categorical variables like '{cat_var['name']}' are best summarized by {correct_cat_summary}s (e.g., counts of each category), "
                f"while quantitative variables like '{quant_var['name']}' are best summarized by {correct_quant_summary}s (e.g., average value). "
                f"This directly addresses {levelDescriptions[3].lower().replace('given a real data context, classify multiple variables and decide which summaries (counts vs. numerical measures) apply.', 'the appropriate summary measures for different variable types.')}"
            )

    # --- Level 4: Variable Type Affects Display and Analysis ---
    elif level == 4:
        templates = [
            "Why is calculating the <strong>mean</strong> of '{cat_var_name}' (e.g., {cat_examples}) generally inappropriate, while it is appropriate for '{quant_var_name}' (e.g., {quant_examples})?",
            "Explain why a <strong>{cat_display}</strong> is suitable for '{cat_var_name}' but a <strong>{quant_display}</strong> is preferred for '{quant_var_name}'.",
            "How does the type of variable, such as '{variable_name}' (e.g., {data_values}), influence the choice of statistical analysis or display?"
        ]
        template = random.choice(templates)

        cat_var = get_random_variable("categorical")
        quant_var = get_random_variable("quantitative")
        while cat_var['name'] == quant_var['name']:
            quant_var = get_random_variable("quantitative")

        if "mean of '{cat_var_name}'" in template:
            question_data["question"] = f"<p>{template.format(cat_var_name=cat_var['name'], cat_examples=', '.join(random.sample(cat_var['examples'], min(3, len(cat_var['examples'])))), quant_var_name=quant_var['name'], quant_examples=', '.join(random.sample(quant_var['examples'], min(3, len(quant_var['examples'])))))}</p>"
            correct_option = (
                f"<p>The <strong>mean</strong> requires numerical values with meaningful arithmetic properties, which categorical data like '{cat_var['name']}' lack. "
                f"Quantitative data like '{quant_var['name']}' possess these properties, making the mean a valid measure.</p>"
            )
            options = [
                correct_option,
                f"<p>Categorical variables are always text, so you can't calculate a mean. (Partially true, but not the core reason)</p>",
                f"<p>Quantitative variables are always integers, making mean calculation easier. (Incorrect, quantitative can be decimals)</p>",
                f"<p>The mean is only for small datasets. (Incorrect)</p>"
            ]
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, "mean requires numerical values")
            question_data["explanation"] = (
                f"The mean is a measure of central tendency for numerical data. Categorical data represents categories or qualities, not quantities, so a mean is mathematically meaningless. "
                f"This illustrates {levelDescriptions[4].lower().replace('analyze how variable type affects data display and analysis (e.g., why computing a mean makes sense for a quantitative variable but not for a categorical one).', 'how variable type dictates appropriate analysis.')}"
            )
        elif "suitable for '{cat_var_name}' but a '{quant_display}' is preferred" in template:
            cat_display = random.choice(display_types_categorical)
            quant_display = random.choice(display_types_quantitative)
            question_data["question"] = f"<p>{template.format(cat_var_name=cat_var['name'], cat_display=cat_display, quant_var_name=quant_var['name'], quant_display=quant_display)}</p>"
            correct_option = (
                f"<p><strong>{cat_display}s</strong> are used for categorical data to show frequencies or proportions of distinct categories, "
                f"while <strong>{quant_display}s</strong> are used for quantitative data to show distribution, spread, and patterns of numerical values.</p>"
            )
            options = [
                correct_option,
                f"<p><strong>{cat_display}s</strong> are for large datasets, <strong>{quant_display}s</strong> for small ones. (Incorrect)</p>",
                f"<p>The choice of display is purely aesthetic and not related to variable type. (Incorrect)</p>",
                f"<p>Both displays can be used interchangeably for any variable type. (Incorrect)</p>"
            ]
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, cat_display)
            question_data["explanation"] = (
                f"Display choices are fundamentally tied to variable type. {cat_display}s (like bar charts) visualize categorical frequencies, "
                f"while {quant_display}s (like histograms) illustrate the distribution of numerical data. "
                f"This directly relates to {levelDescriptions[4].lower().replace('analyze how variable type affects data display and analysis (e.g., why computing a mean makes sense for a quantitative variable but not for a categorical one).', 'how variable type affects data display.')}"
            )
        else: # "How does the type of variable... influence the choice of statistical analysis or display?"
            variable = random.choice([cat_var, quant_var])
            var_desc = get_variable_description(variable)
            question_data["question"] = f"<p>{template.format(variable_name=variable['name'], data_values=var_desc)}</p>"
            correct_option = (
                f"<p>The variable type determines which statistical operations (e.g., mean, mode, correlation, t-tests) are meaningful "
                f"and which graphical displays (e.g., bar chart, histogram, scatter plot) are appropriate for visualizing the data.</p>"
            )
            options = [
                correct_option,
                f"<p>Variable type only affects how data is collected, not how it's analyzed. (Incorrect)</p>",
                f"<p>All variables can be analyzed using the same statistical methods. (Incorrect)</p>",
                f"<p>The influence is minimal; any display or analysis can be used. (Incorrect)</p>"
            ]
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, "statistical operations")
            question_data["explanation"] = (
                f"The type of variable is crucial for selecting valid statistical analyses and displays. "
                f"For instance, you wouldn't calculate a mean for a categorical variable, nor would you use a histogram for it. "
                f"This is central to {levelDescriptions[4].lower().replace('analyze how variable type affects data display and analysis (e.g., why computing a mean makes sense for a quantitative variable but not for a categorical one).', 'understanding the impact of variable type on analysis and display.')}"
            )

    # --- Level 5: Design/Critique Study Plan, Measurement Scales ---
    elif level == 5:
        templates = [
            "You are designing a study on {context}. Propose one categorical and one quantitative variable to collect, justifying your choice of measurement scale for each.",
            "Critique the following data collection plan for a study on {context}: <em>{plan_description}</em>.",
            "A survey asks for '{variable_name}' using a Likert scale (e.g., '1=Strongly Disagree, ..., 5=Strongly Agree'). Is this categorical or quantitative, and why is its measurement scale important for analysis?"
        ]
        template = random.choice(templates)

        context = random.choice(study_contexts)
        cat_var = get_random_variable("categorical")
        quant_var = get_random_variable("quantitative")
        while cat_var['name'] == quant_var['name']:
            quant_var = get_random_variable("quantitative")

        if "Propose one categorical and one quantitative variable" in template:
            question_data["question"] = f"<p>{template.format(context=context)}</p>"
            correct_option = (
                f"<p>Categorical: <strong>{cat_var['name']}</strong> (e.g., {random.choice(cat_var['examples'])}). Appropriate scale: <strong>Nominal</strong> (for distinct categories without order).<br>"
                f"Quantitative: <strong>{quant_var['name']}</strong> (e.g., {random.choice(quant_var['examples'])}). Appropriate scale: <strong>Ratio</strong> (for meaningful numerical comparisons and true zero).</p>"
            )
            options = [
                correct_option,
                f"<p>Categorical: <strong>{quant_var['name']}</strong>; Quantitative: <strong>{cat_var['name']}</strong>. (Incorrect variable types)</p>",
                f"<p>Both should be quantitative for easier analysis. (Incorrect, ignores categorical insights)</p>",
                f"<p>Measurement scales are not important for study design; just collect the data. (Incorrect)</p>"
            ]
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, cat_var['name'])
            question_data["explanation"] = (
                f"A well-designed study includes both variable types to capture different aspects of phenomena. "
                f"'{cat_var['name']}' is categorical, typically using a nominal scale. "
                f"'{quant_var['name']}' is quantitative, often using an interval or ratio scale. "
                f"Measurement scales dictate the valid statistical operations and interpretations. "
                f"This directly addresses {levelDescriptions[5].lower().replace('design or critique a study’s data collection plan with both variable types, including selecting measurement scales and justifying data types.', 'the design of a study with appropriate variable types and measurement scales.')}"
            )
        elif "Critique the following data collection plan" in template:
            # Create a flawed plan where a categorical variable is treated quantitatively
            flawed_var = get_random_variable("categorical")
            # Ensure it's not a Likert scale variable for this specific critique
            while "Rating" in flawed_var['name']:
                flawed_var = get_random_variable("categorical")

            flawed_plan_desc = (
                f"Collect '{flawed_var['name']}' by assigning numerical codes (e.g., 1 for '{flawed_var['examples'][0]}', "
                f"2 for '{flawed_var['examples'][1]}', etc.) and then calculating the average code."
            )
            question_data["question"] = f"<p>{template.format(context=context, plan_description=flawed_plan_desc)}</p>"
            correct_option = (
                f"<p>The plan is flawed because '{flawed_var['name']}' is a <strong>categorical (nominal)</strong> variable. "
                f"Assigning arbitrary numerical codes and then calculating an average (mean) is inappropriate and statistically meaningless, as the numbers do not represent quantity.</p>"
            )
            options = [
                correct_option,
                f"<p>The plan is perfect; assigning numbers makes any variable quantitative. (Incorrect)</p>",
                f"<p>The average rating is always appropriate for any type of data. (Incorrect)</p>",
                f"<p>The plan needs more variables, but the current variable collection is fine. (Incorrect, the method is flawed)</p>"
            ]
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, "flawed because")
            question_data["explanation"] = (
                f"The plan is flawed because '{flawed_var['name']}' is a categorical variable. "
                f"While you can assign numbers to categories for coding, these numbers do not represent a measurable quantity, "
                f"so calculating a mean is statistically invalid and misleading. "
                f"This highlights the importance of {levelDescriptions[5].lower().replace('design or critique a study’s data collection plan with both variable types, including selecting measurement scales and justifying data types.', 'critiquing data collection plans based on variable types and measurement scales.')}"
            )
        else: # "A survey asks for '{variable_name}' using a Likert scale..."
            # Use Satisfaction Rating as a good example of ordinal often treated as quantitative
            likert_var = next((v for v in common_variables if "Rating" in v["name"]), None)
            if not likert_var: # Fallback if not found
                likert_var = {"name": "Agreement Level", "type": "quantitative", "examples": ["1", "2", "3", "4", "5"]}
            
            question_data["question"] = f"<p>{template.format(variable_name=likert_var['name'])}</p>"
            correct_option = (
                f"<p>It is typically treated as <strong>quantitative (ordinal)</strong>, meaning the categories have a meaningful order. "
                f"Its measurement scale is crucial because while numerical operations like the mean can sometimes be applied, "
                f"the interpretation must consider that the intervals between numbers may not be equal (e.g., the difference between '1' and '2' might not be the same as '4' and '5').</p>"
            )
            options = [
                correct_option,
                f"<p>It is purely categorical, so only counts and modes are appropriate. (Too restrictive)</p>",
                f"<p>It is purely quantitative (ratio scale), so any numerical analysis is valid without caution. (Too broad)</p>",
                f"<p>The measurement scale is irrelevant for this variable; it's just a number. (Incorrect)</p>"
            ]
            question_data["options"], question_data["correctAnswer"] = shuffle_options_and_get_correct_index(options, "typically treated as quantitative (ordinal)")
            question_data["explanation"] = (
                f"Likert scales (like '{likert_var['name']}') are ordinal, which is a type of quantitative variable. "
                f"While they use numbers, the intervals between them might not be equal, requiring careful consideration of statistical methods (e.g., when using means). "
                f"This relates to {levelDescriptions[5].lower().replace('design or critique a study’s data collection plan with both variable types, including selecting measurement scales and justifying data types.', 'justifying data types and selecting appropriate measurement scales.')}"
            )

    return json.dumps(question_data)


print('starting')
print(generate_question(1,1))