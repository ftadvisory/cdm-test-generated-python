import sys, os
import json
from pathlib import Path
from pydantic import ValidationError
from cdm.event.common.TradeState import TradeState
from cdm.version import __build_time__
from dict_comp import dict_comp

dirPath = os.path.dirname(__file__)
sys.path.append(os.path.join(dirPath))

def cdm_comparison_test_from_file(path, class_name):
    '''loads the json from a file and runs the comparison'''
    print('testing: ' + path + ' with className: ' + class_name.__name__ + ' using CDM built at: ' + __build_time__)
    json_str  = Path(path).read_text()
    json_dict = json.loads (json_str)
    print('json_dict["trade"]["tradeDate"]: ' + json.dumps(json_dict["trade"]["tradeDate"]))
    try:
        print('raw parse from json_str')
        cdm_object     = class_name.parse_raw(json_str)
        trade          = cdm_object.trade
        print('trade.tradeDate: ' + str(trade.tradeDate))
        json_data_out  = cdm_object.json(exclude_defaults=True, indent=4)
        generated_dict = json.loads(json_data_out)    
        assert dict_comp(json_dict, generated_dict), "Failed corrected dict comparison"
        print('passed: dicts matched')
    except ValidationError as e:
        print('failed to parse')
        print(e)
  
  
  
#    print ('json ... ')
#    print (json_dict['trade']['tradeDate'])

# cdm_object = class_name.parse_raw(json_str)
    

def test_trade_state (cdm_sample=None):
    if cdm_sample == None:
        dirPath = os.path.dirname(__file__)
        sys.path.append(os.path.join(dirPath))
#		cdm_sample = os.path.join(dirPath, 'ird-ex01-vanilla-swap_4_3.json')
        cdm_sample = os.path.join(dirPath, 'EUR-Vanilla-account.json')
    cdm_comparison_test_from_file (cdm_sample, TradeState)
 
if __name__ == "__main__":
    cdm_sample = sys.argv[1] if len(sys.argv) > 1 else None
    test_trade_state(cdm_sample)