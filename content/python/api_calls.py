import pandas as pd
import numpy as np
import warnings
import requests
import json
import pandas

def barrier_extent(barrier_type):

    request1 = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_barrier_extent/items.json?watershed_group_code=BOWR&barrier_type=' + barrier_type
    request2 = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_barrier_extent/items.json?watershed_group_code=QUES&barrier_type=' + barrier_type


    response_api = requests.get(request1)
    parse = response_api.text
    result1 = json.loads(parse)

    response_api = requests.get(request2)
    parse = response_api.text
    result2 = json.loads(parse)

    blocked_km = result1[0]['all_habitat_blocked_km'] + result2[0]['all_habitat_blocked_km']
    blocked_pct = result1[0]['extent_pct'] + result2[0]['extent_pct']

    return blocked_km, blocked_pct

def barrier_count(barrier_type):
    request1 = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_barrier_count/items.json?watershed_group_code=BOWR&barrier_type=' + barrier_type
    request2 = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_barrier_count/items.json?watershed_group_code=QUES&barrier_type=' + barrier_type

    response_api = requests.get(request1)
    parse = response_api.text
    result1 = json.loads(parse)

    response_api = requests.get(request2)
    parse = response_api.text
    result2 = json.loads(parse)

    n_passable = result1[0]['n_passable'] + result2[0]['n_passable']
    n_barrier = result1[0]['n_barrier'] + result2[0]['n_barrier']
    n_potential = result1[0]['n_potential'] + result2[0]['n_potential']
    n_unknown = result1[0]['n_unknown'] + result2[0]['n_unknown']

    sum_bar = (n_passable, n_barrier, n_potential, n_unknown)

    return n_passable, n_barrier, n_potential, n_unknown, sum(sum_bar)

def barrier_severity(barrier_type):

    request1 = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_barrier_severity/items.json?watershed_group_code=BOWR&barrier_type=' + barrier_type
    request2 = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_barrier_severity/items.json?watershed_group_code=QUES&barrier_type=' + barrier_type

    response_api = requests.get(request1)
    parse = response_api.text
    result1 = json.loads(parse)

    response_api = requests.get(request2)
    parse = response_api.text
    result2 = json.loads(parse)

    n_assessed_barrier = result1[0]['n_assessed_barrier'] + result2[0]['n_assessed_barrier']
    n_assess_total = result1[0]['n_assess_total'] + result2[0]['n_assess_total']
    pct_assessed_barrier = result1[0]['pct_assessed_barrier'] + result2[0]['pct_assessed_barrier']

    return n_assessed_barrier, n_assess_total, pct_assessed_barrier

def watershed_connectivity(habitat_type):

    request1 = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_habitat_connectivity_status/items.json?watershed_group_code=BOWR&habitat_type=' + habitat_type
    request2 = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_habitat_connectivity_status/items.json?watershed_group_code=QUES&habitat_type=' + habitat_type

    response_api = requests.get(request1)
    parse = response_api.text
    result1 = json.loads(parse)

    response_api = requests.get(request2)
    parse = response_api.text
    result2 = json.loads(parse)

    connect_stat = (result1[0]['connectivity_status'] + result2[0]['connectivity_status'])/2
    all_habitat = result1[0]['all_habitat'] + result2[0]['all_habitat']
    all_habitat_acc = result1[0]['all_habitat_accessible'] + result2[0]['all_habitat_accessible']

    return round(connect_stat), all_habitat, all_habitat_acc

warnings.filterwarnings('ignore')

connect = watershed_connectivity("ALL")[0]
total = watershed_connectivity("ALL")[1] #total km 
access = watershed_connectivity("ALL")[2]
gain = round((total*0.96)-access,2)

num_dam = barrier_severity('DAM')[1]
km_dam = barrier_extent('DAM')[0]
pct_dam = barrier_extent('DAM')[1]
resource_km = barrier_extent('ROAD, RESOURCE/OTHER')[0]
resource_pct = round(barrier_extent('ROAD, RESOURCE/OTHER')[1])
demo_km = barrier_extent('ROAD, DEMOGRAPHIC')[0]
demo_pct = round(barrier_extent('ROAD, DEMOGRAPHIC')[1])
resource_sev = round(barrier_severity('ROAD, RESOURCE/OTHER')[2])
demo_sev = round(barrier_severity('ROAD, DEMOGRAPHIC')[2])
sum_road = barrier_severity('ROAD, RESOURCE/OTHER')[1] + barrier_severity('ROAD, DEMOGRAPHIC')[1]
