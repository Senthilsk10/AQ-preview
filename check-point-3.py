import random
import html
import json
from collections import defaultdict

def generate_question(dummy_type,level: int) -> dict:
    """
    Given a difficulty level from 1 to 5, this function generates a random practice
    question about categorical vs. quantitative variables. The function is data-driven,
    using a set of templates and data pools to create a wide variety of questions.

    Args:
        level (int): The difficulty level of the question, from 1 to 5.

    Returns:
        dict: A dictionary containing the question, options, correct answer index,
              and an explanation. The format is:
              {
                  "question": "self-contained HTML string",
                  "options": [HTML_str, HTML_str, HTML_str, HTML_str],
                  "correctAnswer": int (index 0-3),
                  "explanation": "string"
              }
    
    Raises:
        ValueError: If the provided level is not between 1 and 5.
    """

    # -- Data & Template Definitions --

    levelDescriptions = {
        1: "Identify whether a given variable (described by context or data values) is categorical (qualitative) or quantitative (numerical).",
        2: "Explain differences between categorical and quantitative variables, including examples of each.",
        3: "Given a real data context, classify multiple variables and decide which summaries (counts vs. numerical measures) apply.",
        4: "Analyze how variable type affects data display and analysis (e.g., why computing a mean makes sense for a quantitative variable but not for a categorical one).",
        5: "Design or critique a study’s data collection plan with both variable types, including selecting measurement scales and justifying data types."
    }

    DATA_POOLS = {
        "contexts": [
            "a survey on household energy use", "a clinical trial for a new medication",
            "a study on employee job satisfaction", "market research for a new smartphone app",
            "an analysis of university student grades", "a fitness tracker's daily activity log",
            "a report on public library usage", "an experiment on plant growth conditions"
        ],
        "quant_vars": [
            {"name": "age", "unit": "years"}, {"name": "height", "unit": "cm"},
            {"name": "weight", "unit": "kg"}, {"name": "temperature", "unit": "°C"},
            {"name": "income", "unit": "dollars"}, {"name": "screen time", "unit": "hours per day"},
            {"name": "test score", "unit": "out of 100"}, {"name": "distance", "unit": "km"}
        ],
        "cat_vars": [
            {"name": "eye color", "cats": ["Blue", "Green", "Brown", "Hazel"]},
            {"name": "employment status", "cats": ["Employed", "Unemployed", "Student"]},
            {"name": "preferred music genre", "cats": ["Rock", "Pop", "Jazz", "Classical"]},
            {"name": "t-shirt size", "cats": ["Small", "Medium", "Large", "X-Large"]},
            {"name": "blood type", "cats": ["A", "B", "AB", "O"]},
            {"name": "highest education level", "cats": ["High School", "Bachelor's", "Master's", "PhD"]}
        ],
        "concepts": ["customer satisfaction", "academic performance", "physical fitness", "product usability"],
        "summaries_quant": ["mean", "median", "standard deviation", "range"],
        "summaries_cat": ["frequency count", "mode", "percentage distribution"],
    }

    TEMPLATES = {
        1: [
            {
                "question": "A researcher is conducting {context}. They record the variable '<b>{quant_var_name}</b>' (measured in {quant_var_unit}). What type of variable is this?",
                "correct": "Quantitative",
                "distractors": ["Categorical", "Both quantitative and categorical", "Neither quantitative nor categorical"],
                "explanation": "The variable '<b>{quant_var_name}</b>' is <b>quantitative</b> because it represents a measurable, numerical quantity ({quant_var_unit}). You can perform mathematical operations like calculating an average on it."
            },
            {
                "question": "In {context}, the variable '<b>{cat_var_name}</b>' is recorded by choosing one of the following options: <i>{cat_var_examples}</i>. What type of variable is this?",
                "correct": "Categorical",
                "distractors": ["Quantitative", "Numerical", "Continuous"],
                "explanation": "The variable '<b>{cat_var_name}</b>' is <b>categorical</b> (or qualitative) because it places individuals into distinct groups or categories (e.g., {cat_var_examples}). It represents a quality or label, not a measurable amount."
            },
            {
                "question": "Which of the following is an example of a <b>quantitative</b> variable?",
                "correct": "{quant_var_name}",
                "distractors": ["{cat_var_name_1}", "{cat_var_name_2}", "{cat_var_name_3}"],
                "explanation": "'<b>{quant_var_name}</b>' is quantitative because it represents a numerical measurement. In contrast, '{cat_var_name_1}', '{cat_var_name_2}', and '{cat_var_name_3}' are categorical because their values are labels or categories."
            }
        ],
        2: [
            {
                "question": "What is the fundamental difference between quantitative and categorical variables?",
                "correct": "Quantitative variables are numerical and represent a measurable quantity, while categorical variables represent labels or groups.",
                "distractors": [
                    "Quantitative variables are always continuous, while categorical variables are always discrete.",
                    "Categorical variables are used in science, while quantitative variables are used in business.",
                    "Quantitative variables can be graphed using bar charts, while categorical variables use histograms."
                ],
                "explanation": "The core distinction lies in what the variable represents. <b>Quantitative</b> data are numbers that measure something (e.g., height, temperature). <b>Categorical</b> data are labels that place items into groups (e.g., gender, brand name)."
            },
            {
                "question": "Why is '<b>{cat_var_name}</b>' classified as a categorical variable?",
                "correct": "Because it assigns items to distinct, non-numerical groups or labels.",
                "distractors": [
                    "Because its values can be counted.",
                    "Because it can be measured with high precision.",
                    "Because there are more than two possible values."
                ],
                "explanation": "A variable is <b>categorical</b> if its values are labels that sort data into groups. For '<b>{cat_var_name}</b>', the values (e.g., {cat_var_examples}) are names for categories, not numerical measurements."
            },
            {
                "question": "A study measures both '<b>{quant_var_name}</b>' and '<b>{cat_var_name}</b>'. Which statement correctly classifies them?",
                "correct": "'{quant_var_name}' is quantitative, and '{cat_var_name}' is categorical.",
                "distractors": [
                    "'{quant_var_name}' is categorical, and '{cat_var_name}' is quantitative.",
                    "Both variables are quantitative.",
                    "Both variables are categorical."
                ],
                "explanation": "'<b>{quant_var_name}</b>' is a numerical measurement, making it <b>quantitative</b>. '<b>{cat_var_name}</b>' sorts subjects into groups, making it <b>categorical</b>."
            }
        ],
        3: [
            {
                "question": "In {context}, a study records the following variables: <b>{var_list_str}</b>. Which variable is categorical, and what is an appropriate summary for it?",
                "correct": "'{cat_var_name}' is categorical; a suitable summary is its <b>{summary_cat}</b>.",
                "distractors": [
                    "'{cat_var_name}' is quantitative; a suitable summary is its <b>{summary_quant}</b>.",
                    "'{quant_var_name}' is categorical; a suitable summary is its <b>{summary_cat}</b>.",
                    "'{quant_var_name}' is quantitative; a suitable summary is its <b>{summary_cat}</b>."
                ],
                "explanation": "The variable '<b>{cat_var_name}</b>' is <b>categorical</b> as it groups data. Therefore, summaries like <b>{summary_cat}</b> are appropriate. In contrast, '{quant_var_name}' is quantitative, for which you would use numerical summaries like mean or median."
            },
            {
                "question": "A dataset from {context} includes the variables 'Department' and 'Avg. Years of Service'. The data is visualized below. How should you classify these two variables?<br><pre class='chartjs'>{chart_config}</pre>",
                "correct": "'Department' is categorical, and 'Avg. Years of Service' is quantitative.",
                "distractors": [
                    "'Department' is quantitative, and 'Avg. Years of Service' is categorical.",
                    "Both are quantitative.",
                    "Both are categorical."
                ],
                "explanation": "The chart shows distinct groups for 'Department' (e.g., Sales, HR), which are labels, making it a <b>categorical</b> variable. 'Avg. Years of Service' is a calculated numerical value, confirming it is a <b>quantitative</b> variable."
            },
            {
                "question": "A researcher collects the following sample data on student performance: {table_html}. Based on this sample, which of these is a meaningful calculation?",
                "correct": "The average (mean) of the '<b>{quant_var_name}</b>' column.",
                "distractors": [
                    "The average (mean) of the '<b>{cat_var_name}</b>' column.",
                    "The sum of the 'Student ID' column.",
                    "The median of the '<b>{cat_var_name}</b>' column."
                ],
                "explanation": "Mathematical operations like calculating the <b>mean</b> are only meaningful for <b>quantitative</b> variables like '<b>{quant_var_name}</b>'. 'Student ID' and '<b>{cat_var_name}</b>' are categorical (one is an identifier, the other a label), so averaging or finding their median (unless it is ordinal) is nonsensical."
            }
        ],
        4: [
            {
                "question": "Why would it be statistically inappropriate to calculate the <i>mean</i> of a variable like '<b>{cat_var_name}</b>'?",
                "correct": "The mean is a measure of central tendency for numerical data; categorical data consists of labels which cannot be meaningfully averaged.",
                "distractors": [
                    "Because categorical data is not normally distributed.",
                    "Because the mean can only be calculated on data with an infinite number of values.",
                    "Because categorical data is always text, and you cannot perform math on text."
                ],
                "explanation": "Calculating a mean requires adding values and dividing. Since the values of '<b>{cat_var_name}</b>' are non-numerical labels (e.g., {cat_var_examples}), arithmetic operations on them are undefined and meaningless. The concept of an 'average {cat_var_name}' makes no sense."
            },
            {
                "question": "A researcher wants to show the distribution of '<b>{quant_var_name}</b>' ({quant_var_unit}), which is a continuous quantitative variable. They create the pie chart below. What is the fundamental flaw in this visualization?<br><pre class='chartjs'>{chart_config}</pre>",
                "correct": "A pie chart is used for showing proportions of categories (parts of a whole), not for displaying the distribution of a continuous quantitative variable. A histogram or box plot would be appropriate.",
                "distractors": [
                    "The colors used in the pie chart are not visually appealing.",
                    "A pie chart should not have more than five slices.",
                    "The data should have been converted to percentages first."
                ],
                "explanation": "The key analytical error is using the wrong tool for the job. A <b>pie chart</b> is designed to show how a total amount is divided into <b>categorical</b> parts. For a <b>quantitative</b> variable like '<b>{quant_var_name}</b>', the goal is to see its shape, center, and spread, for which a <b>histogram</b> or <b>box plot</b> is the correct visualization."
            },
            {
                "question": "Analyze the following data analysis plan: \"To measure the central tendency of our customer's locations, we will assign a number to each city (1=NYC, 2=LA, 3=Chicago) and calculate the average city number.\" Why is this approach flawed?",
                "correct": "City is a nominal categorical variable. Assigning numbers is arbitrary and the resulting average is a meaningless value.",
                "distractors": [
                    "The sample size of cities is too small to calculate a stable average.",
                    "The assigned numbers should start from 0 instead of 1 for proper calculation.",
                    "This approach violates user data privacy by converting locations to numbers."
                ],
                "explanation": "This is a classic error of treating a <b>nominal categorical</b> variable (City) as a <b>quantitative</b> one. The numbers assigned are just labels; they don't have mathematical properties. An average of '1.8' doesn't correspond to a real location or provide any insight. The correct measure of central tendency for nominal data is the <b>mode</b> (the most frequent city)."
            }
        ],
        5: [
            {
                "question": "You are designing {context} and need to measure the concept of '<b>{concept}</b>'. Which of the following describes the <b>best</b> way to structure the data collection to capture both a quantitative and a categorical aspect of this concept?",
                "correct": "Ask for a rating on a scale of 1-10 (quantitative) and also ask them to select a primary reason for their rating from a predefined list (categorical).",
                "distractors": [
                    "Ask participants to write a long paragraph describing their feelings (qualitative text).",
                    "Measure their heart rate (quantitative) and their height (also quantitative).",
                    "Ask if they are 'satisfied' or 'unsatisfied' (categorical) and also their favorite color (also categorical)."
                ],
                "explanation": "A good study design often captures a concept in multiple ways. A 1-10 scale provides a granular <b>quantitative</b> measure. Asking for a 'primary reason' from a list (e.g., 'Price', 'Quality') captures the 'why' as a <b>categorical</b> variable. This combination provides a much richer dataset than one variable type alone."
            },
            {
                "question": "A research team proposes to study employee wellness. They create the data collection plan shown in the diagram below. What is a major critique of this plan in terms of variable measurement?<br><pre class='mermaid'>{mermaid_code}</pre>",
                "correct": "It measures 'wellness' as a single binary categorical variable ('Yes'/'No'), which oversimplifies a complex, continuous concept. A quantitative scale or multiple indicators would be more valid.",
                "distractors": [
                    "The flowchart diagram has arrows pointing in the wrong direction.",
                    "The question 'Are you feeling well?' is too personal to ask in a work setting.",
                    "The plan does not specify what to do if the employee answers 'Maybe'."
                ],
                "explanation": "The critique is about measurement validity. 'Wellness' is not a simple yes/no state; it's a spectrum. By measuring it with a single binary question, the plan treats a complex, arguably <b>quantitative</b> concept as a simplistic <b>categorical</b> one. This loses a vast amount of information. A better approach would use a validated survey with a numerical scale (e.g., WHO-5 Well-Being Index)."
            },
            {
                "question": "A junior analyst suggests investigating the relationship between '<b>{cat_var_name}</b>' and '<b>{quant_var_name}</b>'. Critically evaluate this research proposal.",
                "correct": "This is a valid and common type of analysis. It involves comparing the distribution or average of the quantitative variable ('{quant_var_name}') across the different groups defined by the categorical variable ('{cat_var_name}').",
                "distractors": [
                    "This is invalid because you cannot find a relationship between a categorical and a quantitative variable.",
                    "This is only valid if the categorical variable is converted into numbers first.",
                    "This is invalid because both variables must be of the same type (both quantitative or both categorical)."
                ],
                "explanation": "This is a perfectly valid and standard research design. The goal is to see if the value of a <b>quantitative</b> variable changes depending on the group (the <b>categorical</b> variable). For example, comparing the average '{quant_var_name}' for each '{cat_var_name}' category is a powerful analytical technique (e.g., using ANOVA or t-tests)."
            }
        ]
    }

    if level not in TEMPLATES:
        raise ValueError(f"Invalid level: {level}. Level must be one of {list(TEMPLATES.keys())}.")

    # --- 1. Select a random template for the level ---
    template = random.choice(TEMPLATES[level])

    # --- 2. Prepare dynamic data for placeholders ---
    params = {}
    
    quant_vars_sample = random.sample(DATA_POOLS["quant_vars"], 3)
    cat_vars_sample = random.sample(DATA_POOLS["cat_vars"], 3)

    params['quant_var_name'] = quant_vars_sample[0]['name']
    params['quant_var_unit'] = quant_vars_sample[0]['unit']
    params['cat_var_name'] = cat_vars_sample[0]['name']
    params['cat_var_examples'] = ", ".join(cat_vars_sample[0]['cats'][:3])
    
    # For L1, Q3
    params['cat_var_name_1'] = cat_vars_sample[0]['name']
    params['cat_var_name_2'] = cat_vars_sample[1]['name']
    params['cat_var_name_3'] = cat_vars_sample[2]['name']

    params['context'] = random.choice(DATA_POOLS["contexts"])
    params['concept'] = random.choice(DATA_POOLS["concepts"])
    params['summary_quant'] = random.choice(DATA_POOLS["summaries_quant"])
    params['summary_cat'] = random.choice(DATA_POOLS["summaries_cat"])

    # For L3 variable list
    var_list_for_q = [quant_vars_sample[0]['name'], cat_vars_sample[0]['name'], cat_vars_sample[1]['name']]
    random.shuffle(var_list_for_q)
    params['var_list_str'] = ", ".join(var_list_for_q)

    # --- 3. Generate charts or tables if needed ---
    if level == 3:
        if "{chart_config}" in template["question"]:
            labels = ["Sales", "HR", "Engineering", "Marketing"]
            data = [round(random.uniform(2.5, 15.5), 1) for _ in labels]
            chart_config = {"type": "bar", "data": {"labels": labels, "datasets": [{"label": "Avg. Years of Service", "data": data, "backgroundColor": "rgba(54, 162, 235, 0.6)"}]}, "options": {"plugins": {"legend": {"display": False}}, "scales": {"y": {"title": {"display": True, "text": "Avg. Years of Service"}}, "x": {"title": {"display": True, "text": "Department"}}}}}
            params['chart_config'] = html.escape(json.dumps(chart_config))
        
        if "{table_html}" in template["question"]:
            rows = ""
            for i in range(4):
                cat_val = random.choice(cat_vars_sample[0]['cats'])
                quant_val = round(random.uniform(20, 100), 1) if 'score' in quant_vars_sample[0]['name'] else random.randint(18, 65)
                rows += f"<tr><td>{1001+i}</td><td>{html.escape(cat_val)}</td><td>{quant_val}</td></tr>"
            table_html = f"<style>.q-table{{border-collapse:collapse;margin:1em 0;font-family:sans-serif;min-width:300px;box-shadow:0 0 5px rgba(0,0,0,0.1);}}.q-table th,.q-table td{{border:1px solid #ddd;text-align:left;padding:8px;}}.q-table th{{background-color:#f2f2f2;}} .q-table tr:nth-child(even){{background-color:#f9f9f9;}}</style><table class='q-table'><thead><tr><th>Student ID</th><th>{html.escape(params['cat_var_name'].title())}</th><th>{html.escape(params['quant_var_name'].title())}</th></tr></thead><tbody>{rows}</tbody></table>"
            params['table_html'] = table_html
    
    elif level == 4 and "{chart_config}" in template["question"]:
        labels = [f"{i*10}-{(i+1)*10-1} {params['quant_var_unit']}" for i in range(2, 7)]
        data = [random.randint(5, 50) for _ in labels]
        chart_config = {"type": "pie", "data": {"labels": labels, "datasets": [{"label": f"Distribution of {params['quant_var_name']}", "data": data}]}, "options": {"responsive": True, "plugins": {"title": {"display": True, "text": f"Chart of {params['quant_var_name']}"}}}}
        params['chart_config'] = html.escape(json.dumps(chart_config))

    elif level == 5 and "{mermaid_code}" in template["question"]:
        params['mermaid_code'] = html.escape("graph TD;\n    A[Start] --> B{Ask: 'Are you feeling well today?'};\n    B --> C[Record 'Yes' or 'No'];\n    C --> D[End];")

    # --- 4. Populate templates and create options ---
    # Use format_map with a defaultdict to avoid KeyErrors if a template uses a placeholder not relevant to it.
    dd_params = defaultdict(str, **params)
    
    correct_option = template['correct'].format_map(dd_params)
    distractor_options = [d.format_map(dd_params) for d in template['distractors']]

    options = [correct_option] + distractor_options
    random.shuffle(options)
    correct_answer_index = options.index(correct_option)

    # --- 5. Generate explanation ---
    explanation = template['explanation'].format_map(dd_params)

    # --- 6. Construct final dictionary ---
    question_dict = {
        "question": template['question'].format_map(dd_params),
        "options": options,
        "correctAnswer": correct_answer_index,
        "explanation": explanation
    }

    return json.dumps(question_dict)

# print(json.dumps(generate_question(4)))