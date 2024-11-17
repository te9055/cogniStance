from googletrans import Translator
import csv
from os import listdir
from os.path import isfile, join
import time


# wrapper for the googletrans library. Takes in chinese string returns english
def translate(word):
    translator = Translator()

    result = translator.translate(word, src='zh-cn', dest='en')

    return result


def get_csv(fileName):
    with open(fileName, newline='') as csvfile:
        data = list(csv.reader(csvfile))

    return data

def list_files(directory):
    for f in listdir(directory):
        if isfile(join(directory, f)):
            print(f)
            file = get_csv(directory + "/" +f)

            transfile = []

            for line in file:
                try:
                    translation = translate(line[0])
                    transfile.append(translation.text)
                    time.sleep(1)
                except Exception:
                    pass

            with open(directory + "/" + "trans" +f , 'w', newline='') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow(transfile)

