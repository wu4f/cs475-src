# Derived from https://github.com/OTRF/GenAI-Security-Adventures
# This script downloads the real-time Mitre ATT&CK information on a variety of
# attack groups, formats them in Markdown files, then loads them into a vector
# database (ChromaDB).  This is subsequently used in a RAG chain to handle
# queries through an LLM
from attackcti import attack_client
import os
import re
import copy
from jinja2 import Template

current_directory = f"{os.path.dirname(__file__)}/mitre_rag_data/"
documents_directory = os.path.join(current_directory, "documents")
if not os.path.exists(documents_directory):
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
    technique_used['matrix'] = technique['technique_matrix']
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
