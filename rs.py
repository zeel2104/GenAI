import m

import json


def convert_to_json(content):
    return {
        "Partionkey": ["PartitionKey"] ,
        "Rowkey": ["RowKey"],
        "subcategory": ["Subcategory"],
        "question": ["Question"],
        "answer": ["Answer"],  # Placeholder for answer (to be filled as per requirement)
        "difficulty": ["Difficulty"],  # Placeholder for difficulty (to be filled as per requirement)
        "options": ["Options"]  # Placeholder for options (to be filled as per requirement)
    }
def write_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)



# Main function to generate and print questions
def main():
    Logical="Analogies, Logical Deduction, Logical Connectives, Syllogisms, Verbal Reasoning, Analytical Reasoning, Critical Reasoning, Statement and Assumption, Cause and Effect, Seating Arrangements, Coding-Decoding, Blood Relations, Direction Sense, Series Completion, Data Sufficiency, Mathematical Operations, Decision Making, Assertion and Reason, Inferences, Non-Verbal Reasoning."
    Numerical= "Basic Arithmetic, Percentages, Ratio and Proportion, Averages, Interest, Profit and Loss, Time and Work, Time Speed and Distance, Permutation and Combination, Probability, Number Series, Data Interpretation, Mensuration, Algebra, Geometry, Trigonometry, Logarithms, Progressions, Matrices and Determinants, Indices and Surds"
    Verbal="Sentence Completion, Analogies, Antonyms and Synonyms, Logical Deduction, Vocabulary, Grammar and Syntax, Inference, Verbal Classification, Statement and Conclusion, Word Formation, Sentence Correction, Logical Games, Decoding and Coding, Analogical Reasoning, Inference and Judgement"
   
    prompt = """Generate a question bank for mental ability questions. It should have 3 categories Logical reasoning, Numerical aptitude, and Verbal. The subtopics are in the Logical, Numerical and Verbal String
    
1. PartitionKey: [List as (Partionkey=logical reasoning or numerical aptitude or verbal comprehension]
2. RowKey: [Assign question number in order]
3. Subcategory: [Topic of questions, Eg:Percentages, Ratio and proportion, Profit and Loss,Blood Relation...etc]
4. Question: [The question should be objective]
5. Answer: [Provide the correct answer to the question]
6. Difficulty: [Indicate the difficulty level (e.g., Easy, Medium, Hard)]
7. Options: [Give 4 options(A, B, C, D) with one of them as correct answer and other three incorrect for every question, store it in an array]

Use book (Verbal Ability and Reading Comprehension by Arun Sharma and Meenakshi Upadhyay) for verbal questions
Use RS Aggarwal's books as a reference for the style and content of the questions. But the questions should not be exact same, there can be a change in name etc
Questions should be of higher difficulty level suitable for master's students for company recruitment for technical roles.
Give answer in json format with all 7 in one heirarchy




"""


    # Print generated question

    prompt=prompt+Logical+Numerical+Verbal
    result=m.generate_questions(prompt)
    print(result)
    json_output = convert_to_json(result)
    
    # Define output file name
    output_file = 'generated_questions.json'
    
    # Write JSON output to file
    write_to_file(json_output, output_file)
    
    print(f"Generated questions JSON file saved as '{output_file}'.")

 

if __name__ == "__main__":
    main()
