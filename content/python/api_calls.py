import pandas as pd
import numpy as np
import warnings
import requests
import json
import pandas

def barrier_extent(barrier_type, watershed):

    request = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_barrier_extent/items.json?watershed_group_code='+ watershed + '&barrier_type=' + barrier_type


    response_api = requests.get(request)
    parse = response_api.text
    result = json.loads(parse)
    
    result = [item for item in result if barrier_type in item['crossing_feature_type']]

    blocked_km = result[0]['all_habitat_blocked_km'] 
    blocked_pct = result[0]['extent_pct'] 

    return blocked_km, blocked_pct

def barrier_count(barrier_type, watershed):
    request = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_barrier_count/items.json?watershed_group_code='+ watershed + '&barrier_type=' + barrier_type

    response_api = requests.get(request)
    parse = response_api.text
    result = json.loads(parse)
    
    result = [item for item in result if barrier_type == item['crossing_feature_type'] and item['status'] == 'HABITAT']

    n_passable = result[0]['n_passable'] 
    n_barrier = result[0]['n_barrier']
    n_potential = result[0]['n_potential'] 
    n_unknown = result[0]['n_unknown']

    sum_bar = (n_passable, n_barrier, n_potential, n_unknown)

    return n_passable, n_barrier, n_potential, n_unknown, sum(sum_bar)

def barrier_severity(barrier_type, watershed):

    request = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_barrier_severity/items.json?watershed_group_code='+ watershed + '&barrier_type=' + barrier_type


    response_api = requests.get(request)
    parse = response_api.text
    result = json.loads(parse)
    
    result = [item for item in result if barrier_type in item['structure_type']]

    n_assessed_barrier = result[0]['n_assessed_barrier']
    n_assess_total = result[0]['n_assess_total']
    pct_assessed_barrier = result[0]['pct_assessed_barrier'] 

    return n_assessed_barrier, n_assess_total, pct_assessed_barrier

def watershed_connectivity(habitat_type, watershed):

    request = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_habitat_connectivity_status/items.json?watershed_group_code='+watershed+'&habitat_type=' + habitat_type

    response_api = requests.get(request)
    parse = response_api.text
    result = json.loads(parse)

    connect_stat = (result[0]['connectivity_status']
    all_habitat = result[0]['all_habitat']
    all_habitat_acc = result[0]['all_habitat_accessible']

    return round(connect_stat), all_habitat, all_habitat_acc

warnings.filterwarnings('ignore')

connect_bowr = watershed_connectivity("ALL", "BOWR")[0]
total_bowr = watershed_connectivity("ALL", "BOWR")[1] #total km 
access_bowr = watershed_connectivity("ALL", "BOWR")[2]
gain_bowr = round((total_bowr*0.96)-access_bowr,2)

connect_ques_carr = watershed_connectivity("ALL", "QUES")[0] + watershed_connectivity("ALL", "CARR")[0]
total_ques_carr = watershed_connectivity("ALL", "QUES")[1] + watershed_connectivity("ALL", "CARR")[1] #total km 
access_ques_carr = watershed_connectivity("ALL", "QUES")[2] + watershed_connectivity("ALL", "CARR")[2]
gain_ques_carr = round((total_ques_carr*0.96)-access_bowr_ques_carr,2)

num_dam_bowr = barrier_severity('DAM', 'BOWR')[1]
km_dam_bowr = barrier_extent('DAM', 'BOWR')[0]
pct_dam_bowr = barrier_extent('DAM', 'BOWR')[1]
resource_km_bowr = barrier_extent('ROAD, RESOURCE/OTHER', 'BOWR')[0]
resource_pct_bowr = round(barrier_extent('ROAD, RESOURCE/OTHER', 'BOWR')[1])
demo_km_bowr = barrier_extent('ROAD, DEMOGRAPHIC', 'BOWR')[0]
demo_pct_bowr = round(barrier_extent('ROAD, DEMOGRAPHIC', 'BOWR')[1])
resource_sev_bowr = round(barrier_severity('ROAD, RESOURCE/OTHER', 'BOWR')[2])
demo_sev_bowr = round(barrier_severity('ROAD, DEMOGRAPHIC', 'BOWR')[2])
sum_road_bowr = barrier_severity('ROAD, RESOURCE/OTHER', 'BOWR')[1] + barrier_severity('ROAD, DEMOGRAPHIC', 'BOWR')[1]

num_dam_ques_carr = barrier_severity('DAM', 'QUES')[1] + barrier_severity('DAM', 'CARR')[1]
km_dam_ques_carr = barrier_extent('DAM', 'QUES')[0] + barrier_extent('DAM', 'CARR')[0]
pct_dam_ques_carr = barrier_extent('DAM', 'QUES')[1] + barrier_extent('DAM', 'CARR')[1]
resource_km_ques_carr = barrier_extent('ROAD, RESOURCE/OTHER', 'QUES')[0] + barrier_extent('ROAD, RESOURCE/OTHER', 'CARR')[0]
resource_pct_ques_carr = round(barrier_extent('ROAD, RESOURCE/OTHER', 'QUES')[1] + barrier_extent('ROAD, RESOURCE/OTHER', 'CARR')[1])
demo_km_ques_carr = barrier_extent('ROAD, DEMOGRAPHIC', 'QUES')[0] + barrier_extent('ROAD, DEMOGRAPHIC', 'CARR')[0]
demo_pct_ques_carr = round(barrier_extent('ROAD, DEMOGRAPHIC', 'QUES')[1] + barrier_extent('ROAD, DEMOGRAPHIC', 'CARR')[1])
resource_sev_ques_carr = round(barrier_severity('ROAD, RESOURCE/OTHER', 'QUES')[2] + barrier_severity('ROAD, RESOURCE/OTHER', 'CARR')[2])
demo_sev_ques_carr = round(barrier_severity('ROAD, DEMOGRAPHIC', 'QUES')[2] + barrier_severity('ROAD, DEMOGRAPHIC', 'CARR')[2])
sum_road_ques_carr = barrier_severity('ROAD, RESOURCE/OTHER', 'QUES')[1] + barrier_severity('ROAD, DEMOGRAPHIC', 'QUES')[1] + barrier_severity('ROAD, RESOURCE/OTHER', 'CARR')[1] + barrier_severity('ROAD, DEMOGRAPHIC', 'CARR')[1]
