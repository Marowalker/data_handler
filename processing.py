import xml.dom.minidom
import constants
from collections import defaultdict
import os


# test_example = xml.dom.minidom.parse(constants.DRUGBANK_TRAIN + 'Abarelix_ddi.xml')
#
# docs = test_example.getElementsByTagName('sentence')
#
# sentences = test_example.getElementsByTagName('sentence')
#
# doc_data = defaultdict(dict)
#
# sent_list = []
# doc = test_example.getElementsByTagName('document')[0]
# print(doc.getAttribute('id'))
# for sent in sentences:
#     sent_list.append(sent.getAttribute('text'))
#
# full_doc = ' '.join(sent_list)
# print(full_doc)
# entity_list = test_example.getElementsByTagName('entity')
#
# for ent in entity_list:
#     print("{}\t{}\t{}\t{}".format(ent.getAttribute('id'), ent.getAttribute('charOffset'), ent.getAttribute('type'),
#                                   ent.getAttribute('text')))


def ddi_handler(directory, fileout):
    all_docs = defaultdict(dict)

    for filename in os.listdir(directory):
        print(filename)
        data_parser = xml.dom.minidom.parse(directory + filename)

        sentences = data_parser.getElementsByTagName('sentence')
        for sent in sentences:
            doc_id = sent.getAttribute('id')
            sent_text = sent.getAttribute('text')
            all_docs[doc_id]['abstract'] = doc_id + '|a|' + sent_text

            entity_list = data_parser.getElementsByTagName('entity')
            ent_tups = []

            for ent in entity_list:
                ent_id = ent.getAttribute('id')
                sent_id = ent_id[:-3]
                offset = ent.getAttribute('charOffset')
                ent_type = ent.getAttribute('type')
                text = ent.getAttribute('text')

                all_offsets = offset.split(';')

                if sent_id == doc_id:
                    for off in all_offsets:
                        start, end = off.split('-')
                        if start == end:
                            end = len(sent_text)
                        ent_tups.append(tuple([doc_id, start, end, text, ent_type, ent_id]))

            all_docs[doc_id]['entities'] = ent_tups

            relation_list = data_parser.getElementsByTagName('pair')
            rel_tups = []
            for rel in relation_list:
                rel_type = rel.getAttribute('ddi')
                rel_id = rel.getAttribute('id')
                sent_id = rel_id[:-3]
                e1 = rel.getAttribute('e1')
                e2 = rel.getAttribute('e2')
                if sent_id == doc_id:
                    rel_tups.append(tuple([doc_id, rel_type, e1, e2]))
            all_docs[doc_id]['relations'] = rel_tups

    with open(fileout, 'w') as f:
        for idx in all_docs:
            f.write(all_docs[idx]['abstract'])
            f.write('\n')
            for elem in all_docs[idx]['entities']:
                f.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]))
            for elem in all_docs[idx]['relations']:
                f.write('{}\t{}\t{}\t{}\n'.format(elem[0], elem[1], elem[2], elem[3]))


ddi_handler(constants.DRUGBANK_TEST, constants.DDI_TEST + 'DDI_Drugbank_data.test.txt')
# for idx in ddi_docs:
#     print(idx)
#     print(ddi_docs[idx]['abstract'])
#     for elem in ddi_docs[idx]['entities']:
#         print(elem)
#     for elem in ddi_docs[idx]['relations']:
#         print(elem)
