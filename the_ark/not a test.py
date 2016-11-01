# import s3_client
#
# test = s3_client.S3Client("qa-projects")
# test.store_file(s3_path="/redirects/",
#                 file_to_store="/Users/sdadds/Downloads/Screenshots/accesssolutions_screenshots_05_10_2016_13.20.03.pdf",
#                 filename="hello world.pdf")

from the_ark import selenium_helpers
from time import sleep

s = selenium_helpers.SeleniumHelpers()
dictionary = {'browserName': 'firefox'}

s.create_driver(**dictionary)
s.load_url("https://www.google.com")
#s(dictionary)
s.move_cursor_to_location()
sleep(5)
s.move_cursor_to_location(1040,32)
sleep(5)
s.move_cursor_to_location(1232,78,True)
sleep(1)
s.move_cursor_to_location(True)