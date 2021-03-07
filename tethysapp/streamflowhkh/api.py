from django.http import JsonResponse
import datetime as dt
import psycopg2, json,decimal, datetime
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes
import scipy.stats as sp
import numpy as np
from datetime import timedelta
# from rest_framework import

def check_for_decimals(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

# @login_required()
@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def getFeatures(request):
    json_obj = {}
    conn = psycopg2.connect(host="192.168.10.6", database="servirFlood", user="postgres", password="changeit2")
    cur = conn.cursor()
    query = 'select comid, risk, ST_AsGeoJSON(geom) AS geometry FROM nepaldnetwork'
    cur.execute(query)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    geomIndex = colnames.index("geometry")

    feature_collection = {'type': 'FeatureCollection', 'features': []}
    for row in rows:
        feature = {
            'type': 'Feature',
            'geometry': json.loads(row[geomIndex]),
            'properties': {},
        }
        for index, colname in enumerate(colnames):
            if colname not in ('geometry', 'geom'):
                if isinstance(row[index], datetime.datetime):
                    value = str(row[index])
                else:
                    value = row[index]
                feature['properties'][colname] = value

        feature_collection['features'].append(feature)
    conn.close()
    json_obj["feature"] = feature_collection
    return JsonResponse(feature_collection)
    # return json.dumps(feature_collection, indent=None, default=check_for_decimals)

@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def getreturnPeriod(request):
    comid = request.GET.get('comid')
    conn = psycopg2.connect(host="192.168.10.6", database="servirFlood", user="postgres", password="changeit2")
    cur = conn.cursor()
    query = "SELECT max, two, ten, twenty FROM returnreriodsnepal where comid = " + str(comid)
    cur.execute(query)
    rows = cur.fetchall()
    return_max = rows[0][0]
    return_20 = rows[0][3]
    return_10 = rows[0][2]
    return_2 = rows[0][1]

    content = {
        "return_max" : return_max,
        "return_2" : return_2,
        "return_10" : return_10,
        "return_20" : return_20
    }
    return JsonResponse(content)

@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def getHistoric(request):
    comid = request.GET.get('comid')
    hdates = []
    hvalues= []

    conn = psycopg2.connect(host="192.168.10.6", database="servirFlood", user="postgres", password="changeit2")
    cur = conn.cursor()
    query = "select historydate, historyvalue from historynepal where comid = " + str(comid) + " order by historydate"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        mydate = str(dt.datetime.strftime(row[0], '%Y-%m-%d %H:%M:%S'))
        hdates.append(mydate)
        hvalues.append(row[1])
    content = {
        "mydate": mydate,
        "hdates": hdates,
        "hvalues": hvalues
    }
    return JsonResponse(content)

@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def getFlowDurationCurve(request):
    comid = request.GET.get('comid')
    hdates = []
    hvalues= []
    sorted_daily_avg1 =[]
    conn = psycopg2.connect(host="192.168.10.6", database="servirFlood", user="postgres", password="changeit2")
    cur = conn.cursor()
    query = "select historydate, historyvalue from historynepal where comid = " + str(comid) + " order by historydate"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        mydate = str(dt.datetime.strftime(row[0], '%Y-%m-%d %H:%M:%S'))
        hdates.append(mydate)
        hvalues.append(row[1])
    sorted_daily_avg = np.sort(hvalues)[::-1]
    ranks = len(sorted_daily_avg) - sp.rankdata(sorted_daily_avg, method='average')
    # calculate probability of each rank
    prob = [100 * (ranks[i] / (len(sorted_daily_avg) + 1))
            for i in range(len(sorted_daily_avg))]
    for i in range (len(sorted_daily_avg)):
        sorted_daily_avg1.append(sorted_daily_avg[i])
    conn.close()
    content = {
        "prob": prob,
        "sorted_daily_avg1": sorted_daily_avg1
    }
    return JsonResponse(content)

@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication,))
def getForecast(request):
    comid = request.GET.get('comid')
    runDate = dt.datetime.now().date() - timedelta(days=0)
    dates = []
    hres_dates = []
    mean_values = []
    hres_values = []
    min_values = []
    max_values = []
    std_dev_lower_values = []
    std_dev_upper_values = []
    return_obj = {}
    conn = psycopg2.connect(host="192.168.10.6", database="servirFlood", user="postgres", password="changeit2")
    cur = conn.cursor()
    query = "SELECT forecastdate, high_res, maxval, meanval, minval, std_dev_range_lower, std_dev_range_upper FROM public.forecastnepal where comid =" \
            + str(comid) + " and rundate = '" + str(runDate) + "' order by forecastdate"

    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        hres_dates.append(str(dt.datetime.strftime(row[0],'%Y-%m-%d %H:%M:%S')))
        # hres_values.append(row[1])

        if 'nan' not in str(row[2]):
            dates.append(str(dt.datetime.strftime(row[0],'%Y-%m-%d %H:%M:%S')))
            max_values.append(float(row[2]))
            mean_values.append(float(row[3]))
            min_values.append(float(row[4]))
            std_dev_lower_values.append(row[5])
            std_dev_upper_values.append(row[6])
            hres_values.append(row[1])
    content = {
        "hres_dates": hres_dates,
        "dates": dates,
        "max_values": max_values,
        "mean_values": mean_values,
        "min_values": min_values,
        "std_dev_lower_values": std_dev_lower_values,
        "std_dev_upper_values": std_dev_upper_values,
        "hres_values": hres_values
    }
    return JsonResponse(content)
