import constants
from collections import defaultdict
import re


def get_biogrid_id(text):
    all_biogrid = re.findall(r"biogrid:(\d+(\|*))", text)
    ids = []
    for elem in all_biogrid:
        for e in elem:
            if e != '|':
                e = re.sub(r"\|", '', e)
                if e not in ids:
                    ids.append(e)
    if len(ids) == 1:
        return ids[0]
    elif len(ids) == 0:
        return ''
    else:
        return '|'.join(ids)


def clean_name(text):
    res = []
    all_names = text.split('|')
    for elem in all_names:
        res.append(elem.split(':')[-1])
    return '|'.join(res)


def create_prot_dict():
    biogrid_entity_list = defaultdict(list)

    with open('ChemProt_Corpus/BIOGRID-ALL-4.4.217.mitab.txt', 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            elems = line.split('\t')
            ids_a = '|'.join([elems[0], elems[2]])
            ids_b = '|'.join([elems[1], elems[3]])
            # print(ids)
            bio_id_a = get_biogrid_id(ids_a)
            bio_id_b = get_biogrid_id(ids_b)
            name_a = clean_name('|'.join([elems[0], elems[2], elems[4]])).split('|')
            name_b = clean_name('|'.join([elems[1], elems[3], elems[5]])).split('|')

            biogrid_entity_list[bio_id_a].extend(name_a)
            biogrid_entity_list[bio_id_b].extend(name_b)

    for k in biogrid_entity_list:
        biogrid_entity_list[k] = list(set(biogrid_entity_list[k]))

    return biogrid_entity_list


def create_chem_dict():
    biogrid_entity_list = defaultdict(list)
    with open('ChemProt_Corpus/BIOGRID-CHEMICALS-4.4.217.chemtab.txt', 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            elems = line.split('\t')
            id = elems[13]
            # print(ids)
            name = elems[14].split('|') + elems[15].split('|') + elems[16].split('|')
            biogrid_entity_list[id].extend(name)
        #
        for k in biogrid_entity_list:
            biogrid_entity_list[k] = list(set(biogrid_entity_list[k]))
            if '-' in biogrid_entity_list[k]:
                biogrid_entity_list[k].remove('-')
    return biogrid_entity_list


def create_relation_dict():
    biogrid_relation_list = defaultdict(list)
    with open('ChemProt_Corpus/BIOGRID-ALL-4.4.217.mitab.txt', 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            elems = line.split('\t')
            ids_a = '|'.join([elems[0], elems[2]])
            ids_b = '|'.join([elems[1], elems[3]])

            bio_id_a = get_biogrid_id(ids_a)
            bio_id_b = get_biogrid_id(ids_b)

            rel = get_biogrid_id(elems[13])

            biogrid_relation_list[(bio_id_a, bio_id_b)].append(rel)
    return biogrid_relation_list


datasets = ['training', 'development', 'test']

biogrid_prot_ids = create_prot_dict()
biogrid_chem_ids = create_chem_dict()

# for k in biogrid_prot_ids:
#     # print("key: {} \t entity: {}".format(k, biogrid_chem_ids[k]))
#     if 'ACS1' in biogrid_prot_ids[k]:
#         print("found:\t{} in\tkey: {}".format('ACS1', biogrid_prot_ids[k]))
#     else:
#         # print("not found:\t{} in\tkey: {}".format('ACS1', k))
#         pass

# for key in all_keys:
#     print(key)
#     print(entity_ids[key])

for dataset in datasets:
    print("Processing dataset: {}...".format(dataset))
    if dataset == 'training':
        text_docs = open('ChemProt_Corpus/chemprot_training/chemprot_training_abstracts.tsv', 'r',
                         encoding='utf-8')
        entity_docs = open('ChemProt_Corpus/chemprot_training/chemprot_training_entities.tsv', 'r',
                           encoding='utf-8')
        relation_docs = open('ChemProt_Corpus/chemprot_training/chemprot_training_gold_standard.tsv', 'r',
                             encoding='utf-8')
    elif dataset == 'development':
        text_docs = open('ChemProt_Corpus/chemprot_development/chemprot_development/chemprot_development_abstracts.tsv',
                         'r', encoding='utf-8')
        entity_docs = open(
            'ChemProt_Corpus/chemprot_development/chemprot_development/chemprot_development_entities.tsv', 'r',
            encoding='utf-8')
        relation_docs = open(
            'ChemProt_Corpus/chemprot_development/chemprot_development/chemprot_development_gold_standard.tsv', 'r',
            encoding='utf-8')
    else:
        text_docs = open(
            'ChemProt_Corpus/chemprot_test_gs/chemprot_test_gs/chemprot_test_abstracts_gs.tsv',
            'r', encoding='utf-8')
        entity_docs = open(
            'ChemProt_Corpus/chemprot_test_gs/chemprot_test_gs/chemprot_test_entities_gs.tsv',
            'r', encoding='utf-8')
        relation_docs = open(
            'ChemProt_Corpus/chemprot_test_gs/chemprot_test_gs/chemprot_test_gold_standard.tsv',
            'r', encoding='utf-8')

    doc_titles = defaultdict()
    doc_abstracts = defaultdict()
    doc_entities = defaultdict(list)
    doc_relations = defaultdict(list)

    for line in text_docs.readlines():
        doc_idx, title, abstract = line.split('\t')
        doc_titles[doc_idx] = doc_idx + '|t|' + title.strip() + '\n'
        doc_abstracts[doc_idx] = doc_idx + '|a|' + abstract.strip() + '\n'

    for line in entity_docs.readlines():
        doc_idx, ent_idx, ent_type, start_offset, end_offset, ent_name = line.split('\t')
        ent_idx = doc_idx + ent_idx
        idx_list = []
        ent_name = ent_name.strip()
        ent_type = ent_type.strip()

        if 'CHEMICAL' == ent_type:
            for k in biogrid_chem_ids:
                if ent_name in biogrid_chem_ids[k]:
                    idx_list.append(k)
        else:
            for k in biogrid_prot_ids:
                if ent_name in biogrid_prot_ids[k]:
                    idx_list.append(k)

        if len(idx_list) > 1:
            ent_idx = '|'.join(idx_list)
        elif len(idx_list) == 1:
            ent_idx = idx_list[0]
        else:
            print('Not found: {}\t{}'.format(ent_type, ent_name))

        doc_entities[doc_idx].append(
            '{}\t{}\t{}\t{}\t{}\t{}\n'.format(doc_idx, start_offset, end_offset, ent_name,
                                              ent_type, ent_idx.strip()))

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
            f.write('\n')

        f.close()

    text_docs.close()
    entity_docs.close()
    relation_docs.close()

