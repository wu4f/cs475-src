# Derived from https://github.com/OTRF/GenAI-Security-Adventures
# This script downloads the real-time Mitre ATT&CK information on a variety of
# attack groups, formats them in Markdown files, then loads them into a vector
# database (ChromaDB).  This is subsequently used in a RAG chain to handle
# queries through an LLM
from attackcti import attack_client
import os
import copy
from jinja2 import Template

current_directory = f"{os.path.dirname(__file__)}/04_data/"
documents_directory = os.path.join(current_directory, "documents")
contrib_directory = os.path.join(current_directory, "contrib")
for directory in [documents_directory, contrib_directory]:
   if not os.path.exists(directory):
     os.makedirs(directory)

lift = attack_client()
techniques_used_by_groups = lift.get_techniques_used_by_all_groups()
techniques_used_by_groups[0]

# Create Group docs
all_groups = dict()
for technique in techniques_used_by_groups:
    if technique['id'] not in all_groups:
        group = dict()
        group['group_name'] = technique['name']
        group['group_id'] = technique['external_references'][0]['external_id']
        group['created'] = technique['created']
        group['modified'] = technique['modified']
        group['description'] = technique['description']
        group['aliases'] = technique['aliases']
        if 'x_mitre_contributors' in technique:
            group['contributors'] = technique['x_mitre_contributors']
        group['techniques'] = []
        all_groups[technique['id']] = group
    technique_used = dict()
    technique_used['matrix'] = technique['matrix']
    technique_used['domain'] = technique['x_mitre_domains']
    technique_used['platform'] = technique['platform']
    technique_used['tactics'] = technique['tactic']
    technique_used['technique_id'] = technique['technique_id']
    technique_used['technique_name'] = technique['technique']
    technique_used['use'] = technique['relationship_description']
    if 'data_sources' in technique:
        technique_used['data_sources'] = technique['data_sources']
    all_groups[technique['id']]['techniques'].append(technique_used)

print("[+] Creating markdown files for each group..")
group_template = os.path.join(current_directory, "group_template.md")
markdown_template = Template(open(group_template).read())
for key in list(all_groups.keys()):
    group = all_groups[key]
    print("  [>>] Creating markdown file for {}..".format(group['group_name']))
    group_for_render = copy.deepcopy(group)
    markdown = markdown_template.render(metadata=group_for_render, group_name=group['group_name'], group_id=group['group_id'])
    file_name = (group['group_name']).replace(' ','_')
    open(f'{documents_directory}/{file_name}.md', encoding='utf-8', mode='w').write(markdown)

import glob
from langchain_community.document_loaders import UnstructuredMarkdownLoader
group_files = glob.glob(os.path.join(documents_directory, "*.md"))

# Loading Markdown files
md_docs = []
print("[+] Loading Group markdown files..")
for group in group_files:
    print(f' [*] Loading {os.path.basename(group)}')
    loader = UnstructuredMarkdownLoader(group)
    md_docs.extend(loader.load())

print(f'[+] Number of .md documents processed: {len(md_docs)}')

import tiktoken
tokenizer = tiktoken.encoding_for_model('gpt-3.5-turbo')
token_integers = tokenizer.encode(md_docs[0].page_content, disallowed_special=())
num_tokens = len(token_integers)
token_bytes = [tokenizer.decode_single_token_bytes(token) for token in token_integers]

def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=() #To disable this check for all special tokens
    )
    return len(tokens)

# Get token counts
token_counts = [tiktoken_len(doc.page_content) for doc in md_docs]

print(f"""[+] Token Counts:
Min: {min(token_counts)}
Avg: {int(sum(token_counts) / len(token_counts))}
Max: {max(token_counts)}""")
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Chunking Text
print('[+] Initializing RecursiveCharacterTextSplitter..')
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,  # number of tokens overlap between chunks
    length_function=tiktoken_len,
    separators=['\n\n', '\n', ' ', '']
)
print('[+] Splitting documents in chunks..')
chunks = text_splitter.split_documents(md_docs)

print(f'[+] Number of documents: {len(md_docs)}')
print(f'[+] Number of chunks: {len(chunks)}')

import hashlib
json_documents = []
m = hashlib.md5()
for doc in md_docs:
    doc_name = os.path.basename(doc.metadata['source'])
    m.update(doc_name.encode('utf-8'))
    uid = m.hexdigest()[:12]
    chunks_strings = text_splitter.split_text(doc.page_content)
    for i, chunk in enumerate(chunks_strings):
        # Add JSON object to array
        json_documents.append({
            'id': f'{uid}-{i}',
            'text': chunk,
            'source': doc_name
        })

import json
print(f'[+] Exporting groups as .jsonl file..')
with open(f'{os.path.join(contrib_directory, "attack-groups.jsonl")}', 'w') as f:
    for doc in json_documents:
        f.write(json.dumps(doc) + '\n')

# Ingest into document store using an open-source sentence transformer embedding model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
# Define the open-source embedding function
embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001", task_type="retrieval_query")

# Load documents into Chroma and save it to disk
db = Chroma.from_documents(chunks, embedding_function, collection_name="groups_collection", persist_directory=f"{current_directory}/chroma_db")

# Test ingestion with an initial query
query = "What threat actors send text messages to their targets?"
print(f'[+] Test similarity search with query: {query}')
relevant_docs = db.similarity_search(query)

print(f'[+] Results of retrieval for query: {query}')
print(relevant_docs[0].page_content)
