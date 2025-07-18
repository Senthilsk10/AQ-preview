import random
import math
from typing import Tuple, List, Union, Dict, Set
from enum import Enum
import numpy as np
import re
import sys
import json

class DoubleOperationGenerator:
    def __init__(self):
        self.expr_gen = ExpressionGenerator()
        self.range_gen = IndexRangeGenerator()
    
    def generate_level1(self, operation_type: str = "summation") -> dict:
        """Generate Level 1 double operation with positive indices"""
        expression = random.choice([
            "i+j",
            "i*j",
            "i^j",
            f"{random.randint(2,4)}*i*j",
            f"i^2 + j^2"
        ])
        
        outer_end = random.randint(3, 5)  # Concrete value instead of n
        inner_end = random.randint(4, 6)  # Concrete value instead of m
        
        return {
            "expression": expression,
            "outer_start": "1",
            "outer_end": str(outer_end),
            "inner_start": "1",
            "inner_end": str(inner_end),
            "type": f"double_{operation_type}",
            "level": 1,
            "correlated": False
        }
    
    def generate_level2(self, operation_type: str = "summation") -> dict:
        """Generate Level 2 double operation with varying signs"""
        # Generate random integer ranges instead of using variables
        ranges = [
            random.randint(-5, -1) if random.choice([True, False]) else random.randint(1, 5)
            for _ in range(4)
        ]
        
        expression = random.choice([
            "i+j",
            "i^j",
            "2^(i+j)",
            f"{random.randint(2,4)}*i^2 - j"
        ])
        
        return {
            "expression": expression,
            "outer_start": str(ranges[0]),
            "outer_end": str(ranges[1]),
            "inner_start": str(ranges[2]),
            "inner_end": str(ranges[3]),
            "type": f"double_{operation_type}",
            "level": 2,
            "correlated": False
        }
    
    def generate_level3(self, operation_type: str = "summation") -> dict:
        """Generate Level 3 double operation with correlated indices"""
        correlation = random.choice(["+", "-"])
        offset = random.randint(1, 2)
        outer_end = random.randint(3, 5)  # Concrete value
        inner_end = random.randint(outer_end + 1, outer_end + 3)  # Ensure inner_end > outer_end
        
        inner_start = f"i{correlation}{offset}"  # Correlation with outer index
        expression = random.choice([
            "i+j",
            "(i+j)^2"
        ])
        
        return {
            "expression": expression,
            "outer_start": "1",
            "outer_end": str(outer_end),
            "inner_start": inner_start,
            "inner_end": str(inner_end),
            "type": f"double_{operation_type}",
            "level": 3,
            "correlated": True
        }
    
    def generate_level4(self, operation_type: str = "summation") -> dict:
        """Generate Level 4 double operation with correlated indices and varying signs"""
        correlation = random.choice(["+", "-"])
        offset = random.randint(1, 2)
        
        # Generate concrete integer ranges with different signs
        outer_start = random.randint(-5, -1)
        outer_end = random.randint(1, 5)
        inner_end = random.randint(abs(outer_end) + 1, abs(outer_end) + 3)
        
        inner_start = f"i{correlation}{offset}"  # Correlation with outer index
        
        expression = random.choice([
            "i+j",
            "(i+j)^2"
        ])
        
        return {
            "expression": expression,
            "outer_start": str(outer_start),
            "outer_end": str(outer_end),
            "inner_start": inner_start,
            "inner_end": str(inner_end),
            "type": f"double_{operation_type}",
            "level": 4,
            "correlated": True
        }

class IndexRangeGenerator:
    def generate_range_for_level2(self, variation: str) -> Tuple[int, int]:
        """Generate concrete integer ranges for level 2"""
        if variation == "both_negative":
            return (random.randint(-5, -3), random.randint(-2, -1))
        elif variation == "m_positive_n_negative":
            return (random.randint(1, 3), random.randint(-3, -1))
        else:  # m_negative_n_positive
            return (random.randint(-3, -1), random.randint(1, 3))
            
    def generate_range_for_level3(self) -> Tuple[int, int]:
        """Generate concrete integer ranges for level 3"""
        start = random.randint(-5, -1)
        end = random.randint(start + 2, start + 5)
        return (start, end)

class ExpressionGenerator:
    def __init__(self):
        self.functions = ['sqrt', 'ln']
    
    def generate_complex_expression(self, operation_type: str) -> str:
        """Generate complex expressions for Level 3"""
        if operation_type == "product":
            
            expressions = [
                lambda: f"i",
                lambda: f"i/2",
                lambda: f"(2*i - 1)/i",
                lambda: f"(i + 1)/i"
            ]
        else:
            expressions = [
                lambda: f"i^2",
                lambda: f"sqrt(i)",
                lambda: f"ln(i)",
                lambda: f"(2*i - 1)",
                lambda: f"(i^2 - 3)"
            ]
        return random.choice(expressions)()

def format_double_question(question: dict) -> str:
    """Format double operation questions in mathematical notation."""
    operations = question.get('operation_sequence', 'SS')
    symbols = {'S': '\\sum', 'P': '\\prod'}
    
    # Convert operation sequence to symbols
    op1, op2 = [symbols.get(op, '\\sum') for op in operations]
    
    # Add explicit index variables (i=, j=) to start ranges
    outer_start = f"i={question['outer_start']}"
    inner_start = f"j={question['inner_start']}"
    
    return (f"{op1}_{{{outer_start}}}^{{{question['outer_end']}}} "
            f"{op2}_{{{inner_start}}}^{{{question['inner_end']}}} "
            f"{question['expression']}")

def generate_distractors(expansion: str, operation_type: str) -> tuple[str, str]:
    """Generate two distractors for the expansion"""
    if expansion == "1 (empty range)":
        return ("1 (empty range) + 1", "1 (empty range) × 1")
    
    if operation_type == "double_summation":
        terms = expansion.split(" + ")
        # Remove some terms for first distractor
        mid = len(terms) // 2
        distractor1 = " + ".join(terms[:mid] + terms[mid+2:])
        
        # Duplicate and rearrange some terms for second distractor
        modified_terms = terms.copy()
        if len(modified_terms) > 1:
            modified_terms.insert(1, modified_terms[0])
        distractor2 = " + ".join(modified_terms)
    else:  # double_product
        terms = expansion.split(" × ")
        # Remove some terms for first distractor
        mid = len(terms) // 2
        distractor1 = " × ".join(terms[:mid] + terms[mid+2:])
        
        # Duplicate and rearrange some terms for second distractor
        modified_terms = terms.copy()
        if len(modified_terms) > 1:
            modified_terms.insert(1, modified_terms[0])
        distractor2 = " × ".join(modified_terms)
    
    return distractor1, distractor2

def generate_double_question_by_level(level: int, operation_type: str = "summation") -> dict:
    """Generate a double operation question for the specified level"""
    generator = DoubleOperationGenerator()
    
    # Convert symbolic bounds to actual integers
    if level == 1:
        question = generator.generate_level1(operation_type)
        question['outer_end'] = random.randint(3, 5)  # Replace 'n' with concrete value
        question['inner_end'] = random.randint(4, 6)  # Replace 'm' with concrete value
        return question
    elif level == 2:
        return generator.generate_level2(operation_type)
    elif level == 3:
        return generator.generate_level3(operation_type)
    elif level == 4:
        return generator.generate_level4(operation_type)
    else:
        raise ValueError(f"Invalid level: {level}. Supported levels are 1-4")

def format_single_question(question: dict) -> str:
    """Format single operation questions in mathematical notation"""
    operation_type = question.get('type', 'summation')
    symbol = '\\sum' if operation_type == 'summation' else '\\prod'
    
    # Add explicit index variable (i=) to start range
    start = f"i={question['outer_start']}"
    
    return (f"{symbol}_{{{start}}}"
            f"^{{{question['outer_end']}}} "
            f"{question['expression']}")

def format_double_question(question: dict) -> str:
    """Format double operation questions in mathematical notation"""
    operations = question.get('operation_sequence', 'SS')
    symbols = {'S': '\\sum', 'P': '\\prod'}
    
    # Convert operation sequence to symbols
    op1, op2 = [symbols[op] for op in operations]
    
    # Add explicit index variables (i=, j=) to start ranges
    outer_start = f"i={question['outer_start']}"
    inner_start = f"j={question['inner_start']}"
    
    return (f"{op1}_{{{outer_start}}}"
            f"^{{{question['outer_end']}}} "
            f"{op2}_{{{inner_start}}}"
            f"^{{{question['inner_end']}}} "
            f"{question['expression']}")

def format_triple_question(question: dict) -> str:
    """Format triple operation questions in mathematical notation"""
    operations = question['operation_sequence']
    symbols = {'S': '\\sum', 'P': '\\prod'}
    
    # Convert operation sequence to symbols
    op1, op2, op3 = [symbols[op] for op in operations]
    
    # Add explicit index variables (i=, j=, k=) to start ranges
    outer_start = f"i={question['outer_start']}"
    middle_start = f"j={question['middle_start']}"
    inner_start = f"k={question['inner_start']}"
    
    return (f"{op1}_{{{outer_start}}}"
            f"^{{{question['outer_end']}}} "
            f"{op2}_{{{middle_start}}}"
            f"^{{{question['middle_end']}}} "
            f"{op3}_{{{inner_start}}}"
            f"^{{{question['inner_end']}}} "
            f"{question['expression']}")

def format_question_katex(question: dict) -> str:
    """Format question in proper KaTeX notation"""
    symbols = {
        'S': '\\sum',
        'P': '\\prod'
    }
    ops = question.get('operation_sequence', '')
    
    def balance_expression(expr):
        # Count parentheses and braces
        open_parens = expr.count('(')
        close_parens = expr.count(')')
        open_braces = expr.count('{')
        close_braces = expr.count('}')
        
        # Balance parentheses
        if open_parens > close_parens:
            expr += ')' * (open_parens - close_parens)
        elif close_parens > open_parens:
            expr = '(' * (close_parens - open_parens) + expr
            
        # Balance braces
        if open_braces > close_braces:
            expr += '}' * (open_braces - close_braces)
        elif close_braces > open_braces:
            expr = '{' * (close_braces - open_braces) + expr
            
        return expr

    # Handle single operations
    if not ops or len(ops) == 1:
        symbol = symbols.get(ops, '\\sum')
        expr = question['expression'].replace('^', '^{').replace('*', '\\cdot ')
        expr = balance_expression(expr)
        return f"{symbol}_{{i={question['outer_start']}}}^{{{question['outer_end']}}} ({expr})"
    
    # Handle double operations
    elif len(ops) == 2:
        outer_symbol = symbols.get(ops[0], '\\sum')
        inner_symbol = symbols.get(ops[1], '\\sum')
        expr = question['expression'].replace('^', '^{').replace('*', '\\cdot ')
        expr = balance_expression(expr)
        return (f"{outer_symbol}_{{i={question['outer_start']}}}^{{{question['outer_end']}}} "
                f"{inner_symbol}_{{j={question['inner_start']}}}^{{{question['inner_end']}}} ({expr})")
    
    # Handle triple operations
    else:
        symbols_sequence = [symbols.get(op, '\\sum') for op in ops]
        expr = question['expression'].replace('^', '^{').replace('*', '\\cdot ')
        expr = balance_expression(expr)
        return (f"{symbols_sequence[0]}_{{i={question['outer_start']}}}^{{{question['outer_end']}}} "
                f"{symbols_sequence[1]}_{{j={question['middle_start']}}}^{{{question['middle_end']}}} "
                f"{symbols_sequence[2]}_{{k={question['inner_start']}}}^{{{question['inner_end']}}} ({expr})")

class SingleOperationGenerator:
    def __init__(self):
        self.expr_gen = ExpressionGenerator()
        self.range_gen = IndexRangeGenerator()
    
    def generate_level1(self, operation_type: str = "summation") -> dict:
        """Generate Level 1 question with positive indices"""
        n = random.randint(2, 5)  # Keeping n small for products
        return {
            "expression": "i",
            "start_index": 1,
            "end_index": n,
            "type": operation_type,
            "level": 1
        }
    
    def generate_level2(self, operation_type: str = "summation") -> dict:
        """Generate Level 2 question with varying signs"""
        variation = random.choice([
            "both_negative",
            "m_positive_n_negative",
            "m_negative_n_positive"
        ])
        
        if operation_type == "product":
            m, n = self.range_gen.generate_range_for_level2_product()
        else:
            m, n = self.range_gen.generate_range_for_level2(variation)
            
        return {
            "expression": "i",
            "start_index": m,
            "end_index": n,
            "type": operation_type,
            "level": 2
        }
    
    def generate_level3(self, operation_type: str = "summation") -> dict:
        """Generate Level 3 question with complex expressions"""
        if operation_type == "product":
            m, n = self.range_gen.generate_range_for_level2_product()
        else:
            m, n = self.range_gen.generate_range_for_level2(
                random.choice(["both_negative", "m_positive_n_negative", "m_negative_n_positive"])
            )
        
        expression = self.expr_gen.generate_complex_expression(operation_type)
        return {
            "expression": expression,
            "start_index": m,
            "end_index": n,
            "type": operation_type,
            "level": 3
        }

def generate_question_by_level(level: int, operation_type: str = "summation") -> dict:
    """Generate single, double, or triple operation questions based on the operation sequence."""
    expr_gen = ExpressionGenerator()
    
    if level == 1:
        # Level 1: Small positive integers
        n = random.randint(3, 5)
        return {
            "outer_start": "1",
            "outer_end": str(n),
            "expression": "i",
            "type": operation_type,
            "operation_sequence": "S" if operation_type == "summation" else "P"
        }
    elif level == 2:
        # Level 2: Mix of positive and negative integers
        start = random.randint(-5, -1)
        end = random.randint(1, 5)
        return {
            "outer_start": str(start),
            "outer_end": str(end),
            "expression": "i^2",
            "type": operation_type,
            "operation_sequence": "S" if operation_type == "summation" else "P"
        }
    else:  # level 3 or 4
        # Level 3/4: Larger range of integers with complex expressions
        if operation_type == "product":
            # Keep range smaller for products to avoid huge numbers
            start = random.randint(-4, -1)
            end = random.randint(2, 4)
        else:
            # Larger range for summations
            start = random.randint(-8, -3)
            end = random.randint(3, 8)
            
        return {
            "outer_start": str(start),
            "outer_end": str(end),
            "expression": expr_gen.generate_complex_expression(operation_type),
            "type": operation_type,
            "operation_sequence": "S" if operation_type == "summation" else "P"
        }

class TripleOperationGenerator:
    def __init__(self):
        self.expr_gen = ExpressionGenerator()
        self.range_gen = IndexRangeGenerator()
    
    def generate_level1(self, operation_sequence: str) -> dict:
        """Generate Level 1 triple operation with positive indices."""
        expression = random.choice([
            "i+j+k",
            "i^j*k",
            f"{random.randint(2,3)}*i^2 - j + k"
        ])
        
        return {
            "expression": expression,
            "outer_start": "1",
            "outer_end": "4",
            "middle_start": "1",
            "middle_end": "5",
            "inner_start": "1",
            "inner_end": "6",
            "operation_sequence": operation_sequence,
            "level": 1,
            "correlated": False
        }
    
    def generate_level2(self, operation_sequence: str) -> dict:
        """Generate Level 2 triple operation with mixed signs and independent indices."""
        ranges = [
            random.randint(-5, -1) if random.choice([True, False]) else random.randint(1, 5)
            for _ in range(6)
        ]
        
        expression = random.choice([
            "i+j+k",
            "(i*j)/k",
            "(i-j)^k"
        ])
        
        return {
            "expression": expression,
            "outer_start": str(ranges[0]),
            "outer_end": str(ranges[1]),
            "middle_start": str(ranges[2]),
            "middle_end": str(ranges[3]),
            "inner_start": str(ranges[4]),
            "inner_end": str(ranges[5]),
            "operation_sequence": operation_sequence,
            "level": 2,
            "correlated": False
        }
    
    def generate_level3(self, operation_sequence: str) -> dict:
        """Generate Level 3 triple operation with correlated indices."""
        correlation_type = random.choice(["two_indices", "all_indices"])
        
        if correlation_type == "two_indices":
            # Correlate two indices randomly
            corr_pair = random.choice(["i_j", "i_k", "j_k"])
            if corr_pair == "i_j":
                middle_start = f"i+{random.randint(1,2)}"
                inner_start = "1"
            elif corr_pair == "i_k":
                middle_start = "1"
                inner_start = f"i-{random.randint(1,2)}"
            else:  # j_k
                middle_start = "1"
                inner_start = f"j+{random.randint(1,2)}"
        else:
            # Correlate all three indices
            middle_start = f"i+{random.randint(1,2)}"
            inner_start = f"j-{random.randint(1,2)}"
        
        return {
            "expression": "(i-j)^k",
            "outer_start": str(random.randint(-2, 2)),
            "outer_end": str(random.randint(3, 6)),
            "middle_start": middle_start,
            "middle_end": str(random.randint(4, 7)),
            "inner_start": inner_start,
            "inner_end": str(random.randint(5, 8)),
            "operation_sequence": operation_sequence,
            "level": 3,
            "correlated": True
        }

def format_triple_question(question: dict) -> str:
    """Format triple operation questions in mathematical notation"""
    operations = question['operation_sequence']
    symbols = {'S': '\\sum', 'P': '\\prod'}
    
    # Convert operation sequence to symbols
    op1, op2, op3 = [symbols[op] for op in operations]
    
    # Add explicit index variables (i=, j=, k=) to start ranges
    outer_start = f"i={question['outer_start']}"
    middle_start = f"j={question['middle_start']}"
    inner_start = f"k={question['inner_start']}"
    
    return (f"{op1}_{{{outer_start}}}"
            f"^{{{question['outer_end']}}} "
            f"{op2}_{{{middle_start}}}"
            f"^{{{question['middle_end']}}} "
            f"{op3}_{{{inner_start}}}"
            f"^{{{question['inner_end']}}} "
            f"{question['expression']}")

def generate_triple_question(operation_sequence: str, level: int) -> dict:
    """Generate a triple operation question with specified operation sequence and level."""
    generator = TripleOperationGenerator()
    
    if level == 1:
        return generator.generate_level1(operation_sequence)
    elif level == 2:
        return generator.generate_level2(operation_sequence)
    elif level == 3:
        return generator.generate_level3(operation_sequence)
    else:
        raise ValueError(f"Invalid level: {level}. Supported levels are 1-3")

class ProblemType(Enum):
    SINGLE_SUM = 1
    SINGLE_PRODUCT = 2
    DOUBLE_SUM = 3
    DOUBLE_PRODUCT = 4
    SUM_PRODUCT = 5
    PRODUCT_SUM = 6
    TRIPLE_SUM = 7
    TRIPLE_PRODUCT = 8
    DOUBLE_SUM_PRODUCT = 9
    SUM_PRODUCT_SUM = 10
    SUM_DOUBLE_PRODUCT = 11
    PRODUCT_SUM_SUM = 12
    PRODUCT_SUM_PRODUCT = 13
    PRODUCT_PRODUCT_SUM = 14

def get_operation_sequence(prob_number: int) -> str:
    """Convert problem number to operation sequence based on the design document."""
    sequences = {
        1: "S",      # \sum
        2: "P",      # \prod
        3: "SS",     # \sum \sum
        4: "PP",     # \prod \prod
        5: "SP",     # \sum \prod
        6: "PS",     # \prod \sum
        7: "SSS",    # \sum \sum \sum
        8: "PPP",    # \prod \prod \prod
        9: "SSP",    # \sum \sum \prod
        10: "SPS",   # \sum \prod \sum
        11: "SPP",   # \sum \prod \prod
        12: "PSS",   # \prod \sum \sum
        13: "PSP",   # \prod \sum \prod
        14: "PPS"    # \prod \prod \sum
    }
    return sequences.get(prob_number, "")

def evaluate_expression(expr: str, vars: dict) -> float:
    """Evaluate a mathematical expression with given variables"""
    # Replace variable names with their values
    for var, value in vars.items():
        expr = expr.replace(var, str(value))
    
    # Format powers using ^ instead of superscript
    # Extract all power expressions and format them
    power_pattern = r'\(([^)]+)\)\s*\^\s*([^)\s]+)'
    while re.search(power_pattern, expr):
        expr = re.sub(power_pattern, r'(\1^{\2})', expr)
    
    # Handle simple powers without parentheses
    simple_power_pattern = r'(\d+)\s*\^\s*([^)\s]+)'
    while re.search(simple_power_pattern, expr):
        expr = re.sub(simple_power_pattern, r'\1^{\2}', expr)
    
    try:
        # Convert ^ to ** for Python evaluation
        eval_expr = expr.replace('^', '**')
        return eval(eval_expr)
    except:
        return 0  # Return 0 for invalid expressions

def generate_expansion(question: dict) -> str:
    """Generate the expansion based on the operation sequence"""
    # Get operation sequence
    ops = question.get('operation_sequence', '')
    
    # Handle single operations
    if not ops or len(ops) == 1:
        return expand_single_operation(question)
    # Handle double operations
    elif len(ops) == 2:
        return expand_double_operation(question)
    # Handle triple operations
    else:
        return expand_triple_operation(question)


def expand_single_operation(question: dict) -> str:
    """Expand a single operation expression."""
    start = int(question['outer_start'])
    end = int(question['outer_end'])
    expression = question['expression']
    operation_type = question.get('type', 'summation')
    
    def evaluate_term(expr: str, i: int) -> str:
        """Evaluate a term with the given index."""
        term = expr.replace('i', str(i))
        try:
            # Replace ^ with ** for Python evaluation
            eval_term = term.replace('^', '**')
            result = str(eval(eval_term))
            return result
        except:
            return term
    
    terms = []
    for i in get_range(start, end):
        term = evaluate_term(expression, i)
        terms.append(term)
    
    # Join terms with the appropriate operator
    if operation_type == 'product':
        operator = ' \\cdot '
        result = operator.join(terms) if terms else "1"
    else:
        operator = ' + '
        result = operator.join(terms) if terms else "0"
    
    # Add parentheses if multiple terms
    if len(terms) > 1:
        result = f"({result})"
    
    return result

def format_power_term(base: str, exponent: str) -> str:
    """Format a power expression with proper handling of negative exponents"""
    # Remove any existing parentheses from the base
    base = base.strip('()')
    # Always wrap base in parentheses if it contains operations
    if '+' in base or '-' in base or '\\cdot' in base:
        base = f"({base})"
    # Format the exponent with proper superscript notation
    return f"{base}^{{{exponent}}}"

def evaluate_expression(expr: str, vars: dict) -> float:
    """Evaluate a mathematical expression with given variables."""
    # Replace variable names with their values
    for var, value in vars.items():
        expr = expr.replace(var, str(value))
    
    # Replace ^ with ** for Python evaluation
    expr = expr.replace('^', '**')
    
    try:
        return eval(expr)
    except:
        return 0  # Return 0 for invalid expressions

def expand_double_operation(question: dict) -> str:
    """Expand a double operation expression."""
    outer_start = int(question['outer_start'])
    outer_end = int(question['outer_end'])
    inner_start = question['inner_start']
    inner_end = int(question['inner_end'])
    expression = question['expression']
    ops = question.get('operation_sequence', 'SS')  # e.g., 'SP', 'PS', etc.
    
    def evaluate_term(expr: str, i: int, j: int) -> str:
        """Evaluate a term with the given indices."""
        term = expr.replace('i', str(i)).replace('j', str(j))
        try:
            # Replace ^ with ** for Python evaluation
            eval_term = term.replace('^', '**')
            result = str(eval(eval_term))
            return result
        except:
            return term
    
    outer_terms = []
    for i in get_range(outer_start, outer_end):
        inner_terms = []
        
        # Calculate actual inner start for correlated indices
        try:
            if isinstance(inner_start, str) and 'i' in inner_start:
                actual_inner_start = eval(inner_start.replace('i', str(i)))
            else:
                actual_inner_start = int(inner_start)
        except:
            actual_inner_start = int(inner_start)
        
        for j in get_range(actual_inner_start, inner_end):
            term = evaluate_term(expression, i, j)
            inner_terms.append(term)
        
        # Combine inner terms based on inner operation
        if ops[1] == 'P':
            inner_result = ' \\cdot '.join(inner_terms) if inner_terms else "1"
        else:
            inner_result = ' + '.join(inner_terms) if inner_terms else "0"
        
        # Add parentheses if multiple terms
        if len(inner_terms) > 1:
            inner_result = f"({inner_result})"
        
        outer_terms.append(inner_result)
    
    # Combine outer terms based on outer operation
    if ops[0] == 'P':
        result = ' \\cdot '.join(outer_terms) if outer_terms else "1"
    else:
        result = ' + '.join(outer_terms) if outer_terms else "0"
    
    # Add parentheses if multiple outer terms
    if len(outer_terms) > 1:
        result = f"({result})"
    
    return result

def get_range(start: int, end: int) -> range:
    """Generate a range that handles both ascending and descending sequences."""
    if start <= end:
        return range(start, end + 1)  # Ascending range
    else:
        return range(start, end - 1, -1)  # Descending range

def is_empty_range(start: int, end: int) -> bool:
    """Check if a range is empty"""
    return (start > end) if start >= 0 or end >= 0 else (start < end)

def get_empty_value(operation: str) -> str:
    """Get the identity value for an operation"""
    return "1" if operation == 'P' else "0"

def evaluate_term(expr: str, i: int, j: int, k: int = None) -> str:
    """Evaluate a term with given values"""
    try:
        # Replace variables with values
        term = expr.replace('i', str(i)).replace('j', str(j))
        if k is not None:
            term = term.replace('k', str(k))
        
        # Handle division
        if '/' in term:
            num, den = term.split('/')
            num = num.strip('()')
            den = den.strip('()')
            if eval(den) == 0:  # Check for division by zero
                return "undefined"
            term = f"({num})/({den})"
        
        # Replace ^ with ** for Python evaluation
        eval_term = term.replace('^', '**')
        result = eval(eval_term)
        
        # Format decimal result
        return format_decimal(str(result))
    except:
        return "undefined"

def expand_triple_operation(question: dict) -> str:
    """Expand a triple operation expression with proper range handling."""
    outer_start = int(question['outer_start'])
    outer_end = int(question['outer_end'])
    middle_start = question['middle_start']
    middle_end = int(question['middle_end'])
    inner_start = question['inner_start']
    inner_end = int(question['inner_end'])
    expression = question['expression']
    ops = question['operation_sequence']  # e.g., 'SSP', 'SPS', etc.
    
    outer_terms = []
    for i in get_range(outer_start, outer_end):
        # Calculate actual middle start for correlated indices
        try:
            if isinstance(middle_start, str):
                actual_middle_start = calculate_start_index(middle_start, i=i)
            else:
                actual_middle_start = int(middle_start)
        except:
            actual_middle_start = int(middle_start)
        
        middle_terms = []
        for j in get_range(actual_middle_start, middle_end):
            # Calculate actual inner start for correlated indices
            try:
                if isinstance(inner_start, str):
                    actual_inner_start = calculate_start_index(inner_start, i=i, j=j)
                else:
                    actual_inner_start = int(inner_start)
            except:
                actual_inner_start = int(inner_start)
            
            inner_terms = []
            for k in get_range(actual_inner_start, inner_end):
                term = evaluate_term(expression, i, j, k)
                if term != "undefined":
                    inner_terms.append(term)
            
            # Combine inner terms based on inner operation
            if ops[2] == 'P':
                inner_result = ' \\cdot '.join(inner_terms) if inner_terms else "1"
            else:
                inner_result = ' + '.join(inner_terms) if inner_terms else "0"
            
            # Add parentheses if multiple terms
            if len(inner_terms) > 1:
                inner_result = f"({inner_result})"
            
            middle_terms.append(inner_result)
        
        # Combine middle terms based on middle operation
        if ops[1] == 'P':
            middle_result = ' \\cdot '.join(middle_terms) if middle_terms else "1"
        else:
            middle_result = ' + '.join(middle_terms) if middle_terms else "0"
        
        # Add parentheses if multiple terms
        if len(middle_terms) > 1:
            middle_result = f"({middle_result})"
        
        outer_terms.append(middle_result)
    
    # Combine outer terms based on outer operation
    if ops[0] == 'P':
        result = ' \\cdot '.join(outer_terms) if outer_terms else "1"
    else:
        result = ' + '.join(outer_terms) if outer_terms else "0"
    
    # Add parentheses if multiple outer terms
    if len(outer_terms) > 1:
        result = f"({result})"
    
    return result

def combine_terms(terms: List[str], operation: str) -> str:
    """Combine terms based on operation type"""
    if not terms:
        return get_empty_value(operation)
    
    # Filter out identity values when not needed
    if operation == 'P':
        terms = [t for t in terms if t != '1']
    elif operation == 'S':
        terms = [t for t in terms if t != '0']
    
    if not terms:
        return get_empty_value(operation)
        
    operator = ' \\cdot ' if operation == 'P' else ' + '
    result = operator.join(terms)
    
    # Add parentheses for multiple terms
    if len(terms) > 1:
        result = f"({result})"
    return result

def calculate_start_index(expr: str, i: int = None, j: int = None) -> int:
    """Calculate start index for correlated indices."""
    try:
        # Replace variables with their values
        if 'i' in expr and i is not None:
            expr = expr.replace('i', str(i))
        if 'j' in expr and j is not None:
            expr = expr.replace('j', str(j))
        return eval(expr)
    except:
        return 1  # Default to 1 if evaluation fails

def generate_distractors(correct_expansion: str, question: dict) -> List[str]:
    """Generate plausible but incorrect expansions"""
    operation_type = question.get('type', 'summation')
    operator = ' \\cdot ' if 'product' in operation_type else ' + '
    
    def format_term(term: str) -> str:
        """Format a term with proper fraction notation"""
        if '/' in term:
            parts = term.split('/')
            if len(parts) == 2:
                num, den = parts
                # Handle terms with parentheses
                num = num.strip('()')
                den = den.strip('()')
                return f"\\frac{{{num}}}{{{den.strip('()')}}}"
        return term
    
    def modify_terms(terms: List[str], attempt: int) -> str:
        """Create a plausible wrong expansion by modifying terms"""
        modified = terms.copy()
        
        # Choose modification based on attempt number to ensure variety
        modifications = ['skip_term', 'repeat_term', 'change_sign', 'off_by_one']
        modification = modifications[attempt % len(modifications)]
        
        if modification == 'skip_term':
            if len(modified) > 2:
                modified.pop(random.randint(1, len(modified)-2))
        elif modification == 'repeat_term':
            if modified:
                term_to_repeat = random.choice(modified)
                insert_pos = random.randint(0, len(modified))
                modified.insert(insert_pos, term_to_repeat)
        elif modification == 'change_sign':
            if modified:
                idx = random.randint(0, len(modified)-1)
                try:
                    val = int(modified[idx])
                    modified[idx] = str(-val)
                except:
                    pass
        elif modification == 'off_by_one':
            if modified:
                idx = random.randint(0, len(modified)-1)
                try:
                    val = int(modified[idx])
                    modified[idx] = str(val + random.choice([-1, 1]))
                except:
                    pass
        
        # Format any terms containing division
        modified = [format_term(term) for term in modified]
        return operator.join(modified)
    
    # Split correct expansion into terms
    terms = correct_expansion.split(operator)
    
    # Generate two different distractors with maximum attempts
    max_attempts = 10
    distractors = []
    attempt = 0
    
    while len(distractors) < 2 and attempt < max_attempts:
        distractor = modify_terms(terms, attempt)
        if (distractor != correct_expansion and 
            distractor not in distractors):
            distractors.append(distractor)
        attempt += 1
    
    # If we couldn't generate two unique distractors, fill with default ones
    while len(distractors) < 2:
        default_distractor = correct_expansion + " + 1"
        if default_distractor not in distractors:
            distractors.append(default_distractor)
    
    # Generate third distractor by swapping '+' and '\\cdot'
    temp_distractor = correct_expansion.replace(' + ', 'TEMP').replace(' \\cdot ', ' + ').replace('TEMP', ' \\cdot ')
    if (temp_distractor != correct_expansion and 
        temp_distractor not in distractors):
        distractors.append(temp_distractor)
    
    # Ensure we have 3 distractors, fill with default if needed
    while len(distractors) < 3:
        default_distractor = correct_expansion + " + 1"
        if default_distractor not in distractors:
            distractors.append(default_distractor)

    # print("Distractors: ", distractors)
    
    return distractors

# Helper function for generate_distractors
def format_expression(expression: str) -> str:
    """Format mathematical expression for consistent display"""
    # Remove extra spaces around operators
    expression = re.sub(r'\s*([+×=])\s*', r' \1 ', expression)
    # Ensure proper spacing in fractions
    expression = re.sub(r'(\d+)/(\d+)', r'\1 / \2', expression)
    # Clean up multiple spaces
    expression = re.sub(r'\s+', ' ', expression)
    return expression.strip()

def format_question_katex(question: dict) -> str:
    """Format question in proper KaTeX notation"""
    symbols = {
        'S': '\\sum',
        'P': '\\prod'
    }
    ops = question.get('operation_sequence', '')
    
    def balance_expression(expr):
        # Count parentheses and braces
        open_parens = expr.count('(')
        close_parens = expr.count(')')
        open_braces = expr.count('{')
        close_braces = expr.count('}')
        
        # Balance parentheses
        if open_parens > close_parens:
            expr += ')' * (open_parens - close_parens)
        elif close_parens > open_parens:
            expr = '(' * (close_parens - open_parens) + expr
            
        # Balance braces
        if open_braces > close_braces:
            expr += '}' * (open_braces - close_braces)
        elif close_braces > open_braces:
            expr = '{' * (close_braces - open_braces) + expr
            
        return expr

    # Handle single operations
    if not ops or len(ops) == 1:
        symbol = symbols.get(ops, '\\sum')
        expr = question['expression'].replace('^', '^{').replace('*', '\\cdot ')
        expr = balance_expression(expr)
        return f"{symbol}_{{i={question['outer_start']}}}^{{{question['outer_end']}}} ({expr})"
    
    # Handle double operations
    elif len(ops) == 2:
        outer_symbol = symbols.get(ops[0], '\\sum')
        inner_symbol = symbols.get(ops[1], '\\sum')
        expr = question['expression'].replace('^', '^{').replace('*', '\\cdot ')
        expr = balance_expression(expr)
        return (f"{outer_symbol}_{{i={question['outer_start']}}}^{{{question['outer_end']}}} "
                f"{inner_symbol}_{{j={question['inner_start']}}}^{{{question['inner_end']}}} ({expr})")
    
    # Handle triple operations
    else:
        symbols_sequence = [symbols.get(op, '\\sum') for op in ops]
        expr = question['expression'].replace('^', '^{').replace('*', '\\cdot ')
        expr = balance_expression(expr)
        return (f"{symbols_sequence[0]}_{{i={question['outer_start']}}}^{{{question['outer_end']}}} "
                f"{symbols_sequence[1]}_{{j={question['middle_start']}}}^{{{question['middle_end']}}} "
                f"{symbols_sequence[2]}_{{k={question['inner_start']}}}^{{{question['inner_end']}}} ({expr})")

def format_decimal(value: str) -> str:
    """Format decimal numbers to 3 decimal places"""
    try:
        # Check if the string represents a decimal number
        if '.' in value:
            num = float(value)
            return f"{num:.3f}".rstrip('0').rstrip('.')
        return value
    except ValueError:
        return value

def convert_to_katex(expansion: str) -> str:
    """Convert expansion to proper KaTeX notation with decimal formatting"""
    if not expansion or '=' not in expansion:
        # Format decimal numbers in the expansion
        terms = expansion.split(' ')
        formatted_terms = []
        for term in terms:
            if '\\cdot' in term or '+' in term or term.strip() in ['\\cdot', '+']:
                formatted_terms.append(term)
            else:
                formatted_terms.append(format_decimal(term))
        expansion = ' '.join(formatted_terms)
        
        # Format power expressions in the expansion
        if '^' in expansion:
            # Handle expressions with parentheses first
            expansion = re.sub(r'\((.*?)\)\^(-?\d+)(?!})', r'(\1)^{\2}', expansion)
            # Handle simple expressions without parentheses
            expansion = re.sub(r'([^\^]*?)\^(-?\d+)(?!})', r'\1^{\2}', expansion)
        return expansion.replace('*', '\\cdot')

    # Split the expression and result
    parts = expansion.split('=')
    expression = parts[0].strip()
    
    # Replace all multiplication symbols with \cdot
    expression = expression.replace('×', '\\cdot').replace('*', '\\cdot')
    
    # Convert division expressions to fractions
    def convert_division(match):
        numerator, denominator = match.group(1), match.group(2)
        # Handle arithmetic in numerator and denominator
        if '--' in numerator:
            numerator = numerator.replace('--', '+')
        if '--' in denominator:
            denominator = denominator.replace('--', '+')
        # Remove any stray parentheses around single numbers in denominator
        if denominator.startswith('(') and denominator.endswith(')'):
            denominator = denominator.strip('()')  # Simply strip parentheses
            try:
                # Check if it's a number and not zero
                if float(denominator) == 0:
                    denominator = '0'
                else:
                    denominator = str(float(denominator))
            except ValueError:
                # If not a simple number, put parentheses back
                denominator = f"({denominator})"
        return f"\\frac{{{numerator}}}{{{denominator.strip('()')}}}"
    
    # Handle division with parentheses first
    expression = re.sub(r'\(([^/]+)\)/\(([^)]+)\)', convert_division, expression)
    # Handle simple divisions
    expression = re.sub(r'([^/]+)/([^+\s\\\cdot]+)', convert_division, expression)
    
    # Pre-process power expressions with arithmetic
    def process_power_expr(match):
        expr = match.group(1)
        power = match.group(2)
        # Handle arithmetic in the base
        if '--' in expr:
            expr = expr.replace('--', '+')
        # Format the power - always wrap in curly braces for consistency
        power = '{' + power + '}'
        return f"({expr})^{power}"
    
    # Handle power expressions with arithmetic in base
    expression = re.sub(r'\(([-\d]+--[-\d]+)\)\^(-?\d+)', process_power_expr, expression)
    
    # Format the expression
    terms = expression.split('\\cdot')
    formatted_terms = []
    for term in terms:
        term = term.strip()
        
        # Handle expressions with powers
        if '^' in term:
            if term.startswith('(') and term.endswith(')') and '^{' in term:
                # Already properly formatted with curly braces
                formatted_terms.append(term)
                continue
                
            base, exponent = term.split('^', 1)
            # Clean up the base
            base = base.strip()
            if '(' in base or '+' in base or '-' in base:
                base = f"({base})"
            
            # Clean up the exponent and ensure it's wrapped in curly braces
            exponent = exponent.strip()
            if not (exponent.startswith('{') and exponent.endswith('}')):
                exponent = '{' + exponent + '}'
            
            formatted_term = f"{base}^{exponent}"
        else:
            formatted_term = term
            
        formatted_terms.append(formatted_term)
    
    # Join terms with proper multiplication symbol
    expression = ' \\cdot '.join(formatted_terms)
    
    # Final cleanup for any remaining arithmetic in powers
    expression = re.sub(r'\((\d+)--(\d+)\)', r'(\1+\2)', expression)
    
    # Ensure all remaining exponents are wrapped in curly braces
    expression = re.sub(r'\^(-?\d+)(?!})', r'^{\1}', expression)
    # Handle any remaining power expressions with parentheses
    expression = re.sub(r'\((.*?)\)\^(-?\d+)(?!})', r'(\1)^{\2}', expression)
    
    return expression

def generate_katex_html(math_expression: str) -> str:
    """Generate HTML with KaTeX rendering for a single expression"""
    return f"""
    <div class="math-display">
        <script>
            katex.render(`{math_expression}`, 
                        document.currentScript.parentElement, 
                        {{displayMode: true, throwOnError: false}});
        </script>
    </div>
    """

def standardize_question_format(question: dict) -> dict:
    """Standardize the question dictionary keys"""
    std_question = question.copy()
    
    # Key mappings based on the DoubleOperationGenerator output (lines 8-109)
    key_mappings = {
        'start_index': 'outer_start',
        'end': 'outer_end',
        'start': 'outer_start',
        'end_index': 'outer_end'
    }
    
    # Convert keys to standard format
    for old_key, new_key in key_mappings.items():
        if old_key in std_question:
            std_question[new_key] = std_question.pop(old_key)
    
    # Handle operation type conversion
    if 'type' in std_question:
        if std_question['type'] == 'summation':
            std_question['operation_sequence'] = 'S'
        elif std_question['type'] == 'product':
            std_question['operation_sequence'] = 'P'
        elif std_question['type'].startswith('double_'):
            base_type = std_question['type'].replace('double_', '')
            std_question['operation_sequence'] = 'SS' if base_type == 'summation' else 'PP'
    
    return std_question

def generate_mixed_double_question_by_level(operation_sequence: str, level: int) -> dict:
    """Generate double operation questions with mixed summation and product."""
    outer_op = "summation" if operation_sequence[0] == "S" else "product"
    inner_op = "summation" if operation_sequence[1] == "S" else "product"
    
    # Generate outer question
    outer_question = generate_question_by_level(level, outer_op)
    
    # Generate inner question
    inner_question = generate_question_by_level(level, inner_op)
    
    # Combine into a double operation question with both i and j
    expression = random.choice([
        "i+j",
        "i*j",
        "i^j",
        f"{random.randint(2,4)}*i*j",
        f"i^2 + j^2",
        "(i+j)^2",
         f"ln(i+j)"
    ])

    return {
        "outer_start": outer_question["outer_start"],
        "outer_end": outer_question["outer_end"],
        "inner_start": inner_question["outer_start"],
        "inner_end": inner_question["outer_end"],
        "expression": expression,  # Use the new expression with both i and j
        "type": operation_sequence,
        "level": level,
        "operation_sequence": operation_sequence
    }

def aqg_sums_and_products(prob_number: int, level_number: int) -> dict:
    """Main interface function for auto question generation."""
    if not 1 <= prob_number <= 14:
        raise ValueError("Problem number must be between 1 and 14")
    if not 1 <= level_number <= 4:
        raise ValueError("Level number must be between 1 and 4")

    # Get operation sequence
    operation_sequence = get_operation_sequence(prob_number)
    
    # Determine the number of operations based on operation_sequence length
    num_operations = len(operation_sequence)
    
    # Generate question based on the number of operations
    if num_operations == 1:
        question = generate_question_by_level(level_number, 
                                             "summation" if operation_sequence == "S" else "product")
    elif num_operations == 2:
        if operation_sequence in ["SS", "PP"]:
            # Double summation or double product
            question = generate_double_question_by_level(level_number, 
                                                         "summation" if operation_sequence[0] == "S" else "product")
        else:
            # Mixed operations (e.g., "SP", "PS")
            question = generate_mixed_double_question_by_level(operation_sequence, level_number)
    elif num_operations == 3:
        question = generate_triple_question(operation_sequence, level_number)
    else:
        raise ValueError(f"Unsupported number of operations: {num_operations}")

    # Add operation sequence to single operations if not present
    if 'operation_sequence' not in question:
        question['operation_sequence'] = operation_sequence

    # Generate correct expansion and distractors
    correct_expansion = generate_expansion(question)
    distractors = generate_distractors(correct_expansion, question)

    return {
        "normal_format": {
            "question": question,
            "correct_expansion": correct_expansion,
            "distractors": distractors
        },
        "katex_format": {
            "question": format_question_katex(question),
            "correct_expansion": convert_to_katex(correct_expansion),
            "distractors": [convert_to_katex(d) for d in distractors]
        },
        "html_format": {
            "question": generate_katex_html(format_question_katex(question)),
            "correct_expansion": generate_katex_html(convert_to_katex(correct_expansion)),
            "distractors": [generate_katex_html(convert_to_katex(d)) for d in distractors]
        }
    }

def format_mathematical_output(result: dict) -> str:
    """Format the question and expansions in mathematical notation"""
    question = result["normal_format"]["question"]
    expansion = result["normal_format"]["correct_expansion"]
    distractors = result["normal_format"]["distractors"]
    
    output = [
        "═" * 50,
        "Question:",
        format_question_katex(question),
        "",
        "Correct Expansion:",
        expansion,
        "",
        "Alternative Expansions:",
        f"1. {distractors[0]}",
        f"2. {distractors[1]}",
        f"3. {distractors[2]}",
        "═" * 50
    ]
    
    return "\n".join(output)


def generate_single_katex_html(math_expression: str, is_question: bool = False) -> str:
    """Generate HTML for a single KaTeX expression with no line breaks"""
    instruction = '<p>Expand the below equation:</p>' if is_question else ''
    
    # Use single quotes for HTML attributes to avoid escaping double quotes
    return f'''<!DOCTYPE html><html><head><meta charset='UTF-8'><link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css'><script src='https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js'></script></head><body>{instruction}<div id='math-output'></div><script>document.addEventListener('DOMContentLoaded',function(){{katex.render(`{math_expression}`,document.getElementById('math-output'),{{displayMode:true,throwOnError:false}});}});</script></body></html>'''

def generate_json_output(result: dict) -> str:
    """Generate JSON output with properly escaped KaTeX expressions"""
    # Generate HTML for question and answers
    question_html = generate_single_katex_html(result['katex_format']['question'], is_question=True)
    correct_answer_html = generate_single_katex_html(result['katex_format']['correct_expansion'])
    distractor_htmls = [generate_single_katex_html(d) for d in result['katex_format']['distractors']]
    
    # Create list of all options
    all_options = [correct_answer_html] + distractor_htmls
    
    # Randomly shuffle the options
    random.shuffle(all_options)
    
    # Find the index of correct answer in shuffled options
    correct_answer_index = all_options.index(correct_answer_html)
    
    # Create the output dictionary
    output_dict = {
        "question": question_html,
        "options": all_options,
        "correctAnswer": correct_answer_index
    }
    
    # Use json.dumps with ensure_ascii=False and without escaping HTML quotes
    return json.dumps(output_dict, ensure_ascii=False).replace('\\"', '"')

# Modify the main execution block to return JSON when called via API
def generate_question(prob_number: int, level_number: int) -> str:
    """Main function to generate question and return JSON output"""
    try:
        if not (1 <= prob_number <= 14 and 1 <= level_number <= 4):
            raise ValueError("Problem number must be 1-14 and level must be 1-4")
        
        # Generate question
        result = aqg_sums_and_products(prob_number, level_number)
        # print(result)
        # Convert to required JSON format
        return generate_json_output(result)
        
    except ValueError as e:
        import json
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    # Generate and print properly formatted JSON
    output = generate_question(1, 3)
    # print(output)
    
   



