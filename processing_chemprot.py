import constants
from collections import defaultdict
import re

datasets = ['training', 'development', 'test']

doc_titles = defaultdict()
doc_abstracts = defaultdict()
doc_entities = defaultdict(list)
doc_relations = defaultdict(list)

for dataset in datasets:
    if dataset == 'training':
        text_docs = open(constants.CHEMPROT + dataset + '/chemprot_' + dataset + '_abstracts.tsv', 'r',
                         encoding='utf-8')
        entity_docs = open(constants.CHEMPROT + dataset + '/chemprot_' + dataset + '_entities.tsv', 'r',
                           encoding='utf-8')
        relation_docs = open(constants.CHEMPROT + dataset + '/chemprot_' + dataset + '_gold_standard.tsv', 'r',
                             encoding='utf-8')
    elif dataset == 'development':
        text_docs = open(constants.CHEMPROT + dataset + '/chemprot_' + dataset + '/chemprot_' + dataset + '_abstracts'
                                                                                                          '.tsv', 'r',
                         encoding='utf-8')
        entity_docs = open(
            constants.CHEMPROT + dataset + '/chemprot_' + dataset + '/chemprot_' + dataset + '_entities.tsv', 'r',
            encoding='utf-8')
        relation_docs = open(
            constants.CHEMPROT + dataset + '/chemprot_' + dataset + '/chemprot_' + dataset + '_gold_standard.tsv', 'r',
            encoding='utf-8')
    else:
        text_docs = open(
            constants.CHEMPROT + dataset + '_gs/chemprot_' + dataset + '_gs/chemprot_' + dataset + '_abstracts_gs.tsv',
            'r', encoding='utf-8')
        entity_docs = open(
            constants.CHEMPROT + dataset + '_gs/chemprot_' + dataset + '_gs/chemprot_' + dataset + '_entities_gs.tsv',
            'r', encoding='utf-8')
        relation_docs = open(
            constants.CHEMPROT + dataset + '_gs/chemprot_' + dataset + '_gs/chemprot_' + dataset + '_gold_standard.tsv',
            'r', encoding='utf-8')

    for line in text_docs.readlines():
        doc_idx, title, abstract = line.split('\t')
        doc_titles[doc_idx] = doc_idx + '|t|' + title.strip() + '\n'
        doc_abstracts[doc_idx] = doc_idx + '|a|' + abstract.strip() + '\n'

    for line in entity_docs.readlines():
        doc_idx, ent_idx, ent_type, start_offset, end_offset, ent_name = line.split('\t')
        ent_idx = doc_idx + ent_idx
        doc_entities[doc_idx].append('{}\t{}\t{}\t{}\t{}\t{}\n'.format(doc_idx, start_offset, end_offset, ent_name.strip(),
                                                                       ent_type.strip(), ent_idx.strip()))

    for line in relation_docs.readlines():
        doc_idx, rel_type, e1, e2 = line.split('\t')
        e1 = doc_idx + re.sub(r"Arg\d:", '', e1)
        e2 = doc_idx + re.sub(r"Arg\d:", '', e2)
        doc_relations[doc_idx].append('{}\t{}\t{}\t{}\n'.format(doc_idx, rel_type, e1.strip(), e2.strip()))

    with open(constants.CHEMPROT + 'processed/chemprot_data.' + dataset + '.txt', 'w', encoding='utf-8') as f:
        for idx in doc_titles:
            f.write(doc_titles[idx])
            f.write(doc_abstracts[idx])
            for elem in doc_entities[idx]:
                f.write(elem)
            for elem in doc_relations[idx]:
                f.write(elem)
