import urllib.request
import json

host = "https://api.wheel-size.com"
user_key = "fbdf5822ea7b0c6f5661ec8c5c364276"
url_start_section = 2005


#获取汽车年份
def getYears(vehicles):
    years_list = []
    for vhicle in vehicles:
        years = vhicle['years']
        for year in years:
            if year not in years_list:
                years_list.append(year)

    return years_list


#wheel-size.com服务查询适用车型数据
def grabByRimFromServer(bolt, rim_diameter, rim_width, offset):
    url = "https://api.wheel-size.com/v1/search/by_rim/?user_key=" + user_key + "&bolt_pattern=" +str( bolt) + "&rim_diameter=" + str(rim_diameter) + "&rim_width=" + str(rim_width) #+ "&offset_min=" + str(offset) + "&offset_max=" + str(offset)
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    return data


def get_url_by_rim(bolt, rim_diameter, rim_width, offset):
    url = "https://api.wheel-size.com/v1/search/by_rim/?user_key=" + user_key + "&bolt_pattern=" +str( bolt) + "&rim_diameter=" + str(rim_diameter) + "&rim_width=" + str(rim_width ) #+ "&offset_min=" +str( offset) + "&offset_max=" + str(offset)
    return url


def get_model_detail_url(make, model, year):
    url = "https://api.wheel-size.com/v1/models/" + make + "/" + model + "/" + year + "/?user_key=" + user_key
    return url


#列出所有make(汽车品牌),model(汽车名称),年份
def filter_data(data):
    data_list = json.loads(data)
    fit_make_list = []
    for item in data_list:
        make = item['make']
        make_name = make['slug']
        models = item['models']
        print(make_name)
        make_dict = {}
        make_dict["make_name"] = make_name
        model_list = []
        for model in models:
            model_name = model['slug']
            print(model_name)
            vehicles = model['vehicles']
            model_dict = {"model_name": model_name}
            model_dict["years"] = getYears(vehicles)
            model_list.append(model_dict)
        make_dict["models"] = model_list
        print("")
        fit_make_list.append(make_dict)

    print(fit_make_list)
    return fit_make_list


#列出所有待查询url
def get_urls(car_data):
    url_list = []
    for item in car_data:
        make_name = item['make_name']
        models = item['models']
        for model in models:
            model_name = model['model_name']
            years = model['years']
            for year in years:
                if year > url_start_section:
                    url = host + "/v1/models/" + make_name + "/" + model_name + "/" + str(
                        year) + "/?user_key=" + user_key
                    url_list.append(url)

    return url_list


def custom_print(data_list):
    for item in data_list:
        print(item)


# def getYears(vehicles):
# [
#     {
#         "trim": "116i",
#         "market": {
#             "abbr": "EUDM",
#             "name": "European domestic market",
#             "slug": "eudm",
#             "name_en": "European domestic market"
#         },
#         "years": [
#             2013,
#             2012,
#             2011,
#             2010,
#             2009,
#             2008,
#             2007,
#             2006,
#             2005,
#             2004
#         ]
#     },
#     {
#         "trim": "118i",
#         "market": {
#             "abbr": "EUDM",
#             "name": "European domestic market",
#             "slug": "eudm",
#             "name_en": "European domestic market"
#         },
#         "years": [
#             2013,
#             2012,
#             2011,
#             2010,
#             2009,
#             2008,
#             2007,
#             2006,
#             2005,
#             2004
#         ]
#     },
#     {
#         "trim": "120i",
#         "market": {
#             "abbr": "EUDM",
#             "name": "European domestic market",
#             "slug": "eudm",
#             "name_en": "European domestic market"
#         },
#         "years": [
#             2013,
#             2012,
#             2011,
#             2010,
#             2009,
#             2008,
#             2007,
#             2006,
#             2005,
#             2004
#         ]
#     },
#     {
#         "trim": "130i",
#         "market": {
#             "abbr": "EUDM",
#             "name": "European domestic market",
#             "slug": "eudm",
#             "name_en": "European domestic market"
#         },
#         "years": [
#             2013,
#             2012,
#             2011,
#             2010,
#             2009,
#             2008,
#             2007,
#             2006,
#             2005,
#             2004
#         ]
#     },
#     {
#         "trim": "116d",
#         "market": {
#             "abbr": "EUDM",
#             "name": "European domestic market",
#             "slug": "eudm",
#             "name_en": "European domestic market"
#         },
#         "years": [
#             2013,
#             2012,
#             2011,
#             2010,
#             2009,
#             2008,
#             2007,
#             2006,
#             2005,
#             2004
#         ]
#     },
#     {
#         "trim": "118d",
#         "market": {
#             "abbr": "EUDM",
#             "name": "European domestic market",
#             "slug": "eudm",
#             "name_en": "European domestic market"
#         },
#         "years": [
#             2013,
#             2012,
#             2011,
#             2010,
#             2009,
#             2008,
#             2007,
#             2006,
#             2005,
#             2004
#         ]
#     },
#     {
#         "trim": "120d",
#         "market": {
#             "abbr": "EUDM",
#             "name": "European domestic market",
#             "slug": "eudm",
#             "name_en": "European domestic market"
#         },
#         "years": [
#             2013,
#             2012,
#             2011,
#             2010,
#             2009,
#             2008,
#             2007,
#             2006,
#             2005,
#             2004
#         ]
#     },
#     {
#         "trim": "123d",
#         "market": {
#             "abbr": "EUDM",
#             "name": "European domestic market",
#             "slug": "eudm",
#             "name_en": "European domestic market"
#         },
#         "years": [
#             2013,
#             2012,
#             2011,
#             2010,
#             2009,
#             2008,
#             2007
#         ]
#     }
# ]

#def filterData(data):
#根据轮毂信息获取make(汽车品牌),model(车名称),年份
# [
#     {
#         'make_name': 'bmw',
#         'models': [
#             {
#                 'model_name': '1-series',
#                 'years': [
#                     2013,
#                     2012,
#                     2011,
#                     2010,
#                     2009,
#                     2008,
#                     2007,
#                     2006,
#                     2005,
#                     2004
#                 ]
#             }
#         ]
#     },
#     {
#         'make_name': 'land-rover',
#         'models': [
#             {
#                 'model_name': 'range-rover',
#                 'years': [
#                     2001,
#                     2000,
#                     1999,
#                     1998
#                 ]
#             }
#         ]
#     }
# ]