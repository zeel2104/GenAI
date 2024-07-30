#from azure.storage.table import TableService, Entity
from azure.data.tables import TableServiceClient
from azure.core.credentials import AzureNamedKeyCredential
from azure.core.exceptions import ResourceExistsError

# Azure Storage account details
account_name = 'zeelres1'
account_key = 'JLgYKRr6I7+CvmETn5BRHCEq84Krvvt8LxELbLMPW0yj2ERdrM5L1jWt0u0M8JjMjf2LHVjZU72S+AStePUKpA=='  # Replace with your actual storage account key
table_name = 'QB2'  # Name of the table you want to create

# Create a TableServiceClient using account_name and account_key
connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};"
table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)

# Create a table client
table_client = table_service_client.get_table_client(table_name)


# Create the table if it doesn't already exist
try:
    table_client.create_table()
    print(f"Table '{table_name}' created successfully.")
except ResourceExistsError:
    print(f"Table '{table_name}' already exists.")

# Example JSON data (replace this with your actual JSON data)
json_data = {
    "questions": [
        {
            "PartitionKey": "Logical Reasoning",
            "RowKey": "1",
            "Question": "If APPLE is coded as 95228, ORANGE is coded as: A) 621539 B) 414686 C) 843787 D) 763582",
            "Answer": "D",
            "Difficulty": "Easy",
            "Options": ["A) 621539", "B) 414686", "C) 843787", "D) 763582"]
        },
        {
            "PartitionKey": "Logical Reasoning",
            "RowKey": "2",
            "Question": "Statement: All dogs are loyal. Conclusion: Max is loyal. A) True B) False C) Cannot be determined D) None of these",
            "Answer": "A",
            "Difficulty": "Medium",
            "Options": ["A) True", "B) False", "C) Cannot be determined", "D) None of these"]
        },
        {
            "PartitionKey": "Logical Reasoning",
            "RowKey": "3",
            "Question": "If all Kites are Birds, and some Birds are Owls, then some Kites are definitely Owls: A) True B) False C) Cannot be determined D) None of these",       
            "Answer": "A",
            "Difficulty": "Hard",
            "Options": ["A) True", "B) False", "C) Cannot be determined", "D) None of these"]
        },
        {
            "PartitionKey": "Numerical Aptitude",
            "RowKey": "4",
            "Question": "What is the next number in the series: 2, 5, 10, 17, ? A) 24 B) 26 C) 28 D) 30",
            "Answer": "A",
            "Difficulty": "Easy",
            "Options": ["A) 24", "B) 26", "C) 28", "D) 30"]
        },
        {
            "PartitionKey": "Numerical Aptitude",
            "RowKey": "5",
            "Question": "If the price of a product is increased by 20%, by what percentage should it be reduced to bring it back to the original price? A) 16% B) 18% C) 20% D) 25%",
            "Answer": "C",
            "Difficulty": "Medium",
            "Options": ["A) 16%", "B) 18%", "C) 20%", "D) 25%"]
        },
        {
            "PartitionKey": "Numerical Aptitude",
            "RowKey": "6",
            "Question": "Find the missing number in the series: 1, 4, 9, ?, 25 A) 12 B) 13 C) 14 D) 15",
            "Answer": "C",
            "Difficulty": "Hard",
            "Options": ["A) 12", "B) 13", "C) 14", "D) 15"]
        },
        {
            "PartitionKey": "Verbal",
            "RowKey": "7",
            "Question": "Choose the word which is most similar to the word 'Brave': A) Cowardly B) Timid C) Courageous D) Fearful",
            "Answer": "C",
            "Difficulty": "Easy",
            "Options": ["A) Cowardly", "B) Timid", "C) Courageous", "D) Fearful"]
        },
        {
            "PartitionKey": "Verbal",
            "RowKey": "8",
            "Question": "Identify the synonym for the word 'Ponder': A) Consider B) Neglect C) Ignore D) Dismiss",
            "Answer": "A",
            "Difficulty": "Medium",
            "Options": ["A) Consider", "B) Neglect", "C) Ignore", "D) Dismiss"]
        },
        {
            "PartitionKey": "Verbal",
            "RowKey": "9",
            "Question": "Choose the word which is most opposite to the word 'Generous': A) Selfish B) Stingy C) Greedy D) Frugal",
            "Answer": "A",
            "Difficulty": "Hard",
            "Options": ["A) Selfish", "B) Stingy", "C) Greedy", "D) Frugal"]
        }
        # Add more questions as needed
    ]
}

# # Insert JSON data into Azure Table
# for idx, question in enumerate(json_data['questions'], start=1):
#     task = {
#         'PartitionKey': 'questions',
#         'RowKey': f'question_{idx}',
#         'Question': question['question'],
#         'Answer': question['answer'],
#         'Difficulty': question['difficulty'],
#         'Options': ', '.join(question['options']) if question['options'] else ''
#     }
#     table_service.insert_entity(table_name, task)

# print(f"Data inserted into Azure Table '{table_name}' successfully.")



# Insert JSON data into Azure Table
for question in json_data['questions']:
    entity = {
        'PartitionKey': question['PartitionKey'],
        'RowKey': question['RowKey'],
        'Question': question['Question'],
        'Answer': question['Answer'],
        'Difficulty': question['Difficulty'],
        'Options': ', '.join(question['Options']) if question['Options'] else ''
    }
    try:
        table_client.upsert_entity(mode='merge', entity=entity)
        print(f"Entity inserted successfully.")
    except Exception as e:
        print(f"Failed to insert entity : {str(e)}")