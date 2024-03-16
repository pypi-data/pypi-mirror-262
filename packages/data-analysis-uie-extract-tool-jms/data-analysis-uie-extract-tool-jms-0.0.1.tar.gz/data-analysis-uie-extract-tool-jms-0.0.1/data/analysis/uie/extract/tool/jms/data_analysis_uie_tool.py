# coding:utf-8
from paddlenlp import Taskflow


def get_data_uie_info(df, types=['时间', '地点', '场所', '身份', '人名关系', '行为', '结果', '机构', '公司', '来源', '重要名词']):
    all_uies = []
    for index, row in df.iterrows():
        uie_dicts = {}
        for uies in row['uie']:
            for u_type in types:
                if u_type not in uies:
                    continue
                for info in uies[u_type]:
                    uie_value = info['text'] + "_" + str(info['probability']) + "_" + str(info['freq'])
                    if u_type not in uie_dicts:
                        uie_dicts[u_type] = uie_value
                    else:
                        uie_dicts[u_type] = uie_dicts[u_type] + ';' + uie_value
        all_uies.append(uie_dicts)
    return all_uies
