"""
Preprocessor for ReLearn
Handles text cleaning, token normalization, and Python AST signal extraction.
"""
import ast
import re
from typing import Dict, Any, List, Optional

class ResponsePreprocessor:
    def __init__(self):
        self.stop_words = {
            "a", "an", "the", "in", "on", "at", "by", "for", "with", "about",
            "against", "between", "into", "through", "during", "before", "after",
            "above", "below", "to", "from", "up", "down", "is", "are", "was",
            "were", "be", "been", "being", "have", "has", "had", "do", "does", "did"
        }

    def clean_text(self, text: str) -> str:
        """Standardizes text formatting while preserving critical numeric and programming tokens."""
        if not text:
            return ""
        text = text.strip()
        # Preserve operators and critical characters like //, ==, =, [, ]
        text = re.sub(r'[\r\n\t]+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text

    def extract_ast_signals(self, code_str: str) -> Dict[str, Any]:
        """
        Parses code string safely using Python's native AST
        and extracts structural signals relevant to Python misconceptions.
        """
        signals = {
            "has_syntax_error": False,
            "has_for_loop": False,
            "has_while_loop": False,
            "has_recursion": False,
            "has_range_call": False,
            "range_args_count": 0,
            "has_mutable_default": False,
            "has_assign_in_comparison": False,
            "has_function_def": False,
            "function_has_global": False,
            "function_has_local_assign": False,
            "has_floor_division": False,
            "has_subscript": False,
            "has_bool_op": False
        }

        if not code_str or not code_str.strip():
            return signals

        try:
            tree = ast.parse(code_str)
        except SyntaxError:
            signals["has_syntax_error"] = True
            # Check if syntax error was caused by single '=' inside an if condition
            if re.search(r'if\s+[\w\.\(\)]+\s*=\s*[^=]', code_str):
                signals["has_assign_in_comparison"] = True
            return signals

        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                signals["has_for_loop"] = True
                if isinstance(node.iter, ast.Call):
                    if isinstance(node.iter.func, ast.Name) and node.iter.func.id == "range":
                        signals["has_range_call"] = True
                        signals["range_args_count"] = len(node.iter.args)

            elif isinstance(node, ast.While):
                signals["has_while_loop"] = True

            elif isinstance(node, ast.FunctionDef):
                signals["has_function_def"] = True
                # Check for mutable defaults
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        signals["has_mutable_default"] = True
                # Check for recursive self-call
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id == node.name:
                        signals["has_recursion"] = True
                    if isinstance(sub, ast.Global):
                        signals["function_has_global"] = True
                    if isinstance(sub, ast.Assign):
                        signals["function_has_local_assign"] = True

            elif isinstance(node, ast.BinOp):
                if isinstance(node.op, ast.FloorDiv):
                    signals["has_floor_division"] = True

            elif isinstance(node, ast.Subscript):
                signals["has_subscript"] = True

            elif isinstance(node, ast.BoolOp):
                signals["has_bool_op"] = True

        return signals

    def extract_lexical_markers(self, text: str) -> List[str]:
        """Extracts high-signal cognitive keywords that distinguish specific mental models."""
        markers = []
        lowered = text.lower()

        patterns = [
            (r'\b(inclusive|included|includes|including|through|up to and including)\b', 'signal_inclusive_bound'),
            (r'\b(exclusive|excludes|excluding|stops before|one before)\b', 'signal_exclusive_bound'),
            (r'\b(times|iterations|count|counted|cardinality|off by one)\b', 'signal_counting'),
            (r'\b(=|single equals|assignment|assigns|assigning)\b', 'signal_assignment_op'),
            (r'\b(==|double equals|equality|comparing|comparison)\b', 'signal_comparison_op'),
            (r'\b(global|local|scope|shadow|shadowing|overwritten|outside)\b', 'signal_scope'),
            (r'\b(base case|infinite|recursion|recur|stack|depth|halts)\b', 'signal_recursion'),
            (r'\b(default|shared|persists|accumulate|mutable|fresh list)\b', 'signal_mutable_default'),
            (r'\b(mid-body|mid-iteration|aborts|condition fails immediately)\b', 'signal_while_midbody'),
            (r'\b(floor|decimal|rounds|rounding|integer division|truncate)\b', 'signal_division'),
            (r'\b(0-based|1-based|first element|zero index|negative index|indexerror)\b', 'signal_indexing'),
            (r'\b(precedence|left to right|parentheses|order of operations)\b', 'signal_precedence')
        ]

        for regex, tag in patterns:
            if re.search(regex, lowered):
                markers.append(tag)

        return markers

    def prepare_input_string(self, text_reasoning: str, code_snippet: str = "") -> str:
        """Combines reasoning text, lexical markers, and code signals into a featurizable document."""
        cleaned_text = self.clean_text(text_reasoning)
        markers = self.extract_lexical_markers(cleaned_text)
        ast_signals = self.extract_ast_signals(code_snippet)

        active_ast = [k for k, v in ast_signals.items() if v]

        combined = f"{cleaned_text} {' '.join(markers)} {' '.join(active_ast)}"
        return combined.strip()
