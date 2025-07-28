import random, html, json
from sklearn import datasets
import numpy as np

levelDescriptions = {
    1: "Identify whether a given variable (described by context or data values) is categorical (qualitative) or quantitative (numerical).",
    2: "Explain differences between categorical and quantitative variables, including examples of each.",
    3: "Given a real data context, classify multiple variables and decide which summaries (counts vs. numerical measures) apply.",
    4: "Analyze how variable type affects data display and analysis (e.g., why computing a mean makes sense for a quantitative variable but not for a categorical one).",
    5: "Design or critique a study’s data collection plan with both variable types, including selecting measurement scales and justifying data types."
}

# Variable examples and dataset subsets
categorical_vars = ["Blood Type", "Favorite Color", "Brand of Phone", "Political Affiliation", "Type of Cuisine"]
quantitative_vars = ["Height (cm)", "Weight (kg)", "Age", "Test Score", "Monthly Salary ($)"]
contexts = ["hospital survey", "student performance study", "consumer behavior analysis", "fitness tracker dataset", "employee review system"]
scales = ["Nominal", "Ordinal", "Interval", "Ratio"]

# Dataset-based utilities
iris = datasets.load_iris(as_frame=True).frame
wine = datasets.load_wine(as_frame=True).frame

def sample_from_dataset(dataset, n=5):
    return dataset.sample(n)

def format_table(df):
    return "<table border='1'><tr>" + "".join(f"<th>{html.escape(str(col))}</th>" for col in df.columns) + "</tr>" + "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(val))}</td>" for val in row) + "</tr>" for row in df.to_numpy()
    ) + "</table>"

def generate_question(dummy_type,level: int) -> dict:
    assert level in levelDescriptions, "Invalid level"
    data = None
    # LEVEL 1
    if level == 1:
        templates = [
            "Is the variable <b>{var}</b> categorical or quantitative?",
            "Classify <b>{var}</b> as either a categorical or quantitative variable.",
            "Given a dataset with a column labeled <b>{var}</b>, what type of variable is it?"
        ]
        var_type = random.choice(["categorical", "quantitative"])
        var = random.choice(categorical_vars if var_type == "categorical" else quantitative_vars)
        template = random.choice(templates).format(var=html.escape(var))
        correct = "Categorical" if var_type == "categorical" else "Quantitative"
        options = ["Categorical", "Quantitative", "Ordinal", "Interval"]
        options = random.sample(options, 4)
        if correct not in options:
            options[random.randint(0, 3)] = correct
        explanation = f"'{var}' is {'a category label' if var_type == 'categorical' else 'a measurable quantity'}, so it's {correct.lower()}."
        data =  {
            "question": template,
            "options": options,
            "correctAnswer": options.index(correct),
            "explanation": explanation
        }

    # LEVEL 2
    if level == 2:
        templates = [
            "Which of the following best explains the difference between categorical and quantitative variables?",
            "Pick the most accurate description of categorical vs. quantitative variables.",
            "What distinguishes a quantitative variable from a categorical one?"
        ]
        template = random.choice(templates)
        correct = "Quantitative variables are numerical and measurable, while categorical variables represent group labels."
        distractors = [
            "Categorical variables are always numbers; quantitative variables are always words.",
            "Quantitative variables can’t be used in analysis, only categorized.",
            "Categorical variables are measured with rulers; quantitative variables are not."
        ]
        options = [correct] + random.sample(distractors, 3)
        random.shuffle(options)
        data =  {
            "question": template,
            "options": options,
            "correctAnswer": options.index(correct),
            "explanation": "Quantitative variables involve numeric measurement; categorical variables represent categories or groups."
        }

    # LEVEL 3
    if level == 3:
        df = sample_from_dataset(wine[['alcohol', 'hue', 'target']])
        df['target'] = df['target'].apply(lambda x: f"Type {int(x)}")
        table_html = format_table(df)
        template = f"""
        Below is a sample of a dataset from a wine quality study:<br><br>
        {table_html}<br><br>
        Which of the following best classifies the variables?
        """
        correct = "Alcohol and Hue are quantitative; Type is categorical."
        distractors = [
            "All variables are categorical.",
            "All variables are quantitative.",
            "Hue and Type are categorical; Alcohol is quantitative."
        ]
        options = [correct] + random.sample(distractors, 3)
        random.shuffle(options)
        data =  {
            "question": template,
            "options": options,
            "correctAnswer": options.index(correct),
            "explanation": "Alcohol and Hue are continuous numerical measures; Type represents wine class labels."
        }

    # LEVEL 4
    if level == 4:
        templates = [
            "Why is it incorrect to calculate a mean for the variable <b>{var}</b>?",
            "Which type of variable allows for computing measures like standard deviation?",
            "How does the type of variable affect what kind of graph or summary can be used?"
        ]
        var = random.choice(categorical_vars)
        template = random.choice(templates).format(var=var)
        correct = f"Because {var} is categorical, calculating a mean doesn't make sense since the values are labels, not numbers."
        distractors = [
            f"{var} is quantitative so you should compute standard deviation instead.",
            f"You can always calculate a mean for any variable.",
            f"A histogram is the only suitable graph for {var}."
        ]
        options = [correct] + random.sample(distractors, 3)
        random.shuffle(options)
        data =  {
            "question": template,
            "options": options,
            "correctAnswer": options.index(correct),
            "explanation": "You can only compute numeric summaries like mean or std. dev for quantitative variables."
        }

    # LEVEL 5
    if level == 5:
        templates = [
            "You are designing a {context}. Which pair of variables would you collect, and how would you classify them?",
            "In planning a {context}, which of the following represents a valid choice of both a categorical and a quantitative variable?",
            "You want to analyze both qualitative and quantitative aspects of a {context}. Which pair fits?"
        ]
        context = random.choice(contexts)
        correct_pair = (random.choice(categorical_vars), random.choice(quantitative_vars))
        distractor_pairs = [
            (random.choice(quantitative_vars), random.choice(quantitative_vars)),
            (random.choice(categorical_vars), random.choice(categorical_vars)),
            (random.choice(categorical_vars), "Mood Level (smiley face)")
        ]
        def format_pair(p): return f"{p[0]} (Categorical), {p[1]} (Quantitative)"
        options = [format_pair(correct_pair)] + [format_pair(p) for p in distractor_pairs]
        random.shuffle(options)
        template = random.choice(templates).format(context=html.escape(context))
        data =  {
            "question": template,
            "options": options,
            "correctAnswer": options.index(format_pair(correct_pair)),
            "explanation": f"To capture both types, include one category label (like {correct_pair[0]}) and one measurable quantity (like {correct_pair[1]})."
        }

    
    return json.dumps(data)