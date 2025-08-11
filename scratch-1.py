import random
import html
import json
from sklearn import datasets
from sklearn.datasets import load_iris, load_wine,make_blobs
import statistics
import numpy as np

def level_1() -> dict:
    """
    Returns a new randomly generated practice question dictionary:
    {
      "question": HTML string with all content and embedded visuals,
      "options": [HTML, HTML, HTML, HTML],
      "correctAnswer": int,
      "explanation": str
    }
    """

    # =========================
    # DATA POOLS
    # =========================
    categorical_vars = [
        # People
        "blood type", "eye color", "gender", "marital status", "occupation", "hair color", "nationality",
        "favorite sport", "vehicle type", "language spoken", "zodiac sign", "ethnicity", "pet type",
        # Objects
        "car brand", "product category", "operating system", "book genre", "music genre", "movie genre",
        "shirt size", "department code", "customer ID", "zip code", "license plate", "model name", "flight code",
        # Locations
        "city", "country", "region name", "postal code", "state", "continent", "school name", "hospital name",
        # Events
        "event type", "festival name", "holiday name", "sports league", "game level",
        # Biological
        "species", "genus", "breed", "fruit type", "vegetable type", "flower color",
    ] # + [f"CategoryVar{i}" for i in range(51, 101)]

    quantitative_vars = [
        # Physical measurements
        "height (cm)", "weight (kg)", "age (years)", "temperature (°C)", "distance (km)", "speed (m/s)",
        "length (m)", "width (m)", "volume (liters)", "area (m²)", "depth (m)", "altitude (m)",
        # Counts
        "number of siblings", "number of bedrooms", "page count", "population", "score (%)",
        "income (USD)", "price (USD)", "rating (stars)", "quantity sold",
        # Time measurements
        "duration (minutes)", "time taken (seconds)", "year of birth", "hour of the day", "day of the month",
        # Scientific
        "pH level", "concentration (mg/L)", "mass (grams)", "energy (kJ)", "pressure (Pa)",
        "wavelength (nm)", "current (A)", "voltage (V)", "frequency (Hz)",
    ] # + [f"QuantVar{i}" for i in range(51, 101)]

    contexts = [
        "a survey of college students", "a hospital patient record", "a national census",
        "a football league statistics sheet", "weather station logs", "wildlife research observations",
        "school attendance registers", "an e-commerce customer database", "a transportation schedule",
        "airport passenger manifests", "library loan records", "restaurant menu listings", "festival attendee lists",
        "museum visitor logs", "gym membership data", "hotel booking records", "train ticket sales",
        "online gaming user stats", "social media user profiles", "university enrollment lists",
        "agricultural crop reports", "forest biodiversity surveys", "city traffic monitoring logs",
        "road accident reports", "space mission logs", "marine biology expedition data", "mining site reports",
        "energy consumption logs", "water quality monitoring", "factory production records",
        "school exam results", "sports tournament records", "job application data", "political election results",
        "blood donation center records", "medical prescription records", "child growth charts",
        "nutrition survey", "wildfire incident logs", "weather forecast archives", "ocean temperature logs",
        "market research reports", "real estate property listings", "film festival submissions",
        "art exhibition catalogues", "university research datasets", "postal delivery logs",
        "railway freight data", "volunteer registration lists"
    ]

    # Example value sets
    categorical_examples = [
        ["Red", "Blue", "Green", "Yellow"],
        ["Dog", "Cat", "Rabbit", "Parrot"],
        ["Toyota", "Ford", "BMW", "Tesla"],
        ["A", "B", "AB", "O"],
        ["Pop", "Rock", "Jazz", "Classical"],
        ["Asia", "Europe", "Africa", "America"],
        ["560001", "560002", "560003", "560004"],  # numeric-looking but categorical
        ["Male", "Female", "Other", "Female"],
        ["XL", "L", "M", "S"],
        ["101", "102", "103", "104"]  # jersey numbers
    ]

    quantitative_examples = [
        [150, 160, 170, 180],
        [2.3, 4.5, 6.1, 7.8],
        [45, 50, 55, 60],
        [1200, 1400, 1600, 1800],
        [1, 2, 3, 4],
        [100, 200, 300, 400],
        [10.5, 15.2, 13.8, 19.1],
        [5, 5, 5, 5]
    ]

    # =========================
    # TEMPLATES
    # =========================
    templates = [
        # Direct
        "Is the variable '<b>{var}</b>' in the context of <i>{context}</i> categorical or quantitative?",
        # Dataset
        "Given the dataset values <code>{data_snippet}</code> for the variable '<b>{var}</b>' in <i>{context}</i>, determine whether it is categorical or quantitative.",
        # Measurement method
        "A researcher records '<b>{var}</b>' by {measure_method}. Is this variable categorical or quantitative?",
        # Units
        "If '<b>{var}</b>' is recorded in <i>{unit}</i> for each entry in {context}, is it categorical or quantitative?",
        # Mixed trap
        "A survey asks for '<b>{var}</b>' and records the responses as <code>{data_snippet}</code>. Is this variable categorical or quantitative?",
        # Paired check
        "Between '<b>{var1}</b>' and '<b>{var2}</b>' in {context}, which is categorical and which is quantitative?",
        # Chart interpretation
        "Look at the bar chart of '<b>{var}</b>' in {context}. Is it categorical or quantitative?<br><pre class='chartjs'>{chart}</pre>",
        # Pie chart interpretation
        "Examine the pie chart of '<b>{var}</b>' in {context}. Is this variable categorical or quantitative?<br><pre class='chartjs'>{chart}</pre>",
        # Line chart interpretation
        "Below is a line chart of '<b>{var}</b>' in {context}. Is it categorical or quantitative?<br><pre class='chartjs'>{chart}</pre>",
        # Mermaid flow
        "The following decision flow is used to classify '<b>{var}</b>' in {context}. What is its type?<br><pre class='mermaid'>{mermaid}</pre>",
        # Description trap
        "In {context}, '<b>{var}</b>' is described as {description}. Is this variable categorical or quantitative?",
        # Random fact frame
        "Consider '<b>{var}</b>' collected in {context}. Based on its nature, is it categorical or quantitative?"
    ]

    measure_methods = [
        "measuring with a ruler", "timing with a stopwatch", "counting manually", "selecting from a drop-down list",
        "weighing on a scale", "choosing a color from a palette", "scanning a barcode", "recording GPS coordinates"
    ]

    units = ["cm", "kg", "USD", "minutes", "kilometers", "degrees Celsius", "genre", "color", "model name"]

    descriptions = [
        "a label chosen by the participant", "a number measured in meters", "an identifier assigned by the system",
        "a score based on test results", "a group name given by the observer"
    ]

    # =========================
    # RANDOM SELECTION
    # =========================
    tpl = random.choice(templates)
    is_cat = random.random() < 0.5
    var = random.choice(categorical_vars if is_cat else quantitative_vars)
    context = random.choice(contexts)
    correct_type = "Categorical" if is_cat else "Quantitative"
    values = random.choice(categorical_examples if is_cat else quantitative_examples)
    data_snippet = ", ".join(map(str, values))

    # Chart config if needed
    chart_config = {
        "type": "bar",
        "data": {"labels": [str(i) for i in range(1, len(values) + 1)], "datasets": [{"label": var, "data": values}]},
        "options": {"responsive": True}
    }
    if "pie" in tpl.lower():
        chart_config["type"] = "pie"
    elif "line" in tpl.lower():
        chart_config["type"] = "line"

    # Mermaid if needed
    mermaid_flow = f"graph TD; Start-->CheckType; CheckType{{Are values numeric?}} -->|Yes| Quantitative; CheckType -->|No| Categorical;"

    # Fill placeholders
    question_html = tpl.format(
        var=html.escape(var),
        context=html.escape(context),
        data_snippet=html.escape(data_snippet),
        measure_method=html.escape(random.choice(measure_methods)),
        unit=html.escape(random.choice(units)),
        var1=html.escape(random.choice(categorical_vars)),
        var2=html.escape(random.choice(quantitative_vars)),
        chart=html.escape(json.dumps(chart_config)),
        mermaid=html.escape(mermaid_flow),
        description=html.escape(random.choice(descriptions))
    )

    # =========================
    # OPTIONS
    # =========================
    options = ["Categorical", "Quantitative"]
    distractors = options.copy()
    distractors.remove(correct_type)
    option_list = [correct_type] + distractors * 3
    option_list = option_list[:4]
    random.shuffle(option_list)
    correct_index = option_list.index(correct_type)

    # =========================
    # EXPLANATION
    # =========================
    if is_cat:
        explanation = f"'{var}' groups data into categories or labels; arithmetic operations are not meaningful."
    else:
        explanation = f"'{var}' represents numerical measurements where arithmetic operations are meaningful."

    return {
        "question": question_html,
        "options": option_list,
        "correctAnswer": correct_index,
        "explanation": explanation
    }


def level_2() -> dict:
    """
    Returns a new randomly generated practice question dictionary:
    {
      "question": HTML string with all content and embedded visuals,
      "options": [HTML, HTML, HTML, HTML],
      "correctAnswer": int,  # index of correct option after shuffling
      "explanation": str     # brief rationale behind the correct answer
    }
    The generator mixes reasoning-heavy frames (slice-angle inference, missing counts,
    inconsistency detection, table↔chart matching, best-display selection, etc.)
    and produces one correct answer + three plausible distractors, shuffled.
    """
    # ----------------------------
    # Pools and configuration
    # ----------------------------
    rng = random.Random()
    rng.seed()  # system randomness

    # Contexts and variable pools (kept modest; combinatorics below show scaling)
    contexts = [
        "A classroom survey", "A market poll", "A town census", "An online poll",
        "A hospital intake record", "A customer feedback study", "A campus survey",
        "A botanical observation"
    ]

    # Primary category pools (some realistic, some from datasets)
    pool_manual = [
        ["Apple", "Banana", "Mango", "Orange"],
        ["Toyota", "Honda", "Ford", "BMW", "Tesla"],
        ["A", "B", "AB", "O"],
        ["Red", "Blue", "Green", "Yellow", "Purple"],
        ["Cat", "Dog", "Bird", "Fish"]
    ]

    # Add dataset-derived category sets (iris species, wine classes)
    iris = load_iris()
    iris_species = list(map(str, iris.target_names))
    wine = load_wine()
    wine_classes = list(map(str, wine.target_names))

    category_pools = pool_manual + [iris_species, wine_classes]

    # Chart styles we may embed (affects combinatorics)
    chart_styles = ["chartjs_pie", "chartjs_bar", "table_only", "mermaid_bar"]

    # Numerical selection spaces used only to compute TOTAL_POSSIBILITIES comment later
    angle_space = list(range(10, 351, 5))         # many possible angles (36 values)
    percentage_space = list(range(5, 96, 1))      # 5..95%
    sample_sizes = list(range(30, 2001, 10))      # many sample sizes

    # Frames (reasoning-oriented). Each returns tuple (html_question, correct_value, distractor_candidates, explanation)
    def _chartjs_block(config_obj):
        """Return HTML-escaped Chart.js JSON block inside a <pre class='chartjs'> so the UI can render it."""
        return "<pre class='chartjs'>{}</pre>".format(html.escape(json.dumps(config_obj)))

    def _mermaid_bar(labels, values, title):
        """Simple mermaid bar (bar charts not native to mermaid but we can use a simple sequence or table)."""
        # Use a simple markdown-like table for clarity, but placed in mermaid class to meet spec
        rows = "\n".join(f"{lbl}: {val}" for lbl, val in zip(labels, values))
        return "<pre class='mermaid'>{}</pre>".format(html.escape(f"{title}\n{rows}"))

    # Helper: build plausible numerical distractors for percent/angle/count
    def _numeric_distractors(correct, kind="percent"):
        # produce 3 plausible distractors based on common errors
        distractors = set()
        attempts = 0
        while len(distractors) < 3 and attempts < 30:
            attempts += 1
            if kind == "percent":
                # common mistakes: forget to multiply by 100, off-by-rounding, complement, nearest multiple of 5
                choice = None
                err_type = rng.choice(["off_round", "complement", "divide_by_10", "near5"])
                if err_type == "off_round":
                    # add/sub small amount
                    choice = round(correct + rng.choice([-4, -3, -2, 2, 3, 4]), 1)
                elif err_type == "complement":
                    choice = round(100 - correct + rng.choice([-2, 0, 2]), 1)
                elif err_type == "divide_by_10":
                    choice = round(correct / 10, 1)
                else:  # near5
                    choice = round(max(0.0, correct + rng.choice([-5, 5, 10, -10])), 1)
                if choice != correct and choice >= 0:
                    distractors.add(choice)
            elif kind == "angle":
                # mistakes mapping percent<->angle, rounding, or using 180 instead of 360
                choice = None
                err_type = rng.choice(["half_circle", "percent_as_angle", "off_by_30", "round"])
                if err_type == "half_circle":
                    choice = round(correct / 2, 1)
                elif err_type == "percent_as_angle":
                    # treat percent value as degrees
                    choice = round(correct % 360, 1)
                elif err_type == "off_by_30":
                    choice = round(correct + rng.choice([-30, 30]), 1)
                else:
                    choice = round(correct + rng.choice([-10, -5, 5, 10]), 1)
                if choice != correct and 0 <= choice <= 360:
                    distractors.add(choice)
            elif kind == "count":
                # plausible off-by errors in counts
                choice = None
                err_type = rng.choice(["off_by_small", "complement", "round_to_10"])
                if err_type == "off_by_small":
                    choice = int(max(0, correct + rng.choice([-5, -3, 3, 5])))
                elif err_type == "complement":
                    # complement relative to total if available (we'll not use if not provided)
                    choice = max(0, int(correct + rng.choice([10, -10])))
                else:
                    choice = int(round(correct / 10) * 10 + rng.choice([-10, 10]))
                if choice != correct and choice >= 0:
                    distractors.add(choice)
        # fallback if insufficient distractors
        while len(distractors) < 3:
            distractors.add(correct + rng.choice([1, 2, 3, -1, -2]) if isinstance(correct, int) else round(correct + rng.choice([1.0, -1.0]), 1))
        return list(distractors)

    # --- FRAME IMPLEMENTATIONS ---

    # Frame A: PIE SLICE ANGLE -> PERCENT (reasoning: convert angle to percent; distractors: complements, half-circle)
    def frame_angle_to_percent():
        categories = rng.choice(category_pools)
        # choose a category and an angle that's coherent with an integer-ish percent to reduce trivial edge cases
        # choose percent first from percentage_space then transform to angle (ensures sensible percent)
        percent = float(rng.choice([5,10,12,15,18,20,22,25,30,33,40,45,50,60]))  # varied set
        angle = round((percent / 100.0) * 360.0, 1)
        cat = rng.choice(categories)
        ctx = rng.choice(contexts)
        q_html = (
            f"<p>{html.escape(ctx)} recorded a pie chart of <b>{html.escape(', '.join(categories))}</b>.</p>"
            f"<p>The slice corresponding to <b>{html.escape(cat)}</b> measures <b>{angle}°</b>. "
            f"What percentage of the total does this slice represent? Show the best choice.</p>"
            f"<pre class='chartjs'>{html.escape(json.dumps({'type':'pie','data':{'labels':categories,'datasets':[{'data':[1]*len(categories)}]}}))}</pre>"
        )
        correct = round((angle / 360.0) * 100.0, 1)
        distracts = _numeric_distractors(correct, kind="percent")
        options_vals = [correct] + distracts
        # format as HTML options (percent sign)
        options_html = [f"<div class='option'>{v}%</div>" for v in options_vals]
        rng.shuffle(options_html)
        correct_index = options_html.index(f"<div class='option'>{correct}%</div>")
        explanation = f"Percent = (angle / 360) × 100 = ({angle} / 360) × 100 = {correct}%."
        return q_html, options_html, correct_index, explanation

    # Frame B: PERCENT -> SLICE ANGLE (reasoning: convert percent to degrees)
    def frame_percent_to_angle():
        categories = rng.choice(category_pools)
        percent = float(rng.choice([5,8,10,12,15,18,20,25,30,33,40,45]))
        cat = rng.choice(categories)
        ctx = rng.choice(contexts)
        q_html = (
            f"<p>{html.escape(ctx)}: <b>{html.escape(cat)}</b> accounts for <b>{percent}%</b> of responses.</p>"
            f"<p>If shown as a pie chart, what would be the angle (in degrees) of this slice?</p>"
        )
        correct = round((percent / 100.0) * 360.0, 1)
        distracts = _numeric_distractors(correct, kind="angle")
        options_vals = [correct] + distracts
        options_html = [f"<div class='option'>{v}°</div>" for v in options_vals]
        rng.shuffle(options_html)
        correct_index = options_html.index(f"<div class='option'>{correct}°</div>")
        explanation = f"Angle = (percent / 100) × 360 = ({percent}/100)×360 = {correct}°."
        return q_html, options_html, correct_index, explanation

    # Frame C: IDENTIFY CATEGORY FROM ANGLE (given pie config, one label hidden — reasoning about relative size)
    def frame_identify_category_from_angle():
        categories = list(rng.choice(category_pools))
        # generate realistic counts
        counts = [rng.randint(5, 80) for _ in categories]
        total = sum(counts)
        angles = [round((c / total) * 360.0, 1) for c in counts]
        target_idx = rng.randrange(len(categories))
        target_angle = angles[target_idx]
        # build a Chart.js-like block that hides that label (we'll replace label with X(angle))
        labels_with_hidden = categories.copy()
        labels_with_hidden[target_idx] = f"Category X ({target_angle}°)"
        chart_config = {"type":"pie","data":{"labels":labels_with_hidden,"datasets":[{"data":counts}]}}
        q_html = (
            f"<p>{html.escape(rng.choice(contexts))} produced the pie chart below for <b>{html.escape(', '.join(categories))}</b>.</p>"
            f"{_chartjs_block(chart_config)}"
            f"<p>Which actual category corresponds to the <b>{target_angle}°</b> slice labeled 'Category X'?</p>"
        )
        correct = categories[target_idx]
        distracts = rng.sample([c for c in categories if c != correct], k=min(3, max(1, len(categories)-1)))
        # if fewer than 3 distractors (very small category sets), create plausible extra names
        while len(distracts) < 3:
            distracts.append(rng.choice(["Other", "Unknown", "Misc"]))
        options_vals = [correct] + distracts
        rng.shuffle(options_vals)
        options_html = [f"<div class='option'>{html.escape(opt)}</div>" for opt in options_vals]
        correct_index = options_html.index(f"<div class='option'>{html.escape(correct)}</div>")
        explanation = (
            f"The {target_angle}° slice equals {(counts[target_idx]/total)*100:.1f}% of total (counts: {counts[target_idx]}/{total}), "
            f"which matches category '{correct}'."
        )
        return q_html, options_html, correct_index, explanation

    # Frame D: MISSING COUNT FROM TOTAL & TABLE (reasoning: infer missing count)
    def frame_missing_count():
        categories = list(rng.choice(category_pools))
        # produce counts and then hide one
        counts = [rng.randint(5, 80) for _ in categories]
        total = sum(counts)
        missing_idx = rng.randrange(len(categories))
        given = [c if i != missing_idx else None for i, c in enumerate(counts)]
        # build HTML table
        rows_html = "".join(f"<tr><td>{html.escape(cat)}</td><td>{(val if val is not None else '?')}</td></tr>" for cat, val in zip(categories, given))
        q_html = (
            f"<p>{html.escape(rng.choice(contexts))} recorded these counts (one missing) for <b>{html.escape(', '.join(categories))}</b>:</p>"
            f"<table border='1' cellpadding='4'><tr><th>Category</th><th>Count</th></tr>{rows_html}</table>"
            f"<p>If the total number of responses is <b>{total}</b>, what is the missing count?</p>"
        )
        correct = counts[missing_idx]
        distracts = _numeric_distractors(correct, kind="count")
        options_vals = [correct] + distracts
        options_html = [f"<div class='option'>{v}</div>" for v in options_vals]
        rng.shuffle(options_html)
        correct_index = options_html.index(f"<div class='option'>{correct}</div>")
        explanation = f"Missing = total {total} − sum(known counts) = {correct}."
        return q_html, options_html, correct_index, explanation

    # Frame E: DETECT INCONSISTENT PERCENTAGE (reasoning: check percentages vs counts)
    def frame_detect_inconsistent_percentage():
        categories = list(rng.choice(category_pools))
        counts = [rng.randint(5, 80) for _ in categories]
        total = sum(counts)
        # compute true percentages and then introduce one erroneous reported percentage
        true_pcts = [round((c / total) * 100.0, 1) for c in counts]
        reported = true_pcts.copy()
        wrong_idx = rng.randrange(len(categories))
        # introduce error: off by +/− random 3..10
        reported[wrong_idx] = round(max(0.0, reported[wrong_idx] + rng.choice([-10, -7, -5, 5, 7, 10])), 1)
        # build HTML with chart and list
        chart_config = {"type":"pie","data":{"labels":categories,"datasets":[{"data":counts}]}}
        pct_list_html = "".join(f"<li>{html.escape(cat)}: {p}%</li>" for cat, p in zip(categories, reported))
        q_html = (
            f"{_chartjs_block(chart_config)}"
            f"<p>Below are reported percentages for the categories shown in the chart:</p><ul>{pct_list_html}</ul>"
            f"<p>Which category has a reported percentage that does <b>not</b> match the chart's counts?</p>"
        )
        correct = categories[wrong_idx]
        distracts = rng.sample([c for c in categories if c != correct], k=min(3, max(1, len(categories)-1)))
        while len(distracts) < 3:
            distracts.append("Other")
        options_vals = [correct] + distracts
        rng.shuffle(options_vals)
        options_html = [f"<div class='option'>{html.escape(v)}</div>" for v in options_vals]
        correct_index = options_html.index(f"<div class='option'>{html.escape(correct)}</div>")
        explanation = (
            f"Calculate true% = (count/total)×100 for each category and compare to reported. "
            f"The reported percentage for '{correct}' differs from its computed proportion."
        )
        return q_html, options_html, correct_index, explanation

    # Frame F: BEST DISPLAY CHOICE (reasoning: pick best chart type for the task)
    def frame_best_display():
        # variable could be categorical or quantitative; we'll choose mostly categorical to keep scope
        variable = rng.choice([
            ("favorite fruit", "categorical"),
            ("age of respondents", "quantitative"),
            ("blood type", "categorical"),
            ("monthly income", "quantitative"),
            ("preferred transport", "categorical")
        ])
        var_name, var_type = variable
        goal = rng.choice([
            "compare exact counts across categories",
            "show relative proportions of a whole",
            "show distribution shape and spread",
            "highlight a dominant category"
        ])
        # mapping sensible best answers
        if goal == "compare exact counts across categories":
            best = "bar chart"
        elif goal == "show relative proportions of a whole":
            best = "pie chart" if var_type == "categorical" else "stacked bar"
        elif goal == "show distribution shape and spread":
            best = "histogram"
        else:
            best = "emphasized (exploded) pie chart"
        distractors_pool = ["bar chart", "pie chart", "histogram", "scatter plot", "stacked bar", "table"]
        distractors = [d for d in rng.sample(distractors_pool, k=4) if d != best][:3]
        options_vals = [best] + distractors
        rng.shuffle(options_vals)
        options_html = [f"<div class='option'>{html.escape(v)}</div>" for v in options_vals]
        correct_index = options_html.index(f"<div class='option'>{html.escape(best)}</div>")
        q_html = (
            f"<p>For the variable <b>{html.escape(var_name)}</b>, which display is most appropriate if the goal is to <b>{html.escape(goal)}</b>?</p>"
        )
        explanation = f"For the stated goal, a '{best}' best communicates the intended information (readability and precision reasons)."
        return q_html, options_html, correct_index, explanation

    # Frame G: TABLE → PIE ANGLES (compute all angles; ask which angle corresponds to a given category)
    def frame_table_to_angles():
        categories = list(rng.choice(category_pools))
        counts = [rng.randint(5, 120) for _ in categories]
        total = sum(counts)
        angles = [round((c / total) * 360.0, 1) for c in counts]
        idx = rng.randrange(len(categories))
        cat = categories[idx]
        angle = angles[idx]
        table_html = "<table border='1' cellpadding='4'><tr><th>Category</th><th>Count</th></tr>" + "".join(
            f"<tr><td>{html.escape(c)}</td><td>{n}</td></tr>" for c, n in zip(categories, counts)
        ) + "</table>"
        q_html = (
            f"<p>{html.escape(rng.choice(contexts))} recorded the following frequency table for <b>{html.escape(', '.join(categories))}</b>:</p>"
            f"{table_html}"
            f"<p>If the data are shown as a pie chart, what is the slice angle (in degrees) for <b>{html.escape(cat)}</b>?</p>"
        )
        correct = angle
        distracts = _numeric_distractors(correct, kind="angle")
        options_vals = [correct] + distracts
        options_html = [f"<div class='option'>{v}°</div>" for v in options_vals]
        rng.shuffle(options_html)
        correct_index = options_html.index(f"<div class='option'>{correct}°</div>")
        explanation = f"Angle = (count / total) × 360 = ({counts[idx]}/{total})×360 = {correct}°."
        return q_html, options_html, correct_index, explanation

    # Collect frame functions in list to pick randomly (mix of old + new)
    frame_funcs = [
        frame_angle_to_percent,
        frame_percent_to_angle,
        frame_identify_category_from_angle,
        frame_missing_count,
        frame_detect_inconsistent_percentage,
        frame_best_display,
        frame_table_to_angles
    ]

    # Choose a random frame and build question
    frame = rng.choice(frame_funcs)
    q_html, options_html, correct_index, explanation = frame()

    # Ensure options are 4 elements: if fewer, pad with plausible distractors; if more, cut to 4
    if len(options_html) < 4:
        filler_pool = ["None of these", "All of the above", "Approximately 0", "Approximately 100"]
        while len(options_html) < 4:
            candidate = rng.choice(filler_pool)
            if candidate not in options_html:
                options_html.append(f"<div class='option'>{html.escape(candidate)}</div>")
    elif len(options_html) > 4:
        options_html = options_html[:4]
        if correct_index >= 4:
            # fallback: pick 0
            correct_index = 0

    return {
        "question": q_html,
        "options": options_html,
        "correctAnswer": int(correct_index),
        "explanation": explanation
    }

# Preload some sklearn datasets to sample from (safe, lightweight)
_SKLEARN_DATASETS = {
    "Iris sepal length (cm)": datasets.load_iris().data[:, 0].tolist(),
    "Iris sepal width (cm)": datasets.load_iris().data[:, 1].tolist(),
    "Wine alcohol (%)": datasets.load_wine().data[:, 0].tolist(),
    "Diabetes BMI": datasets.load_diabetes().data[:, 2].tolist(),
    "Diabetes blood pressure": datasets.load_diabetes().data[:, 3].tolist(),
    "Wine color intensity": datasets.load_wine().data[:, 9].tolist(),
}

# Small pools for textual variable names to increase combinatorics
_TEXT_POOLS = {
    "context": [
        "student exam scores (out of 100)",
        "daily step counts",
        "heights (cm)",
        "weights (kg)",
        "reaction times (ms)",
        "monthly sales ($k)"
    ],
    "chart_types": ["dotplot", "histogram", "stemplot", "boxplot"],
    "skew_labels": ["left-skewed (negative skew)", "approximately symmetric", "right-skewed (positive skew)", "bimodal/unclear"],
}

def _sample_dataset():
    """Pick a dataset name and return a small random sample (list of numbers)."""
    name = random.choice(list(_SKLEARN_DATASETS.keys()))
    full = _SKLEARN_DATASETS[name]
    # sample without replacement to produce varied small samples
    n = random.randint(14, 30)
    if n >= len(full):
        sample = full[:]
    else:
        sample = random.sample(full, n)
    # convert to rounded numeric values for many displays (keeps realism)
    # choose rounding scheme
    round_to = random.choice([0, 0, 1])  # bias toward integers, sometimes 1 decimal
    if round_to == 0:
        sample = [int(round(x)) for x in sample]
    else:
        sample = [round(float(x), 1) for x in sample]
    return name, sample

def _make_chartjs_config(chart_kind, sample):
    """Return a Chart.js-like JSON config (as dict) for embedding."""
    if chart_kind == "dotplot":
        # use scatter plot with y = 1 and jitter for visualization
        data = [{"x": float(x), "y": 1 + random.uniform(-0.12, 0.12)} for x in sample]
        config = {
            "type": "scatter",
            "data": {"datasets": [{"label": "Dotplot (jittered)", "data": data, "pointRadius": 6}]},
            "options": {"scales": {"x": {"title": {"display": True, "text": "Value"}}, "y": {"display": False}}}
        }
    elif chart_kind == "histogram":
        # create bins (use 6 bins by default)
        bins = 6
        mn = min(sample); mx = max(sample)
        if mn == mx:
            mx = mn + 1
        bin_width = (mx - mn) / bins
        bin_edges = [mn + i * bin_width for i in range(bins + 1)]
        counts = [0] * bins
        for v in sample:
            # find bin index
            if v == mx:
                idx = bins - 1
            else:
                idx = int((v - mn) / bin_width)
                idx = max(0, min(bins - 1, idx))
            counts[idx] += 1
        labels = [f"{round(bin_edges[i],1)}–{round(bin_edges[i+1],1)}" for i in range(bins)]
        config = {
            "type": "bar",
            "data": {"labels": labels, "datasets": [{"label": "Histogram counts", "data": counts}]},
            "options": {"scales": {"x": {"title": {"display": True, "text": "Bins"}}, "y": {"title": {"display": True, "text": "Count"}}}}
        }
    elif chart_kind == "boxplot":
        # Boxplot config: we will supply the raw data in a dataset entry
        config = {
            "type": "boxplot",
            "data": {"labels": ["Sample"], "datasets": [{"label": "Boxplot", "data": [sample]}]},
            "options": {"plugins": {"legend": {"display": False}}}
        }
        print(config)
    elif chart_kind == "stemplot":
        # For stem-and-leaf we will not rely on Chart.js; produce a textual stem/leaf mapping
        # but still return a config-like dict so we have something to embed
        # Build stem-leaf
        # choose stem divisor (10 or 1) depending on magnitudes
        span = max(sample) - min(sample) if sample else 1
        divisor = 10 if span >= 10 else 1
        stems = {}
        for v in sample:
            stem = int(v) // divisor
            leaf = int(abs(v) % divisor)
            stems.setdefault(stem, []).append(leaf)
        stems_sorted = {str(k): sorted(v) for k, v in sorted(stems.items())}
        config = {"type": "stemplot-text", "stemplot": stems_sorted}
    else:
        config = {"type": "unknown", "data": sample}
    return config

def _html_escape_json(obj):
    """Dump to JSON and HTML-escape for safe embedding."""
    return html.escape(json.dumps(obj, separators=(",", ":"), default=str))

def level_3() -> dict:
    """
    Returns:
    {
      "question": HTML string with all content and embedded visuals,
      "options": [HTML, HTML, HTML, HTML],
      "correctAnswer": int,
      "explanation": str
    }
    """
    # --- Create template frames (at least 6) ---
    frames = []

    # Frame A: Dotplot — count of a particular value
    def frame_dot_count():
        dataset_name, sample = _sample_dataset()
        # Use integer values to count easily; ensure at least one repeated
        values = sample[:]
        # ensure some duplicates by sampling some value twice
        v = random.choice(values)
        # build dotplot config
        config = _make_chartjs_config("dotplot", values)
        # target value chosen from sample
        target = random.choice(values)
        count = values.count(target)
        correct = str(count)
        # distractors: count +/-1 and swapped other value count
        distracts = []
        distracts.append(str(max(0, count - 1)))
        distracts.append(str(count + 1))
        # pick another value's count
        other = random.choice([x for x in values if x != target] or values)
        distracts.append(str(values.count(other)))
        # Build HTML
        q_html = (
            f"<p>Dotplot showing a sample of <b>{html.escape(dataset_name)}</b> (values shown on x-axis). "
            f"In this sample, how many observations equal <b>{target}</b>?</p>"
            f"<pre class='chartjs'>{_html_escape_json(config)}</pre>"
        )
        options = [correct] + distracts
        explanation = f"The dotplot data (raw sample) contains {count} occurrences of {target} — count them to confirm."
        return q_html, options, correct, explanation

    frames.append(frame_dot_count)

    # Frame B: Histogram — proportion in a bin
    def frame_hist_bin_proportion():
        dataset_name, sample = _sample_dataset()
        config = _make_chartjs_config("histogram", sample)
        # extract bins and counts from config
        labels = config["data"]["labels"]
        counts = config["data"]["datasets"][0]["data"]
        total = sum(counts)
        # pick a random bin index
        idx = random.randrange(len(counts))
        bin_label = labels[idx]
        count_in_bin = counts[idx]
        proportion = count_in_bin / total
        # prepare answers: proportion as percentage approx
        correct_pct = round(proportion * 100, 1)
        # distractors: off by ± a few percent, or swap with adjacent bin
        distracts = []
        distracts.append(round(max(0, correct_pct - random.uniform(3, 10)), 1))
        distracts.append(round(min(100, correct_pct + random.uniform(3, 10)), 1))
        # adjacent bin swap if exists
        adj_idx = idx + (1 if idx < len(counts) - 1 else -1)
        distracts.append(round(counts[adj_idx] / total * 100, 1))
        q_html = (
            f"<p>Histogram of a sample of <b>{html.escape(dataset_name)}</b> (bins labeled). "
            f"Approximately what percentage of observations fall into the bin <b>{html.escape(bin_label)}</b>?</p>"
            f"<pre class='chartjs'>{_html_escape_json(config)}</pre>"
        )
        options = [f"{p}%" for p in ([correct_pct] + distracts)]
        explanation = (
            f"Count in bin = {count_in_bin}; total = {total}. Percentage = 100×({count_in_bin}/{total}) = {correct_pct}% (rounded)."
        )
        return q_html, options, f"{correct_pct}%", explanation

    frames.append(frame_hist_bin_proportion)

    # Frame C: Boxplot — IQR question
    def frame_boxplot_iqr():
        dataset_name, sample = _sample_dataset()
        # compute quartiles using statistics.quantiles
        try:
            q1, q2, q3 = statistics.quantiles(sorted(sample), n=4)
        except Exception:
            # fallback compute by medians
            s = sorted(sample)
            q2 = statistics.median(s)
            half = len(s) // 2
            lower = s[:half]
            upper = s[-half:]
            q1 = statistics.median(lower)
            q3 = statistics.median(upper)
        iqr = round(q3 - q1, 1 if isinstance(q3, float) else 0)
        config = _make_chartjs_config("boxplot", sample)
        # create distractors: swap Q3-Q2 etc
        distracts = []
        distracts.append(round((q2 - q1), 1))
        distracts.append(round((q3 - q2), 1))
        distracts.append(round(iqr + random.choice([-2, -1, 1, 2]), 1))
        q_html = (
            f"<p>Boxplot created from a sample of <b>{html.escape(dataset_name)}</b>. "
            f"What is the <b>IQR (interquartile range)</b> for this sample?</p>"
            f"<pre class='chartjs'>{_html_escape_json(config)}</pre>"
        )
        # ensure strings with units consistent
        options = [str(i) for i in [iqr] + distracts]
        explanation = (
            f"IQR = Q3 − Q1. Using the sample's quartiles Q1={round(q1,1)}, Q3={round(q3,1)}, "
            f"so IQR = {round(q3 - q1,1)}."
        )
        return q_html, options, str(iqr), explanation

    frames.append(frame_boxplot_iqr)

    # Frame D: Stemplot — reading a stem/leaf
    def frame_stemplot_read():
        dataset_name, sample = _sample_dataset()
        # choose divisor based on span
        span = max(sample) - min(sample)
        divisor = 10 if span >= 10 else 1
        # build stem-leaf textual representation
        stems = {}
        for v in sample:
            stem = int(v) // divisor
            leaf = int(abs(v) % divisor)
            stems.setdefault(stem, []).append(leaf)
        # pick a stem randomly from available stems
        chosen_stem = random.choice(list(stems.keys()))
        leaves = sorted(stems[chosen_stem])
        # target ask: which leaves correspond to stem X ?
        correct_leaves = ",".join(str(l) for l in leaves)
        # distractors: jumbled, missing one, or off-by-one leaves
        distracts = []
        if len(leaves) >= 2:
            distracts.append(",".join(str(l) for l in leaves[:-1]))  # missing last
        else:
            distracts.append(",".join(str((l + 1) % 10) for l in leaves))
        distracts.append(",".join(str((l + random.choice([-1,1])) % 10) for l in leaves))
        # another stem's leaves
        other_stem = random.choice([s for s in stems.keys() if s != chosen_stem] or [chosen_stem])
        distracts.append(",".join(str(l) for l in sorted(stems[other_stem])))
        # Build a simple stemplot textual visual embedded as a mermaid-looking block (or pre)
        stemplot_text_lines = []
        for s, ls in sorted(stems.items()):
            stemplot_text_lines.append(f"{s} | {' '.join(str(x) for x in sorted(ls))}")
        stemplot_text = "\n".join(stemplot_text_lines)
        config = {"type": "stemplot-text", "text": stemplot_text}
        q_html = (
            f"<p>Stemplot of a sample from <b>{html.escape(dataset_name)}</b> (stem | leaves). "
            f"For the stem <b>{chosen_stem}</b>, which list of leaves is correct?</p>"
            f"<pre class='mermaid'>{html.escape(stemplot_text)}</pre>"
        )
        options = [correct_leaves] + distracts
        explanation = (
            f"The stemplot row for stem {chosen_stem} shows leaves: {correct_leaves}. "
            "Read the 'stem | leaves' row to confirm."
        )
        return q_html, options, correct_leaves, explanation

    frames.append(frame_stemplot_read)

    # Frame E: Shape/skewness from histogram or summary
    def frame_skewness_identify():
        dataset_name, sample = _sample_dataset()
        s_sorted = sorted(sample)
        mean_v = statistics.mean(sample)
        median_v = statistics.median(s_sorted)
        # approximate skew determination
        diff = mean_v - median_v
        if abs(diff) < 0.05 * (max(sample) - min(sample) or 1):
            skew = _TEXT_POOLS["skew_labels"][1]  # approx symmetric
        elif diff > 0:
            skew = _TEXT_POOLS["skew_labels"][2]  # right skew
        else:
            skew = _TEXT_POOLS["skew_labels"][0]  # left skew
        # make plausible distractors (other labels)
        distracts = [lab for lab in _TEXT_POOLS["skew_labels"] if lab != skew]
        random.shuffle(distracts)
        config = _make_chartjs_config("histogram", sample)
        q_html = (
            f"<p>Examine the histogram below for a sample of <b>{html.escape(dataset_name)}</b>. "
            f"Which description best matches the distribution's skewness?</p>"
            f"<pre class='chartjs'>{_html_escape_json(config)}</pre>"
        )
        options = [skew] + distracts[:3]
        explanation = (
            f"Mean = {round(mean_v,2)}, median = {round(median_v,2)}. Mean > median indicates a right (positive) skew; "
            "Mean ≈ median indicates symmetry; mean < median indicates left skew."
        )
        return q_html, options, skew, explanation

    frames.append(frame_skewness_identify)

    # Frame F: Which chart best represents dataset (data-to-chart)
    def frame_best_chart_type():
        # create small synthetic description from a sampled dataset
        dataset_name, sample = _sample_dataset()
        # compute nature: many repeated exact values? if many duplicates -> dotplot/stemplot
        uniques = len(set(sample))
        n = len(sample)
        if uniques <= n * 0.35:
            best = "dotplot"
        elif (max(sample) - min(sample)) > 20:
            best = "histogram"
        else:
            best = random.choice(["stemplot", "boxplot"])
        distracts = [c for c in _TEXT_POOLS["chart_types"] if c != best]
        random.shuffle(distracts)
        # Short textual mini-data summary
        summary = f"n={n}, min={min(sample)}, max={max(sample)}, unique={uniques}"
        q_html = (
            f"<p>Given a small sample described as <b>{html.escape(summary)}</b> from <b>{html.escape(dataset_name)}</b>, "
            "which display would best show the exact individual values while also revealing repeated observations?</p>"
        )
        # correct is best (e.g., dotplot or stemplot)
        options = [best] + distracts[:3]
        explanation = (
            f"A dotplot (or stemplot) shows each individual observation (and repeats) clearly. "
            f"Options like histogram group data into bins so they hide exact repeated values."
        )
        return q_html, options, best, explanation

    frames.append(frame_best_chart_type)

    # Frame G: Read approximate median from dotplot/boxplot
    def frame_median_from_dotplot_box():
        dataset_name, sample = _sample_dataset()
        sample_sorted = sorted(sample)
        median_val = statistics.median(sample_sorted)
        # choose representation: sometimes dotplot, sometimes boxplot
        rep = random.choice(["dotplot", "boxplot"])
        config = _make_chartjs_config(rep, sample)
        # distractors: nearby values
        distracts = [median_val + random.choice([-2, -1, 1, 2]), median_val + random.choice([3, -3]), random.choice(sample_sorted)]
        # ensure numeric strings
        opts = [str(round(median_val, 1) if isinstance(median_val, float) else str(median_val))] + [str(round(float(x),1)) for x in distracts[:3]]
        q_html = (
            f"<p>Using the {rep} below for <b>{html.escape(dataset_name)}</b>, what is the sample median (approx)?</p>"
            f"<pre class='chartjs'>{_html_escape_json(config)}</pre>"
        )
        explanation = f"The median is the middle observation; computed from sorted data it is {median_val}."
        return q_html, opts, str(median_val), explanation

    frames.append(frame_median_from_dotplot_box)

    # --- Randomly choose one frame and produce question ---
    frame_fn = random.choice(frames)
    q_html, options_raw, correct_raw, explanation = frame_fn()

    # Normalize options into HTML strings (escape)
    options_html = [f"<div class='mc-option'>{html.escape(str(opt))}</div>" for opt in options_raw]

    # Shuffle options and find correctAnswer index
    indexed = list(enumerate(options_html))
    # preserve mapping between displayed option string and raw answer to compare
    option_texts = [opt for opt in options_raw]  # parallel list
    combined = list(zip(option_texts, options_html))
    random.shuffle(combined)
    shuffled_texts, shuffled_htmls = zip(*combined)
    # find index where shuffled_text equals correct_raw (string equality)
    try:
        correct_index = shuffled_texts.index(str(correct_raw))
    except ValueError:
        # fallback: attempt numeric approximate match
        correct_index = 0

    # Build final HTML question including instruction to pick one option
    full_question_html = (
        f"{q_html}"
        "<p><em>Select the best answer from the options below.</em></p>"
    )

    # Return the structure
    return {
        "question": full_question_html,
        "options": list(shuffled_htmls),
        "correctAnswer": int(correct_index),
        "explanation": explanation
    }


def level_4() -> dict:
    """
    Returns:
    {
      "question": HTML string with all content and embedded visuals,
      "options": [HTML, HTML, HTML, HTML],
      "correctAnswer": int,
      "explanation": str
    }
    """
    # ----------------------------
    # Data pools for placeholders
    # ----------------------------
    categories = ["Test scores", "Heights", "Weights", "Daily temperatures", "Sales figures", "Exam marks"]
    units = {"Test scores": "points", "Heights": "cm", "Weights": "kg",
             "Daily temperatures": "°C", "Sales figures": "USD", "Exam marks": "marks"}

    
    # --------------------------------
    # Helper generators for each frame
    # --------------------------------

    def mean_from_list(category, units):
        data = [random.randint(10, 100) for _ in range(random.randint(5, 8))]
        mean_val = round(statistics.mean(data), 2)
        # distractors: off-by-one, median, wrong rounding
        median_val = round(statistics.median(data), 2)
        wrong1 = round(mean_val + random.choice([-2, 2]), 2)
        wrong2 = round(statistics.mean(data[:-1]), 2)
        options = [mean_val, median_val, wrong1, wrong2]
        random.shuffle(options)
        correct_idx = options.index(mean_val)
        q_html = f"""
        <p>Given the following {category.lower()} data (in {units[category]}):</p>
        <p>{data}</p>
        <p>What is the <b>mean</b> of the dataset?</p>
        """
        expl = f"The mean is the sum of the data divided by the number of values: {sum(data)}/{len(data)} = {mean_val}."
        return {"question": q_html, "options": [str(o) for o in options], "correctAnswer": correct_idx, "explanation": expl}

    def median_from_list(category, units):
        data = [random.randint(10, 100) for _ in range(random.randint(5, 9))]
        median_val = round(statistics.median(data), 2)
        mean_val = round(statistics.mean(data), 2)
        wrong1 = median_val + random.choice([-3, 3])
        wrong2 = mean_val
        options = [median_val, wrong1, wrong2, median_val + 5]
        random.shuffle(options)
        correct_idx = options.index(median_val)
        q_html = f"""
        <p>Here are the {category.lower()} data values (in {units[category]}):</p>
        <p>{data}</p>
        <p>What is the <b>median</b> value?</p>
        """
        expl = f"Sort the data and take the middle value(s). The median is {median_val}."
        return {"question": q_html, "options": [str(o) for o in options], "correctAnswer": correct_idx, "explanation": expl}

    def mode_from_list(category, units):
        values = [random.randint(1, 10) for _ in range(8)]
        values[random.randint(0, 7)] = values[0]  # ensure at least one duplicate
        try:
            mode_val = statistics.mode(values)
        except statistics.StatisticsError:
            mode_val = values[0]
        wrong1 = mode_val + 1
        wrong2 = mode_val - 1 if mode_val > 1 else mode_val + 2
        wrong3 = statistics.median(values)
        options = [mode_val, wrong1, wrong2, wrong3]
        random.shuffle(options)
        correct_idx = options.index(mode_val)
        q_html = f"""
        <p>Below are {category.lower()} values (in {units[category]}):</p>
        <p>{values}</p>
        <p>What is the <b>mode</b> of the dataset?</p>
        """
        expl = f"The mode is the most frequent value, which here is {mode_val}."
        return {"question": q_html, "options": [str(o) for o in options], "correctAnswer": correct_idx, "explanation": expl}

    def measure_from_chart(category, units):
        labels = [f"Group {i}" for i in range(1, 5)]
        values = [random.randint(40, 90) for _ in labels]
        measure_type = random.choice(["mean", "median", "mode"])
        if measure_type == "mean":
            correct_val = round(statistics.mean(values), 2)
            expl = f"Mean = {sum(values)}/{len(values)} = {correct_val}"
        elif measure_type == "median":
            correct_val = round(statistics.median(values), 2)
            expl = f"Sorted values → middle → {correct_val}"
        else:  # mode
            try:
                correct_val = statistics.mode(values)
            except statistics.StatisticsError:
                correct_val = values[0]
            expl = f"Mode = most frequent value → {correct_val}"
        distractors = {correct_val + 5, correct_val - 5, round(statistics.mean(values), 2), round(statistics.median(values), 2)}
        distractors.discard(correct_val)
        options = list(distractors)[:3] + [correct_val]
        random.shuffle(options)
        chart_config = {
            "type": "bar",
            "data": {"labels": labels, "datasets": [{"label": category, "data": values}]}
        }
        return {
            "question": f"<p>Bar chart of {category.lower()} (in {units[category]}):</p>"
                        f"<pre class='chartjs'>{html.escape(json.dumps(chart_config))}</pre>"
                        f"<p>Find the <b>{measure_type}</b> of the values.</p>",
            "options": [str(o) for o in options],
            "correctAnswer": options.index(correct_val),
            "explanation": expl
        }

    def compare_three_measures(category, units):
        data = [random.randint(50, 100) for _ in range(7)]
        mean_val = round(statistics.mean(data), 2)
        median_val = round(statistics.median(data), 2)
        try:
            mode_val = statistics.mode(data)
        except statistics.StatisticsError:
            mode_val = data[0]
        statements = [
            f"Mean > Median > Mode",
            f"Median > Mean > Mode",
            f"Mode > Median > Mean",
            "All are equal"
        ]
        # Find truth
        order = sorted([("Mean", mean_val), ("Median", median_val), ("Mode", mode_val)], key=lambda x: x[1], reverse=True)
        correct_statement = " > ".join(name for name, _ in order) if len(set([mean_val, median_val, mode_val])) == 3 else "All are equal"
        random.shuffle(statements)
        return {
            "question": f"<p>{category} data: {data} ({units[category]})</p><p>Which ordering is correct?</p>",
            "options": statements,
            "correctAnswer": statements.index(correct_statement),
            "explanation": f"Mean={mean_val}, Median={median_val}, Mode={mode_val} → {correct_statement}"
        }

    def missing_value_from_mean(category, units):
        full_data = [random.randint(20, 80) for _ in range(5)]
        missing_index = random.randint(0, 4)
        target_mean = round(statistics.mean(full_data), 2)
        known_data = full_data[:]
        known_data[missing_index] = "x"
        total_sum = target_mean * 5
        missing_val = int(total_sum - sum(v for v in full_data if isinstance(v, int)))
        options = [missing_val, missing_val + 2, missing_val - 2, missing_val + 5]
        random.shuffle(options)
        return {
            "question": f"<p>Data ({units[category]}): {known_data}</p>"
                        f"<p>The mean is {target_mean}. Find x.</p>",
            "options": [str(o) for o in options],
            "correctAnswer": options.index(missing_val),
            "explanation": f"Mean × n = sum → {target_mean} × 5 = {total_sum}, missing = {missing_val}"
        }

    def missing_value_from_median(category, units):
        data = sorted([random.randint(10, 50) for _ in range(5)])
        mid_index = len(data) // 2
        target_median = data[mid_index]
        missing_index = random.choice([0, len(data) - 1])
        orig_value = data[missing_index]
        data[missing_index] = "x"
        missing_val = orig_value
        options = [missing_val, missing_val + 3, missing_val - 3, missing_val + 5]
        random.shuffle(options)
        return {
            "question": f"<p>Data ({units[category]}): {data}</p>"
                        f"<p>The median is {target_median}. Find x.</p>",
            "options": [str(o) for o in options],
            "correctAnswer": options.index(missing_val),
            "explanation": f"Median unaffected by ends → x = {missing_val}"
        }

    def missing_value_from_mode(category, units):
        mode_val = random.randint(10, 30)
        others = [random.randint(5, 35) for _ in range(4)]
        data = [mode_val, mode_val] + others
        missing_index = random.randint(0, 5)
        if missing_index >= len(data):
            data.append("x")
            missing_val = mode_val
        else:
            orig_value = data[missing_index]
            data[missing_index] = "x"
            missing_val = orig_value
        options = [missing_val, mode_val + 1, mode_val - 1, random.choice(others)]
        random.shuffle(options)
        return {
            "question": f"<p>Data ({units[category]}): {data}</p>"
                        f"<p>The mode is {mode_val}. Find x.</p>",
            "options": [str(o) for o in options],
            "correctAnswer": options.index(missing_val),
            "explanation": f"Mode = most frequent value ({mode_val}), so x must be {missing_val}"
        }

    # ----------------------------
    # Question Frames
    # ----------------------------
    frames = [
        lambda: mean_from_list(random.choice(categories), units),
        lambda: median_from_list(random.choice(categories), units),
        lambda: mode_from_list(random.choice(categories), units),
        lambda: measure_from_chart(random.choice(categories), units),  # updated
        lambda: compare_three_measures(random.choice(categories), units),  # updated
        lambda: missing_value_from_mean(random.choice(categories), units),  # new
        lambda: missing_value_from_median(random.choice(categories), units),  # new
        lambda: missing_value_from_mode(random.choice(categories), units)  # new
    ]
    # Pick one random frame
    return random.choice(frames)()

def level_5() -> dict:
    """
    Returns:
    {
      "question": HTML string with all content and embedded visuals,
      "options": [HTML, HTML, HTML, HTML],
      "correctAnswer": int,
      "explanation": str
    }
    """
    # Pools
    contexts = [
        ("household incomes", "USD"),
        ("test scores", "points"),
        ("daily temperatures", "°C"),
        ("waiting times", "minutes"),
        ("product ratings", "stars"),
        ("ages of participants", "years")
    ]
    
    # -----------------------------
    # Helper frames and utilities
    # -----------------------------

    def _sample_clustered_data(n=50, centers=1, spread=1.0, low=0, high=100):
        """Use sklearn.make_blobs to create clustered data and map to a numeric range.
        This helps create symmetric or skewed shapes depending on params."""
        X, _ = make_blobs(n_samples=n, centers=centers, cluster_std=spread, random_state=random.randint(0,9999))
        xs = [float(x[0]) for x in X]
        # normalize to [low, high]
        mn, mx = min(xs), max(xs)
        if mx == mn:
            return [low + (high-low)/2 for _ in xs]
        scaled = [low + (x - mn) * (high - low) / (mx - mn) for x in xs]
        return [round(v, 2) for v in scaled]


    def _hist_chart_config(bins, values, label):
        return {
            "type": "bar",
            "data": {
                "labels": [f"bin{i+1}" for i in range(len(bins)-1)],
                "datasets": [{"label": label, "data": values}]
            },
            "options": {"scales": {"x": {"title": {"display": True, "text": "Bins"}}}}
        }


    def shape_from_hist(context, unit):
        """Create histograms that are roughly symmetric, right-skewed, or left-skewed.
        Ask the student to identify shape (symmetric / skew-right / skew-left)."""
        shape = random.choice(["symmetric", "right-skewed", "left-skewed"])
        if shape == "symmetric":
            data = _sample_clustered_data(n=60, centers=2, spread=3.0, low=10, high=90)
        elif shape == "right-skewed":
            # produce a long tail to the right by mixing a small cluster far right
            left = _sample_clustered_data(n=50, centers=1, spread=1.2, low=10, high=60)
            tail = _sample_clustered_data(n=10, centers=1, spread=0.8, low=61, high=100)
            data = left + tail
        else:
            right = _sample_clustered_data(n=50, centers=1, spread=1.2, low=40, high=90)
            tail = _sample_clustered_data(n=10, centers=1, spread=0.8, low=0, high=39)
            data = right + tail

        # create histogram counts (simple equal-width bins)
        bins = [round(min(data) + i*(max(data)-min(data))/6,2) for i in range(7)]
        counts = [0]*6
        for v in data:
            # find bin
            if v == max(data):
                counts[-1] += 1
            else:
                idx = int((v - min(data)) / (max(data) - min(data)) * 6)
                counts[idx] += 1

        chart = _hist_chart_config(bins, counts, f"{context} ({unit})")
        options = ["Symmetric", "Right-skewed (long right tail)", "Left-skewed (long left tail)", "Bimodal"]
        # correct mapping
        correct = {
            "symmetric": "Symmetric",
            "right-skewed": "Right-skewed (long right tail)",
            "left-skewed": "Left-skewed (long left tail)"
        }[shape]

        random.shuffle(options)
        return {
            "question": (
                f"<p>The histogram below shows {context} ({unit}). Identify the <b>shape</b> of the distribution.</p>"
                f"<pre class='chartjs'>{html.escape(json.dumps(chart))}</pre>"
            ),
            "options": options,
            "correctAnswer": options.index(correct),
            "explanation": f"This distribution was generated to be {shape}; observe the tail direction and peak symmetry."
        }

    def histogram_with_ranges(full_data, bins=6, data_range=None):
        counts, edges = np.histogram(full_data, bins=bins, range=data_range)
        labels = [f"{int(edges[i])}–{int(edges[i+1])}" for i in range(len(edges)-1)]
        return counts.tolist(), labels

    def compare_spread(context, unit):
        tight = _sample_clustered_data(n=40, centers=1, spread=0.8, low=30, high=60)
        wide  = _sample_clustered_data(n=40, centers=1, spread=3.5, low=20, high=80)

        # Randomly assign labels
        if random.choice([True, False]):
            A, B = tight, wide
            labelA, labelB = "A", "B"
            correct = "B has greater spread"
        else:
            A, B = wide, tight
            labelA, labelB = "A", "B"
            correct = "A has greater spread"

        # Shared bin edges
        min_val = min(min(A), min(B))
        max_val = max(max(A), max(B))

        countsA, labels = histogram_with_ranges(A, bins=6, data_range=(min_val, max_val))
        countsB, _      = histogram_with_ranges(B, bins=6, data_range=(min_val, max_val))

        chart_A = {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [{"label": labelA, "data": countsA}]
            }
        }
        chart_B = {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [{"label": labelB, "data": countsB}]
            }
        }

        # Show only 8 numbers from each for readability
        sampleA = sorted(random.sample(A, 8))
        sampleB = sorted(random.sample(B, 8))

        options = [
            f"{labelA} has greater spread",
            f"{labelB} has greater spread",
            "Both have similar spread",
            "Cannot tell"
        ]
        random.shuffle(options)

        return {
            "question": (
                f"<p>Two samples of {context} ({unit}) are shown below (8 values each) "
                f"and their full dataset histograms. Which sample has greater spread?</p>"
                f"<p>{labelA}: {sampleA}</p><p>{labelB}: {sampleB}</p>"
                f"<pre class='chartjs'>{html.escape(json.dumps(chart_A))}</pre>"
                f"<pre class='chartjs'>{html.escape(json.dumps(chart_B))}</pre>"
            ),
            "options": options,
            "correctAnswer": options.index(correct),
            "explanation": (
                f"The full dataset for {'A' if correct.startswith('A') else 'B'} "
                f"is spread across more bins and has a wider range, "
                f"so it has greater variability."
            )
        }


    def compute_iqr_from_data(context, unit):
        data = sorted([random.randint(10, 100) for _ in range(random.randint(7, 11))])
        q1 = statistics.median(data[:len(data)//2])
        q3 = statistics.median(data[(len(data)+1)//2:])
        iqr = q3 - q1
        distractors = [iqr + random.randint(1,5), abs(iqr - random.randint(1,4)), iqr + random.randint(6,10)]
        options = [iqr] + distractors[:3]
        random.shuffle(options)
        return {
            "question": (
                f"<p>Given the following {context} data ({unit}):</p><p>{data}</p><p>Compute the <b>IQR</b> (interquartile range).</p>"
            ),
            "options": [str(o) for o in options],
            "correctAnswer": options.index(iqr),
            "explanation": f"IQR = Q3 - Q1 = {q3} - {q1} = {iqr}. Q1 and Q3 found from lower/upper halves."
        }


    def boxplot_question(context, unit):
        # build a five-number summary ensuring non-equal numbers
        data = sorted([random.randint(5, 95) for _ in range(random.randint(7, 12))])
        minimum = data[0]
        maximum = data[-1]
        median = statistics.median(data)
        q1 = statistics.median(data[:len(data)//2])
        q3 = statistics.median(data[(len(data)+1)//2:])
        # ask which are potential outliers by 1.5*IQR rule
        iqr = q3 - q1
        lower_fence = q1 - 1.5*iqr
        upper_fence = q3 + 1.5*iqr
        # pick a candidate point (maybe an outlier or not)
        candidate = random.choice(data)
        is_outlier = candidate < lower_fence or candidate > upper_fence
        options = ["Outlier", "Not an outlier", "Must be median", "Must be min"]
        random.shuffle(options)
        correct = "Outlier" if is_outlier else "Not an outlier"
        summary = {"Min": minimum, "Q1": q1, "Median": median, "Q3": q3, "Max": maximum}
        return {
            "question": (
                f"<p>A boxplot has five-number summary for {context} ({unit}): {summary}.</p>"
                f"<p>Is the value {candidate} an <b>outlier</b> according to the 1.5×IQR rule?</p>"
            ),
            "options": options,
            "correctAnswer": options.index(correct),
            "explanation": (
                f"IQR = {iqr}; fences = ({round(lower_fence,2)}, {round(upper_fence,2)}). {candidate} {'is' if is_outlier else 'is not'} outside these fences."
            )
        }


    def skew_from_mean_median(context, unit):
        """Given mean and median relationship, infer skewness. Also increase cognitive load by providing a small sample where mean and median values are given with one removed value."""
        # Generate data and possibly remove one value shown as x
        data = sorted([random.randint(5, 95) for _ in range(7)])
        mean_val = round(statistics.mean(data), 2)
        median_val = round(statistics.median(data), 2)

        # sometimes mask one value and give mean and median to infer masked value or skew
        if False:
            missing_idx = random.randrange(len(data))
            masked = data[:]
            masked[missing_idx] = 'x'
            # ask: given mean and median, find x (ensuring integer)
            total = mean_val * len(data)
            missing_val = int(total - sum(v for v in data if isinstance(v, int)))
            options = [missing_val, missing_val + 2, missing_val - 2, data[missing_idx]]
            random.shuffle(options)
            q = (
                f"<p>Sample of {context} ({unit}) with one missing value x: {masked}.</p>"
                f"<p>The mean is given as {mean_val} and the median is {median_val}. Find x.</p>"
            )
            expl = f"Mean × n = sum → {mean_val}×{len(data)} = {total}. Sum of known values = {sum(v for v in data if isinstance(v, int))}. So x = {missing_val}."
            return {"question": q, "options": [str(o) for o in options], "correctAnswer": options.index(missing_val), "explanation": expl}
        else:
            # ask inference about skew from mean & median
            if mean_val > median_val:
                correct = "Right-skewed (mean > median)"
            elif mean_val < median_val:
                correct = "Left-skewed (mean < median)"
            else:
                correct = "Approximately symmetric (mean ≈ median)"
            options = ["Right-skewed (mean > median)", "Left-skewed (mean < median)", "Approximately symmetric (mean ≈ median)", "Bimodal"]
            random.shuffle(options)
            q = (
                f"<p>For a sample of {context} ({unit}), the mean is {mean_val} and the median is {median_val}.</p>"
                f"<p>What does this suggest about the <b>skewness</b> of the distribution?</p>"
            )
            expl = f"Mean = {mean_val}, Median = {median_val}. Comparison indicates: {correct}."
            return {"question": q, "options": options, "correctAnswer": options.index(correct), "explanation": expl}

        
    frames = [
        #  lambda: shape_from_hist(*random.choice(contexts)),
         lambda: compare_spread(*random.choice(contexts)),
        #  lambda: compute_iqr_from_data(*random.choice(contexts)),
        #  lambda: boxplot_question(*random.choice(contexts)),
        #  lambda: skew_from_mean_median(*random.choice(contexts)),
     ]

    return random.choice(frames)()




def generate_question(t,level):
    functions = [
        level_1,
        level_2,
        level_3,
        level_4,
        level_5
    ]
    
    return json.dumps(functions[level-1]())