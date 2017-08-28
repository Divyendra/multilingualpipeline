# -*- coding: utf-8 -*-

import numpy as np, sys
import argparse, re

def xmlescape(x):
    #Function to escape certain characters so that the output is a valid xml file
    x = re.sub(r'&', '&amp;', x);
    x = re.sub(r'"', '&quot;', x);
    x = re.sub(r'\'', '&apos;', x);
    x = re.sub(r'>', '&gt;', x);
    x = re.sub(r'<', '&lt;', x);
    return x

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", type=str, help="Name of\
                    input file")
parser.add_argument("-l", "--lemmas", type=str, help="Name of\
                    lemmas file")
parser.add_argument("-t", "--timing", type=str, help="Name of\
                    file with timing")
parser.add_argument("-s", "--synt_out", type=str, help="Name of\
                    syntaxnet output file")
args = parser.parse_args()

#List of fields in the file header
fields = {"TOP":"N/A", "COL":"N/A", "UID":"N/A", "PID":"N/A", "ACQ":"N/A", "DUR":"N/A", "VID":"N/A",
        "TTL":"N/A", "URL":"N/A", "TTS":"N/A", "SRC":"N/A", "CMT":"N/A", "LAN":"N/A", "TTP":"N/A",
        "HED":"N/A", "OBT":"N/A", "LBT":"N/A", "CC1":"N/A", "CC2":"N/A"}
with open(args.input_file) as f:
    content = f.readlines()
content = [x.strip() for x in content]
f.close()
for line in content:
    l = line.split('|')
    try:
        fields[l[0]] = l[1:]
    except KeyError:
        break

file_name = fields["TOP"][-1]
country, channel = file_name.split('_')[2:4]
channel = re.sub(r"[^A-Za-z0-9]", "_", channel)
channel = re.sub(r"^([0-9])", r"_\1", channel)
title = xmlescape(' '.join(file_name.split('_')[4:]))
year, month, day, time = fields["TOP"][1][:4], fields["TOP"][1][5:7], fields["TOP"][1][8:10], fields["TOP"][1][11:15]
date = year+'-'+month+'-'+day
collection = xmlescape(fields['COL'][0])
text_id = fields['UID'][-1]
text_id = text_id.replace('-','_')
duration = xmlescape(fields['DUR'][-1])
vid_res = xmlescape(fields['VID'][0])
event_title = xmlescape(fields['TTL'][-1])

with open(args.lemmas) as f: #Reading the lemmas
    lemmas = f.readlines()
lemmas = [x.strip() for x in lemmas[2:]]
f.close()

with open(args.timing) as f: #Tokenizer output with time(for sentence beginnings)
    tokenized_out_with_time = f.readlines()
tokenized_out_with_time = [x.strip().split(' ') for x in tokenized_out_with_time]
f.close()

parser_out = np.genfromtxt(args.synt_out, dtype='object') #syntaxnet parser output
parser_out[:,[0,6]] = parser_out[:,[0,6]].astype('int')
#List of indices marking end-of-sentence from the parser output
sent_breaks = [i+1 for i,x in enumerate(parser_out[:-1,0]) if parser_out[i,0]>parser_out[i+1,0]]
sent_breaks.append(parser_out.shape[0])

#List of dependencies(according to UD v1)
dep_list = ['acl', 'acl:relcl', 'advcl', 'advmod', 'amod', 'appos',
            'aux', 'auxpass', 'case', 'cc', 'cc:preconj', 'ccomp',
            'compound', 'compound:prt', 'conj', 'cop', 'csubj',
            'csubjpass', 'dep', 'det', 'det:predet', 'discourse',
            'dislocated', 'dobj', 'expl', 'fixed', 'name', 'foreign',
            'goeswith', 'iobj', 'list', 'mark', 'neg', 'nmod',
            'nmod:npmod', 'nmod:poss', 'nmod:tmod', 'nsubj', 'nsubjpass',
            'nummod', 'orphan', 'parataxis', 'punct', 'reparandum', 'root',
            'vocative', 'xcomp', 'mwe']
#List of morphological features
morph_feats_list = ['Animacy', 'Case', 'Gender', 'Number', 'Aspect',
                'Tense', 'Voice', 'VerbForm', 'Degree', 'Mood', 'AdpType', 'Person', 'Variant', 'Abbr', 'PronType',
                 'Reflex', 'Negative', 'PrepCase', 'NumType', 'Hyph', 'Typo', 'Definite', 'Poss', 'fPOS']

#Indexing the dep_list and morph_feats_list so that it's easier to reference them
num_tags = len(dep_list)
dep_dict = {}
for ind,i in enumerate(dep_list):
    dep_dict[i] = ind

num_morph_feats = len(morph_feats_list)
morph_dict = {}
for ind,i in enumerate(morph_feats_list):
    morph_dict[i] = ind

#Printing the file header
sys.stdout.write("<text id=\"t__%s\" collection=\"%s\" file=\"%s\" date=\"%s\" year=\"%s\" month=\"%s\" day=\"%s\" time=\"%s\" duration=\"%s\" country=\"%s\" channel=\"%s\" title=\"%s\" video_resolution=\"%s\""\
    % (text_id, collection, file_name, date, year, month, day, time, duration, country, channel, title, vid_res))
if len(fields['VID']) == 2:
    sys.stdout.write(" video_resolution_original=\"%s\"" % xmlescape(fields['VID'][1]))
if fields['LBT']!='N/A':
    sys.stdout.write(" local_broadcast_date=\"%s\" local_broadcast_time=\"%s\" local_broadcast_timezone=\"%s\"" % tuple(fields['LBT'][0].split(' ')))
if fields['LAN']!='N/A':
    sys.stdout.write(" language=\"%s\"" % xmlescape(fields['LAN'][-1]))
if fields['TTP']!='N/A':
    sys.stdout.write(" teletext_page=\"%s\"" % fields['TTP'][0])
if fields['URL']!='N/A':
    sys.stdout.write(" url=\"%s\"" % xmlescape(fields['URL'][0]))
if fields['SRC']!='N/A':
    sys.stdout.write(" recording_location=\"%s\"" % xmlescape(fields['SRC'][-1]))
if fields['PID']!='N/A':
    sys.stdout.write(" program_id=\"%s\"" % xmlescape(fields['PID'][0]))
if fields['TTS']!='N/A':
    sys.stdout.write(" transcript_type=\"%s\"" % xmlescape(fields['TTS'][0]))
if fields['CMT']!='N/A' and len(fields['CMT'][0])>0:
    sys.stdout.write(" scheduler_comment=\"%s\"" % xmlescape(fields['CMT'][0]))
if fields['HED']!='N/A':
    sys.stdout.write(" header=\"%s\"" % xmlescape(fields['HED'][0]))
if fields['OBT']!='N/A':
    try:
        original_broadcast_date, original_broadcast_time, original_broadcast_timezone = fields['OBT'][1].split(" ")
        sys.stdout.write(" original_broadcast_date=\"%s\" original_broadcast_time=\"%s\" original_broadcast_timezone=\"%s\"" % (original_broadcast_date, original_broadcast_time, original_broadcast_timezone))
    except ValueError:
        pass
    except IndexError:
        try:
            original_broadcast_date, original_broadcast_time, original_broadcast_timezone = fields['OBT'][0].split(" ")
            sys.stdout.write(" original_broadcast_date=\"%s\" original_broadcast_time=\"%s\" original_broadcast_timezone=\"%s\"" % (original_broadcast_date, original_broadcast_time, original_broadcast_timezone))
        except ValueError:
            pass
    else:
        original_broadcast_estimated = "true"
        sys.stdout.write(" original_broadcast_estimated=\"%s\"" % (original_broadcast_estimated))
    sys.stdout.write(" original_broadcast_date=\"%s\" original_broadcast_time=\"%s\" original_broadcast_timezone=\"%s\"" % xmlescape(fields['OBT'][0]))
sys.stdout.write(">\n")

prev = 0
count = 0
sent_num = 0
for i in sent_breaks:
    #Checking for start time of sentence
    if tokenized_out_with_time[sent_num][0][:2] == 'S_':
        time_ = tokenized_out_with_time[sent_num][0][2:]
    else:
        for w in reversed(xrange(len(tokenized_out_with_time[sent_num-1]))):
            if tokenized_out_with_time[sent_num-1][w][:2] == 'S_': #and tokenized_out_with_time[sent_num-1][w][:2] == '__':
                time_ = tokenized_out_with_time[sent_num-1][w][2:]
                break
    print "<s id=\""+str(sent_num+1)+"\" reltime=\""+time_+"\">" #sentence header
    sent = parser_out[prev:i]
    #List of outgoing dependencies for each word in the sentence
    outdeps = [['|' for j in xrange(num_tags)] for k in xrange(i-prev)]
    for row in sent:
        if row[7]!='ROOT':
            # print row[6], i - prev, i, prev
            try:
                outdeps[row[6]-1][dep_dict[row[7]]]+=row[7]+'(0,'+str(row[0]-row[6])+')|'
            except KeyError:
                outdeps[row[6]-1][dep_dict[row[7].split(':')[0]]]+=row[7]+'(0,'+str(row[0]-row[6])+')|'

    for j in xrange(sent.shape[0]):
        #Morphological features for each word
        morph_feats_token = ['0' for k in xrange(num_morph_feats)]
        for feature in sent[j][5].split('|'):
            try:
                morph_feats_token[morph_dict[feature.split('=')[0]]] = feature.split('=')[1]
            except IndexError:
                pass

        lemma = lemmas[count].split('\t')[-1]
        root = int(sent[j][6]==0)
        #Incoming dependency, if any
        if root:
            indep = '|'
        else:
            indep = '|'+sent[j][7]+'('+str(sent[j][6]-sent[j][0])+',0)|'
        #Final output for each word
        print '\t'.join([sent[j][1], sent[j][3], lemma, lemma+'_'+sent[j][3], lemma.lower(), sent[j][1].lower(), '\t'.join(morph_feats_token), str(root), indep, '\t'.join(outdeps[j])])
        count+=1
    print '</s>'

    prev = i
    sent_num+=1
print '</text>'
