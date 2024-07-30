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

document_analysis_client = DocumentAnalysisClient(
    endpoint=rec_endpoint, credential=AzureKeyCredential(rec_key)
)

def get_embedding(x, engine='text-embedding-ada-002'):
    response = client.embeddings.create(
        input=x,
        model=engine
    )
    return response.data[0].embedding
def startAnalysis():
    form_urls = os.listdir("documents_invoice")
    print(form_urls)
    # id , entity_id , content , content_vector
    for index, url in enumerate(form_urls, 1):
        data = {}
        with open("documents_invoice/" + url, "rb") as file:
            poller = document_analysis_client.begin_analyze_document("prebuilt-invoice", file)
            invoices = poller.result()
            for idx1, invoice in enumerate(invoices.documents):
                print("--------Recognizing invoice #{}--------".format(index))
                invoice_id = invoice.fields.get("InvoiceId")
                if invoice_id:
                    print(f"Invoice Id: {invoice_id.value} has confidence: {invoice_id.confidence}")
                    data["invoice_id"] = invoice_id.value

                vendor_name = invoice.fields.get("VendorName")
                if vendor_name:
                    print(f"Vendor Name: {vendor_name.value} has confidence: {vendor_name.confidence}")
                    data["vendor_name"] = vendor_name.value

                vendor_address = invoice.fields.get("VendorAddress")
                if vendor_address:
                    print(f"Vendor Address: {vendor_address.value} has confidence: {vendor_address.confidence}")
                    data["vendor_address"] = vendor_address.value

                vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
                if vendor_address_recipient:
                    print(
                        f"Vendor Address Recipient: {vendor_address_recipient.value} has confidence: {vendor_address_recipient.confidence}")
                    data["vendor_address_recipient"] = vendor_address_recipient.value

                customer_name = invoice.fields.get("CustomerName")
                if customer_name:
                    print(f"Customer Name: {customer_name.value} has confidence: {customer_name.confidence}")
                    data["customer_name"] = customer_name.value

                customer_id = invoice.fields.get("CustomerId")
                if customer_id:
                    print(f"Customer Id: {customer_id.value} has confidence: {customer_id.confidence}")
                    data["customer_id"] = customer_id.value

                customer_address = invoice.fields.get("CustomerAddress")
                if customer_address:
                    print(f"Customer Address: {customer_address.value} has confidence: {customer_address.confidence}")
                    data["customer_address"] = customer_address.value

                customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
                if customer_address_recipient:
                    print(
                        f"Customer Address Recipient: {customer_address_recipient.value} has confidence: {customer_address_recipient.confidence}")
                    data["customer_address_recipient"] = customer_address_recipient.value

                invoice_date = invoice.fields.get("InvoiceDate")
                if invoice_date:
                    print(f"Invoice Date: {invoice_date.value} has confidence: {invoice_date.confidence}")
                    data["invoice_date"] = invoice_date.value

                invoice_total = invoice.fields.get("InvoiceTotal")
                if invoice_total:
                    print(f"Invoice Total: {invoice_total.value} has confidence: {invoice_total.confidence}")
                    data["invoice_total"] = invoice_total.value

                due_date = invoice.fields.get("DueDate")
                if due_date:
                    print(f"Due Date: {due_date.value} has confidence: {due_date.confidence}")
                    data["due_date"] = due_date.value

                purchase_order = invoice.fields.get("PurchaseOrder")
                if purchase_order:
                    print(f"Purchase Order: {purchase_order.value} has confidence: {purchase_order.confidence}")
                    data["purchase_order"] = purchase_order.value

                billing_address = invoice.fields.get("BillingAddress")
                if billing_address:
                    print(f"Billing Address: {billing_address.value} has confidence: {billing_address.confidence}")
                    data["billing_address"] = billing_address.value

                billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
                if billing_address_recipient:
                    print(
                        f"Billing Address Recipient: {billing_address_recipient.value} has confidence: {billing_address_recipient.confidence}")
                    data["billing_address_recipient"] = billing_address_recipient.value

                shipping_address = invoice.fields.get("ShippingAddress")
                if shipping_address:
                    print(f"Shipping Address: {shipping_address.value} has confidence: {shipping_address.confidence}")
                    data["shipping_address"] = shipping_address.value

                shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
                if shipping_address_recipient:
                    print(
                        f"Shipping Address Recipient: {shipping_address_recipient.value} has confidence: {shipping_address_recipient.confidence}")
                    data["shipping_address_recipient"] = shipping_address_recipient.value

                # Handle invoice items
                invoice_items = []
                for idx, item in enumerate(invoice.fields.get("Items").value):
                    item_data = {}
                    print(f"...Item #{idx + 1}")
                    item_description = item.value.get("Description")
                    if item_description:
                        print(
                            f"......Description: {item_description.value} has confidence: {item_description.confidence}")
                        item_data["description"] = item_description.value

                    item_quantity = item.value.get("Quantity")
                    if item_quantity:
                        print(f"......Quantity: {item_quantity.value} has confidence: {item_quantity.confidence}")
                        item_data["quantity"] = item_quantity.value

                    unit = item.value.get("Unit")
                    if unit:
                        print(f"......Unit: {unit.value} has confidence: {unit.confidence}")
                        item_data["unit"] = unit.value

                    unit_price = item.value.get("UnitPrice")
                    if unit_price:
                        print(f"......Unit Price: {unit_price.value} has confidence: {unit_price.confidence}")
                        item_data["unit_price"] = unit_price.value

                    product_code = item.value.get("ProductCode")
                    if product_code:
                        print(f"......Product Code: {product_code.value} has confidence: {product_code.confidence}")
                        item_data["product_code"] = product_code.value

                    item_date = item.value.get("Date")
                    if item_date:
                        print(f"......Date: {item_date.value} has confidence: {item_date.confidence}")
                        item_data["date"] = item_date.value

                    tax = item.value.get("Tax")
                    if tax:
                        print(f"......Tax: {tax.value} has confidence: {tax.confidence}")
                        item_data["tax"] = tax.value

                    amount = item.value.get("Amount")
                    if amount:
                        print(f"......Amount: {amount.value} has confidence: {amount.confidence}")
                        item_data["amount"] = amount.value

                    # Add the item data to the invoice items list
                    invoice_items.append(item_data)

                # Add the invoice items to the main data dictionary
                data["items"] = invoice_items

                # Add any remaining fields
                subtotal = invoice.fields.get("SubTotal")
                if subtotal:
                    print(f"Subtotal: {subtotal.value} has confidence: {subtotal.confidence}")
                    data["subtotal"] = subtotal.value

                total_tax = invoice.fields.get("TotalTax")
                if total_tax:
                    print(f"Total Tax: {total_tax.value} has confidence: {total_tax.confidence}")
                    data["total_tax"] = total_tax.value

                previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
                if previous_unpaid_balance:
                    print(
                        f"Previous Unpaid Balance: {previous_unpaid_balance.value} has confidence: {previous_unpaid_balance.confidence}")
                    data["previous_unpaid_balance"] = previous_unpaid_balance.value

                amount_due = invoice.fields.get("AmountDue")
                if amount_due:
                    print(f"Amount Due: {amount_due.value} has confidence: {amount_due.confidence}")
                    data["amount_due"] = amount_due.value

                service_start_date = invoice.fields.get("ServiceStartDate")
                if service_start_date:
                    print(
                        f"Service Start Date: {service_start_date.value} has confidence: {service_start_date.confidence}")
                    data["service_start_date"] = service_start_date.value

                service_end_date = invoice.fields.get("ServiceEndDate")
                if service_end_date:
                    print(f"Service End Date: {service_end_date.value} has confidence: {service_end_date.confidence}")
                    data["service_end_date"] = service_end_date.value

                service_address = invoice.fields.get("ServiceAddress")
                if service_address:
                    print(f"Service Address: {service_address.value} has confidence: {service_address.confidence}")
                    data["service_address"] = service_address.value

                service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
                if service_address_recipient:
                    print(
                        f"Service Address Recipient: {service_address_recipient.value} has confidence: {service_address_recipient.confidence}")
                    data["service_address_recipient"] = service_address_recipient.value

                remittance_address = invoice.fields.get("RemittanceAddress")
                if remittance_address:
                    print(
                        f"Remittance Address: {remittance_address.value} has confidence: {remittance_address.confidence}")
                    data["remittance_address"] = remittance_address.value

                remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
                if remittance_address_recipient:
                    print(
                        f"Remittance Address Recipient: {remittance_address_recipient.value} has confidence: {remittance_address_recipient.confidence}")
                    data["remittance_address_recipient"] = remittance_address_recipient.value

                print("----------------------------------------")

def writeBlob(filename):
    blob_client = blob_service_client.get_blob_client(container="cont1", blob=filename)

    print("\nUploading to Azure Storage as blob:\n\t" + filename)

    # Upload the created file
    with open(file=filename, mode="rb") as data:
        blob_client.upload_blob(data, overwrite=True)



if __name__ == '__main__':
 