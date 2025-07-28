import random
import json
import html
import numpy as np
from sklearn.datasets import load_iris, load_diabetes, load_wine
import pandas as pd

def generate_level_1_question() -> str:
    """
    Returns a new randomly generated practice question dictionary for identifying
    variable types (categorical vs. quantitative).

    The function generates questions based on different templates:
    1.  Context-based: Describes a scenario and asks to classify the variable.
    2.  Data-based: Shows a snippet of data and asks for classification.
    3.  Chart-based: Displays a chart (Bar for categorical, Histogram for quantitative)
        and asks to classify the variable it represents.

    Args:
        level (int): The difficulty level (currently unused, for future expansion).

    Returns:
        dict: A dictionary containing the question, options, correct answer index,
              and an explanation, formatted as specified.
    """
    # --- Data Pools ---
    # Pool of categorical variables with context and example values
    categorical_vars = [
        {'name': 'Dominant Hand', 'context': 'a survey of students', 'values': ['Left-handed', 'Right-handed', 'Ambidextrous']},
        {'name': 'Car Manufacturer', 'context': 'tracking cars in a parking lot', 'values': ['Toyota', 'Ford', 'Honda', 'BMW', 'Nissan']},
        {'name': 'Blood Type', 'context': 'patient records at a hospital', 'values': ['A', 'B', 'AB', 'O']},
        {'name': 'Iris Species', 'context': 'a botanical study of flowers', 'values': ['Setosa', 'Versicolor', 'Virginica']}
    ]

    # Pool of quantitative variables with context and units
    quantitative_vars = [
        {'name': 'Height', 'context': 'measuring a group of adults', 'unit': 'cm'},
        {'name': 'Age', 'context': 'a survey of a town\'s population', 'unit': 'years'},
        {'name': 'Body Temperature', 'context': 'a clinical health check', 'unit': '°C'},
        {'name': 'Annual Income', 'context': 'an economic survey', 'unit': 'dollars'},
        {'name': 'Sepal Length', 'context': 'a botanical study of flowers', 'unit': 'cm'}
    ]

    # --- Template Selection ---
    question_type = random.choice(['categorical', 'quantitative'])
    template = random.choice(['context_only', 'data_snippet', 'chart'])

    question_html = ""
    explanation = ""
    correct_answer_text = ""

    if question_type == 'categorical':
        var_info = random.choice(categorical_vars)
        correct_answer_text = "Categorical (Qualitative)"
        explanation = (f"The variable '{var_info['name']}' is categorical because it represents distinct "
                       f"groups or labels ({', '.join(var_info['values'])}). You can't perform meaningful "
                       f"mathematical calculations like averaging them.")

        if template == 'context_only':
            question_html = (f"<p>A researcher is conducting a study on {var_info['context']}. "
                             f"They record the <strong>{var_info['name']}</strong> for each subject.</p>"
                             f"<p>What type of variable is '{var_info['name']}'?</p>")

        elif template == 'data_snippet':
            sample_size = min(len(var_info['values']), 5)
            data_snippet = ', '.join(random.sample(var_info['values'], k=sample_size))
            question_html = (f"<p>In a study, a researcher collects the following data for the variable "
                             f"<strong>'{var_info['name']}'</strong>:</p>"
                             f"<pre style='background-color:#f0f0f0; padding: 10px; border-radius: 5px;'>"
                             f"{data_snippet}, ...</pre>"
                             f"<p>What type of variable is this?</p>")

        else: # chart template
            labels = var_info['values']
            data = [random.randint(10, 50) for _ in labels]
            chart_config = {
                'type': 'bar',
                'data': {
                    'labels': labels,
                    'datasets': [{
                        'label': f'Count of {var_info["name"]}',
                        'data': data,
                        'backgroundColor': [
                            'rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)',
                            'rgba(255, 206, 86, 0.5)', 'rgba(75, 192, 192, 0.5)',
                            'rgba(153, 102, 255, 0.5)'
                        ],
                        'borderColor': [
                            'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)'
                        ],
                        'borderWidth': 1
                    }]
                },
                'options': {'scales': {'y': {'beginAtZero': True}}}
            }
            escaped_config = html.escape(json.dumps(chart_config))
            question_html = (f"<p>The following chart shows the distribution of the variable "
                             f"<strong>'{var_info['name']}'</strong> from a sample.</p>"
                             f"<pre class='chartjs'>{escaped_config}</pre>"
                             f"<p>Based on the chart, what type of variable is '{var_info['name']}'?</p>")

    else: # quantitative
        var_info = random.choice(quantitative_vars)
        correct_answer_text = "Quantitative (Numerical)"
        explanation = (f"The variable '{var_info['name']}' is quantitative because it represents a measurable "
                       f"quantity. The values are numbers that you can perform meaningful mathematical "
                       f"operations on, like finding an average or sum.")

        # Load appropriate dataset for realistic values
        if 'Sepal' in var_info['name']:
            data_source = load_iris().data[:, 0] # Sepal Length
        elif 'Age' in var_info['name']:
            data_source = load_diabetes().data[:, 0] * 100 # Age is normalized, scale it up
        else:
            data_source = np.random.normal(loc=60, scale=15, size=100) # Generic data

        if template == 'context_only':
            question_html = (f"<p>As part of {var_info['context']}, a researcher measures the "
                             f"<strong>{var_info['name']}</strong> (in {var_info['unit']}) for each participant.</p>"
                             f"<p>What type of variable is '{var_info['name']}'?</p>")

        elif template == 'data_snippet':
            sample_data = np.random.choice(data_source, 5).round(1)
            data_snippet = ', '.join(map(str, sample_data))
            question_html = (f"<p>A researcher collects the following measurements for the variable "
                             f"<strong>'{var_info['name']}'</strong>:</p>"
                             f"<pre style='background-color:#f0f0f0; padding: 10px; border-radius: 5px;'>"
                             f"{data_snippet}, ...</pre>"
                             f"<p>What type of variable is this?</p>")

        else: # chart template (histogram)
            counts, bin_edges = np.histogram(data_source, bins=5)
            labels = [f'{edge:.1f}-{bin_edges[i+1]:.1f}' for i, edge in enumerate(bin_edges[:-1])]
            chart_config = {
                'type': 'bar',
                'data': {
                    'labels': labels,
                    'datasets': [{
                        'label': f'Frequency of {var_info["name"]}',
                        'data': counts.tolist(),
                        'backgroundColor': 'rgba(75, 192, 192, 0.5)',
                        'borderColor': 'rgba(75, 192, 192, 1)',
                        'borderWidth': 1
                    }]
                },
                'options': {
                    'scales': {'y': {'beginAtZero': True, 'title': {'display': True, 'text': 'Frequency'}}},
                    'plugins': {'legend': {'display': False}},
                    'tooltips': {'enabled': False}
                }
            }
            escaped_config = html.escape(json.dumps(chart_config))
            question_html = (f"<p>The histogram below shows the distribution of the variable "
                             f"<strong>'{var_info['name']}'</strong> from a sample.</p>"
                             f"<pre class='chartjs'>{escaped_config}</pre>"
                             f"<p>Based on the chart, what type of variable is '{var_info['name']}'?</p>")


    # --- Options and Shuffling ---
    options = [
        correct_answer_text,
        "Categorical (Qualitative)" if question_type == 'quantitative' else "Quantitative (Numerical)",
        "Identifier Variable",
        "Neither Categorical nor Quantitative"
    ]
    random.shuffle(options)
    correct_answer_index = options.index(correct_answer_text)

    return json.dumps({
        "question": question_html,
        "options": options,
        "correctAnswer": correct_answer_index,
        "explanation": explanation
    })


def generate_level_2_question() -> dict:
    """
    Returns a new randomly generated practice question dictionary for identifying
    variable types (categorical vs. quantitative).

    The function generates questions based on the learning goal: "Explain
    differences between categorical and quantitative variables, including
    examples of each. (e.g., recognizing that “ZIP code” is categorical,
    “temperature” is quantitative."

    Args:
        level (int): The difficulty level (currently unused, for future expansion).

    Returns:
        dict: A dictionary with the following keys:
            - "question" (str): HTML string with all content.
            - "options" (list): A list of four HTML strings for the answers.
            - "correctAnswer" (int): The index of the correct option after shuffling.
            - "explanation" (str): A brief rationale behind the correct answer.
    """
    # --- Data Pools ---
    # General pools for non-contextual questions
    general_categorical_vars = [
        ("ZIP Code", "e.g., 90210, 10001"),
        ("Car Brand", "e.g., Ford, Toyota, Honda"),
        ("Blood Type", "e.g., A, B, AB, O"),
        ("Eye Color", "e.g., Blue, Brown, Green"),
        ("T-shirt Size", "e.g., Small, Medium, Large"),
        ("Type of Music", "e.g., Rock, Pop, Classical"),
        ("Employment Status", "e.g., Employed, Unemployed, Student"),
        ("Planet in Solar System", "e.g., Mercury, Venus, Earth"),
        ("Day of the Week", "e.g., Monday, Tuesday, Wednesday"),
        ("Marital Status", "e.g., Single, Married, Divorced"),
        ("Hair Color", "e.g., Blonde, Brown, Black, Red")
    ]

    general_quantitative_vars = [
        ("Temperature", "in degrees Celsius"),
        ("Height", "in centimeters"),
        ("Weight", "in kilograms"),
        ("Annual Income", "in US dollars"),
        ("Reaction Time", "in milliseconds"),
        ("Number of Siblings", "as a count"),
        ("Wind Speed", "in kilometers per hour"),
        ("Daily Steps", "as a count"),
        ("Screen Time", "in hours per day")
    ]
    
    # NEW: Context-aware data structure inspired by sklearn datasets
    # This ensures variables are logically tied to their context.
    studies = [
        {
            "context_phrase": "a biological study of iris flowers",
            "subject_noun": "flower",
            "quant_vars": [("Sepal Length", "in cm"), ("Sepal Width", "in cm"), ("Petal Length", "in cm"), ("Petal Width", "in cm")],
            "cat_vars": [("Species", "e.g., Setosa, Versicolor")]
        },
        {
            "context_phrase": "a medical study on diabetes progression",
            "subject_noun": "patient",
            "quant_vars": [("Age", "in years"), ("Body Mass Index (BMI)", ""), ("Average Blood Pressure", "in mm Hg"), ("Blood Serum Level", "in mg/dL")],
            "cat_vars": [("Sex", "e.g., Male, Female")]
        },
        {
            "context_phrase": "an analysis of different Italian wines",
            "subject_noun": "wine",
            "quant_vars": [("Alcohol Content", "% by volume"), ("Malic Acid Level", "in g/L"), ("Color Intensity", "as an index")],
            "cat_vars": [("Cultivar", "e.g., Class 0, Class 1, Class 2")]
        },
        {
            "context_phrase": "a real estate market analysis",
            "subject_noun": "house",
            "quant_vars": [("Median Value", "in $1000s"), ("Age of House", "in years"), ("Number of Rooms", "as a count")],
            "cat_vars": [("Proximity to River", "e.g., Yes, No")]
        }
    ]


    # --- Question Templates ---

    def template_identify_type():
        """Template: Asks to identify a variable as either categorical or quantitative. Uses general pools."""
        if random.random() > 0.5:
            correct_type = "Quantitative"
            distractor_type = "Categorical"
            correct_pool = general_quantitative_vars
            distractor_pool = general_categorical_vars
            explanation_focus = "can be measured numerically and averaged."
        else:
            correct_type = "Categorical"
            distractor_type = "Quantitative"
            correct_pool = general_categorical_vars
            distractor_pool = general_quantitative_vars
            explanation_focus = "places an individual into a group or category."

        question_html = f"Which of the following is a <strong>{correct_type.lower()}</strong> variable?"
        correct_answer, _ = random.choice(correct_pool)
        distractors = [var[0] for var in random.sample(distractor_pool, 3)]
        explanation = (f"'{correct_answer}' is a {correct_type.lower()} variable because it "
                       f"{explanation_focus} The other options are {distractor_type.lower()} variables.")
        if correct_answer == "ZIP Code":
            explanation = ("Although a ZIP code is a number, it is a categorical variable. "
                           "The numbers are labels for a location, and it doesn't make sense "
                           "to perform mathematical operations like finding the average ZIP code.")

        return question_html, correct_answer, distractors, explanation

    def template_contextual_identification():
        """Template: Provides a context and asks for the type of a specific variable. Uses context-aware data."""
        study = random.choice(studies)
        context_phrase = study["context_phrase"]
        subject_noun = study["subject_noun"]
        
        # Decide whether to ask about a quantitative or categorical variable from this study
        has_quant = bool(study["quant_vars"])
        has_cat = bool(study["cat_vars"])

        # Prioritize asking about a type that exists, then choose randomly if both exist
        if (has_quant and not has_cat) or (has_quant and has_cat and random.random() > 0.5):
            # The variable is quantitative
            variable, unit = random.choice(study["quant_vars"])
            correct_option = "Quantitative"
            distractor_options = ["Categorical", "Identifier", "Textual"]
            unit_text = f" ({unit})" if unit else ""
            explanation = (f"The variable '{variable}' is quantitative because it represents a measurable quantity"
                           f"{unit_text}. You can perform meaningful mathematical operations on it, like calculating an average.")
        elif has_cat:
            # The variable is categorical
            variable, desc = random.choice(study["cat_vars"])
            correct_option = "Categorical"
            distractor_options = ["Quantitative", "Continuous", "Numerical"]
            explanation = (f"The variable '{variable}' is categorical because it assigns each {subject_noun} to a distinct group "
                           f"or category ({desc}). Mathematical operations like addition or averaging are not meaningful for it.")
        else:
            # Fallback in case a study has no variables defined, though this shouldn't happen with current data
            return template_identify_type()

        question_html = (f"In {context_phrase}, a researcher records the <strong>{html.escape(variable)}</strong> for each {subject_noun}. "
                         f"What type of variable is this?")

        return question_html, correct_option, distractor_options, explanation

    def template_list_identification():
        """Template: Presents a list of variables and asks to pick the one of a certain type. Uses general pools."""
        if random.random() > 0.5:
            correct_type = "quantitative"
            distractor_type = "categorical"
            correct_var, _ = random.choice(general_quantitative_vars)
            distractor_vars = [var[0] for var in random.sample(general_categorical_vars, 3)]
            explanation_focus = "is a measurable numerical value."
        else:
            correct_type = "categorical"
            distractor_type = "quantitative"
            correct_var, _ = random.choice(general_categorical_vars)
            distractor_vars = [var[0] for var in random.sample(general_quantitative_vars, 3)]
            explanation_focus = "represents a group or category."

        variable_list = distractor_vars + [correct_var]
        random.shuffle(variable_list)
        variable_list_str = ", ".join([f"'{v}'" for v in variable_list])
        question_html = (f"A dataset contains the following variables: {variable_list_str}.<br>"
                         f"Which of these variables is <strong>{correct_type}</strong>?")
        explanation = (f"'{correct_var}' is the {correct_type} variable because it {explanation_focus} "
                       f"The other variables are all {distractor_type}.")
        if correct_var == "ZIP Code":
            explanation = ("While represented by a number, 'ZIP Code' is categorical because it's a label for a geographic area. "
                           "Calculating an average ZIP code wouldn't make sense. The other variables are all measurable quantities.")

        return question_html, correct_var, distractor_vars, explanation


    # --- Generation Logic ---
    # Randomly select a template function to execute
    template_functions = [
        template_identify_type,
        template_contextual_identification,
        template_list_identification
    ]
    # Give the contextual template a higher chance of being picked
    selected_template = random.choices(template_functions, weights=[25, 50, 25], k=1)[0]

    # Generate the question parts from the template
    question_html, correct_answer, distractors, explanation = selected_template()

    # Create and shuffle the final options list
    options = distractors + [correct_answer]
    random.shuffle(options)

    # Find the index of the correct answer in the shuffled list
    correct_answer_index = options.index(correct_answer)

    # HTML-escape all options to be safe
    html_options = [html.escape(str(opt)) for opt in options]

    return json.dumps({
        "question": question_html,
        "options": html_options,
        "correctAnswer": correct_answer_index,
        "explanation": explanation
    })

def generate_level_3_question() -> dict:
    """
    Returns a new randomly generated practice question dictionary for classifying variables.

    Args:
        level: An integer representing the difficulty level (currently unused but included for signature consistency).

    Returns:
        A dictionary with the following keys:
        - "question": An HTML string with all content and embedded visuals.
        - "options": A list of four HTML strings representing the answer choices.
        - "correctAnswer": An integer index of the correct option after shuffling.
        - "explanation": A string providing a brief rationale for the correct answer.
    """
    # --- Data Pools ---
    contexts = [
        "a study on the health of office workers",
        "an analysis of customer purchasing habits at a bookstore",
        "a survey of high school students' academic performance",
        "research on the biodiversity of a local park",
        "an investigation into the effectiveness of a new workout routine"
    ]

    # Variables are tuples: (Name, Type, Correct Summary, Plausible Distractor Summary)
    variables = [
        ("Blood Type", "Categorical", "Counts and Frequencies", "Mean and Standard Deviation"),
        ("Car Brand", "Categorical", "Counts and Percentages", "Median and Range"),
        ("Gender", "Categorical", "Frequencies and Proportions", "Average and Sum"),
        ("Species of plant", "Categorical", "Counts and Mode", "Standard Deviation"),
        ("Height (in cm)", "Quantitative", "Mean and Standard Deviation", "Counts and Frequencies"),
        ("Weight (in kg)", "Quantitative", "Median and Interquartile Range", "Proportions and Percentages"),
        ("Age (in years)", "Quantitative", "Mean and Range", "Frequencies and Mode"),
        ("Daily Income (in $)", "Quantitative", "Median and Standard Deviation", "Counts and Percentages"),
        ("Temperature (in Celsius)", "Quantitative", "Mean, Median, and Range", "Mode and Frequencies")
    ]

    # --- Template Selection ---
    # Templates determine the structure of the question.
    templates = [
        "template_basic_classification",
        "template_with_data_snippet",
        "template_summary_focus"
    ]
    # chosen_template = random.choice(templates)
    chosen_template = 'template_with_data_snippet' # used for specifically tsting the table format..
    # --- Content Generation ---
    context = random.choice(contexts)
    variable_name, var_type, correct_summary, distractor_summary = random.choice(variables)

    question_html = ""
    options = []
    explanation = ""

    # --- Template 1: Basic Classification ---
    if chosen_template == "template_basic_classification":
        question_html = f"""
            <p>In the context of {context}, a researcher collects data on the variable '<strong>{variable_name}</strong>'.</p>
            <p>How would you classify this variable, and what is the most appropriate way to summarize it?</p>
        """
        correct_option = f"{var_type}; summarized with {correct_summary}"
        distractor_1 = f"{'Quantitative' if var_type == 'Categorical' else 'Categorical'}; summarized with {correct_summary}"
        distractor_2 = f"{var_type}; summarized with {distractor_summary}"
        distractor_3 = f"{'Quantitative' if var_type == 'Categorical' else 'Categorical'}; summarized with {distractor_summary}"

        options = [correct_option, distractor_1, distractor_2, distractor_3]
        explanation = f"The variable '{variable_name}' is {var_type} because it represents distinct categories (or numerical values that can be measured). Therefore, it should be summarized using {correct_summary}."

    # --- Template 2: Classification with Data Snippet ---
    elif chosen_template == "template_with_data_snippet":
        data_snippet_html = ""
        if var_type == "Categorical":
            iris = load_iris()
            df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
            df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
            # Use a categorical variable from the dataset
            variable_name = "Species"
            var_type = "Categorical"
            correct_summary = "Counts and Frequencies"
            distractor_summary = "Mean and Standard Deviation"
            snippet = df[['species']].sample(5, random_state=random.randint(1, 100)).to_html(index=False, classes='table table-sm table-striped w-auto mx-auto my-3')
            data_snippet_html = snippet.replace('<table', '<table style="width: auto; margin: 1em auto; border-collapse: collapse; border: 1px solid #ccc;"')
        else: # Quantitative
            diabetes = load_diabetes()
            df = pd.DataFrame(data=diabetes.data, columns=diabetes.feature_names)
            # Use a quantitative variable
            quant_var = random.choice(['age', 'bmi', 'bp'])
            variable_name = f"Patient {quant_var.upper()}"
            var_type = "Quantitative"
            correct_summary = "Mean and Median"
            distractor_summary = "Counts and Frequencies"
            snippet = df[[quant_var]].sample(5, random_state=random.randint(1, 100)).round(2).to_html(index=False, classes='table table-sm table-striped w-auto mx-auto my-3')
            data_snippet_html = snippet.replace('<table', '<table style="width: auto; margin: 1em auto; border-collapse: collapse; border: 1px solid #ccc;"')


        question_html = f"""
            <p>A researcher is conducting {context}. They collect data on several variables, including '<strong>{variable_name}</strong>'.</p>
            <p>Here is a small snippet of the data:</p>
            {data_snippet_html}
            <p>Based on this data, how should the variable '<strong>{variable_name}</strong>' be classified and summarized?</p>
        """

        correct_option = f"{var_type}; summarized with {correct_summary}"
        distractor_1 = f"{'Quantitative' if var_type == 'Categorical' else 'Categorical'}; summarized with {correct_summary}"
        distractor_2 = f"{var_type}; summarized with {distractor_summary}"
        distractor_3 = f"{'Quantitative' if var_type == 'Categorical' else 'Categorical'}; summarized with {distractor_summary}"

        options = [correct_option, distractor_1, distractor_2, distractor_3]
        explanation = f"The variable '{variable_name}' is {var_type}. {var_type} data is best summarized using measures like {correct_summary} to understand its distribution."

    # --- Template 3: Summary Focus ---
    elif chosen_template == "template_summary_focus":
        question_html = f"""
            <p>For {context}, you are given the variable '<strong>{variable_name}</strong>', which is a <strong>{var_type}</strong> variable.</p>
            <p>Which of the following is the most appropriate statistical summary for this type of data?</p>
        """
        correct_option = f"{correct_summary}"
        distractor_1 = f"{distractor_summary}"
        # Add more distractors
        distractor_2 = "Correlation Coefficient"
        distractor_3 = "Chi-squared Test" if var_type == "Quantitative" else "T-test"


        options = [correct_option, distractor_1, distractor_2, distractor_3]
        explanation = f"Since '{variable_name}' is a {var_type} variable, the most suitable summaries are measures like {correct_summary}. The other options are either for the wrong variable type or are inferential tests, not summaries."


    # --- Shuffling and Final Assembly ---
    shuffled_options = options.copy()
    random.shuffle(shuffled_options)
    correct_answer_index = shuffled_options.index(correct_option)

    return json.dumps({
        "question": question_html,
        "options": [html.escape(opt) for opt in shuffled_options],
        "correctAnswer": correct_answer_index,
        "explanation": explanation
    })

def generate_question(question_type,level):
    if not level:
        raise ValueError('level is Needed')
    
    function_map = {
        1:generate_level_1_question,
        2:generate_level_2_question,
        3:generate_level_3_question,
    }
    
    return function_map[level]()
# --- Example Usage ---
# if __name__ == '__main__':
#     # Generate and print a few example questions to demonstrate functionality
#     for i in range(3):
#         print(f"--- Example Question {i+1} ---")
#         question_data = generate_variable_type_question(level=1)
#         print("Question HTML:\n", question_data['question'])
#         print("\nOptions:")
#         for idx, option in enumerate(question_data['options']):
#             print(f"  {idx}: {option}")
#         print("\nCorrect Answer Index:", question_data['correctAnswer'])
#         print("Explanation:", question_data['explanation'])
#         print("-" * 30, "\n")
