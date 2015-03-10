import logging
import json
import requests

#TODO: Possibly create a "build picard object" method that takes a site url and test environment and sets the Schema_url and Referer

class PicardClient(object):
    s3_connection = None
    bucket = None

    def __init__(self):
        """
        Creating a connection to the S3 bucket.
        :return:
        """
        #TODO: Does this class do any logging, or does the PicardException handle all of it?
        self.log = logging.getLogger(self.__class__.__name__)

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
        return json.dumps(r.text)

    def create_headers(self, referer="localhost"):
        #TODO: Change the default value here to the "QA" referer.
        return {"Referer": referer}


class PicardClientException(Exception):
    def __init__(self, arg):
        self.msg = arg


if __name__ == '__main__':
    pc = PicardClient()
    schema_url = "https://register.genentech.com/7723e4db-f545-4975-8d97-12da804bff69"
    headers = pc.create_headers(referer="https://register.genentech.com")
    form_data = {"email-address": "ywnpegu.tnpfbrlabtif@meltmedia.com",
                 "first-name": "yWNPEGu",
                 "last-name": "TnpfbRlAbtif"}

    print pc.send_to_picard(
        schema_url,
        form_data,
        headers=headers
    )