"""
Intervention Templates and Pedagogical Scaffolds for ReLearn
Provides misconception-specific, multi-stage cognitive interventions including
visual models, counterexamples, Socratic prompts, and micro-practice.
"""
from typing import Dict, Any

INTERVENTION_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "M001": {
        "misconception_id": "M001",
        "name": "Range Upper-Bound Inclusion",
        "concept": "Python range() boundaries",
        "pedagogical_goal": "Reframe range(start, stop) from inclusive [start, stop] to half-open interval [start, stop).",
        "stages": [
            {
                "type": "conceptual_reframing",
                "title": "Mental Model Shift: Half-Open Intervals",
                "content": (
                    "In Python, range(start, stop) follows the mathematical half-open interval: [start, stop).\n"
                    "It generates numbers where: start <= value < stop.\n"
                    "The stop value is an EXCLUSIVE boundary—it acts as a 'stop sign' telling Python where to halt BEFORE printing."
                )
            },
            {
                "type": "visual_model",
                "title": "Visual Interval Blueprint",
                "visual_type": "range_interval_bar",
                "data": {
                    "start": 1,
                    "stop": 5,
                    "generated": [1, 2, 3, 4],
                    "excluded_stop": 5,
                    "interval_notation": "[1, 5) -> values: 1, 2, 3, 4 (Count = 5 - 1 = 4)"
                }
            },
            {
                "type": "counterexample",
                "title": "Predictable Counterexample",
                "code": "# Notice the length matches (stop - start):\nnums = list(range(1, 4))\nprint(nums)        # Output: [1, 2, 3]\nprint(len(nums))   # Output: 3  (4 - 1 = 3)",
                "explanation": "If 4 were included, len(range(1, 4)) would be 4. But it is 3! The upper bound 4 is never generated."
            },
            {
                "type": "socratic_prompt",
                "title": "Socratic Reflection",
                "prompt": "If range(0, 10) generated 10, how many total numbers would you have starting from 0? Would that match the length of a 10-element list?"
            },
            {
                "type": "micro_practice",
                "title": "Micro-Practice Check",
                "question": "Which numbers are produced by list(range(3, 7))?",
                "options": [
                    "[3, 4, 5, 6, 7]",
                    "[3, 4, 5, 6]",
                    "[2, 3, 4, 5, 6]"
                ],
                "correct_index": 1,
                "feedback_correct": "Spot on! The sequence stops right before 7, yielding exactly [3, 4, 5, 6].",
                "feedback_incorrect": "Remember the boundary rule: start <= x < stop. 7 is the stop sign, so it halts at 6."
            }
        ]
    },
    "M002": {
        "misconception_id": "M002",
        "name": "Off-by-One Iteration Count",
        "concept": "Loop Iteration & Counting",
        "pedagogical_goal": "Disentangle 0-based indexing from sequence cardinality (N items span 0 to N-1).",
        "stages": [
            {
                "type": "conceptual_reframing",
                "title": "Counting Cardinality in 0-Indexed Systems",
                "content": (
                    "When counting from 0, the N-th item has index N-1.\n"
                    "For example, range(5) starts at index 0 and ends at index 4.\n"
                    "Count them: index 0 (1st), index 1 (2nd), index 2 (3rd), index 3 (4th), index 4 (5th).\n"
                    "The total number of executions is exactly 5, not 6."
                )
            },
            {
                "type": "visual_model",
                "title": "0-Indexed Step Grid",
                "visual_type": "index_counting_grid",
                "data": {
                    "total_count": 5,
                    "indices": [0, 1, 2, 3, 4],
                    "cardinal_counts": ["1st", "2nd", "3rd", "4th", "5th"]
                }
            },
            {
                "type": "counterexample",
                "title": "Concrete Counterexample",
                "code": "total = 0\nfor _ in range(5):\n    total += 1\nprint('Total iterations:', total)  # Prints: 5",
                "explanation": "Even though the maximum value of i is 4, starting at 0 means exactly 5 iterations occur."
            },
            {
                "type": "micro_practice",
                "title": "Micro-Practice Check",
                "question": "How many times will a loop with range(0, 10) execute?",
                "options": ["9 times", "10 times", "11 times"],
                "correct_index": 1,
                "feedback_correct": "Correct! Indices 0 through 9 contain exactly 10 iterations (10 - 0 = 10).",
                "feedback_incorrect": "Notice that 10 - 0 = 10. Counting 0, 1, ..., 9 gives exactly 10 executions."
            }
        ]
    },
    "M003": {
        "misconception_id": "M003",
        "name": "Assignment vs Equality Operator",
        "concept": "Variables & Conditionals",
        "pedagogical_goal": "Separate variable mutation ('=') from boolean comparison ('==').",
        "stages": [
            {
                "type": "conceptual_reframing",
                "title": "Action vs Inquiry",
                "content": (
                    "Single '=' is a COMMAND (Mutation): 'Place this value into that memory box'.\n"
                    "Double '==' is an INQUIRY (Comparison): 'Are the contents of these two sides equal?'.\n"
                    "In Python, using '=' inside an if condition is a SyntaxError to protect against accidental mutation."
                )
            },
            {
                "type": "visual_model",
                "title": "Operator Anatomy",
                "visual_type": "operator_comparison",
                "data": {
                    "assignment": {"op": "=", "meaning": "Assign / Store", "valid_in_if": False},
                    "equality": {"op": "==", "meaning": "Compare / Test", "valid_in_if": True}
                }
            },
            {
                "type": "micro_practice",
                "title": "Micro-Practice Check",
                "question": "Which line correctly checks if user_role is equal to 'admin'?",
                "options": [
                    "if user_role = 'admin':",
                    "if user_role == 'admin':",
                    "if user_role := 'admin':"
                ],
                "correct_index": 1,
                "feedback_correct": "Exactly! '==' performs the equality test and returns True/False.",
                "feedback_incorrect": "Use '==' for comparison. Single '=' is for assigning variables."
            }
        ]
    },
    "M004": {
        "misconception_id": "M004",
        "name": "Variable Scope Shadowing",
        "concept": "Functions & Variable Scope",
        "pedagogical_goal": "Illustrate stack frame isolation and explain that assignment inside a function creates a local variable by default.",
        "stages": [
            {
                "type": "conceptual_reframing",
                "title": "Stack Frames & Local Isolation",
                "content": (
                    "Every function call creates its own private 'local room' (stack frame).\n"
                    "When you write 'x = 10' inside a function, Python builds a new variable inside that local room.\n"
                    "It shadows the global x, leaving the outside global variable completely untouched!"
                )
            },
            {
                "type": "visual_model",
                "title": "Scope Isolation Diagram",
                "visual_type": "scope_boxes",
                "data": {
                    "global_frame": {"x": 20},
                    "local_frame": {"x": 50, "note": "Local shadow, destroyed on return"}
                }
            },
            {
                "type": "micro_practice",
                "title": "Micro-Practice Check",
                "question": "What is printed outside after calling def f(): x = 99 when global x was 5?",
                "options": ["99", "5", "None"],
                "correct_index": 1,
                "feedback_correct": "Correct! Without 'global x', the outer x remains 5.",
                "feedback_incorrect": "Remember: assignment inside creates a local variable. The global variable stays 5."
            }
        ]
    },
    "M005": {
        "misconception_id": "M005",
        "name": "Missing Base Case in Recursion",
        "concept": "Recursion",
        "pedagogical_goal": "Demonstrate the call stack and why an explicit stopping condition (base case) is mandatory.",
        "stages": [
            {
                "type": "conceptual_reframing",
                "title": "The Infinite Call Stack",
                "content": (
                    "Functions do not know when to stop on their own.\n"
                    "Without an explicit 'if' condition returning a fixed value, countdown(0) calls countdown(-1), which calls countdown(-2)...\n"
                    "Python halts with RecursionError: maximum recursion depth exceeded."
                )
            },
            {
                "type": "visual_model",
                "title": "Call Stack Overflow",
                "visual_type": "stack_overflow",
                "data": {
                    "frames": ["countdown(3)", "countdown(2)", "countdown(1)", "countdown(0)", "countdown(-1)..."]
                }
            },
            {
                "type": "micro_practice",
                "title": "Micro-Practice Check",
                "question": "What is the role of a base case in recursion?",
                "options": [
                    "To print intermediate values",
                    "To halt recursion and return without making further self-calls",
                    "To initialize loop counters"
                ],
                "correct_index": 1,
                "feedback_correct": "Spot on. The base case stops the chain of calls.",
                "feedback_incorrect": "A base case is the essential stopping condition that guards against infinite recursion."
            }
        ]
    },
    "M006": {
        "misconception_id": "M006",
        "name": "Mutable Default Argument Aliasing",
        "concept": "Function Defaults & Mutability",
        "pedagogical_goal": "Explain that default argument objects are created once at definition time, not on each call.",
        "stages": [
            {
                "type": "conceptual_reframing",
                "title": "Definition-Time Binding",
                "content": (
                    "In Python, default arguments are evaluated ONCE when the function definition is executed, not each time the function is called.\n"
                    "If you use a mutable default like lst=[], every call without that argument shares the EXACT same list in memory!"
                )
            },
            {
                "type": "visual_model",
                "title": "Pointer Aliasing View",
                "visual_type": "memory_pointer",
                "data": {
                    "function_object": "append_item",
                    "shared_default_id": "0x7f88... list instance",
                    "call_1_appends": "apple",
                    "call_2_appends": "banana -> ['apple', 'banana']"
                }
            },
            {
                "type": "micro_practice",
                "title": "Micro-Practice Check",
                "question": "What is the recommended Python pattern to avoid mutable default sharing?",
                "options": [
                    "def f(lst=[]):",
                    "def f(lst=None): if lst is None: lst = []",
                    "def f(lst=list()):"
                ],
                "correct_index": 1,
                "feedback_correct": "Exactly! Using None as a sentinel creates a fresh list every call.",
                "feedback_incorrect": "Use None as the default sentinel, then initialize lst = [] inside the body."
            }
        ]
    },
    "M007": {
        "misconception_id": "M007",
        "name": "While-Loop Mid-Body Termination",
        "concept": "While Loops & Control Flow",
        "pedagogical_goal": "Clarify that loop condition checks occur strictly at the top of each iteration, not continuously mid-statement.",
        "stages": [
            {
                "type": "conceptual_reframing",
                "title": "Loop Condition Checkpoint",
                "content": "Python only checks the while condition at the START of the iteration. Any statements in the body finish before checking again."
            },
            {
                "type": "micro_practice",
                "title": "Micro-Practice Check",
                "question": "If x increments to 3 on line 2, does line 3 'print(x)' still run in that iteration?",
                "options": ["Yes, the body runs to completion", "No, it immediately stops"],
                "correct_index": 0,
                "feedback_correct": "Correct! Python finishes the current iteration body before re-checking the condition.",
                "feedback_incorrect": "Python always finishes the active iteration body unless 'break' is executed."
            }
        ]
    },
    "M008": {
        "misconception_id": "M008",
        "name": "Integer Division Truncation",
        "concept": "Arithmetic Operators",
        "pedagogical_goal": "Distinguish '/' (float) from '//' (floor division towards negative infinity).",
        "stages": [
            {
                "type": "conceptual_reframing",
                "title": "Floor Division Rule",
                "content": "'//' performs math.floor() on the quotient. 7 // 2 = 3. Notice it does NOT round to nearest; it always rounds DOWN."
            },
            {
                "type": "micro_practice",
                "title": "Micro-Practice Check",
                "question": "What is the output of 8 // 3?",
                "options": ["2.66", "3", "2"],
                "correct_index": 2,
                "feedback_correct": "8 / 3 is 2.66..., floor division rounds down to 2.",
                "feedback_incorrect": "Floor division rounds down to the nearest integer (2)."
            }
        ]
    },
    "M009": {
        "misconception_id": "M009",
        "name": "1-Indexed Sequence Access",
        "concept": "Lists & Indexing",
        "pedagogical_goal": "Reinforce that sequence memory offsets start at 0, and -1 accesses the terminal item.",
        "stages": [
            {
                "type": "conceptual_reframing",
                "title": "Offset-Based Indexing",
                "content": "Index represents the OFFSET from the start of the list. Zero steps from start = element 0."
            },
            {
                "type": "micro_practice",
                "title": "Micro-Practice Check",
                "question": "What is items[0] for items = ['cat', 'dog']?",
                "options": ["'cat'", "'dog'", "IndexError"],
                "correct_index": 0,
                "feedback_correct": "Correct! Index 0 accesses the initial element.",
                "feedback_incorrect": "Python lists are 0-indexed; items[0] is 'cat'."
            }
        ]
    },
    "M010": {
        "misconception_id": "M010",
        "name": "Boolean Operator Precedence",
        "concept": "Boolean Logic & Expressions",
        "pedagogical_goal": "Demonstrate boolean operator hierarchy: not > and > or.",
        "stages": [
            {
                "type": "conceptual_reframing",
                "title": "Logical Order of Operations",
                "content": "Just as multiplication (*) binds tighter than addition (+), 'and' binds tighter than 'or' in Python."
            },
            {
                "type": "micro_practice",
                "title": "Micro-Practice Check",
                "question": "In 'A or B and C', which operator evaluates first?",
                "options": ["or", "and", "Left to right"],
                "correct_index": 1,
                "feedback_correct": "'and' has higher precedence and is grouped first.",
                "feedback_incorrect": "'and' binds tighter than 'or' in Python."
            }
        ]
    },
    "NONE": {
        "misconception_id": "NONE",
        "name": "No Misconception / Sound Mental Model",
        "concept": "General Python Programming",
        "pedagogical_goal": "Reinforce mastery and challenge the learner with higher-difficulty concepts.",
        "stages": [
            {
                "type": "positive_reinforcement",
                "title": "Mastery Confirmed",
                "content": "Excellent reasoning! Your mental model aligns with Python's language invariants. Ready to advance to the next challenge."
            }
        ]
    }
}
