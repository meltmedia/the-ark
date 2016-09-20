import util as c
import time

from the_ark import input_generator
from the_ark.field_handlers import STRING_FIELD, EMAIL_FIELD, PHONE_FIELD, ZIP_CODE_FIELD, DATE_FIELD


class Action:
    def __init__(self, screenshot_thread, selenium_helper, padding):
        self.t = screenshot_thread
        self.sh = selenium_helper
        self.padding = padding
        self.iteration = 0

    def capture(self, action, element):
        suffix = action.get(c.SUFFIX_KEY, "")
        padding = action.get(c.SCROLL_PADDING, "")
        if self.iteration:
            suffix = "{0}_{1:03d}".format(suffix, self.iteration)

        self.t.launch_capture(suffix, action.get(c.VIEWPORT_ONLY_KEY, False), padding)

    def capture_scrolling_element(self, action, element):
        suffix = action.get(c.SUFFIX_KEY, "")
        padding = action.get(c.SCROLL_PADDING, self.padding)
        if self.iteration:
            suffix = "{0}_{1:03d}".format(suffix, self.iteration)
        self.t.launch_capture_scrolling_element(action[c.CSS_SELECTOR_KEY], suffix, padding,
                                                action.get(c.VIEWPORT_ONLY_KEY, False))

    def load_url(self, action, element):
        path = action[c.PATH_KEY]
        test_url = c.concatenate_test_url(self.t.base_url, path, self.t.content_path)

        # - Always bypass the 404 check on author environments because the request library that does
        # the check is not authorized to check, returning a 401
        bypass = True if self.t.author else action.get(c.BYPASS_404_KEY, False)

        self.sh.load_url(test_url, bypass)

    def click(self, action, element):
        if element and action.get(c.ELEMENT_KEY):
            self.sh.click_an_element(web_element=element)
        else:
            self.sh.click_an_element(action[c.CSS_SELECTOR_KEY])

    def hover(self, action, element):
        if element and action.get(c.ELEMENT_KEY):
            self.sh.hover_on_element(web_element=element)
        else:
            self.sh.hover_on_element(action[c.CSS_SELECTOR_KEY])

    def enter_text(self, action, element):
        text = "Not-Set"
        if action.get(c.INPUT_TYPE_KEY):
            input_type = action.get(c.INPUT_TYPE_KEY)
            if input_type == STRING_FIELD:
                text = input_generator.generate_string()
            elif input_type == EMAIL_FIELD:
                text = input_generator.generate_email()
            elif input_type == ZIP_CODE_FIELD:
                text = input_generator.generate_zip_code()
            elif input_type == PHONE_FIELD:
                text = input_generator.generate_phone()
            elif input_type == DATE_FIELD:
                text = input_generator.generate_date()
        else:
            text = action[c.INPUT_KEY]
            if text == "brand":
                text = self.t.project

        if element and action.get(c.ELEMENT_KEY):
            self.sh.fill_an_element(text, web_element=element)
        else:
            self.sh.fill_an_element(text, action[c.CSS_SELECTOR_KEY])

    def scroll_window_to_position(self, action, elementn):
        self.sh.scroll_window_to_position(action.get(c.Y_POSITION_KEY, 0),
                                          action.get(c.X_POSITION_KEY, 0),
                                          action.get(c.POSITION_TOP_KEY, 0),
                                          action.get(c.POSITION_BOTTOM_KEY, 0))

    def scroll_window_to_element(self, action, element):
        if element and action.get(c.ELEMENT_KEY):
            self.sh.scroll_to_element(web_element=element,
                                      position_bottom=action.get(c.POSITION_BOTTOM_KEY),
                                      position_middle=action.get(c.POSITION_MIDDLE_KEY))
        else:
            self.sh.scroll_to_element(action[c.CSS_SELECTOR_KEY],
                                      position_bottom=action.get(c.POSITION_BOTTOM_KEY),
                                      position_middle=action.get(c.POSITION_MIDDLE_KEY))

    def scroll_an_element(self, action, element):
        y_pos = action.get(c.Y_POSITION_KEY)
        x_pos = action.get(c.X_POSITION_KEY)
        padding = action.get(c.SCROLL_PADDING)
        top = action.get(c.POSITION_TOP_KEY)
        bottom = action.get(c.POSITION_BOTTOM_KEY)

        if element and action.get(c.ELEMENT_KEY):
            self.sh.scroll_an_element(web_element=element, y_position=y_pos, x_position=x_pos,
                                      scroll_padding=padding, scroll_top=top, scroll_bottom=bottom)
        else:
            self.sh.scroll_an_element(css_selector=action[c.CSS_SELECTOR_KEY], y_position=y_pos,
                                      x_position=x_pos, scroll_padding=padding, scroll_top=top,
                                      scroll_bottom=bottom)

    def refresh(self, action, element):
        self.sh.refresh_driver()

    def sleep(self, action, element):
        time.sleep(action[c.DURATION_KEY])

    def wait_for_element(self, action, element):
        self.sh.wait_for_element(action[c.CSS_SELECTOR_KEY], action.get(c.DURATION_KEY, 15))

    def send_special_key(self, action, element):
        self.sh.send_special_key(action[c.SPECIAL_KEY_KEY])

    def reference(self, action, element):
        reference_key = action[c.REFERENCE_KEY]
        if isinstance(reference_key, list):
            for reference in reference_key:
                self.t.dispatch_actions(self.t.reference_actions[reference])
        else:
            self.t.dispatch_actions(self.t.reference_actions[reference_key])

    def show_element(self, action, element):
        if element and action.get(c.ELEMENT_KEY):
            self.sh.show_element(web_element=element)
        else:
            self.sh.show_element(action[c.CSS_SELECTOR_KEY])

    def hide_element(self, action, element):
        if element and action.get(c.ELEMENT_KEY):
            self.sh.hide_element(web_element=element)
        else:
            self.sh.hide_element(action[c.CSS_SELECTOR_KEY])

    def execute_script(self, action, element):
        if element and action.get(c.ELEMENT_KEY):
            self.sh.execute_script(action[c.SCRIPT_KEY], element)
        else:
            self.sh.execute_script(action[c.SCRIPT_KEY])

    def switch_window_handle(self, action, element):
        index = action.get(c.INDEX_KEY)
        if index is not None:
            handles = self.sh.get_window_handles()
            self.sh.switch_window_handle(handles[index])
        else:
            self.sh.switch_window_handle()

    def close_window(self, action, element):
        self.sh.close_window()

    def external(self, action, element):
        references = action[c.REFERENCE_KEY]
        if isinstance(references, list):
            for reference in references:
                self.t.dispatch_external_reference(action, reference)
        else:
            self.t.dispatch_external_reference(action, references)

    def for_each(self, action, element):
        elements = self.sh.get_list_of_elements(action[c.CSS_SELECTOR_KEY])

        # TODO: Raise Exception here if the elements list is empty
        for y, element in enumerate(elements):
            if not action.get(c.DO_NOT_INCREMENT_KEY):
                self.iteration += 1
            self.t.dispatch_actions(action[c.ACTION_LIST_KEY], element=element)

        if not action.get(c.CHILD_KEY):
            self.iteration = 0
