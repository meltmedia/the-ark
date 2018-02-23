import unittest
from mock import patch, Mock, call
from the_ark import jcr_helpers
import requests.exceptions

TEST_URL = "http://www.test.com"
TEST_PATH = "/content/path"

JCR_NON_PAGE = {
    "jcr:primaryType": "nt:unstructured",
    "jcr:lastModifiedBy": "admin",
    "jcr:lastModified": "Thu Dec 08 2016 00:19:17 GMT+0000"
}

JCR_GREATGRANDCHILD = {
    "jcr:primaryType": "cq:Page",
    "jcr:createdBy": "admin",
    "jcr:created": "Thu Jan 18 2018 00:17:21 GMT+0000",
    "jcr:content": {
        "jcr:primaryType": "cq:PageContent",
        "jcr:createdBy": "admin",
        "jcr:title": "Great Grandchild 1",
        "jcr:versionHistory": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "cq:template": "/greatgrandchild",
        "jcr:lastModifiedBy": "admin",
        "jcr:predecessors": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
        ],
        "jcr:created": "Thu Jan 18 2018 00:17:21 GMT+0000",
        "cq:lastModified": "Wed Jan 11 2017 16:15:23 GMT+0000",
        "jcr:baseVersion": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "jcr:lastModified": "Wed Jan 11 2017 16:15:23 GMT+0000",
        "jcr:uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "sling:resourceType": "/greatgrandchild",
        "cq:lastModifiedBy": "admin"
    }
}

JCR_GRANDCHILD_1 = {
    "jcr:primaryType": "cq:Page",
    "jcr:createdBy": "admin",
    "jcr:created": "Thu Jan 18 2018 00:17:21 GMT+0000",
    "jcr:content": {
        "jcr:primaryType": "cq:PageContent",
        "jcr:createdBy": "admin",
        "jcr:title": "Grandchild 1",
        "jcr:versionHistory": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "cq:template": "/grandchild1",
        "jcr:lastModifiedBy": "admin",
        "jcr:predecessors": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
        ],
        "jcr:created": "Thu Jan 18 2018 00:17:21 GMT+0000",
        "cq:lastModified": "Wed Jan 11 2017 16:15:23 GMT+0000",
        "jcr:baseVersion": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "jcr:lastModified": "Wed Jan 11 2017 16:15:23 GMT+0000",
        "jcr:uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "sling:resourceType": "/grandchild1",
        "cq:lastModifiedBy": "admin"
    },
    "great_grandchild1": JCR_GREATGRANDCHILD
}

JCR_GRANDCHILD_2 = {
    "jcr:primaryType": "cq:Page",
    "jcr:createdBy": "admin",
    "jcr:created": "Thu Jan 18 2018 00:17:21 GMT+0000",
    "jcr:content": {
        "jcr:primaryType": "cq:PageContent",
        "jcr:createdBy": "admin",
        "jcr:title": "Grandchild 2",
        "jcr:versionHistory": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "cq:template": "/grandchild2",
        "jcr:lastModifiedBy": "admin",
        "jcr:predecessors": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
        ],
        "jcr:created": "Thu Jan 18 2018 00:17:21 GMT+0000",
        "cq:lastModified": "Wed Jan 11 2017 16:15:23 GMT+0000",
        "jcr:baseVersion": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "jcr:lastModified": "Wed Jan 11 2017 16:15:23 GMT+0000",
        "jcr:uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "sling:resourceType": "/grandchild2",
        "cq:lastModifiedBy": "admin"
    },
    "nonpage3": JCR_NON_PAGE,
}

JCR_CHILD_1 = {
    "jcr:primaryType": "cq:Page",
    "jcr:createdBy": "admin",
    "jcr:created": "Mon Feb 19 2018 00:17:26 GMT+0000",
    "jcr:content": {
        "jcr:primaryType": "cq:PageContent",
        "jcr:createdBy": "admin",
        "jcr:title": "Child 1",
        "jcr:versionHistory": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "cq:template": "/child",
        "jcr:lastModifiedBy": "admin",
        "jcr:predecessors": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
        ],
        "jcr:created": "Fri Dec 09 2016 18:34:21 GMT+0000",
        "cq:lastModified": "Mon Feb 06 2017 17:33:11 GMT+0000",
        "jcr:baseVersion": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "jcr:uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "sling:resourceType": "/child",
        "cq:lastModifiedBy": "admin"
    }
}

JCR_CHILD_2 = {
    "jcr:primaryType": "cq:Page",
    "jcr:createdBy": "admin",
    "jcr:created": "Thu Jan 18 2018 00:17:21 GMT+0000",
    "jcr:content": {
        "jcr:primaryType": "cq:PageContent",
        "jcr:createdBy": "admin",
        "jcr:title": "Child 2",
        "jcr:versionHistory": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "cq:template": "/child2",
        "jcr:lastModifiedBy": "admin",
        "jcr:predecessors": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
        ],
        "jcr:created": "Thu Jan 18 2018 00:17:21 GMT+0000",
        "cq:lastModified": "Wed Nov 08 2017 18:22:25 GMT+0000",
        "jcr:description": "testing",
        "jcr:baseVersion": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "jcr:lastModified": "Thu Jan 12 2017 18:40:21 GMT+0000",
        "jcr:uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
        "sling:resourceType": "/child",
        "cq:lastModifiedBy": "admin"
    },
    "nonpage1": JCR_NON_PAGE,
    "nonpage2": JCR_NON_PAGE,
    "grandchild1": JCR_GRANDCHILD_1,
    "grandchild2": JCR_GRANDCHILD_2
}


class UtilsTestCase(unittest.TestCase):

    def setUp(self):

        self.jcr_content_infinity_dict = {
            "jcr:primaryType": "cq:Page",
            "jcr:createdBy": "admin",
            "jcr:created": "Thu Jan 18 2018 00:17:21 GMT+0000",
            "jcr:content": {
                "jcr:primaryType": "cq:PageContent",
                "jcr:createdBy": "admin",
                "jcr:title": "Root",
                "jcr:versionHistory": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
                "cq:template": "/root",
                "jcr:lastModifiedBy": "admin",
                "jcr:predecessors": [
                    "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
                ],
                "jcr:created": "Thu Jan 18 2018 00:17:21 GMT+0000",
                "cq:lastModified": "Mon Apr 24 2017 20:44:33 GMT+0000",
                "jcr:baseVersion": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
                "jcr:lastModified": "Mon Apr 24 2017 20:44:33 GMT+0000",
                "jcr:uuid": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
                "sling:resourceType": "/root",
                "cq:designPath": "/etc/designs/test",
                "cq:lastModifiedBy": "admin"
            },
            "nonpage": JCR_NON_PAGE,
            "child1": JCR_CHILD_1,
            "child2": JCR_CHILD_2
        }

        self.jcr_content_infinity_list = [
            "{}.2.json".format(TEST_PATH),
            "{}.1.json".format(TEST_PATH),
            "{}.0.json"
        ]

        self.page_hierarchy_with_jcr_content = {
            '{}.html'.format(TEST_PATH): {
                'children': ['{}/child1.html'.format(TEST_PATH), '{}/child2.html'.format(TEST_PATH)],
                'template': self.jcr_content_infinity_dict["jcr:content"]["cq:template"],
                'depth': 0,
                'parent': False,
                'jcr_content': self.jcr_content_infinity_dict["jcr:content"],
                'url': '{}{}.html'.format(TEST_URL, TEST_PATH)
            },
            '{}/child1.html'.format(TEST_PATH): {
                'children': [],
                'template': JCR_CHILD_1["jcr:content"]["cq:template"],
                'depth': 1,
                'parent': '{}.html'.format(TEST_PATH),
                'jcr_content': JCR_CHILD_1["jcr:content"],
                'url': '{}{}/child1.html'.format(TEST_URL, TEST_PATH)
            },
            '{}/child2.html'.format(TEST_PATH): {
                'children': ['{}/child2/grandchild1.html'.format(TEST_PATH),
                             '{}/child2/grandchild2.html'.format(TEST_PATH)],
                'template': JCR_CHILD_2["jcr:content"]["cq:template"],
                'depth': 1,
                'parent': '{}.html'.format(TEST_PATH),
                'jcr_content': JCR_CHILD_2["jcr:content"],
                'url': '{}{}/child2.html'.format(TEST_URL, TEST_PATH)
            },
            '{}/child2/grandchild1.html'.format(TEST_PATH): {
                'children': ['{}/child2/grandchild1/great_grandchild1.html'.format(TEST_PATH)],
                'template': JCR_GRANDCHILD_1["jcr:content"]["cq:template"],
                'depth': 2,
                'parent': '{}/child2.html'.format(TEST_PATH),
                'jcr_content': JCR_GRANDCHILD_1["jcr:content"],
                'url': '{}{}/child2/grandchild1.html'.format(TEST_URL, TEST_PATH)
            },
            '{}/child2/grandchild1/great_grandchild1.html'.format(TEST_PATH): {
                'children': [],
                'template': JCR_GREATGRANDCHILD["jcr:content"]["cq:template"],
                'depth': 3,
                'parent': '{}/child2/grandchild1.html'.format(TEST_PATH),
                'jcr_content': JCR_GREATGRANDCHILD["jcr:content"],
                'url': '{}{}/child2/grandchild1/great_grandchild1.html'.format(TEST_URL, TEST_PATH)
            },
            '{}/child2/grandchild2.html'.format(TEST_PATH): {
                'children': [],
                'template': JCR_GRANDCHILD_2["jcr:content"]["cq:template"],
                'depth': 2,
                'parent': '{}/child2.html'.format(TEST_PATH),
                'jcr_content': JCR_GRANDCHILD_2["jcr:content"],
                'url': '{}{}/child2/grandchild2.html'.format(TEST_URL, TEST_PATH)
            }
        }

        self.page_hierarchy = {
            k: {x: v[x] for x in v if x != "jcr_content"} for k, v in self.page_hierarchy_with_jcr_content.iteritems()
        }

    @patch('requests.get')
    def test_get_jcr_content_default_depth(self, requests_get):
        mock_response = Mock()
        mock_response.json.return_value = JCR_CHILD_1
        requests_get.return_value = mock_response

        resp = jcr_helpers.get_jcr_content(root_url=TEST_URL, root_path=TEST_PATH)
        requests_get.assert_called_once_with("{}{}.0.json".format(TEST_URL, TEST_PATH))
        self.assertEqual(resp, JCR_CHILD_1)

    @patch('requests.get')
    def test_get_jcr_content_provided_depth(self, requests_get):
        mock_response = Mock()
        mock_response.json.return_value = self.jcr_content_infinity_dict
        requests_get.return_value = mock_response

        test_url = "{}/".format(TEST_URL)
        test_path = TEST_PATH[1:]
        resp = jcr_helpers.get_jcr_content(root_url=test_url, root_path=test_path, depth=100)
        requests_get.assert_called_once_with("{}{}.100.json".format(test_url[:-1], "/{}".format(test_path)))
        self.assertEqual(resp, self.jcr_content_infinity_dict)

    @patch('requests.get')
    def test_get_jcr_content_infinity(self, requests_get):
        mock_response = Mock()
        mock_response.json.return_value = self.jcr_content_infinity_dict
        requests_get.return_value = mock_response

        resp = jcr_helpers.get_jcr_content(root_url=TEST_URL, root_path=TEST_PATH, infinity=True)
        requests_get.assert_called_once_with("{}{}.infinity.json".format(TEST_URL, TEST_PATH))
        self.assertEqual(resp, self.jcr_content_infinity_dict)

    @patch('requests.get')
    def test_get_jcr_content_missing_scheme(self, requests_get):
        mock_response = Mock()
        mock_response.json.return_value = JCR_CHILD_1
        requests_get.return_value = mock_response

        test_url = TEST_URL[7:]
        test_path = "{}.html".format(TEST_PATH)
        resp = jcr_helpers.get_jcr_content(root_url=test_url, root_path=test_path)
        requests_get.assert_called_once_with("http://{}{}.0.json".format(test_url, test_path[:-5]))
        self.assertEqual(resp, JCR_CHILD_1)

    @patch('requests.get')
    def test_get_jcr_content_request_exception(self, requests_get):
        requests_get.side_effect = requests.exceptions.ConnectionError()
        self.assertRaises(
            jcr_helpers.JCRHelperException, jcr_helpers.get_jcr_content,
            root_url=TEST_URL, root_path=TEST_PATH, infinity=True)

    @patch('requests.get')
    def test_get_jcr_content_unexpected_jcr_content_response(self, requests_get):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError()
        requests_get.return_value = mock_response
        self.assertRaises(
            jcr_helpers.JCRHelperException, jcr_helpers.get_jcr_content,
            root_url=TEST_URL, root_path=TEST_PATH, infinity=True)

    @patch('requests.get')
    def test_get_jcr_content_unexpected_error(self, requests_get):
        requests_get.return_value = {}
        self.assertRaises(
            jcr_helpers.JCRHelperException, jcr_helpers.get_jcr_content,
            root_url="", root_path=TEST_PATH, infinity=True)

    @patch('the_ark.jcr_helpers.get_jcr_content')
    def test_get_page_hierarchy_non_paginated(self, get_jcr_content):
        get_jcr_content.return_value = self.jcr_content_infinity_dict
        resp = jcr_helpers.get_page_hierarchy(TEST_URL, TEST_PATH)
        get_jcr_content.assert_called_once_with(root_url=TEST_URL, root_path=TEST_PATH, infinity=True)
        self.assertEqual(resp, self.page_hierarchy)

    @patch('the_ark.jcr_helpers.get_jcr_content')
    def test_get_page_hierarchy_paginated(self, get_jcr_content):
        get_jcr_content.side_effect = [self.jcr_content_infinity_list, self.jcr_content_infinity_dict]
        resp = jcr_helpers.get_page_hierarchy(TEST_URL, TEST_PATH)
        get_jcr_content.assert_has_calls([
            call(root_url=TEST_URL, root_path=TEST_PATH, infinity=True),
            call(root_url=TEST_URL, root_path=TEST_PATH, depth=self.jcr_content_infinity_list[0].split('.')[1])
        ])
        self.assertEqual(resp, self.page_hierarchy)

    @patch('the_ark.jcr_helpers.get_jcr_content')
    def test_get_page_hierarchy_missing_scheme(self, get_jcr_content):
        get_jcr_content.return_value = self.jcr_content_infinity_dict

        test_url = TEST_URL[7:]
        test_path = "{}.html".format(TEST_PATH)
        resp = jcr_helpers.get_page_hierarchy(root_url=test_url, root_path=test_path)
        get_jcr_content.assert_called_once_with(root_url=TEST_URL, root_path=TEST_PATH, infinity=True)
        self.assertEqual(resp, self.page_hierarchy)

    @patch('the_ark.jcr_helpers.get_jcr_content')
    def test_get_page_hierarchy_with_jcr_content(self, get_jcr_content):
        get_jcr_content.return_value = self.jcr_content_infinity_dict
        resp = jcr_helpers.get_page_hierarchy(TEST_URL, TEST_PATH, include_jcr_content=True)
        get_jcr_content.assert_called_once_with(root_url=TEST_URL, root_path=TEST_PATH, infinity=True)
        self.assertEqual(resp, self.page_hierarchy_with_jcr_content)

    @patch('the_ark.jcr_helpers.get_jcr_content')
    def test_get_page_hierarchy_unexpected_jcr_content(self, get_jcr_content):
        get_jcr_content.return_value = {}
        self.assertRaises(
            jcr_helpers.JCRHelperException, jcr_helpers.get_page_hierarchy,
            root_url=TEST_URL, root_path=TEST_PATH)

    def test_jcrhelperexception_to_string(self):
        jcr_exc = jcr_helpers.JCRHelperException(msg="error message")
        self.assertIn("error message", str(jcr_exc))

    def test_jcrhelperexception_with_stacktrace(self):
        jcr_exc = jcr_helpers.JCRHelperException(msg="error message", stacktrace="test")
        self.assertIn("test", str(jcr_exc))

    def test_exception_with_details(self):
        details = {"test": "testing"}
        jcr_exc = jcr_helpers.JCRHelperException(msg="error message", details=details)
        self.assertIn("test: testing", str(jcr_exc))
        self.assertIn("Exception Details", str(jcr_exc))
