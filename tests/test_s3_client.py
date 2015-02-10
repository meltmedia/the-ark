import unittest
from the_ark.s3_client import S3Client
from mock import Mock, patch
from boto.s3.key import Key

__author__ = 'chaley'

bucket = "some bucket"


class S3InitTestCase(unittest.TestCase):

    @patch('boto.s3.connection.S3Connection')
    def test_class_init(self, s3con):
        s3con(False).return_value = {}
        client = S3Client(bucket)
        self.assertIsNotNone(client)

    @patch('boto.s3.connection.S3Connection')
    def test_class_init_fail(self, s3con):
        s3con.side_effect = Exception('Boom')
        client = S3Client(bucket)
        self.assertIsNone(client.s3_connection)


class S3MethodTestCase(unittest.TestCase):

    def setUp(self):
        self.client = S3Client(bucket)
        self.client.s3_connection = Mock()
        self.client.bucket = Mock()

    def test_generate_path(self):
        self.assertEqual('s3_path/file_to_store',
                         self.client._generate_file_path("/s3_path",
                                                         "file_to_store"))
        self.assertEqual('s3_path/file_to_store',
                         self.client._generate_file_path("s3_path/",
                                                         "file_to_store"))
        self.assertEqual('s3_path/file_to_store',
                         self.client._generate_file_path("s3_path",
                                                         "file_to_store/"))
        self.assertEqual('s3_path/file_to_store',
                         self.client._generate_file_path(
                             "/s3_path/", "///////file_to_store/"))
        self.assertEqual('qa/tools/marketing/file_to_store',
                         self.client._generate_file_path(
                             "/qa/tools/marketing", "file_to_store/"))

    def test_verify_file(self):
        self.client.bucket.get_key.return_value = None
        self.assertFalse(self.client.verify_file("s3_path", "file_to_store"))

        self.client.bucket.get_key.return_value = "testing"
        self.assertTrue(self.client.verify_file("s3_path", "file_to_store"))

    def test_verify_file_boom(self):
        self.client.bucket.get_key.side_effect = Exception(
            'Here Comes the Boom!')
        self.assertRaises(Exception, self.client.verify_file(
            'stuff', 'more stuff'))

    @patch('the_ark.s3_client.S3Client.verify_file')
    def test_get_file(self, verify):
        file = Mock()
        verify.return_value = True
        self.client.bucket.get_key.return_value = file
        self.client.get_file('stuff', 'more stuff')

        self.client.bucket.get_key.assert_called_once_with(
            'stuff/more stuff')

    def test_get_file_boom(self):
        self.client.bucket.get_key.side_effect = Exception(
            'Here Comes the Boom!')
        self.assertRaises(Exception, self.client.get_file(
            'stuff', 'more stuff'))

    def test_store_file_boom(self):
        self.assertRaises(Exception, self.client.store_file(
            'stuff', 'more stuff', 'file_name'))
        self.assertRaises(Exception, self.client.store_file(
            'stuff', 'more stuff', filename="bob's file"))

    @patch('mimetypes.guess_type')
    @patch('boto.s3.key.Key.set_contents_from_file')
    def test_store_file(self, set_contents, guess_type):
        guess_type.return_value("image/png")
        set_contents.return_value(True)
        self.client.store_file(
            'stuff', 1, return_url=True, filename="this file")

        self.client.store_file(
            'stuff', 1, return_url=False, filename="this file")

    @patch('boto.s3.bucket.Bucket.list')
    def test_get_all_filenames_in_folder(self, list):
        list.return_value = []
        self.client.get_all_filenames_in_folder('path', True)

    def test_get_most_recent_file_from_s3_key_list(self):
        first = Key()
        second = Key()
        third = Key()
        first.last_modified = 3
        second.last_modified = 4
        third.last_modified = 1
        key_list = [first, second, third]

        most_recent_key = self.client.\
            get_most_recent_file_from_s3_key_list(key_list)
        self.assertEqual(
            most_recent_key.last_modified, key_list[1].last_modified)

if __name__ == '__main__':
    unittest.main()
