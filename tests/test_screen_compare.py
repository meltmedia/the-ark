from mock import patch
import os
from PIL import Image
from StringIO import StringIO
from the_ark.screen_compare import image_difference, compare_image, ScreenCompareException
import unittest

ROOT = os.path.abspath(os.path.dirname(__file__))
COMPARE_IMAGE_1_PNG = '{0}/etc/compare_image1.png'.format(ROOT)
COMPARE_IMAGE_2_PNG = '{0}/etc/compare_image2.png'.format(ROOT)
BLACK_300_PNG = '{0}/etc/black_300x300.png'.format(ROOT)
IMAGE_COMPARE_RESULT_1_PNG = '{0}/etc/image_compare_result_1.jpeg'.format(ROOT)


class ScreenCompareTestCase(unittest.TestCase):

    # ===================================================================
    # --- Image Difference Test Cases
    # ===================================================================
    def test_image_difference(self):
        im1 = Image.open(COMPARE_IMAGE_1_PNG)
        im2 = Image.open(COMPARE_IMAGE_2_PNG)

        diff_amount = image_difference(im1, im2)
        self.assertEquals(int(diff_amount), 1448)

    # ===================================================================
    # --- Compare Image Cases
    # ===================================================================
    def test_compare_image(self):
        im1 = Image.open(COMPARE_IMAGE_1_PNG)
        im2 = Image.open(COMPARE_IMAGE_2_PNG)

        # TODO: Add an assert to make sure that the returned compare image matches this one
        static_compare_image = Image.open(IMAGE_COMPARE_RESULT_1_PNG)

        percent, comp_image = compare_image(im1, im2)

        self.assertEqual(int(percent), 31)
        self.assertIsInstance(comp_image, Image.Image)

    @patch("numpy.asarray")
    def test_comare_image_gather_data_error(self, mock_asarray):
        im1 = Image.open(COMPARE_IMAGE_1_PNG)
        im2 = Image.open(COMPARE_IMAGE_2_PNG)

        mock_asarray.side_effect = Exception("AHHHH!!")

        with self.assertRaises(ScreenCompareException) as compare_error:
            compare_image(im1, im2)

        self.assertIn("gathering the data", compare_error.exception.msg)

    def test_compare_image_too_wide_and_too_tall(self):
        im1 = Image.open(COMPARE_IMAGE_2_PNG)
        im2 = Image.open(BLACK_300_PNG)

        # TODO: Add an assert to make sure that the returned compare image matches this one
        # black_300 = Image.open(BLACK_300_PNG)

        percent, comp_image = compare_image(im1, im2)

        self.assertEqual(int(percent), 49)
        self.assertIsInstance(comp_image, Image.Image)



