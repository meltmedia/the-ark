__author__ = 'alow'

import logging
import mimetypes

from StringIO import StringIO
from boto.s3.key import Key
from boto.s3.connection import S3Connection


class S3Client(object):
    s3_connection = None
    bucket = None

    def __init__(self, bucket):
        """
        Creating a connection to the S3 bucket.
        :return:
        """
        self.log = logging.getLogger(self.__class__.__name__)
        try:
            # --- Amazon S3 credentials will use Boto's fall back config,
            # looks for boto.cfg
            # then environment variables
            self.s3_connection = S3Connection(is_secure=False)
            self.bucket = self.s3_connection.get_bucket(bucket, validate=False)

        except Exception as s3_connection_exception:
            self.log.warning("Exception while connecting to S3: " +
                             s3_connection_exception.message)

    def store_file(self, s3_path, file_to_store, filename, return_url=False,
                   mime_type=None):
        """
        Pushes the desired file up to S3 (e.g. log file).
        :param s3_path:
        :param file_to_store:
        :param return_url:
        :param mime_type:
        :param filename:
        :return:
        """
        try:
            s3_file = Key(self.bucket)
            s3_file.key = self._generate_file_path(s3_path, filename)
            # --- Set the Content type for the file being sent
            # (so that it downloads properly)
            # --- content_type can be 'image/png',
            # 'application/pdf', 'text/plain', etc.
            mime_type = mimetypes.guess_type(file_to_store) if mime_type is None \
                else mime_type
            s3_file.set_metadata('Content-Type', mime_type)

            # --- Determine whether the file_to_store is
            # an object or file path/string
            file_type = type(file_to_store)
            if file_type == str:
                s3_file.set_contents_from_filename(file_to_store)
            else:
                s3_file.set_contents_from_file(file_to_store)

            if return_url:
                file_key = self.bucket.get_key(s3_file.key)
                file_key.set_acl('public-read')
                file_url = file_key.generate_url(0, query_auth=False)
                return file_url

        except Exception as store_file_exception:
            self.log.warning("Exception while storing file on S3: " +
                             store_file_exception.message)

    def get_file(self, s3_path, file_to_get):
        """
        Stores the desired file locally (e.g. configuration file).
        :param s3_path:
        :param file_to_get:
        :return:
        """
        try:
            if self.verify_file(s3_path, file_to_get):
                retrieved_file = StringIO()
                # --- s3_path = "qa-projects/results/%s/%s/%s"
                # % (brand, branch, build_ID)
                s3_file = self.bucket.get_key(
                    self._generate_file_path(s3_path, file_to_get))
                s3_file.get_contents_to_file(retrieved_file)
                return retrieved_file
            else:
                raise S3ClientException("File not found in S3")

        except Exception as get_file_exception:
            self.log.warning("Exception while retrieving file from S3: " +
                             get_file_exception.message)

    def verify_file(self, s3_path, file_to_verify):
        """
        Verifies a file (e.g. configuration file) is on S3 and returns
        "True" or "False".
        :param s3_path:
        :param file_to_verify:
        :return "True" if .get_key returns an instance of a Key object or
        "False" if .get_key returns "None":
        """
        try:
            # --- s3_path = "qa-tools/marketing/baseline_tests/%s/%s/%s"
            # % (brand, branch, build_ID)
            file_path = self._generate_file_path(s3_path, file_to_verify)
            s3_file = self.bucket.get_key(file_path)
            if s3_file:
                return True
            else:
                return False

        except Exception as verify_file_exception:
            self.log.warning("Exception while verifying file on S3: " +
                             verify_file_exception.message)

    def _generate_file_path(self, s3_path, file_to_store):
        """
        Ensures that the / situation creates a proper path by removing any
        double slash possibilities
        :param s3_path: The path to the folder you wish to store the file in
        :param file_to_store: The name of the file you wish to store
        :return: The concatenated version of the /folder/filename path
        """
        return self.remove_leading_and_trailing_slashes(s3_path) + '/' \
            + self.remove_leading_and_trailing_slashes(file_to_store)

    def remove_leading_and_trailing_slashes(self, value):
        """
        Ensures that the value doesn't begin or end with a /
        :param value: The string to be parsed
        :return: The parsed version value
        """
        while value[0] is '/' or value[-1:] is '/':
            if value[0] is '/':
                value = value[1:]
            if value[-1:] is '/':
                value = value[:-1]
        return value

    def get_all_filenames_in_folder(self, path_to_folder, sort_by_date=True):
        s3_folder_path = str(path_to_folder)
        key_list = self.bucket.list(prefix=s3_folder_path)
        return key_list

    def get_most_recent_file_from_s3_key_list(self, key_list):
        # --- Sort out the most recent file for the list of keys
        most_recent_key = None
        for key in key_list:
            if not most_recent_key:
                most_recent_key = key
                continue
            if key.last_modified > most_recent_key.last_modified:
                most_recent_key = key
        return most_recent_key


class S3ClientException(Exception):
    def __init__(self, arg):
        self.msg = arg
