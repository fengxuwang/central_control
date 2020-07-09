import json
import datetime

import requests

from central_control.db import DBUtil


def collect():
    is_connection = check()
    if is_connection:
        try:
            dbUtil = DBUtil(host='39.96.38.182', user='root', password='Wdyk@2018', database='pub_env')
            # 获取最近一次采集的时间
            last_date_sql = "select collection_time, failure_times from collection_setting"
            last_date = dbUtil.query_one(last_date_sql)
            # 获取采集时间
            collect_sql = "select a.collection_time from T_HVAC a where a.collection_time > %s group by a.collection_time order by a.collection_time limit 1"
            collect_times = dbUtil.query_all(collect_sql, (last_date[0],))
            if len(collect_times) == 0:
                return

            datas = list()
            for collect_time in collect_times:
                # 获取采集的数据
                sql = """select a.id, a.tag_node, a.tag_name, a.building_indentity, a.tag_value, a.tag_description, a.device_id, a.device_identity, a.device_location, a.device_name, a.device_item, a.plance_id, a.system, a.sub_system, a.device_profession, a.collection_time, a.colletion_seq, a.record_time, a.project_id from T_HVAC a where a.collection_time = %s"""
                collect_data = dbUtil.query_all(sql, (collect_time,))
                datas.extend(map_data(collect_data))
            push_data(datas)
            # 更新最新的采集时间
            update_last_date_sql = "update collection_setting set collection_time = %s, failure_times = 0 where id = 1"
            dbUtil.update(update_last_date_sql, (collect_times[len(collect_times) - 1],))

            dbUtil.commit()
            dbUtil.close()
            if last_date[1] > 0:
                send_message()
        except Exception as e:
            print(e)


def send_message():
    url = "http://39.96.8.100:8180/nts/v1/sms/send"
    data = json.dumps({"name": "上海奉贤项目", "phone": "18007132790", "smsTypeEnum": "CENTER_CONTROL_SERVER_ON_LINE"})
    requests.post(url, data=data, headers={'Content-Type': 'application/json'})


def map_data(results):
    data = list()
    # 遍历数据
    for row in results:
        id = row[0]
        tag_node = row[1]
        tag_name = row[2]
        building_indentity = row[3]
        tag_value = row[4]
        tag_description = row[5]
        device_id = row[6]
        device_identity = row[7]
        device_location = row[8]
        device_name = row[9]
        device_item = row[10]
        plance_id = row[11]
        system = row[12]
        sub_system = row[13]
        device_profession = row[14]
        collection_time = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(minutes=-5)
        colletion_seq = row[16]
        record_time = row[17]
        project_id = row[18]

        value = (
            id, tag_node, tag_name, building_indentity, tag_value, tag_description, device_id, device_identity,
            device_location,
            device_name, device_item, plance_id, system, sub_system, device_profession, collection_time, colletion_seq,
            record_time, project_id)
        data.append(value)
    return data


def check():
    # 检测是否能访问远程数据库
    try:
        DBUtil(host='192.168.0.155', user='wdyk', password='Wdyk@123', database='pub_env')
        return True
    except Exception as e:
        print("连接数据库失败")
        print(e)
        update_error_times()
        return False


def update_error_times():
    dbUtil = DBUtil(host='39.96.38.182', user='root', password='Wdyk@2018', database='pub_env')
    sql = "update collection_setting set failure_times = ifnull(failure_times, 0) + 1 where id = 1"
    dbUtil.update(sql, None)
    dbUtil.commit()


def push_data(collect_data):
    remote_db = DBUtil(host='192.168.0.155', user='wdyk', password='Wdyk@123', database='pub_env')
    insert_sql = "insert into T_HVAC(id, tag_node, tag_name, building_indentity, tag_value, tag_description, device_id, device_identity, device_location, device_name, device_item, plance_id, system, sub_system, device_profession, collection_time, colletion_seq, record_time, project_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    remote_db.insert(insert_sql, collect_data)
    remote_db.commit()


if __name__ == '__main__':
    collect()
