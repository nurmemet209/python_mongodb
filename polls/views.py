from django.http import HttpResponse
import urllib
from pymongo import MongoClient
import json
import logging
import threading
import formatdata
from excelhelper import ExcelWriteHelper, ExcelReadHelper

# 每次根据轮毂尺寸从wheel-siz.com服务器中获取到的数据到该集合当中
fit_car_collection = "fit_car_collection"
# 保存车辆信息（包含轮毂信息）
car_detail_with_rim_collection = "car_detail_with_rim_collection"

logger = logging.getLogger(__name__)


def test(request, year, month, day):
    return HttpResponse("Chengo")


def index(request):
    return HttpResponse(
        "Hello, world. You're at the polls index.fdffffffffffffffffffff")


# http://127.0.0.1:8082/polls/detail/bmw/1-series/2013/
def detail(request, make, model, year):
    data = find_car_with_detail(make, model, year)
    return HttpResponse(data)


# http://127.0.0.1:8082/polls/findByRim/?bolt=5x105&rim_diameter=18.0&rim_width=8.5&offset=35
def get_suite_car_by_rim(request):
    bolt = str(request.GET.get('bolt'))
    rim_diameter = str(request.GET.get('rim_diameter'))
    rim_width = str(request.GET.get('rim_width'))
    offset = str(request.GET.get('offset'))
    # data = grab_by_rim(bolt, rim_width, rim_width, offset)
    # exportThread = dataExportThread(100)
    # exportThread.start()
    return HttpResponse("data")


# 清空集合
def clearCollection(db, collectionName):
    db[collectionName].remove()


# 删除数据库
def clearSchema(client, dbName):
    client.drop_database(dbName)


# 保存jSON数组
def saveJsonArray(db, collectionName, jsonArrayData):
    db[collectionName].insert_many(json.loads(jsonArrayData))


# 保存dictionary到数据库
def saveDictionary(db, collectionName, dict_):
    db[collectionName].insert_one(dict_)


# 集合中根据条件查询,如 { 'name_en': 'Chevy'}
def findByCondition(db, collectionName, jsonCondition):
    return db[collectionName].find_one(jsonCondition)


def grab_by_rim(bolt, rim_diameter, rim_width, offset):
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.wheeldb
    url = formatdata.get_url_by_rim(bolt, rim_diameter, rim_width, offset)
    print(url)
    data = findByCondition(db, fit_car_collection, {"key": url})
    if data is not None:
        print("本地服务器中读取...")
        # 删除_id
        del data['_id']
        # dictionary转json
        return json.dumps(data['value'])
    else:
        print("从wheel-size.com中获取...")
        data = formatdata.grabByRimFromServer(bolt, rim_diameter, rim_width,
                                              offset)
        # 保存到mongodb
        dict_ = {"key": url}
        # data(json数据) 转换list
        dict_["value"] = json.loads(data)
        saveDictionary(db, fit_car_collection, dict_)
        # 进一步拉数据
        fit_make_list = formatdata.filter_data(data)
        urls = formatdata.get_urls(fit_make_list)
        formatdata.custom_print(urls)
        for r in urls:
            # 如果该车信息已经存在则不再请求
            car_data = findByCondition(db, car_detail_with_rim_collection,
                                       {"key": r})
            if car_data is not None:
                print("记录不存在，请求wheel-size.com ...")
                response = urllib.request.urlopen(r)
                new_data = response.read().decode('utf-8')
                car_data_dict = {"key": r}
                car_data_dict["value"] = json.loads(new_data)
                saveDictionary(db, car_detail_with_rim_collection,
                               car_data_dict)
            else:
                print("记录已存在,不再请求 url:" + r)

        return data


# 同步相关车型数据
# 根据汽车品牌(make),汽车名称(model),年份 查询详情,返回json
def find_car_with_detail(make, model, year):
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.wheeldb
    url = formatdata.get_model_detail_url(make, model, year)
    detail = findByCondition(db, car_detail_with_rim_collection, {"key": url})
    if detail is not None:
        # dictionary转json返回
        del detail['_id']
        print("本地服务器中获取...")
        return json.dumps(detail)
    else:
        print("远程服务器中获取...")
        response = urllib.request.urlopen(url)
        new_data = response.read().decode('utf-8')
        car_data_dict = {"key": url}
        car_data_dict["value"] = json.loads(new_data)
        saveDictionary(db, car_detail_with_rim_collection, car_data_dict)
        return new_data


# 删除测试环境中的collection
def deleteData():
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.wheeldb
    clearCollection(db, fit_car_collection)
    print("collection cleared...")


def get_car_name(data):
    car_name_list = []
    actural_name_list = []
    for item in data:
        make = item['make']
        make_anme = make['slug']
        models = item['models']
        for model in models:
            model_name = model['slug']
            vehicles = model['vehicles']
            for vehicle in vehicles:
                trim = vehicle['trim']
                years = vehicle['years']
                car_name_list.append({
                    'make': make_anme,
                    'model': model_name,
                    'years': years,
                    'trim': trim
                })

    for item in car_name_list:
        name = item['make'] + " " + item['model'] + " " + item['trim'] + " "
        years = item['years']
        item_len = len(years)
        if item_len is not 1:
            name = name + str(years[item_len - 1]) + "-" + str(years[0])
        else:
            name = name + str(years[0])
        actural_name_list.append(name)
    return actural_name_list


class dataExportThread(threading.Thread):
    num = 20
    title_list = ['编码', '尺寸', 'ET', 'CB', 'PCD', '颜色', '适配车型']

    def __init__(self, delay):
        threading.Thread.__init__(self)
        self.delay = delay
        self.reader = ExcelReadHelper("data.xls")
        self.writer = ExcelWriteHelper("rotiform_new.xls", self.title_list)

    def run(self):
        print("running...")
        for i in range(self.num):
            raw_data = self.reader.get_next_raw()
            raw_index = self.reader.current_raw
            bolt = self.reader.get_pcd(raw_data).replace('*', 'x')
            rim_width = self.reader.get_rim_width(raw_data)
            rim_diameter = self.reader.get_rim_diameter(raw_data)
            offset = self.reader.get_et(raw_data)
            data = grab_by_rim(bolt, rim_diameter, rim_width, offset)
            name_list = get_car_name(json.loads(data))
            pro_name = '，'.join(name_list)
            raw_data.append(pro_name)
            self.writer.write_raw(raw_index, raw_data)

        self.writer.save()




        # exportThread = dataExportThread(100)
        # exportThread.start()
