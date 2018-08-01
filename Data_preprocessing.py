import csv
import re
import codecs
import nltk

def main():
    filename="C:/Users/Amruta Deshpande/Documents/RIT/FIS/GitHub/remaining_data.csv"
    with codecs.open(filename, "r", encoding='utf-8', errors='ignore') as file:
        reader = csv.reader(file)
        for index,row in enumerate(reader):
            row = [replace_invalid_characters(d) for d in row]

            content_description = row[0]+" " + row[2] +" "+ row[3]
            list_posTag=pos_tag(content_description)

            # print("POS",list_posTag)
            # print('TPOS', type(list_posTag))
            description_list=[]
            noun_sentence=" ".join(list_posTag)
            description_list.append(noun_sentence)
            print(description_list)

            labels=row[1]
            actual_labels=[]
            actual_labels.append(labels)
            print(actual_labels)

            generate_cleaned_csv(actual_labels,description_list)

def  generate_cleaned_csv(actual_labels,description_list):
            rows=zip(actual_labels,description_list)
            with open("cleaned_remaining_data.csv", "a") as f:
                writer = csv.writer(f)
                for row in rows:
                    writer.writerow(row)


def pos_tag(content_description):
    tokens = nltk.word_tokenize(content_description)
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tagged \
             if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    downcased = [x.lower() for x in nouns]
    joined = " ".join(downcased).encode('utf-8')
    # into_string = str(nouns)
    # print(into_string)
    print("Nouns",nouns)
    return nouns

def replace_invalid_characters(input_data):
    """
     This function removes the invalid characters from the input.
    :param input_data: data to be cleaned.
    :return:
    """
    # List of characters to be removed from user reviews.
    for ch in ["&", "#", "\t", "\n", '”', "“", "\'", '"', "'", "!", "%", "$", "&", "*", "/", "(", ")"
               "@", "-", ">", "<", "?", "+", ";", ":","[", "]", "{", "},", "_", "|", "~", "`", "’"]:
        if ch in input_data:
            input_data = input_data.replace(ch," ")
            input_data = input_data.strip()

    # Replace URL's in string
    input_data = re.sub(r'^https?:\/\/.*[\r\n]*', '', input_data, flags=re.MULTILINE)

    return input_data

if __name__ == '__main__':
    main()
