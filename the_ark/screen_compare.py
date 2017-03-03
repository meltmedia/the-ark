import math
from PIL import Image


def image_difference(image_1, image_2):
    image_1 = image_1.histogram()
    image_2 = image_2.histogram()

    diff_squares = [(image_1[i] - image_2[i]) ** 2 for i in xrange(len(image_1))]
    rms = math.sqrt(sum(diff_squares) / len(image_1))

    return rms


def compare_image(image_1, image_2):

    # Gather the image data from each image and create an image object to map which pixels matched or not
    try:
        # Use the largest width and height between image_1 and image_2 to determine size of the compare_overlay
        overlay_width = image_1.size[0] if image_1.size[0] > image_2.size[0] else image_2.size[0]
        overlay_height = image_1.size[1] if image_1.size[1] > image_2.size[1] else image_2.size[1]

        # Create the overlay image canvas that the comare data will be injected to
        compare_overlay = Image.new("RGBA", (overlay_width, overlay_height))

        # TODO: Reminder to talk with Alex about the PNG vs JPEG updates he and Vince made on his local (converting jpegs to png so that they can be comparable to eachother?)
        # Get the pixel data for the images
        im1_data = image_1.getdata()
        im2_data = image_2.getdata()

        # Set up the variables used in the compare logic
        pixel_total = (image_1.size[0] * image_1.size[1])
        total_pixels_changed = 0
        new_data = []
    except Exception as e:
        raise ScreenCompareException("Error gathering the data for the images: {}".format(e))

    try:
        for i in range(pixel_total):
            if im1_data[i] != im2_data[i]:
                new_data.append((220, 20, 60, 0))
                total_pixels_changed += 1
            else:
                new_data.append((255, 255, 255, 0))
    except Exception as e:
        raise ScreenCompareException("Error while appending red pixels: {}".format(e))

    # TODO: What are these pixels? The extra at the bottom when images aren't the same size?
    # ----- YES! these are the extra pixels in the bigger image.
    # ----- These won't matter if we're making compare_overlay the proper size
    for i in range(abs(len(im1_data) - len(new_data))):
        # TODO: Maybe make these black and count them as changed pixels?
        # ----- We will still need to find out how to calculate the extra pixels into the compare
        new_data.append((255, 255, 255, 0))

    percentage_changed = 100 * float(total_pixels_changed)/float(pixel_total)

    try:
        compare_overlay.putdata(new_data)
        if compare_overlay.mode != image_1.mode:
            compare_overlay = compare_overlay.convert(image_1.mode)
        updated_image = Image.blend(image_1, compare_overlay, .8)

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
