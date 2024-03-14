import time
import robot
import ast
import inspect
import os
#FROM จาก AppiumFlutterlibrary
from AppiumFlutterLibrary.keywords.keywordgroup import KeywordGroup
# from appium.webdriver.webelement import WebElement
# from AppiumFlutterLibrary.finder import ElementFinder

#FROM จาก Appiumlibrary
from appium.webdriver.common.appiumby import AppiumBy
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from AppiumLibrary.locators import ElementFinder
from unicodedata import normalize


def isstr(s):
    return isinstance(s, str)


class _MyAisHelpper(KeywordGroup):

    def __init__(self):
        self._element_finder_native = ElementFinder()
        self._bi = BuiltIn()

    #KEY WORD#
    
    #Switch_Mode#

    def myais_switch_mode(self,mode):
        """Switch Mode to NATIVE_APP OR FLUTTER.
        """
        driver = self._current_application()

        if mode == 'NATIVE_APP':
            driver.switch_to.context('NATIVE_APP')

        if mode == 'FLUTTER':
            driver.switch_to.context('FLUTTER')

    #Clear_Chace#

    def myais_quit(self):
        """Clear Chace.
        """
        driver = self._current_application()
        driver.quit()

    #Click#


    def myais_click_element(self,locator):
        """Tap the specified element , Click NATIVE_APP.

        If the element does not support tapping an error
        will be raised.
        """
        self._info("Clicking element '%s'." % locator)
        self._element_find(locator, True, True).click()

    #Wait#


    def myais_wait_until_element_is_visible(self, locator, timeout=None, error=None):
        """ยังใช้ไม่ได้
        Waits until element specified with `locator` is visible.

        Fails if `timeout` expires before the element is visible. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Page Contains`, `Wait Until Page Contains 
        Element`, `Wait For Condition` and BuiltIn keyword `Wait Until Keyword
        Succeeds`.
        """
        def check_visibility():
            visible = self._is_visible(locator)
            if visible:
                return
            elif visible is None:
                return error or "Element locator '%s' did not match any elements after %s" % (locator, self._format_timeout(timeout))
            else:
                return error or "Element '%s' was not visible in %s" % (locator, self._format_timeout(timeout))
        self._wait_until_no_error(timeout, check_visibility)

    
    def myais_wait_until_page_contains(self, text, timeout=None, error=None):
        """Waits until `text` appears on current page.

        Fails if `timeout` expires before the text appears. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Page Does Not Contain`,
        `Wait Until Page Contains Element`,
        `Wait Until Page Does Not Contain Element` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        if not error:
            error = "Text '%s' did not appear in <TIMEOUT>" % text
        self._wait_until(timeout, error, self._is_text_present, text)

    def myais_wait_until_page_does_not_contain(self, text, timeout=None, error=None):
        """
        Waits until `text` disappears from current page.

        Fails if `timeout` expires before the `text` disappears. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Page Contains`,
        `Wait Until Page Contains Element`,
        `Wait Until Page Does Not Contain Element` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.
        """

        def check_present():
            present = self._is_text_present(text)
            if not present:
                return
            else:
                return error or "Text '%s' did not disappear in %s" % (text, self._format_timeout(timeout))

        self._wait_until_no_error(timeout, check_present)

    def myais_wait_until_page_contains_element(self, locator, timeout=None, error=None):
        """ใช้ได้ปกติ
        Waits until element specified with `locator` appears on current page.

        Fails if `timeout` expires before the element appears. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Page Contains`,
        `Wait Until Page Does Not Contain`
        `Wait Until Page Does Not Contain Element`
        and BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        if not error:
            error = "Element '%s' did not appear in <TIMEOUT>" % locator
        self._wait_until(timeout, error, self._is_element_present, locator)
  
    def myais_wait_until_page_does_not_contain_element(self, locator, timeout=None, error=None):
        """ยังใช้ไม่ได้
        Waits until element specified with `locator` disappears from current page.

        Fails if `timeout` expires before the element disappears. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Page Contains`,
        `Wait Until Page Does Not Contain`,
        `Wait Until Page Contains Element` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.
        """

        def check_present():
            present = self._is_element_present(locator)
            if not present:
                return
            else:
                return error or "Element '%s' did not disappear in %s" % (locator, self._format_timeout(timeout))

        self._wait_until_no_error(timeout, check_present)

    #GET,Input_Text#
        
    def myais_input_text(self, locator, text):
        """Types the given `text` into text field identified by `locator`.

        See `introduction` for details about locating elements.
        """
        self._info("Typing text '%s' into text field '%s'" % (text, locator))
        self._element_input_text_by_locator(locator, text)


    def myais_get_text(self, locator):
        """Get element text (for hybrid and mobile browser use `xpath` locator, others might cause problem)

        Example:

        | ${text} | Get Text | //*[contains(@text,'foo')] |

        New in AppiumLibrary 1.4.
        """
        text = self._get_text(locator)
        self._info("Element '%s' text is '%s' " % (locator, text))
        return text

    def myais_get_element_attribute(self, locator, attribute):
        """Get element attribute using given attribute: name, value,...

        Examples:

        | Get Element Attribute | locator | name |
        | Get Element Attribute | locator | value |
        """
        elements = self._element_find(locator, False, True)
        ele_len = len(elements)
        if ele_len == 0:
            raise AssertionError("Element '%s' could not be found" % locator)
        elif ele_len > 1:
            self._info("CAUTION: '%s' matched %s elements - using the first element only" % (locator, len(elements)))

        try:
            attr_val = elements[0].get_attribute(attribute)
            self._info("Element '%s' attribute '%s' value '%s' " % (locator, attribute, attr_val))
            return attr_val
        except:
            raise AssertionError("Attribute '%s' is not valid for element '%s'" % (attribute, locator))
        

    #Swipe&Scroll#
    
    def myais_swipe(self, start_x, start_y, offset_x, offset_y, duration=1000):
        """
        Swipe from one point to another point, for an optional duration.

        Args:
         - start_x - x-coordinate at which to start
         - start_y - y-coordinate at which to start
         - offset_x - x-coordinate distance from start_x at which to stop
         - offset_y - y-coordinate distance from start_y at which to stop
         - duration - (optional) time to take the swipe, in ms.

        Usage:
        | Swipe | 500 | 100 | 100 | 0 | 1000 |

        _*NOTE: *_
        Android 'Swipe' is not working properly, use ``offset_x`` and ``offset_y`` as if these are destination points.
        """
        x_start = int(start_x)
        x_offset = int(offset_x)
        y_start = int(start_y)
        y_offset = int(offset_y)
        driver = self._current_application()
        driver.swipe(x_start, y_start, x_offset, y_offset, duration)


    def myais_scroll(self, start_locator, end_locator):
        """
        Scrolls from one element to another
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        el1 = self._element_find(start_locator, True, True)
        el2 = self._element_find(end_locator, True, True)
        driver = self._current_application()
        driver.scroll(el1, el2)



    #FUNCTION_DEF#
        
    #FUNCTION_Click#  
        
    def _find_element(self, locator):
        application = self._current_application()
        return self._element_finder_native.find(application, locator)
    
    def _element_find(self, locator, first_only, required, tag=None):
        application = self._current_application()
        elements = None
        if isstr(locator):
            _locator = locator
            elements = self._element_finder_native.find(application, _locator, tag)
            if required and len(elements) == 0:
                raise ValueError("Element locator '" + locator + "' did not match any elements.")
            if first_only:
                if len(elements) == 0: return None
                return elements[0]
        elif isinstance(locator, WebElement):
            if first_only:
                return locator
            else:
                elements = [locator]
        # do some other stuff here like deal with list of webelements
        # ... or raise locator/element specific error if required
        return elements
    
    #Function_Wait#

    def _wait_until(self, timeout, error, function, *args):
        error = error.replace('<TIMEOUT>', self._format_timeout(timeout))

        def wait_func():
            return None if function(*args) else error

        self._wait_until_no_error(timeout, wait_func)

    def _wait_until_no_error(self, timeout, wait_func, *args):
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else self._timeout_in_secs
        maxtime = time.time() + timeout
        while True:
            timeout_error = wait_func(*args)
            if not timeout_error:
                return
            if time.time() > maxtime:
                self.log_source()
                raise AssertionError(timeout_error)
            time.sleep(0.2)

    def _format_timeout(self, timeout):
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else self._timeout_in_secs
        return robot.utils.secs_to_timestr(timeout)
    

    def _is_element_present(self, locator):
        application = self._current_application()
        elements = self._element_finder_native.find(application, locator, None)
        return len(elements) > 0
    
    def _is_text_present(self, text):
        text_norm = normalize('NFD', text)
        source_norm = normalize('NFD', self.get_source())
        return text_norm in source_norm
    
    def _is_visible(self, locator):
        element = self._element_find(locator, True, False)
        if element is not None:
            return element.is_displayed()
        return None
    
    #Function_GET,Input_Text#

    def _element_input_text_by_locator(self, locator, text):
        try:
            element = self._element_find(locator, True, True)
            element.send_keys(text)
        except Exception as e:
            raise e

    def _get_text(self, locator):
        element = self._element_find(locator, True, True)
        if element is not None:
            return element.text
        return None


    #Function_OpenApp#

    def get_source(self):
        """Returns the entire source of the current page."""
        return self._current_application().page_source
    
    def log_source(self, loglevel='INFO'):
        """Logs and returns the entire html source of the current page or frame.

        The `loglevel` argument defines the used log level. Valid log levels are
        `WARN`, `INFO` (default), `DEBUG`, `TRACE` and `NONE` (no logging).
        """
        ll = loglevel.upper()
        if ll == 'NONE':
            return ''
        else:
            if  "run_keyword_and_ignore_error" not in [check_error_ignored[3] for check_error_ignored in inspect.stack()]:
                source = self._current_application().page_source
                self._log(source, ll)
                return source
            else:
                return ''


        
        