# coding:utf8
import jieba.posseg as pseg


def get_data_attribute(data, attrs=None):
    words = pseg.cut(data)

    result = []
    for word, flag in words:
        if attrs:
            if flag in attrs:
                result.append((word, flag))
            continue
        else:
            result.append((word, flag))
    return result


if __name__ == '__main__':
    result = get_data_attribute("我爱我家")
    print(result)

    result = get_data_attribute("我爱我家",['v'])
    print(result)
