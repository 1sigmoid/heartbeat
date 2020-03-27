from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import os
import json
import re
import nltk


nltk.download('stopwords')


def datacreator(inputpath, outputpath):
    datals = []
    entries = os.listdir(inputpath)
    for i in entries:
        with open(inputpath+i) as f:
            dat = json.load(f)
            datals.append(dat)

    abstractls = []
    bodyls = []
    temp_ls = []
    for i in range(len(datals)):
        current_data = datals[i]
        for j in range(len(current_data["abstract"])):
            # Selects each dictionary in the abstract list
            current_block = current_data["abstract"][j]

            # This selects the text in each block of data
            text = current_block["text"]

            # To ensure that random bits of data do not creep in to the code
            if len(text) > 200:
                temp_ls.append(text)

        # Now we append the list of abstract texts from EACH file, to the abstractls if it is not empty
        if len(temp_ls) != 0:
            abstractls.append(temp_ls)

        # When we delete it
        temp_ls = []

        for k in range(len(current_data["body_text"])):
            # Selecting the block in the body text
            current_block = current_data["body_text"][k]

            # Selecting the text in the current block
            text = current_block["text"]
            if len(text) > 200:
                temp_ls.append(text)

        if len(temp_ls) != 0:
            bodyls.append(temp_ls)

        temp_ls = []
    var2 = len(bodyls)
    var1 = len(abstractls)
    ps = PorterStemmer()
    for i in range(len(bodyls)):
        if i%10 ==0: 
            print("body", i , "/", var2, "Perecent done is ", 100*(i/var2))
        current_list = bodyls[i]

        for j in range(len(current_list)):
            bodyls[i][j] = bodyls[i][j].lower()
            bodyls[i][j] = re.sub('[^a-zA-Z]', ' ', bodyls[i][j])
            bodyls[i][j] = bodyls[i][j].split()
            bodyls[i][j] = [ps.stem(word) for word in bodyls[i][j] if not word in set(stopwords.words('english'))]
            bodyls[i][j] = ' '.join(bodyls[i][j])


    for i in range(len(abstractls)):
        if i%10==0: 
            print("abstract", i, '/', var1, "Perecent done is ", 100*(i/var1))
        clist2 = abstractls[i]

        for k in range(len(clist2)):
            abstractls[i][k] = abstractls[i][k].lower()
            abstractls[i][k] = re.sub('[^a-zA-Z]', ' ', abstractls[i][k])
            abstractls[i][k] = abstractls[i][k].split()
            abstractls[i][k] = [ps.stem(word) for word in abstractls[i][k] if not word in set(stopwords.words('english'))]
            abstractls[i][k] = ' '.join(abstractls[i][k])


    fname1 = outputpath+"-abstract.txt"
    fname2 = outputpath+"-body.txt"
    with open(fname1, "w+") as f:
        f.write(str(abstractls))
    with open(fname2, "w+") as f:
        f.write(str(bodyls))



datacreator('./../../datasets/CORD-19/biorxiv_medrxiv/biorxiv_medrxiv/', 'biomed')
datacreator('./../../datasets/CORD-19/comm_use_subset/comm_use_subset/', 'commonsub')
datacreator('./../../datasets/CORD-19/custom_license/custom_license/', 'custom_license')
datacreator('./../../datasets/CORD-19/noncomm_use_subset/noncomm_use_subset/', 'noncommonsub')
