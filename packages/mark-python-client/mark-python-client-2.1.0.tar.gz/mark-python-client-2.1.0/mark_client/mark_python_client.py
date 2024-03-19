"""
Python version : 3.8.10
Mark_python_client script is instantiate a client which communicate
with the mark server and read or write data to the Mongo database
"""
from operator import itemgetter
import logging
import json
import requests
class MarkClient:
    """
    MarkClient is the python client for the MARk framework.
    It contains 36 methods to add or find evidences,
    data, detectors, file and so on ...
    """

    def __init__(self, server_url:str=None, logging_level:int=logging.INFO, proxy:str=None, client_id:int=124):
        self.server_url = server_url
        self.proxy = proxy
        self.client_id = client_id
        logging.basicConfig(level=logging_level)

    def set_server_url(self, server_url: str):
        '''
        Set URL of the mark server
        '''
        self.server_url = server_url

    def get_server_url(self)->str:
        '''
        Get URL set
        '''
        return self.server_url

    def set_logging_level(self, level:int):
        '''
        Set logging_level option 
        '''
        logging.getLogger().setLevel(level=level)

    def get_logging_level(self) -> bool:
        '''
        Get logging_level option
        '''
        return logging.root.level

    def toggle_verbse(self) -> bool:
        '''
        Toggle logging_level param
        '''
        return logging.basicConfig(level=(logging.root.level + 10) % 30)

    def set_proxy(self, proxy:str):
        '''
        Set the proxy for the requests
        '''
        self.proxy = proxy

    def get_proxy(self) -> str:
        '''
        Get the proxy used for the requests

        '''
        return self.proxy

    def _post(self, parameters:list):
        '''
        Post request to the MARk server
        '''
        parameters["id"] = self.client_id
        response = requests.post(self.server_url,
                                 data=json.dumps(parameters),
                                 proxies=self.proxy,
                                 timeout=5)
        logging.debug("-- Status of the %s request:", parameters["method"])
        logging.debug("-- %s", response.json())
        if 'result' in response.json():
            return response.json()['result']
        return None

    def test(self) -> str:
        '''
        Testing the server
        '''
        logging.info("- Testing the server -")

        return self._post({"method":"test"})

    def post_test(self, data_string:str):
        """
        Test by sending it a string
        """
        logging.info("- Sending a test string the server -")
        self._post({"method": "testString", 'params' : [data_string]})

    def set_agent_profile(self, profile):
        """
        Add or update the configuration a detector.
        If profile.label is already defined, the configuration is updated, *
        otherwise a new detector is added.
        :param profile: A profile, as a list of activated and configured detectors
        :return:
        """
        logging.info("-- Setting the Agent Profile of the detectors --")
        self._post({'method' : 'setAgentProfile', 'params' : [profile]})

    def get_server_status(self):
        '''
        Get the status of the server
        '''
        logging.info("- Get the status of the server")
        response_data = self._post({'method': 'status'})
        logging.info("-- Current Active Jobs: %s", str(response_data["executor.jobs.running"]))
        return response_data

    def add_evidence(self, evidence_data:dict):
        '''
        Adding Evidence Data to the server
        '''
        logging.info("- Adding Evidence Data to the server")
        self._post({'method': 'addEvidence', 'params': [evidence_data]})

    def find_last_evidences(self)->list:
        '''
        Fetching Last Evidences from to the server
        '''
        logging.info("- Fetching Evidences from to the server")
        return self._post({'method': 'findLastEvidences'})

    def find_last_evidences_by_label(self, label:str, subject:dict)->list:
        '''
        Find the evidences according to a pattern (that start with provided pattern),
        and if multiple evidences are found with same label,
        return the most recent one.
        :param label: is a string
        :param subject: is a map object, which a duble of strings
        under the following form ("key1","value1")
        :return: Evidence as a list
        '''
        logging.info("-- Fetching Last evidence thanks "
              "to the label from the server --")
        return self._post({'method': 'findLastEvidences',
                          'params': [label, subject]})

    def find_evidences_by_label_in_page(self, label:str, page:int):
        """
        :param label: is a string
        :param page: is an integer, corresponding to a page of the memory
        :return: evidence as a list
        """
        logging.info("-- Fetching Evidences thanks to the label in a page from the server --")
        return self._post({'method': 'findEvidence',
                      'params': [label,page]})


    def find_evidence_since_by_label_and_subject(self, label:str, subject: dict, time:float):
        """
        Find all evidences for a specific detector since a given date.
        :param label: is a string
        :param subject: is a map object, which a duble of strings
        under the following form ("key1","value1")
        :param time: is a time, under the form of a long signed float
        :return: Evidence is returned as a list
        """
        logging.info ('Fetching Evidences from the server since %d ',time)
        return self._post({'method' : 'findEvidenceSince',
                      'params' : [label,subject,time]})

    def find_evidence_by_idfile(self, id_file):
        """
        Get a single evidence by id.
        :param id:
        :return: Evidence
        """
        logging.info("--Fetching an evidence thanks to its id")
        return self._post({'method' : 'findEvidenceById',
                     'params' : [id_file]
                     })

    def find_evidence_for_period_and_interval(self, periode, interval):
        '''
        Find all evidences during a specific period, 
        response: information on how many evidences
                were produced by a specific agent for a given time.
        '''
        logging.info("--Find all evidences during a specific period")
        return self._post({'method' : 'findEvidenceById',
                     'params' : [periode, interval]
                     })


    def add_raw_data(self, raw_data:dict):
        """
        A method to add raw data to the datastore and eventually trigger analysis.
        method : "addRawData"
        :param data: is a raw data, as a string
        :return:
        """
        logging.info ("-- Adding raw data to the database --")
        self._post({'method': 'addRawData', 'params': [raw_data]})

    def find_last_raw_data(self):
        """
        Send a get request to the server to obtain the last raw data in the server
        :return: a list containing the last raw data
        """
        logging.info("--finding the last raw data--")
        return self._post({'method':'findLastRawData'})

    def find_last_raw_data_interval(self, label:str, subject: dict, start:int, stop:int):
        """
        :param label: is a string, the name of the data we are looking for
        :param subject: is a map object, which a duble of strings
        under the following form ("key1","value1")
        :param start: is a long signed float, corresponding to the strating time of the research
        :param stop: is a long signed float, corresponding
        to the ending time of the research
        :return: RawData as a list of raw data posted during the interval
        between the starting and the ending times
        """
        logging.info('--Fetching Raw Data from the server between %d and %d --', start, stop)
        return self._post({'method': 'findRawData',
                      'params': [label, subject, start, stop]})

    def add_file(self, file_bytes, filename:str):
        """
        :param bytes: is a byte (under the form of a list ?)
        :param filename: is string
        :return: An object ID
        """
        logging.info ("-- Adding file to the data base --")
        self._post({'method': 'addFile', 'params': [file_bytes,filename], })

    def find_file(self, file_id):
        """
        Send a request to the server to Find the last data records that were inserted in database
        :param file_id: is a ObjectID
        :return: a byte
        """
        logging.info ("-- Looking in the server for the file with the ID : ")
        logging.info("%s --", file_id)
        return self._post({'method': 'findFile', 'id': file_id})

    def store_in_cache(self, key, value):
        """
        Store the value in the cache with the key.
        :param key:
        :param value:
        :return: Nothing
        """
        logging.info('-- Storing the value %s in the %s cache --', value, key)
        self._post({'method': 'storeInCache',
                          'params': [key,value]})

    def get_from_cache(self, key):
        """
        get value from cache represented by a map.
        :param key: is a value corresponding to the cache we want data from
        :return: an object from the cache
        """
        logging.info('-- Getting data from the %s cache --', key)
        return self._post({'method' : 'getFromCache', 'params' : [key]})

    def remplace_in_cache(self, key, new_value, old_value):
        """
        Compare and swap verify if the current stored value in the cache is
        equals to old_value, or if the value has never been stored in the cache
        for this key. Since multiple agents can get access to the cache, We do
        this verification to not overwrite new values from other agents.

        :param key: is a string corresponding to the cache we want to work in
        :param new_value: is an object we want to put into the cache instead of the ancient one
        :param old_value:is an object we want to remplace by the new value
        :return:boolean
        """
        logging.info('-- posting the new value %s ' \
                   'instead of the old value %s ' \
                   'in the %s cache --', new_value, old_value, key)
        return self._post({'method' : 'compareAndSwapInCache',
                          'params' : [key,new_value,old_value]})

    def pause(self):
        """
        Pause execution (no algorithm will be scheduled).
        """
        self._post({'method': 'pause'})

    def resume(self):
        """
        Resume execution.
        :return:
        """
        self._post({'method': 'resume'})

    def reload(self):
        """
        Reload the directory containing detection agents profiles.
        :return:
        """
        self._post({'method': 'reload' })

    def restart(self):
        """
        A method to restart the server analysis
        Dangerous! Restart the server: wipe the DB and restart the data agents.
        :return:
        """
        self._post({'method': 'restart', })

    def history(self):
        """
        Get the last previous status objects.
        :return: the history of the actions on the server as a list
        """
        return self._post({'method':'history'})

    def get_ranked_list(self, label):
        '''
        Fetching Evidence Ranked List from the server
        '''
        logging.info("- Fetching Evidence Ranked List from the server")
        result_data = []
        result_data = self._post({'method': 'findEvidence', 'params': [label]})
        # sort the fetched data in descending order (highest score at the top)
        sorted_result_data = sorted(result_data, key=itemgetter('score'), reverse=True)
        return sorted_result_data

    def get_unique_subject_count(self, subject:dict):
        '''
        Fetching count of unique subjects in Evidences
        '''
        logging.info("- Fetching count of unique subjects in Evidences")
        return self._post({'method': 'findUniqueSubjects',
                                  'params': [subject]})

    def get_distinct_entries_for_field(self, field):
        '''
        Fetching unique entries for given field
        '''
        logging.info("- Fetching unique entries for given field")
        return self._post({'method': 'findDistinctEntries',
                                  'params': [field]})

    def get_detectors_activated(self):
        '''
        Fetching unique evidence labels
        '''
        logging.info("- Fetching unique evidence labels")
        unique_labels = []
        response_data = self._post({'method': 'activation'})
        for item in response_data:
            unique_labels.append(item["label"])
        return unique_labels

    def sources(self):
        """
        Get the configuration of data sources.
        :return: DataAgentProfile as a list
        """
        logging.info("-- Getting the configuration of data sources:")
        return self._post({'method' : 'sources'})
