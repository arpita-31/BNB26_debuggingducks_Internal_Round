"""
Dataset Generator for ReLearn
Generates high-quality, varied training and held-out test datasets
for 10 formal Python misconceptions plus NONE (correct) class.
Includes hard negatives where different misconceptions yield identical surface answers.
"""
import json
import random
from pathlib import Path

random.seed(42)

MISCONCEPTIONS = {
    "M001": {
        "name": "Range Upper-Bound Inclusion",
        "concept": "Python range() boundaries",
        "train_templates": [
            ("Q_PY_RANGE_01", "for i in range(1, 5): print(i)", "1 2 3 4 5", [
                "It will print 1, 2, 3, 4, 5 because range(1,5) includes the upper bound 5.",
                "The loop starts at 1 and goes up to and including 5.",
                "range(1,5) produces numbers from 1 through 5, so 5 is definitely printed.",
                "Output is 1 2 3 4 5 since 5 is the stopping value and is included in the loop.",
                "In Python range(start, stop) includes both start and stop, printing 1 to 5.",
                "It prints 1, 2, 3, 4, 5 because the interval is [1, 5].",
                "Numbers 1 through 5 will be displayed on screen.",
                "The loop ends at 5, meaning 5 is the last number printed.",
                "range(1, 5) generates five numbers: 1, 2, 3, 4, and 5.",
                "It prints all numbers up to 5 inclusive."
            ]),
            ("Q_PY_RANGE_02", "for x in range(3, 8): print(x)", "3 4 5 6 7 8", [
                "Prints 3, 4, 5, 6, 7, 8 because range(3,8) includes 8.",
                "It starts at 3 and ends at 8 inclusive.",
                "range(3, 8) includes the ending number 8.",
                "Output will be 3 4 5 6 7 8 since the upper limit 8 is included in python.",
                "The numbers printed are 3 through 8.",
                "Starts at 3 and stops at 8, printing 3, 4, 5, 6, 7, 8."
            ]),
            ("Q_PY_RANGE_03", "for n in range(0, 3): print(n)", "0 1 2 3", [
                "Prints 0, 1, 2, 3 because 3 is the upper limit and is included.",
                "It includes the stop parameter 3.",
                "range(0,3) goes from 0 up to 3 inclusive.",
                "The sequence generated will be 0 1 2 3."
            ])
        ],
        "test_templates": [
            ("Q_PY_RANGE_HELD_01", "for val in range(2, 7): print(val)", "2 3 4 5 6 7", [
                "The output is 2 3 4 5 6 7 because 7 is included in range(2, 7).",
                "range(2, 7) executes for 2, 3, 4, 5, 6, and 7 because stop is inclusive.",
                "It will print 2, 3, 4, 5, 6, 7 because the loop reaches 7.",
                "Prints all integers from 2 up to and including 7."
            ]),
            ("Q_PY_RANGE_HELD_02", "for i in range(10, 15): print(i)", "10 11 12 13 14 15", [
                "Outputs 10, 11, 12, 13, 14, 15 since range includes the endpoint 15.",
                "From 10 through 15 inclusive.",
                "15 is printed because range(10, 15) stops at 15 including it."
            ])
        ]
    },
    "M002": {
        "name": "Off-by-One Iteration Count",
        "concept": "Loop Iteration & Counting",
        "train_templates": [
            ("Q_PY_COUNT_01", "count = 0\nfor i in range(5): count += 1", "Total: 6", [
                "The loop runs 6 times because it starts at 0 and goes up to 5.",
                "Total is 6 because counting 0, 1, 2, 3, 4, 5 gives six iterations.",
                "It executes 6 times since 0 counts as the first and 5 is the last.",
                "Count is 6 because range(5) has 6 numbers.",
                "There are 6 iterations from 0 to 5.",
                "Loop runs 4 times because range stops early at 4 and starts at 1.",
                "It executes 4 times because it skipped an iteration.",
                "The count will be 6 because you have to add 1 for index zero."
            ]),
            ("Q_PY_COUNT_02", "for k in range(1, 6): total += 1", "Total: 4", [
                "Loop runs 4 times because 6 - 1 - 1 = 4.",
                "It runs 6 times because 6 - 1 is 5 plus 1 for offset.",
                "Iteration count is off by one, running 6 times."
            ])
        ],
        "test_templates": [
            ("Q_PY_COUNT_HELD_01", "for x in range(4): pass", "Runs 5 times", [
                "The loop will execute 5 times because index 0 to 4 is 5 steps.",
                "Count is 5 since 0, 1, 2, 3, 4 is five iterations.",
                "It runs 3 times because range stops one before 4."
            ])
        ]
    },
    "M003": {
        "name": "Assignment vs Equality Operator",
        "concept": "Variables & Conditionals",
        "train_templates": [
            ("Q_PY_ASSIGN_01", "if status = 'admin': print('OK')", "SyntaxError", [
                "It will print OK because status equals admin.",
                "The if statement checks if status is admin using the = operator.",
                "In Python = is used to check if values are equal.",
                "It assigns admin and evaluates to true so it prints OK.",
                "The single equal sign checks equality like in algebra.",
                "if status = 'admin' will compare status with admin and return true.",
                "It sets status to admin and prints OK without any errors."
            ]),
            ("Q_PY_ASSIGN_02", "if x = 10: print('Ten')", "Prints Ten", [
                "Checks if x is equal to 10 with = and prints Ten.",
                "In if x = 10, the = tests equality and succeeds.",
                "Single equals compares x to 10."
            ])
        ],
        "test_templates": [
            ("Q_PY_ASSIGN_HELD_01", "if count = 0: print('Zero')", "Prints Zero", [
                "Evaluates if count is equal to 0 using =.",
                "The single equal checks equality in if conditions.",
                "It checks whether count equals 0 and prints Zero."
            ])
        ]
    },
    "M004": {
        "name": "Variable Scope Shadowing",
        "concept": "Functions & Variable Scope",
        "train_templates": [
            ("Q_PY_SCOPE_01", "val = 20\ndef f(): val = 50\nf()\nprint(val)", "Outside: 50", [
                "It prints Outside: 50 because f() changed val to 50.",
                "val was updated to 50 inside the function so the global val is now 50.",
                "Both print statements will show 50 because val is modified.",
                "The function alters the outer variable val permanently.",
                "val becomes 50 everywhere after calling f().",
                "Since val is 50 inside f, outside val will also be 50.",
                "Global variable val is overwritten by the local assignment."
            ]),
            ("Q_PY_SCOPE_02", "x = 5\ndef mod(): x = 99\nmod()\nprint(x)", "99", [
                "Prints 99 because mod() reassigned x.",
                "The value of x is changed to 99 globally.",
                "x is now 99 after calling the function mod."
            ])
        ],
        "test_templates": [
            ("Q_PY_SCOPE_HELD_01", "total = 100\ndef add(): total = 200\nadd()\nprint(total)", "200", [
                "Outside total will print 200 because the function modified total.",
                "total is 200 because function assignment changed the outer total.",
                "The variable total was modified globally to 200."
            ])
        ]
    },
    "M005": {
        "name": "Missing Base Case in Recursion",
        "concept": "Recursion",
        "train_templates": [
            ("Q_PY_RECURSION_01", "def countdown(n): return countdown(n-1)", "Stops at 0", [
                "The function naturally stops when n reaches 0.",
                "It counts down 3, 2, 1, 0 and then finishes execution.",
                "Recursion automatically halts when n hits zero.",
                "It will return 0 when the countdown reaches the end.",
                "Python knows to stop recursion when the counter runs out.",
                "No error occurs because it finishes after 3 steps.",
                "It decrements n until 0 and returns none."
            ]),
            ("Q_PY_RECURSION_02", "def loop(x): return loop(x - 1)", "Terminates at zero", [
                "It will stop recurring once x reaches 0.",
                "The recursive call terminates when x becomes zero.",
                "It runs until x is 0 then returns."
            ])
        ],
        "test_templates": [
            ("Q_PY_RECURSION_HELD_01", "def f(k): return f(k - 1)", "Stops at 0", [
                "The function terminates when k reaches 0 without error.",
                "Recursion stops automatically when k reaches zero.",
                "It executes down to 0 and stops naturally."
            ])
        ]
    },
    "M006": {
        "name": "Mutable Default Argument Aliasing",
        "concept": "Function Defaults & Mutability",
        "train_templates": [
            ("Q_PY_MUTABLE_DEF_01", "def add(x, lst=[]): lst.append(x); return lst", "['apple'], ['banana']", [
                "Second call prints ['banana'] because lst defaults to a new empty list each call.",
                "Every call gets a fresh empty list [] so it prints ['apple'] then ['banana'].",
                "Default arguments are reset on each function invocation.",
                "lst is re-initialized to [] whenever add is called without parameters.",
                "Both calls return a single item list: ['apple'] and ['banana'].",
                "It won't keep previous items because default is [].",
                "Each function call is independent with a brand new default list."
            ]),
            ("Q_PY_MUTABLE_DEF_02", "def push(item, d={}): d[item]=1; return d", "{'a':1}, {'b':1}", [
                "Second call returns {'b': 1} because d is initialized to {} again.",
                "Default dictionary is created anew for each call.",
                "The dictionary starts empty every time push() is run."
            ])
        ],
        "test_templates": [
            ("Q_PY_MUTABLE_DEF_HELD_01", "def store(v, cache=[]): cache.append(v); return cache", "[v]", [
                "cache resets to empty list on every call so each result is just [v].",
                "Default parameter cache=[] creates a fresh list every invocation.",
                "It prints separate single-element lists because default is empty."
            ])
        ]
    },
    "M007": {
        "name": "While-Loop Mid-Body Termination",
        "concept": "While Loops & Control Flow",
        "train_templates": [
            ("Q_PY_WHILE_01", "x = 1\nwhile x < 3:\n x += 1\n print(x)", "Prints 2 only", [
                "When x becomes 3, x < 3 is false, so print(x) does not execute.",
                "The loop immediately stops mid-iteration the instant x hits 3.",
                "Only 2 is printed because when x reaches 3 the while condition fails right away.",
                "The print statement is skipped because 3 is not less than 3.",
                "The loop aborts immediately as soon as the condition turns false inside the body.",
                "It halts before the print on the second iteration.",
                "Execution terminates mid-body as soon as x becomes 3."
            ])
        ],
        "test_templates": [
            ("Q_PY_WHILE_HELD_01", "n = 0\nwhile n < 2:\n n += 1\n print('n is', n)", "Only prints 1", [
                "When n becomes 2, the loop stops immediately and doesn't print 2.",
                "The while condition stops the loop right when n increments to 2.",
                "It exits mid-body before printing n is 2."
            ])
        ]
    },
    "M008": {
        "name": "Integer Division Truncation",
        "concept": "Arithmetic Operators",
        "train_templates": [
            ("Q_PY_DIV_01", "print(7 // 2)", "3.5 or 4", [
                "7 // 2 gives 3.5 because // is division.",
                "7 // 2 rounds up to 4 because 3.5 rounds to 4.",
                "// performs standard division so the answer is 3.5.",
                "It rounds to the nearest integer which is 4.",
                "Double slash divides and keeps the decimal part 3.5.",
                "// is regular division in Python returning float 3.5."
            ])
        ],
        "test_templates": [
            ("Q_PY_DIV_HELD_01", "print(9 // 2)", "4.5 or 5", [
                "9 // 2 produces 4.5 like regular division.",
                "It rounds up to 5 because 4.5 rounds to nearest.",
                "Double slash // gives decimal result 4.5."
            ])
        ]
    },
    "M009": {
        "name": "1-Indexed Sequence Access",
        "concept": "Lists & Indexing",
        "train_templates": [
            ("Q_PY_INDEX_01", "colors = ['red', 'green', 'blue']; print(colors[1])", "red", [
                "colors[1] prints 'red' because 1 is the first element.",
                "The first item is at index 1 so it outputs red.",
                "Index 1 refers to the first position in the list.",
                "Python lists start at index 1 so colors[1] is red.",
                "colors[-1] will raise an IndexError because negative indices are invalid.",
                "Negative index -1 is an error in Python syntax."
            ])
        ],
        "test_templates": [
            ("Q_PY_INDEX_HELD_01", "items = ['first', 'second']; print(items[1])", "first", [
                "items[1] is 'first' because index 1 is the initial element.",
                "Lists begin with index 1 so the first element is returned.",
                "Index 1 accesses the first item."
            ])
        ]
    },
    "M010": {
        "name": "Boolean Operator Precedence",
        "concept": "Boolean Logic & Expressions",
        "train_templates": [
            ("Q_PY_BOOL_01", "result = True or False and False", "False", [
                "It evaluates to False because (True or False) is True, and True and False is False.",
                "Left to right evaluation: True or False is True, then True and False gives False.",
                "Python evaluates booleans strictly from left to right.",
                "or and and have the same precedence so it computes (True or False) first.",
                "False because the expression is read left-to-right giving False at the end."
            ])
        ],
        "test_templates": [
            ("Q_PY_BOOL_HELD_01", "val = False or True and False", "False", [
                "Evaluates left to right: (False or True) is True, then True and False is False.",
                "Left-to-right order makes the whole expression False.",
                "Computes or first because it appears first in the line."
            ])
        ]
    },
    "NONE": {
        "name": "No Misconception / Correct Reasoning",
        "concept": "General Python Programming",
        "train_templates": [
            ("Q_PY_RANGE_01", "for i in range(1, 5): print(i)", "1 2 3 4", [
                "It prints 1, 2, 3, 4 because range(1, 5) stops before 5 (exclusive upper bound).",
                "Output is 1, 2, 3, 4. Python range excludes the stop parameter.",
                "Generates 1 to 4 because the end value 5 is not included.",
                "range(1, 5) produces numbers starting at 1 up to but excluding 5.",
                "It will print 1, 2, 3, and 4."
            ]),
            ("Q_PY_COUNT_01", "count = 0\nfor i in range(5): count += 1", "Total: 5, Last: 4", [
                "Loop runs exactly 5 times (0, 1, 2, 3, 4), so count is 5 and last i is 4.",
                "range(5) produces 5 values from 0 to 4, total count is 5.",
                "Total is 5 because range(5) iterates 5 times."
            ]),
            ("Q_PY_ASSIGN_01", "if status = 'admin':", "SyntaxError", [
                "Throws SyntaxError because '=' is assignment, while '==' is needed for comparison.",
                "Invalid syntax because single equals cannot be used in an if condition.",
                "Python syntax error: you must use '==' to compare equality."
            ]),
            ("Q_PY_SCOPE_01", "val = 20\ndef f(): val = 50", "Inside: 50, Outside: 20", [
                "Inside is 50, outside is 20 because assigning val inside f creates a local variable.",
                "The outer val remains 20 because the local assignment shadows the global variable.",
                "Local variable inside function does not affect global variable outside."
            ]),
            ("Q_PY_MUTABLE_DEF_01", "def append_item(x, items=[]):", "['apple'], ['apple', 'banana']", [
                "Outputs ['apple'] then ['apple', 'banana'] because default list is shared across calls.",
                "Default argument items=[] is evaluated once at definition time, so it accumulates elements.",
                "The same list object is mutated across subsequent calls."
            ]),
            ("Q_PY_DIV_01", "print(7 // 2)", "3", [
                "7 // 2 is 3 because // performs floor division, rounding down to the nearest integer.",
                "Floor division truncates the decimal part, giving integer 3.",
                "Result is 3 because // is integer floor division."
            ]),
            ("Q_PY_INDEX_01", "print(colors[1])", "green", [
                "colors[1] prints 'green' because Python uses 0-based indexing (colors[0] is 'red').",
                "Index 1 accesses the second item which is 'green'.",
                "First index is 0, so index 1 gives 'green' and -1 gives 'yellow'."
            ]),
            ("Q_PY_BOOL_01", "True or False and False", "True", [
                "'and' has higher precedence than 'or', so 'False and False' is False, then 'True or False' is True.",
                "Evaluates to True because 'and' binds tighter than 'or'.",
                "True because operator precedence evaluates False and False first."
            ])
        ],
        "test_templates": [
            ("Q_PY_RANGE_HELD_01", "for val in range(2, 6): print(val)", "2 3 4 5", [
                "Prints 2, 3, 4, 5 because the upper bound 6 is excluded.",
                "range(2, 6) produces 2, 3, 4, 5. 6 is not included.",
                "Generates values 2 through 5, stopping before 6."
            ]),
            ("Q_PY_SCOPE_HELD_01", "c = 10\ndef f(): c = 30", "10", [
                "Outer c stays 10 because f() assigns to local c.",
                "Local c does not mutate outer scope variable.",
                "c remains 10 due to lexical scope."
            ])
        ]
    }
}

# Add Hard Negative Pairs where surface answers collide
# Example: Surface answer mentions '5' or '4' but for completely different reasons:
HARD_NEGATIVES = [
    {
        "question_id": "Q_PY_RANGE_01",
        "question": "What will this Python code print? Explain your reasoning.\n\nfor i in range(1, 5):\n    print(i)",
        "surface_answer": "5",
        "samples": [
            {
                "misconception_id": "M001",
                "response": "The last number printed is 5 because range(1, 5) goes all the way up to 5.",
                "reasoning_evidence": ["Believes stop value 5 is included in range generation"]
            },
            {
                "misconception_id": "M002",
                "response": "The loop prints 5 numbers because 5 - 1 is 4 plus 1 for the first element.",
                "reasoning_evidence": ["Confounds interval calculation with cardinality count"]
            },
            {
                "misconception_id": "NONE",
                "response": "The loop prints 1, 2, 3, 4. 5 is not printed because range excludes the upper bound.",
                "reasoning_evidence": ["Correctly excludes 5"]
            }
        ]
    },
    {
        "question_id": "Q_PY_COUNT_01",
        "question": "How many times does this loop execute?\n\nfor i in range(5): count += 1",
        "surface_answer": "4",
        "samples": [
            {
                "misconception_id": "M002",
                "response": "It executes 4 times because range(5) stops at 4 so only 4 iterations happen.",
                "reasoning_evidence": ["Miscounts total iterations by ignoring 0th index"]
            },
            {
                "misconception_id": "M001",
                "response": "It runs 4 times because 1, 2, 3, 4 are the numbers and it skipped 5.",
                "reasoning_evidence": ["Assumes 1-indexed range and missing endpoint"]
            },
            {
                "misconception_id": "NONE",
                "response": "It executes 5 times (0, 1, 2, 3, 4) so count is 5.",
                "reasoning_evidence": ["Correct count"]
            }
        ]
    }
]

def generate_samples():
    train_samples = []
    test_samples = []
    sample_id = 1

    for misc_id, meta in MISCONCEPTIONS.items():
        # Train templates
        for q_id, code, exp_out, responses in meta["train_templates"]:
            for resp in responses:
                # Add slight phrasing variations to enrich linguistic diversity
                variations = [
                    resp,
                    f"My answer: {resp}",
                    f"I think {resp.lower()}",
                    f"Explanation: {resp}"
                ] if misc_id != "NONE" else [resp, f"My answer: {resp}"]
                
                for v in variations:
                    train_samples.append({
                        "id": f"SMP_TR_{sample_id:04d}",
                        "question_id": q_id,
                        "question_code": code,
                        "expected_output": exp_out,
                        "learner_response": v,
                        "response_type": "text+code",
                        "correct": (misc_id == "NONE"),
                        "misconception_id": misc_id,
                        "misconception_name": meta["name"],
                        "concept": meta["concept"],
                        "difficulty": "beginner" if "RANGE" in q_id or "COUNT" in q_id or "DIV" in q_id else "intermediate",
                        "split": "train"
                    })
                    sample_id += 1

        # Test templates (Held-out question templates unseen in training)
        for q_id, code, exp_out, responses in meta["test_templates"]:
            for resp in responses:
                test_samples.append({
                    "id": f"SMP_TE_{sample_id:04d}",
                    "question_id": q_id,
                    "question_code": code,
                    "expected_output": exp_out,
                    "learner_response": resp,
                    "response_type": "text+code",
                    "correct": (misc_id == "NONE"),
                    "misconception_id": misc_id,
                    "misconception_name": meta["name"],
                    "concept": meta["concept"],
                    "difficulty": "beginner" if "RANGE" in q_id or "COUNT" in q_id or "DIV" in q_id else "intermediate",
                    "split": "test"
                })
                sample_id += 1

    # Add hard negatives into train and test
    for hn in HARD_NEGATIVES:
        for s in hn["samples"]:
            misc_id = s["misconception_id"]
            meta = MISCONCEPTIONS[misc_id]
            train_samples.append({
                "id": f"SMP_HN_{sample_id:04d}",
                "question_id": hn["question_id"],
                "question_code": hn["question"],
                "expected_output": hn["surface_answer"],
                "learner_response": s["response"],
                "response_type": "text+code",
                "correct": (misc_id == "NONE"),
                "misconception_id": misc_id,
                "misconception_name": meta["name"],
                "concept": meta["concept"],
                "difficulty": "intermediate",
                "is_hard_negative": True,
                "split": "train"
            })
            sample_id += 1

    random.shuffle(train_samples)
    random.shuffle(test_samples)

    return train_samples, test_samples

if __name__ == "__main__":
    train_data, test_data = generate_samples()
    base_dir = Path("C:/Users/arpit_24zh6yw/.gemini/antigravity/scratch/relearn/data")
    
    with open(base_dir / "training_dataset.json", "w", encoding="utf-8") as f:
        json.dump({"samples": train_data, "count": len(train_data)}, f, indent=2)

    with open(base_dir / "test_dataset.json", "w", encoding="utf-8") as f:
        json.dump({"samples": test_data, "count": len(test_data)}, f, indent=2)

    print(f"Generated {len(train_data)} training samples and {len(test_data)} test samples.")
