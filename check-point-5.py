import random
import html
import json
from sklearn import datasets
import numpy as np

# -- Data Pools and Pre-loaded Datasets --

levelDescriptions = {
    1: "Identify whether a given variable (described by context or data values) is categorical (qualitative) or quantitative (numerical).",
    2: "Explain differences between categorical and quantitative variables, including examples of each.",
    3: "Given a real data context, classify multiple variables and decide which summaries (counts vs. numerical measures) apply.",
    4: "Analyze how variable type affects data display and analysis (e.g., why computing a mean makes sense for a quantitative variable but not for a categorical one).",
    5: "Design or critique a study’s data collection plan with both variable types, including selecting measurement scales and justifying data types."
}

# Load lightweight datasets on startup
iris = datasets.load_iris()
wine = datasets.load_wine()

# Reusable pools of examples for dynamic question generation
DATA_POOLS = {
    "contexts": [
        "a study on student academic performance", "an analysis of customer purchasing habits",
        "a health survey of local residents", "a report on employee productivity",
        "an experiment on plant growth", "a market research survey for a new app"
    ],
    "categorical_vars": [
        ("Eye Color", ["Blue", "Green", "Brown"]), ("Blood Type", ["A", "B", "AB", "O"]),
        ("Car Manufacturer", ["Ford", "Toyota", "Honda"]), ("T-Shirt Size", ["S", "M", "L", "XL"]),
        ("Employment Status", ["Employed", "Unemployed", "Student"])
    ],
    "quantitative_vars": [
        ("Height", "cm", (150, 200)), ("Test Score", "%", (0, 100)),
        ("Age", "years", (18, 65)), ("Weight", "kg", (50, 100)),
        ("Temperature", "°C", (20, 40))
    ],
    "numeric_labels": [ # Categorical variables that look numeric
        ("Jersey Number", [10, 23, 7]), ("ZIP Code", [90210, 10001, 60601]),
        ("Model Number", [2023, 4, 11])
    ]
}

# -- Helper Functions --

def _create_shuffled_options(correct_option: str, distractors: list) -> tuple:
    """Combines correct option with distractors, shuffles them, and finds the new correct index."""
    options = [correct_option] + distractors
    random.shuffle(options)
    correct_index = options.index(correct_option)
    return options, correct_index

# -- Level 1 Question Generators --

def _level1_from_context():
    """Ask to identify a variable type from its name and context."""
    if random.random() < 0.5: # Ask about a quantitative variable
        var_name, unit, _ = random.choice(DATA_POOLS["quantitative_vars"])
        question = f"In a scientific study, a researcher measures the <b>{var_name} ({unit})</b> of each subject. What type of variable is this?"
        correct = "Quantitative"
        explanation = f"'{var_name}' is a <b>quantitative</b> variable because it represents a measurable, numerical quantity. You can perform mathematical operations like calculating an average on these values."
        distractors = ["Categorical", "Neither", "Both"]
    else: # Ask about a categorical variable
        var_name, examples = random.choice(DATA_POOLS["categorical_vars"])
        question = f"A survey asks participants to state their <b>{var_name}</b>. What type of variable is this?"
        correct = "Categorical"
        explanation = f"'{var_name}' is a <b>categorical</b> variable because its values (e.g., {', '.join(examples)}) fit into distinct groups or labels. They are not numerical measurements."
        distractors = ["Quantitative", "Neither", "Both"]
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

def _level1_from_data():
    """Ask to identify a variable type from a small sample of data."""
    if random.random() < 0.5: # Quantitative data
        var_name, _, (min_val, max_val) = random.choice(DATA_POOLS["quantitative_vars"])
        data_points = [f"{random.uniform(min_val, max_val):.1f}" for _ in range(4)]
        question = f"A dataset for '{var_name}' contains the following values: <code>{', '.join(data_points)}</code>. What type of data is this?"
        correct = "Quantitative"
        explanation = "The data consists of numerical measurements that can be ordered and averaged. This makes it <b>quantitative</b>."
    else: # Categorical data
        var_name, examples = random.choice(DATA_POOLS["categorical_vars"])
        data_points = random.sample(examples, min(len(examples), 4))
        question = f"A dataset for '{var_name}' contains the following values: <code>{', '.join(data_points)}</code>. What type of data is this?"
        correct = "Categorical"
        explanation = "The data consists of labels or categories, not numerical measurements. This makes it <b>categorical</b>."
    options, correct_index = _create_shuffled_options(correct, ["Quantitative", "Categorical"] if correct == "N/A" else ["Quantitative" if correct == "Categorical" else "Categorical", "Identifier", "Boolean"])
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

def _level1_numeric_label_trap():
    """Ask to identify a categorical variable that uses numbers as labels."""
    var_name, examples = random.choice(DATA_POOLS["numeric_labels"])
    question = f"A researcher collects the <b>{var_name}</b> for each person/item. The values look like this: <code>{', '.join(map(str, examples))}</code>. What type of variable is this?"
    correct = "Categorical"
    explanation = f"Although '{var_name}' uses numbers, it is a <b>categorical</b> variable. The numbers are just labels or identifiers. You cannot meaningfully calculate an average {var_name}."
    distractors = ["Quantitative", "Continuous Quantitative", "Discrete Quantitative"]
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

# -- Level 2 Question Generators --

def _level2_key_difference():
    """Ask about the fundamental difference between the two variable types."""
    quant_var, _, _ = random.choice(DATA_POOLS["quantitative_vars"])
    cat_var, _ = random.choice(DATA_POOLS["categorical_vars"])
    question = f"What is the most important difference between a quantitative variable like <b>{quant_var}</b> and a categorical variable like <b>{cat_var}</b>?"
    correct = "Quantitative variables represent numerical measurements, while categorical variables represent labels or groups."
    distractors = [
        "Quantitative variables have more unique values than categorical variables.",
        "Categorical variables are used in science, while quantitative are used in business.",
        "Quantitative variables are always whole numbers, and categorical variables are always text."
    ]
    explanation = "The core distinction is what the values represent. <b>Quantitative</b> variables are about 'how much' or 'how many' and are numerical. <b>Categorical</b> variables are about 'what kind' and place individuals into groups."
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

def _level2_define_type():
    """Ask for the best definition of one of the variable types."""
    if random.random() < 0.5: # Define quantitative
        question = "Which of the following statements best describes a <b>quantitative</b> variable?"
        correct = "It has numerical values where arithmetic operations (like averaging) make sense."
        distractors = [
            "It is any variable that is represented by numbers, including ID numbers.",
            "It describes a quality or characteristic that cannot be measured.",
            "It must be a continuous value and cannot be a whole number."
        ]
        explanation = "A key feature of <b>quantitative</b> variables is that they are numerical values on which you can perform meaningful arithmetic, reflecting their nature as measurements or counts."
    else: # Define categorical
        question = "Which of the following statements best describes a <b>categorical</b> variable?"
        correct = "It places an individual into one of several groups or categories."
        distractors = [
            "It is a variable whose values are always text-based.",
            "It can be any variable as long as there are fewer than 10 possible values.",
            "It measures the quantity of a characteristic."
        ]
        explanation = "A <b>categorical</b> variable's primary function is classification—sorting observations into named groups. These can be represented by text (e.g., 'Blue') or numbers (e.g., ZIP codes)."
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

def _level2_example_classification():
    """Given two examples, explain why they are classified differently."""
    context = random.choice(DATA_POOLS["contexts"])
    quant_var, unit, _ = random.choice(DATA_POOLS["quantitative_vars"])
    cat_var, _ = random.choice(DATA_POOLS["categorical_vars"])
    question = f"In {context}, a researcher collects data on <b>'{quant_var} ({unit})'</b> and <b>'{cat_var}'</b>. Why is '{quant_var}' considered quantitative while '{cat_var}' is categorical?"
    correct = f"Because '{quant_var}' is a numerical measurement, while '{cat_var}' represents distinct, non-numeric categories."
    distractors = [
        f"Because '{quant_var}' has units and '{cat_var}' does not.",
        f"Because there are more possible values for '{quant_var}' than for '{cat_var}'.",
        f"Because '{quant_var}' data is more accurate and scientific than '{cat_var}' data."
    ]
    explanation = f"The distinction lies in the nature of the data itself. <b>{quant_var}</b> is a measurement on a numerical scale. <b>{cat_var}</b> is a label that assigns an item to a group. This fundamental difference dictates how they are analyzed."
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

# -- Level 3 Question Generators --

def _level3_appropriate_summary():
    """Given a variable, identify the correct summary statistic."""
    if random.random() < 0.5: # Summarize a quantitative variable
        var_name, unit, _ = random.choice(DATA_POOLS["quantitative_vars"])
        question = f"A dataset contains the <b>{var_name} ({unit})</b> for 100 people. Which of the following is an appropriate way to summarize this variable?"
        correct = f"Calculate the mean (average) {var_name}."
        distractors = [
            f"Count the number of letters in each person's name.",
            f"List the most common {var_name} (mode) as the only summary.",
            f"Create a frequency table of categories."
        ]
        explanation = f"Since <b>{var_name}</b> is a quantitative variable, calculating numerical summaries like the <b>mean</b>, median, or standard deviation is a standard and meaningful way to describe its central tendency and spread."
    else: # Summarize a categorical variable
        var_name, examples = random.choice(DATA_POOLS["categorical_vars"])
        question = f"For a study, you collect data on participants' <b>{var_name}</b> (e.g., {', '.join(examples)}). What is the most appropriate way to summarize this variable?"
        correct = "Create a frequency table or bar chart showing the count for each category."
        distractors = [
            f"Calculate the average {var_name}.",
            f"Find the range of the {var_name}.",
            f"Calculate the standard deviation of the names."
        ]
        explanation = f"For a <b>categorical</b> variable like '{var_name}', the most useful summary is to count how many observations fall into each category. This is often visualized with a <b>bar chart</b>."
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

def _level3_from_dataset_table():
    """Show a small table from a real dataset and ask to classify variables."""
    # Sample 4 rows from the wine dataset
    indices = np.random.choice(wine.data.shape[0], 4, replace=False)
    sample_data = wine.data[indices, :3]  # Alcohol, Malic Acid, Ash
    sample_target = wine.target[indices]
    
    table_html = "<table class='table'><thead><tr><th>Alcohol (%)</th><th>Malic Acid</th><th>Ash</th><th>Wine Class</th></tr></thead><tbody>"
    for i in range(4):
        table_html += f"<tr><td>{sample_data[i, 0]:.2f}</td><td>{sample_data[i, 1]:.2f}</td><td>{sample_data[i, 2]:.2f}</td><td>{wine.target_names[sample_target[i]]}</td></tr>"
    table_html += "</tbody></table>"
    
    question = f"A researcher is analyzing the wine dataset, a snippet of which is shown below.<br>{table_html}<br>Based on this table, how should the 'Wine Class' and 'Alcohol' variables be classified?"
    correct = "'Wine Class' is categorical, and 'Alcohol' is quantitative."
    distractors = [
        "'Wine Class' is quantitative, and 'Alcohol' is categorical.",
        "Both 'Wine Class' and 'Alcohol' are quantitative.",
        "Both 'Wine Class' and 'Alcohol' are categorical."
    ]
    explanation = "<b>'Wine Class'</b> sorts each wine into a named group ('class_0', 'class_1', etc.), making it <b>categorical</b>. <b>'Alcohol'</b> is a numerical measurement (percentage), making it <b>quantitative</b>."
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

def _level3_mermaid_chart():
    """Show a Mermaid bar chart and ask what it represents."""
    cat_var, examples = random.choice(DATA_POOLS["categorical_vars"])
    counts = {ex: random.randint(10, 50) for ex in examples}
    
    mermaid_code = f"graph TD\n    subgraph &quot;Frequency of {cat_var}&quot;\n"
    for cat, count in counts.items():
        mermaid_code += f"    {cat} --> {cat}Count[{count}]\n"
    mermaid_code += "    end"
    
    chart_html = f"<pre class='mermaid'>{mermaid_code}</pre>"
    question = f"The following chart was created to summarize data for the variable '{cat_var}'.<br>{chart_html}<br>What does this chart show?"
    correct = "A frequency count of a categorical variable."
    distractors = [
        "The average value of a quantitative variable.",
        "The distribution of a continuous quantitative variable.",
        "The relationship between two different quantitative variables."
    ]
    explanation = f"The chart displays distinct categories ('{', '.join(examples)}') and a count for each. This is a <b>frequency distribution</b>, the standard way to summarize <b>categorical</b> data."
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

# -- Level 4 Question Generators --

def _level4_meaningless_calculation():
    """Ask why a specific calculation is meaningless."""
    var_name, examples = random.choice(DATA_POOLS["numeric_labels"])
    question = f"A data analyst new to the team calculates the 'average {var_name}' from a list of {len(examples)} items and gets a result of {np.mean(examples):.2f}. Why is this calculation statistically meaningless?"
    correct = f"Because '{var_name}' is a categorical variable where the numbers are labels, not quantities."
    distractors = [
        "Because the sample size is too small to calculate a meaningful average.",
        "Because averages can only be calculated on data that includes decimals.",
        "Because the median should have been used instead of the mean for these numbers."
    ]
    explanation = f"The core issue is variable type. <b>{var_name}</b> is a <b>categorical</b> identifier. Averaging labels (even if they are numbers) does not produce a meaningful result. It's like averaging phone numbers."
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

def _level4_chart_choice():
    """Generate a histogram and ask why it's a better choice than a pie chart."""
    data_sample = np.random.choice(iris.data[:, 0], size=80) # Sepal Length
    hist, bin_edges = np.histogram(data_sample, bins=8)
    labels = [f"{bin_edges[i]:.1f}-{bin_edges[i+1]:.1f}" for i in range(len(bin_edges)-1)]
    
    chart_config = {
        "type": 'bar',
        "data": { "labels": labels, "datasets": [{"label": 'Frequency', "data": hist.tolist(), "backgroundColor": 'rgba(75, 192, 192, 0.5)'}] },
        "options": {
            "plugins": {"title": {"display": True, "text": 'Distribution of Sepal Length (cm)'}},
            "scales": { "y": {"title": {"display": True, "text": "Count"}}, "x": {"title": {"display": True, "text": "Length Bins"}} }
        }
    }
    chart_html = f"<pre class='chartjs'>{html.escape(json.dumps(chart_config))}</pre>"
    
    question = f"The histogram below displays the distribution of sepal lengths from a sample of flowers.<br>{chart_html}<br>Why is this histogram a more appropriate visualization for this data than a pie chart?"
    correct = "A histogram shows the distribution (shape, center, spread) of a quantitative variable, which a pie chart cannot do."
    distractors = [
        "A pie chart cannot be used for data with more than 5 categories.",
        "A histogram is better because it uses bars instead of slices, which are easier to read.",
        "A pie chart is only used for categorical data that adds up to exactly 100%."
    ]
    explanation = "Sepal length is a continuous <b>quantitative</b> variable. A <b>histogram</b> is the standard choice for visualizing its frequency distribution. A <b>pie chart</b> is used to show proportions of a whole for a small number of <b>categorical</b> variables, which is not suitable here."
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

def _level4_analysis_validity():
    """Ask if a proposed analysis step is valid given the variable types."""
    context = random.choice(DATA_POOLS["contexts"])
    quant_var, _, _ = random.choice(DATA_POOLS["quantitative_vars"])
    cat_var, _ = random.choice(DATA_POOLS["categorical_vars"])
    
    question = f"As part of {context}, an analyst wants to compare the average <b>{quant_var}</b> across different groups of <b>{cat_var}</b>. Is this a valid analytical step?"
    correct = f"Yes, this is a valid and common analysis, as it compares a numerical outcome across defined categories."
    distractors = [
        f"No, because you cannot mix categorical and quantitative variables in one analysis.",
        f"No, because you should calculate the average {cat_var} for each {quant_var} instead.",
        f"Only if the number of categories in {cat_var} is less than three."
    ]
    explanation = f"This is a classic and powerful analytical technique (e.g., an ANOVA or t-test). It is valid because you are using the <b>categorical</b> variable ('{cat_var}') to define groups, and then calculating a meaningful summary statistic (the mean) for the <b>quantitative</b> variable ('{quant_var}') within each of those groups."
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}
    
# -- Level 5 Question Generators --

def _level5_design_a_variable():
    """Ask how to properly define and measure a variable for a study."""
    quant_var, _, _ = random.choice(DATA_POOLS["quantitative_vars"])
    context = random.choice(["employee wellness", "customer satisfaction", "academic success"])
    question = f"A team is designing a study on <b>{context}</b>. They want to measure '{quant_var}' as a key outcome. Which of the following is the best way to operationalize this as a quantitative variable?"
    correct = f"Measure it directly using a standard scale (e.g., a survey question asking for {quant_var} in {random.choice(['exact numbers', 'a scale from 1 to 10'])})."
    distractors = [
        f"Classify people into 'High {quant_var}' and 'Low {quant_var}' groups.",
        f"Ask people to describe their {quant_var} in words.",
        f"Assign a random number to each person to represent their {quant_var}."
    ]
    explanation = "To treat a variable as <b>quantitative</b>, you must measure it on a numerical scale where the values have a consistent meaning (e.g., interval or ratio scale). Classifying it into groups ('High'/'Low') would turn it into a categorical (ordinal) variable, losing detailed information."
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

def _level5_critique_a_plan():
    """Ask for a critique of a flawed data collection plan."""
    cat_var, examples = random.choice(DATA_POOLS["categorical_vars"])
    quant_var, _, _ = random.choice(DATA_POOLS["quantitative_vars"])
    question = f"Critique this data collection plan: 'To study the link between {cat_var} and {quant_var}, we will ask people for their {cat_var} and then ask if their {quant_var} is `Above Average` or `Below Average`.'"
    correct = f"The plan unnecessarily converts the quantitative variable '{quant_var}' into a categorical one, losing valuable detail."
    distractors = [
        f"The plan is invalid because '{cat_var}' is not a scientific variable.",
        "The plan is perfect and is the most efficient way to collect the data.",
        "The plan should also ask for a third variable, like age, to be valid."
    ]
    explanation = f"By reducing the measurement of <b>{quant_var}</b> to two categories ('Above Average'/'Below Average'), the plan loses the actual numerical data. This prevents powerful analyses like calculating the actual average or checking for correlations. It's almost always better to collect the raw quantitative data if possible."
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}

def _level5_propose_variables_mermaid():
    """Use a Mermaid diagram to frame a study design question."""
    context = random.choice(["smartphone usage habits", "commuter travel patterns", "diet and exercise trends"])
    mermaid_code = f"graph TD\n    A[Start: Study on {context}] --> B[Step 1: Define Variables];\n    B --> C[Step 2: Collect Data];"
    chart_html = f"<pre class='mermaid'>{html.escape(mermaid_code)}</pre>"
    
    cat_var, _ = random.choice(DATA_POOLS["categorical_vars"])
    quant_var, unit, _ = random.choice(DATA_POOLS["quantitative_vars"])
    
    question = f"You are designing a study on <b>{context}</b> as outlined below.<br>{chart_html}<br>In 'Step 1: Define Variables', which option correctly proposes one categorical AND one quantitative variable relevant to this topic?"
    correct = f"Categorical: 'Primary Use Case' (e.g., Social, Work, Gaming); Quantitative: 'Screen Time' (in hours/day)."
    distractors = [
        f"Categorical: '{quant_var}'; Quantitative: '{cat_var}'", # Swapped
        "Categorical: 'Phone Color'; Quantitative: 'User ID Number'", # Poor choices
        "Both 'Primary Use Case' and 'Screen Time' should be measured as categorical variables for simplicity."
    ]
    explanation = "A good study design requires correctly identifying variable types. 'Primary Use Case' correctly groups users (<b>categorical</b>), while 'Screen Time' correctly measures a numerical amount (<b>quantitative</b>). This allows for rich analysis, such as comparing the average screen time across different use cases."
    options, correct_index = _create_shuffled_options(correct, distractors)
    return {"question": question, "options": options, "correctAnswer": correct_index, "explanation": explanation}


# -- Main Question Generation Function --

QUESTION_GENERATORS = {
    1: [_level1_from_context, _level1_from_data, _level1_numeric_label_trap],
    2: [_level2_key_difference, _level2_define_type, _level2_example_classification],
    3: [_level3_appropriate_summary, _level3_from_dataset_table, _level3_mermaid_chart],
    4: [_level4_meaningless_calculation, _level4_chart_choice, _level4_analysis_validity],
    5: [_level5_design_a_variable, _level5_critique_a_plan, _level5_propose_variables_mermaid]
}

def generate_question(dummy_type: int ,level: int) -> dict:
    """
    Given a difficulty level from 1 to 5, this function returns a randomly generated
    practice question about categorical vs. quantitative variables.

    Args:
        level: An integer from 1 to 5 representing the desired difficulty.

    Returns:
        A dictionary containing the question, options, correct answer index, and an explanation.
        The format is:
        {
          "question": "self-contained HTML string",
          "options": [HTML_str, HTML_str, HTML_str, HTML_str],
          "correctAnswer": int (index 0-3),
          "explanation": "string"
        }
    """
    if level not in levelDescriptions:
        raise ValueError(f"Invalid level: {level}. Please choose a level from 1 to {len(levelDescriptions)}.")

    # Randomly select a question generator function for the specified level
    generator_func = random.choice(QUESTION_GENERATORS[level])
    
    # Generate and return the question dictionary
    return json.dumps(generator_func())