# coding:utf8
import re


def word_count_processor(data_list):
    '''
    对词进行再分词处理，统计词频和文档数
    :return:
    '''
    total_freq = 0
    count_dict = {}
    total_doc_num = 0
    word_docnum = {}
    for path in data_list:
        with open(path, 'r') as file:
            for line in file:
                total_doc_num += 1
                distinct = set()
                for word1 in line.strip().split("\t"):
                    # 过滤空值
                    if len(word1) <= 1:
                        continue
                    word_ = word1.split("#")[0]
                    attr_ = word1.split("#")[1]
                    if attr_ == '':
                        continue
                    for word in re.split(
                            "_|《|》|<|>|：|（|）|－|\\(|\\)|\\+|-|。|·|@|#|、|—|丨|】|【|/|\\\|&|	| |‬|┈|【|】|▍|\\*|►|\\?|？|,|,|;|:|；|ⅰ|ⅱ|ⅲ|ⅳ|ⅴ|ⅵ|ⅶ|ⅷ|ⅸ|ⅹ|①|②|③|④|⑤|⑥|⑦|⑧|⑨|⑩|⑪|⑫|⑬|⑭|⑮|⑯|⑰|⑱|⑲|⑳|ⓐ|ⓑ|ⓒ|ⓓ|ⓔ|ⓕ|ⓖ|ⓗ|ⓘ|ⓙ|ⓚ|ⓛ|ⓜ|ⓝ|ⓠ|ⓡ|ⓢ|ⓣ|ⓤ|ⓥ|ⓦ|ⓧ|ⓨ|ⓩ|⒈|⒉|⒊|⒋|⒌|⒍|⒎|⒏|⒐|⒑|⒒|⒓|⒔|⒕|⒖|⒗|⒘|⒙|⒚|⒛|⑴|⑵|⑶|⑷|⑸|⑹|⑺|⑻|⑼|⑽|⑾|⑿|⒀|⒁|⒂|⒃|⒄|⒅|⒆|⒇|￥",
                            word_):
                        if len(word) < 2:
                            continue
                        if re.match("^[0-9]+$", word):
                            continue
                        if re.match("\d+.\d?", word):
                            continue
                        total_freq += 1
                        count_attr_dict = {}
                        if word in count_dict:
                            count_attr_dict = count_dict[word]
                            if attr_ in count_attr_dict:
                                count_attr_dict[attr_] = count_attr_dict[attr_] + 1
                            else:
                                count_attr_dict[attr_] = 1
                        else:
                            count_attr_dict[attr_] = 1
                        count_dict[word] = count_attr_dict

                        docnum_attr_dict = {}
                        if word not in distinct:
                            distinct.add(word)
                            if word in word_docnum:
                                docnum_attr_dict = word_docnum[word]
                                if attr_ in docnum_attr_dict:
                                    docnum_attr_dict[attr_] = docnum_attr_dict[attr_] + 1
                                else:
                                    docnum_attr_dict[attr_] = 1
                            else:
                                docnum_attr_dict[attr_] = 1
                            word_docnum[word] = docnum_attr_dict
    return total_freq, total_doc_num, count_dict, word_docnum
