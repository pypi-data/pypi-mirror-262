# -*- coding: utf-8 -*-

import ast

from AppiumLibrary.locators import ElementFinder
from AppiumLibrary.keywords._logging import _LoggingKeywords
from .connectionmanagement import ConnectionManagement
from selenium.webdriver.remote.webelement import WebElement

cache_app = ConnectionManagement()
log = _LoggingKeywords()
element_finder_t = ElementFinder()


def isstr(s):
    return isinstance(s, str)


class ControlElement:

    def __init__(self):
         #เนื่องจากปัญหาเรื่องโครงสร้าง structure เลยยังไม่สามารถใช้ได้
        # self._element_finder_t = ElementFinder()
        # self._co = ConnectionManagement()
        # self._log = _LoggingKeywords()
        pass
    #KeyWord
    
        #Switch_Mode
        
    def t_switch_mode(self,mode):
        """
        Switch Mode ระหว่าง Flutter และ NATIVE_APP
        จำเป็นต้อง Run ด้วย automationname : Flutter เท่านั้น
        """
        driver = cache_app._current_application()

        if mode == 'NATIVE_APP':
            driver.switch_to.context('NATIVE_APP')
        if mode == 'FLUTTER':
            driver.switch_to.context('FLUTTER')
 
        #Click_Element
    def t_click_element(self,locator):
        """กด click หรือ tap element
        ตาม locator ที่ระบุเข้ามา
        """
        log._info("Clicking element '%s'." % locator)
        self._element_find_t(locator, True , True).click()

        #Get
    def t_get_element_attribute(self, locator, attribute):
        """Get element attribute using given attribute: name, value,...

        Examples:

        | Get Element Attribute | locator | name |
        | Get Element Attribute | locator | value |
        """
        elements = self._element_find_t(locator, False, True)
        ele_len = len(elements)
        if ele_len == 0:
            raise AssertionError("Element '%s' could not be found" % locator)
        elif ele_len > 1:
            log._info("CAUTION: '%s' matched %s elements - using the first element only" % (locator, len(elements)))

        try:
            attr_val = elements[0].get_attribute(attribute)
            log._info("Element '%s' attribute '%s' value '%s' " % (locator, attribute, attr_val))
            return attr_val
        except:
            raise AssertionError("Attribute '%s' is not valid for element '%s'" % (attribute, locator))
        
    def t_get_text(self, locator):
        """Get element text (for hybrid and mobile browser use `xpath` locator, others might cause problem)

        Example:

        | ${text} | Get Text | //*[contains(@text,'foo')] |

        New in AppiumLibrary 1.4.
        """
        text = self._get_text(locator)
        self._info("Element '%s' text is '%s' " % (locator, text))
        return text
    
    #PRIVATE_FUNCTION
        
    def _element_find_t(self, locator, first_only, required, tag=None):
        application = cache_app._current_application()
        elements = None
        if isstr(locator):
            _locator = locator
            elements = element_finder_t.find(application, _locator, tag)
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
    
    def _is_visible(self, locator):
        element = self._element_find_t(locator, True, False)
        if element is not None:
            return element.is_displayed()
        return None
    
    def _is_element_present(self, locator):
        application = cache_app._current_application()
        elements = element_finder_t.find(application, locator, None)
        return len(elements) > 0

    def _get_text(self, locator):
        element = self._element_find_t(locator, True, True)
        if element is not None:
            return element.text
        return None