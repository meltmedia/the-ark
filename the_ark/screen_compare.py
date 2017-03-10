import math
import numpy
from PIL import Image

OVERLAY_DIFFERENCE_COLOR = (220, 20, 60, 0)


def image_difference(image_1, image_2):
    image_1 = image_1.histogram()
    image_2 = image_2.histogram()

    diff_squares = [(image_1[i] - image_2[i]) ** 2 for i in xrange(len(image_1))]
    rms = math.sqrt(sum(diff_squares) / len(image_1))

    return rms


def compare_image(image_1, image_2, overlay_color=OVERLAY_DIFFERENCE_COLOR):

    # Gather the image data from each image and create an image object to map which pixels matched or not
    try:
        # Use the largest width and height between image_1 and image_2 to determine size of the compare_overlay
        overlay_width = image_1.size[0] if image_1.size[0] > image_2.size[0] else image_2.size[0]
        overlay_height = image_1.size[1] if image_1.size[1] > image_2.size[1] else image_2.size[1]

        # Create the overlay image canvas that the comare data will be injected to
        compare_overlay = Image.new("RGBA", (overlay_width, overlay_height))

        # TODO: Reminder to talk with Alex about the PNG vs JPEG updates he and Vince made on his local (converting jpegs to png so that they can be comparable to eachother?)
        # Get the pixel data for the images
        im1_data = numpy.asarray(image_1)
        im2_data = numpy.asarray(image_2)
        overlay_data = numpy.asarray(compare_overlay)

        # Set up the variables used in the compare logic
        pixel_total = (overlay_width * overlay_height)
        total_pixels_changed = 0
        # - The compare data for each pixel that will be stored in the overlay
        compare_data = []
    except Exception as e:
        raise ScreenCompareException("Error gathering the data for the images: {}".format(e))

    try:
        # TODO: Consider taking the image width difference, divided by two, then adding that to the X value of the wider image
        # TODO: Consider straight up checking if im1_data == im2_data before even jumping in

        for y, overlay_row in enumerate(overlay_data):
            if len(im1_data) - 1 >= y and len(im2_data) - 1 >= y:

                # Both images are at least "y" rows tall
                for x, overlay_pixel in enumerate(overlay_row):
                    # Both images are at least "x" pixels wide
                    if len(im1_data[y]) - 1 >= x and len(im2_data[y]) - 1 >= x:
                        # Check that the X pixel in the Y row for each image is the same
                        # - They are NOT the same
                        pixel1 = im1_data[y][x]
                        pixel2 = im2_data[y][x]
                        if pixel1.all() != pixel2.all():
                            compare_data.append(overlay_color)
                            total_pixels_changed += 1
                        else:
                            compare_data.append((255, 255, 255, 0))

                    # If either image is not X wide, color the pixel
                    else:
                        compare_data.append(overlay_color)
                        total_pixels_changed += 1

            # If either of the images is not Y tall, color the whole row
            else:
                for x in overlay_row:
                    compare_data.append(overlay_color)
                    total_pixels_changed += 1

    except Exception as e:
        raise ScreenCompareException("Error while appending red pixels: {}".format(e))

    percentage_changed = 100 * float(total_pixels_changed)/float(pixel_total)

    try:
        combined_image = Image.new("RGBA", (overlay_width, overlay_height))
        combined_image.paste(image_1)

        compare_overlay.putdata(compare_data)
        if compare_overlay.mode != image_1.mode:
            compare_overlay = compare_overlay.convert(image_1.mode)
        updated_image = Image.blend(combined_image, compare_overlay, .8)

        return percentage_changed, updated_image

    except Exception as e:
        raise ScreenCompareException("Could not merge and save the updated image : {}".format(e))


class ScreenCompareException(Exception):
    def __init__(self, msg, stacktrace=None, details=None):
        self.msg = msg
        self.details = {} if details is None else details
        self.details["stracktrace"] = stacktrace
        super(ScreenCompareException, self).__init__()

    def __str__(self):
        exception_msg = "Screenshot Exception: \n"
        detail_string = "Exception Details:\n"
        for key, value in self.details.items():
            detail_string += "{0}: {1}\n".format(key, value)
        exception_msg += detail_string
        exception_msg += "Message: {0}".format(self.msg)

        return exception_msg

