import json
from openai import OpenAI
import pandas as pd
import numpy as np
from getpass import getpass
import time
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SimpleField, SearchFieldDataType, SearchIndex
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

import main2

#
# credential = EnvironmentCredential()
api_key = "sk-proj-FhWYYZqWl0Ls2N12NvHOT3BlbkFJFlC955c5Yefhk4kuU2Qi"
pdf_path = 'resume/SabarishMN_MS_CPE.pdf'
client = OpenAI(api_key=api_key)
account_url = "https://sabarishmnblob.blob.core.windows.net"
search_service_name = "sabaaisvc"
search_svc_endpoint = "https://sabaaisvc.search.windows.net"
index_name = "resume_index"
default_credential = DefaultAzureCredential()
credential = AzureKeyCredential("NkXz0p9WRzXLlzhwjV1MbkwrCinPl20CknsQalAdxRAzSeArgRcu")
blob_service_client = BlobServiceClient(account_url, credential=default_credential)
search_client = SearchClient(endpoint=search_svc_endpoint, index_name=index_name, credential=credential)
index_client = SearchIndexClient(endpoint=search_svc_endpoint, credential=credential)


def get_embedding(x, engine):
    response = client.embeddings.create(
        input=x,
        model=engine
    )
    return response.data[0].embedding




    # with open('resume.json', 'r', encoding='utf-8') as file:
    #     resume_data = json.load(file)
    #     print(resume_data)
    df = pd.read_csv('resume/resume.csv')
    # print(df)
    df['embedding'] = df['text'].apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))
    df.to_csv('resume_embeddings.csv')


    df_em = pd.read_csv('resume/resume_embeddings.csv')
    df_em['embedding'] = df_em['embedding'].apply(eval).apply(np.array)
    print(df_em['embedding'][0].shape)
    # print(df_em.columns[0])
    df_em.rename(columns={df_em.columns[0]: 'id', df_em.columns[1]: 'content', df_em.columns[2]: 'content_vector'},
                 inplace=True)
    # attributes : id, content, content_vector
    print(df_em.columns)
    # print(df_em.dtypes)
    filename = "resume/resume_em.json"
    df_em.to_json(filename, orient="records", index=4)


def vector_search(query_vector, top_k=5):
    vector_query = VectorizedQuery(vector=query_vector, k_nearest_neighbors=top_k, fields="content_vector",
                                   exhaustive=True)
    results = search_client.search(
        search_text="*",
        vector_queries=[vector_query],
        select=["id", "content"],
        top=5

    )
    return results


    user_query = input("How can I help you ? ")
    user_query_term_vector = get_embedding(user_query, engine="text-embedding-ada-002")
    results = vector_search(user_query_term_vector, 5)
    data_to_search = []
    for result in results:
        print(result['id'])
        print(result['content'])
        data_to_search.append(result['content'])
        # print(f"Score: {result['@search.score']}")
        print("----")
    print(" ##############  ")
    prompt = "Users Question : " + user_query + "Documents provided:"
    for index, value in enumerate(data_to_search, 1):
        prompt += (f"document {index}: \"value of row {index}\" {value}")
    print(prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant designed to answer users question based on the documents provided. If you don't find the answer based on the documents provided, please respond you couldn't find any information based on the documents provided."},
            {"role": "user", "content": "" + prompt + ""}
        ]
    )
    print(response.choices[0].message.content)


def writeBlob(filename):
    blob_client = blob_service_client.get_blob_client(container="cont1", blob=filename)

    print("\nUploading to Azure Storage as blob:\n\t" + filename)

    # Upload the created file
    with open(file=filename, mode="rb") as data:
        blob_client.upload_blob(data, overwrite=True)



if __name__ == '__main__':
 