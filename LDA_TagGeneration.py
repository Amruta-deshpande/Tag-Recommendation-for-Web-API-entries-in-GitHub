import csv
import heapq
import numpy as np
import re

def main():
    '''
    This function recommend tags based on document topic distribution
    and top term distribution
    :return:recommended tags
    '''
    with open('total_test_dataLDA-document-topic-distributuions.csv', newline='') as doc_topic_file:
        with open('total_test_dataLDA-top-terms.csv', newline='') as top_term_file:
            reader = csv.reader(doc_topic_file)
            reader1 = csv.reader(top_term_file)
            list=[]
            recommended_tag_list=[]

            for row in reader1:
                list.append(row)
            top_termlist=np.array(list)
            for docindex,row in enumerate(reader):
                row_value1=[float(i) for i in row]
                row_value1.pop(0)
                # print("First val of max topic",heapq.nlargest(2, row_value1))
                tags_to_recommend = []
                maxVal_Topics=heapq.nlargest(2, row_value1)
                flag=0
                for val in maxVal_Topics:
                    final_topic=row_value1.index(val)
                    # print('Final Topic-->',final_topic)
                    # if(final_topic!=0):
                    final_topic=final_topic+1
                    print("Topic",final_topic)
                    # print("Top_Term",top_termlist)
                    term_list=top_termlist[final_topic]
                    print('Term_list',term_list)
                    if(flag==0):
                        for index, term in enumerate(term_list[:4]):
                            if(index!=0):
                                tags_to_recommend.append(term)
                                flag=1
                    else:
                        count=0
                        for index,term in enumerate(term_list[:5]):
                            if(index!=0):
                                if term in tags_to_recommend:
                                    continue
                                else:
                                    if(count<4):
                                        tags_to_recommend.append(term)
                                        count+=1
                recommended_tag_list.append(tags_to_recommend)

    # print("Recommended LiSt",recommended_tag_list)
    original_tag_list,document_length=get_original_labels()

    recall=calculate_recall(recommended_tag_list,original_tag_list,document_length)
    print("Recall after for",recall)
    #
    precision=calculate_precision(recommended_tag_list,original_tag_list,document_length)
    print("Precision after for",precision)
    # #
    f1_score=calculate_f1_score(recall,precision)
    print("F1-score",f1_score)

    # accuracy=compute_accuracy(recommended_tag_list,original_tag_list)
    # print("Accuracy",accuracy)

    # (original_tag_list, recommended_tag_list)

def get_original_labels():
    '''
    Get the actual labels from test data
    :return:
    '''
    with open('remaining_test_data.csv','r', encoding='utf-8',newline='') as labels_test:
        reader = csv.reader(labels_test)
        Original_labels1=[]
        length_of_doc=0
        for row in reader:
            val=re.split(',',row[0])
            Original_labels1.append(val)
            length_of_doc+=1

        Original_labels = [[w.lower() for w in line] for line in Original_labels1]
        return Original_labels,length_of_doc

def calculate_recall(recommended_tag_list,original_tag_list,document_length):
    '''
    Calculate the recall which is intersection relevant tags and recommended tags divided
    by relevant tags
    :param recommended_tag_list: recommeded tag list
    :param original_tag_list:original label list
    :param document_length: total length of document
    :return:
    '''
    # print("Original",original_tag_list)
    sum_recall=0
    for orig, recommend in zip(original_tag_list,recommended_tag_list):
            # print("ZIP")
            # print(orig,recommend)
            # print(len(orig))
            count=0
            for val_re in recommend:
                if val_re in orig:
                    print(val_re,orig)
                    count=count+1

            print(count/len(orig))
            doc_recall=(count / len(orig))
            sum_recall+=doc_recall

        # print("length_doc",document_length)
        # print("summation_recall",sum_recall)
    recall_val=(1/document_length)*sum_recall
    # print("Recall in for",recall_val)
    return recall_val

def calculate_precision(recommended_tag_list,original_tag_list,document_length):
    '''
        Calculate the precision which is intersection relevant tags and recommended tags divided
        by recommended tags
        :param recommended_tag_list: recommeded tag list
        :param original_tag_list: original label list
        :param document_length: length of document

        '''
    sum_precision = 0
    for orig, recommend in zip(original_tag_list, recommended_tag_list):
        # print("ZIP")
        # print(orig, recommend)
        recommend_length=len(recommend)
        count1 = 0
        for val_re in recommend:
            if val_re in orig:
                # print(val_re, orig)
                count1 = count1 + 1

        # print(count1 / recommend_length)
        doc_precision= (count1 / recommend_length)
        sum_precision += doc_precision

    # print("length_doc", document_length)
    # print("summation_precision", sum_precision)
    precision_val = (1 / document_length) * sum_precision
    # print("Precision in for loop", precision_val)
    return precision_val

def calculate_f1_score(recall,precision):
    '''
    Calculate the f1 score which is harmonic mean of precision and recall

    '''
    f1_score=2*((recall*precision)/(recall+precision))
    # print(f1_score)
    return f1_score


def compute_accuracy(recommended_tag_list,original_tag_list):
    '''
    This function calculates the accuracy
    '''

    predicted_tags=[]
    for row in original_tag_list:
        for val in row:
            if val not in predicted_tags:
                predicted_tags.append(val)

    # print("set_orig",predicted_tags)
    # print("groundthruth length",len(predicted_tags))

    groundtruth=[]
    # print("Recommend tag list",recommended_tag_list)
    for row in recommended_tag_list:
        for val in row:
            if val not in groundtruth:
                groundtruth.append(val)

    # print("set_recommend", groundtruth)
    # print("recommend length", len(groundtruth))

    gt = len(predicted_tags)
    number_of_extracted_features = 0
    for item in groundtruth:
        if item in predicted_tags:
            number_of_extracted_features += 1
    # print(number_of_extracted_features, "/", gt)
    return number_of_extracted_features / gt

if __name__ == '__main__':
    main()
