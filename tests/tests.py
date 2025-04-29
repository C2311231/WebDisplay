import tests.test_engine as test_engine
import threading, time
from base import api, commons, database, browser, peers, scheduler, updater, networking, auto_discovery, cec, calander

def test_required_config_networking(name, completion, printing):
    printing()
    if networking.NetworkingManager.required_config() != {
            "web_version": None,
            "api_version": None,
            "web_url": None,
            "web_port": None,
            "web_encryption": None,
            "device_name": None,
            "device_state": None,
            "device_platform": None,
            "device_id": None,
            "device_ip": None,
        }:
            time.sleep(1)
            completion(100)
            printing()
            return test_engine.TestResult(name, False, ["Incorrect config"])
    
    time.sleep(1)
    completion(100)
    printing()
    return test_engine.TestResult(name, True)




def add_tests(engine: test_engine.Tester):
    engine.add_test(test_engine.Test("Testing Networking Required Config", test_required_config_networking))