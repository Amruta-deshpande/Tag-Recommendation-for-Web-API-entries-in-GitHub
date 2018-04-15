import csv
import heapq

def main():
    '''
        This function recommend tags based on document topic distribution
        and top term distribution
        :return:recommended tags
        '''
    with open('total_test_data-document-topic-distributions-res.csv', newline='') as doc_topic_file:
        with open('topic-label.csv', newline='') as label_topic_file:
            reader = csv.reader(doc_topic_file)
            reader1=csv.reader(label_topic_file)
            topic_label_list = []
            recommend_list=[]
            for row in reader1:
                topic_label_list.append(row)
            for docindex, row in enumerate(reader):
                print("Document", docindex)
                print('Doc-topic Distribution', row)
                row=[float(i) for i in row]
                row.pop(0)
                print("First val of max topic", heapq.nlargest(3, row))
                max_topTopics_distribution = heapq.nlargest(3, row)
                label_row_list=[]
                for val in max_topTopics_distribution:
                    topic_index=row.index(val)
                    print(topic_index)
                    label_index= topic_label_list[topic_index]
                    print(label_index[1])
                    label_row_list.append(label_index[1])

                recommend_list.append(label_row_list)

    print("Recommended string labels",recommend_list)
    recommend_label_list=separate_recommended_labels(recommend_list)
    original_label_list=get_original_labels()

    recall=calculate_recall(original_label_list,recommend_label_list)
    print("Recall", recall)
    precision=calculate_precision(original_label_list,recommend_label_list)
    print("Precision", precision)

    f1score=calculate_f1_score(recall, precision)
    print("F1-score",f1score)

    # print(recommend_label_list)


def separate_recommended_labels(recommend_list):
    '''
    Generate multiple labels from a given set of label
    :param recommend_list: list of multiple labels
    :return: recommed label list
    '''
    print("----")
    final_label_list=[]
    print("Recommend list",recommend_list)
    for row in recommend_list:
        inner_label=[]
        for label_string in row:
            for x in label_string.split(','):
                label_str=x.strip()
                if label_str not in inner_label:
                    inner_label.append(label_str)

        final_label_list.append(inner_label)

    print("Final labels",final_label_list)
    return final_label_list

def get_original_labels():
    '''
        Get the actual labels from test data
        :return: list of original labels
    '''
    with open('total_test_data.csv', newline='') as test_file:
        reader = csv.reader(test_file)
        orig_labels=[]
        for row in reader:
            orig_labels.append(row[0])

    print("Original string",orig_labels)
    label_list=[]
    for str in orig_labels:
        inner_orig_labels=[]
        for x in str.split(','):
            label_str = x.strip()
            inner_orig_labels.append(label_str.lower())

        label_list.append(inner_orig_labels)
    print("Original labels",label_list)
    return label_list

def calculate_recall(original_label_list,recommend_label_list):
    '''
        Calculate the recall which is intersection relevant tags and recommended tags divided
        by relevant tags
        :param recommend_label_list: recommeded tag list
        :param original_label_list:original label list
        :param doc_length: total length of document
        :return: recall value
    '''
    print("-------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    doc_length=len(original_label_list)
    sum_recall = 0
    for orig, recommend in zip(original_label_list, recommend_label_list):
        print("ZIP")
        print("orig",orig,"recommend",recommend)
        # print(len(orig))
        count = 0
        for val_re in recommend:
            if val_re in orig:
                print(val_re, orig)
                count = count + 1

        print(count / len(orig))
        doc_recall = (count / len(orig))
        sum_recall += doc_recall

    # print("length_doc", doc_length)
    # print("summation_recall", sum_recall)
    recall_val = (1 / doc_length) * sum_recall
    # print("Recall in for", recall_val)
    # accuracy=recall_val*100;
    return recall_val

def calculate_precision(original_label_list,recommend_label_list):
    '''
            Calculate the precision which is intersection relevant tags and recommended tags divided
            by recommended tags
            :param recommend_label_list: recommeded tag list
            :param original_label_list: original label list
            :param docu_length: length of document

    '''
    doc_length = len(original_label_list)
    sum_precision = 0
    for orig, recommend in zip(original_label_list, recommend_label_list):
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
    precision_val = (1 / doc_length) * sum_precision
    # print("Precision in for loop", precision_val)
    return precision_val

def calculate_f1_score(recall,precision):
    '''
        Calculate the f1 score which is harmonic mean of precision and recall
        :return: F1-score value
    '''
    f1_score=2*((recall*precision)/(recall+precision))
    # print(f1_score)
    return f1_score

if __name__ == '__main__':
    main()