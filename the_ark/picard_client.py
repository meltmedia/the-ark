import logging
import json
import requests

#TODO: Possibly create a "build picard object" method that takes a site url and test environment and sets the Schema_url and Referer

class PicardClient(object):

    def __init__(self):
        """
        Contains methods used to query Epsilon.
        """

    def send_to_picard(self, schema_url, form_data, headers=None):
        r = None

        if not headers:
            headers = self.create_headers()

        r = requests.post(schema_url, form_data, headers=headers)

        #- Able to reach Picard, but request failed
        if r.status_code == 400:
            raise PicardClientException(r.text)
        #- Unable to reach picard
        if r.status_code is not 200:
            raise PicardClientException("Unable to Post to Picard")

        #- Received a valid response from Picard. Return the data received.
        return json.loads(r.text)

    def create_headers(self, referer="localhost"):
        #TODO: Change the default value here to the "QA" referer.
        return {"Referer": referer}


class PicardClientException(Exception):
    def __init__(self, arg):
        self.msg = arg