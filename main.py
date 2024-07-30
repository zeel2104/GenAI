import m

import json


def convert_to_json(content):
    return {
        "question": content.strip(),
        "answer": "",  # Placeholder for answer (to be filled as per requirement)
        "difficulty": "",  # Placeholder for difficulty (to be filled as per requirement)
        "options": []  # Placeholder for options (to be filled as per requirement)
    }
def write_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)



# Main function to generate and print questions
def main():
    prompt = """Generate a question bank for mental ability questions. Each question should test a different aspect of mental ability such as logical reasoning, numerical aptitude, and verbal comprehension. It should include the topics like  Include the following for each question:
    
1. Question: [The question should be objective]
2. Answer: [Provide the correct answer to the question]
3. Difficulty: [Indicate the difficulty level (e.g., Easy, Medium, Hard)]
4. Options: [Give 4 options with one of them as correct answer and other three incorrect for every question]


"""


    # Print generated questions

    
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
