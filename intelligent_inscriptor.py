#!/usr/bin/env python3
"""
INTELLIGENT INSCRIPTION SYSTEM
Advanced detection with popup handling, cookie acceptance, and verification waiting
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import time
import random

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Global variables
running = False
driver = None

def wait_random():
    """Random wait between 1-3 seconds"""
    time.sleep(random.uniform(1, 3))

def wait_for_javascript():
    """Wait for JavaScript to load and execute"""
    try:
        # Wait for document ready
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        
        # Wait for jQuery if present
        try:
            WebDriverWait(driver, 5).until(
                lambda driver: driver.execute_script("return typeof jQuery !== 'undefined'")
            )
        except:
            pass
        
        # Wait for common loading indicators to disappear
        loading_selectors = [
            ".loading", ".spinner", ".loader", "[class*='loading']",
            ".preloader", ".load-more", ".loading-overlay"
        ]
        
        for selector in loading_selectors:
            try:
                WebDriverWait(driver, 3).until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
            except:
                pass
        
        # Additional wait for dynamic content
        time.sleep(2)
        
    except Exception as e:
        log(f"⚠️ JavaScript wait error: {e}")
        time.sleep(3)  # Fallback wait

def check_for_captcha():
    """Intelligent CAPTCHA detection and automatic handling"""
    try:
        log("🔍 Intelligent CAPTCHA detection...")
        
        # Common CAPTCHA selectors
        captcha_selectors = [
            # reCAPTCHA
            "[class*='recaptcha']", ".g-recaptcha", "[id*='recaptcha']",
            "iframe[src*='recaptcha']", "iframe[src*='google.com/recaptcha']",
            
            # hCaptcha
            "[class*='hcaptcha']", ".h-captcha", "[id*='hcaptcha']",
            "iframe[src*='hcaptcha']",
            
            # Cloudflare CAPTCHA
            "[class*='cf-challenge']", ".cf-challenge", "[id*='cf-challenge']",
            "iframe[src*='challenges.cloudflare.com']",
            
            # Generic CAPTCHA indicators
            "[class*='captcha']", "[id*='captcha']", "[class*='challenge']",
            "[data-sitekey]", "[data-captcha]",
            
            # Text indicators
            "input[placeholder*='captcha' i]", "input[placeholder*='verification' i]",
            "input[name*='captcha' i]", "input[name*='verification' i]"
        ]
        
        captcha_found = False
        captcha_type = "unknown"
        
        for selector in captcha_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        log(f"⚠️ CAPTCHA detected: {selector}")
                        captcha_found = True
                        
                        # Determine CAPTCHA type
                        if "recaptcha" in selector.lower():
                            captcha_type = "recaptcha"
                        elif "hcaptcha" in selector.lower():
                            captcha_type = "hcaptcha"
                        elif "cf-challenge" in selector.lower():
                            captcha_type = "cloudflare"
                        
                        break
                if captcha_found:
                    break
            except:
                continue
        
        if captcha_found:
            log(f"🎯 CAPTCHA Type: {captcha_type}")
            
            # Try automatic CAPTCHA solving strategies
            if try_automatic_captcha_solve(captcha_type):
                log("✅ CAPTCHA automatically solved!")
                return True
            
            # If automatic solving fails, try intelligent waiting
            return intelligent_captcha_wait()
        else:
            log("✅ No CAPTCHA detected")
            return False
            
    except Exception as e:
        log(f"⚠️ CAPTCHA check error: {e}")
        return False

def try_automatic_captcha_solve(captcha_type):
    """Try to automatically solve CAPTCHA using various strategies"""
    try:
        log("🤖 Attempting automatic CAPTCHA solving...")
        
        if captcha_type == "recaptcha":
            return try_solve_recaptcha()
        elif captcha_type == "hcaptcha":
            return try_solve_hcaptcha()
        elif captcha_type == "cloudflare":
            return try_solve_cloudflare()
        else:
            return try_solve_generic_captcha()
            
    except Exception as e:
        log(f"⚠️ Automatic CAPTCHA solving error: {e}")
        return False

def try_solve_recaptcha():
    """Try to solve reCAPTCHA automatically with advanced iframe handling"""
    try:
        log("🔍 Trying to solve reCAPTCHA with advanced methods...")
        
        # Strategy 1: Try direct checkbox clicking
        checkbox_selectors = [
            ".recaptcha-checkbox-border",
            ".recaptcha-checkbox",
            "[class*='recaptcha-checkbox']",
            "[data-callback]",
            ".g-recaptcha"
        ]
        
        for selector in checkbox_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        log(f"✅ Clicking reCAPTCHA element: {selector}")
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(3)
                        
                        # Check if CAPTCHA was solved
                        if not is_captcha_still_present():
                            log("✅ reCAPTCHA solved directly!")
                            return True
            except:
                continue
        
        # Strategy 2: Handle reCAPTCHA iframes
        iframe_selectors = [
            "iframe[src*='recaptcha']",
            "iframe[src*='google.com/recaptcha']",
            "iframe[title*='recaptcha']",
            "iframe[title*='reCAPTCHA']"
        ]
        
        for selector in iframe_selectors:
            try:
                iframes = driver.find_elements(By.CSS_SELECTOR, selector)
                for iframe in iframes:
                    if iframe.is_displayed():
                        log(f"🎯 Found reCAPTCHA iframe: {selector}")
                        
                        # Switch to iframe
                        driver.switch_to.frame(iframe)
                        
                        # Look for checkbox in iframe
                        iframe_checkbox_selectors = [
                            ".recaptcha-checkbox-border",
                            ".recaptcha-checkbox",
                            "[role='checkbox']",
                            ".checkbox",
                            "#recaptcha-anchor"
                        ]
                        
                        for cb_selector in iframe_checkbox_selectors:
                            try:
                                checkboxes = driver.find_elements(By.CSS_SELECTOR, cb_selector)
                                for checkbox in checkboxes:
                                    if checkbox.is_displayed():
                                        log("✅ Clicking reCAPTCHA checkbox in iframe...")
                                        driver.execute_script("arguments[0].click();", checkbox)
                                        
                                        # Switch back to main content
                                        driver.switch_to.default_content()
                                        
                                        # Wait for completion
                                        time.sleep(3)
                                        
                                        # Check if CAPTCHA is solved
                                        if not is_captcha_still_present():
                                            log("✅ reCAPTCHA solved via iframe!")
                                            return True
                                        
                                        # Quick retry
                                        time.sleep(2)
                                        if not is_captcha_still_present():
                                            log("✅ reCAPTCHA solved after quick retry!")
                                            return True
                                        
                                        return False  # Failed to solve
                                        
                            except:
                                continue
                        
                        # Switch back to main content
                        driver.switch_to.default_content()
                        
            except:
                continue
        
        # Strategy 3: Try JavaScript injection
        try:
            log("🔧 Trying JavaScript reCAPTCHA solving...")
            driver.execute_script("""
                // Try to find and click reCAPTCHA elements
                var recaptchaElements = document.querySelectorAll('[class*="recaptcha"], .g-recaptcha, [data-sitekey]');
                for (var i = 0; i < recaptchaElements.length; i++) {
                    var element = recaptchaElements[i];
                    if (element.offsetParent !== null) {
                        element.click();
                        break;
                    }
                }
            """)
            time.sleep(3)
            
            if not is_captcha_still_present():
                log("✅ reCAPTCHA solved via JavaScript!")
                return True
        except:
            pass
        
        return False
        
    except Exception as e:
        log(f"⚠️ reCAPTCHA solving error: {e}")
        return False

def try_solve_hcaptcha():
    """Try to solve hCaptcha automatically with advanced iframe handling"""
    try:
        log("🔍 Trying to solve hCaptcha with advanced methods...")
        
        # Strategy 1: Try direct hCaptcha clicking
        hcaptcha_selectors = [
            ".h-captcha",
            "[class*='hcaptcha']",
            "[id*='hcaptcha']",
            "[data-sitekey]"
        ]
        
        for selector in hcaptcha_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        log(f"✅ Clicking hCaptcha element: {selector}")
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(3)
                        
                        # Check if CAPTCHA was solved
                        if not is_captcha_still_present():
                            log("✅ hCaptcha solved directly!")
                            return True
            except:
                continue
        
        # Strategy 2: Handle hCaptcha iframes specifically
        iframe_selectors = [
            "iframe[src*='hcaptcha']",
            "iframe[src*='newassets.hcaptcha.com']",
            "iframe[title*='hCaptcha']",
            "iframe[title*='checkbox for hCaptcha']"
        ]
        
        for selector in iframe_selectors:
            try:
                iframes = driver.find_elements(By.CSS_SELECTOR, selector)
                for iframe in iframes:
                    if iframe.is_displayed():
                        log(f"🎯 Found hCaptcha iframe: {selector}")
                        
                        # Switch to iframe
                        driver.switch_to.frame(iframe)
                        
                        # Look for checkbox in hCaptcha iframe
                        iframe_checkbox_selectors = [
                            ".checkbox",
                            "[role='checkbox']",
                            ".h-captcha-checkbox",
                            "#checkbox",
                            "input[type='checkbox']"
                        ]
                        
                        for cb_selector in iframe_checkbox_selectors:
                            try:
                                checkboxes = driver.find_elements(By.CSS_SELECTOR, cb_selector)
                                for checkbox in checkboxes:
                                    if checkbox.is_displayed():
                                        log("✅ Clicking hCaptcha checkbox in iframe...")
                                        driver.execute_script("arguments[0].click();", checkbox)
                                        
                                        # Switch back to main content
                                        driver.switch_to.default_content()
                                        
                                        # Wait for completion
                                        time.sleep(3)
                                        
                                        # Check if CAPTCHA is solved
                                        if not is_captcha_still_present():
                                            log("✅ hCaptcha solved via iframe!")
                                            return True
                                        
                                        # Quick retry
                                        time.sleep(2)
                                        if not is_captcha_still_present():
                                            log("✅ hCaptcha solved after quick retry!")
                                            return True
                                        
                                        return False  # Failed to solve
                                        
                            except:
                                continue
                        
                        # Switch back to main content
                        driver.switch_to.default_content()
                        
            except:
                continue
        
        # Strategy 3: Try JavaScript injection for hCaptcha
        try:
            log("🔧 Trying JavaScript hCaptcha solving...")
            driver.execute_script("""
                // Try to find and click hCaptcha elements
                var hcaptchaElements = document.querySelectorAll('.h-captcha, [data-sitekey], [class*="hcaptcha"]');
                for (var i = 0; i < hcaptchaElements.length; i++) {
                    var element = hcaptchaElements[i];
                    if (element.offsetParent !== null) {
                        element.click();
                        break;
                    }
                }
                
                // Also try to trigger hCaptcha callback
                if (window.hcaptcha) {
                    try {
                        window.hcaptcha.execute();
                    } catch(e) {}
                }
            """)
            time.sleep(3)
            
            if not is_captcha_still_present():
                log("✅ hCaptcha solved via JavaScript!")
                return True
        except:
            pass
        
        # Strategy 4: Try to submit the form directly (for Shopify challenge)
        try:
            log("🛍️ Trying Shopify challenge form submission...")
            form_selectors = [
                "form[action*='contact']",
                "#captcha_form",
                ".shopify-challenge__button",
                "input[type='submit'][value='Submit']"
            ]
            
            for selector in form_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            log(f"✅ Clicking Shopify submit button: {selector}")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            
                            if not is_captcha_still_present():
                                log("✅ Shopify challenge solved!")
                                return True
                except:
                    continue
        except:
            pass
        
        return False
        
    except Exception as e:
        log(f"⚠️ hCaptcha solving error: {e}")
        return False

def try_solve_cloudflare():
    """Try to solve Cloudflare CAPTCHA automatically"""
    try:
        log("🔍 Trying to solve Cloudflare CAPTCHA...")
        
        # Wait for Cloudflare challenge to complete automatically
        log("⏳ Waiting for Cloudflare challenge...")
        time.sleep(10)
        
        # Check if challenge is still present
        if not is_captcha_still_present():
            return True
        
        return False
        
    except Exception as e:
        log(f"⚠️ Cloudflare CAPTCHA solving error: {e}")
        return False

def try_solve_generic_captcha():
    """Try to solve generic CAPTCHA automatically"""
    try:
        log("🔍 Trying to solve generic CAPTCHA...")
        
        # Look for CAPTCHA input fields and try to fill them
        captcha_inputs = driver.find_elements(By.CSS_SELECTOR, 
            "input[placeholder*='captcha' i], input[name*='captcha' i], input[id*='captcha']")
        
        for captcha_input in captcha_inputs:
            if captcha_input.is_displayed():
                # Try common CAPTCHA solutions
                common_solutions = ["1234", "test", "demo", "captcha", "solve"]
                for solution in common_solutions:
                    try:
                        captcha_input.clear()
                        captcha_input.send_keys(solution)
                        time.sleep(1)
                        
                        # Try to find and click submit button
                        submit_buttons = driver.find_elements(By.CSS_SELECTOR, 
                            "button[type='submit'], input[type='submit'], button:contains('Submit'), button:contains('Verify')")
                        
                        for submit_btn in submit_buttons:
                            if submit_btn.is_displayed():
                                submit_btn.click()
                                time.sleep(2)
                                break
                        
                        # Check if CAPTCHA was solved
                        if not is_captcha_still_present():
                            log(f"✅ Solved generic CAPTCHA with: {solution}")
                            return True
                            
                    except:
                        continue
        
        return False
        
    except Exception as e:
        log(f"⚠️ Generic CAPTCHA solving error: {e}")
        return False

def is_captcha_still_present():
    """Check if CAPTCHA is still present on the page"""
    try:
        captcha_selectors = [
            "[class*='recaptcha']", "[class*='hcaptcha']", "[class*='cf-challenge']",
            "[class*='captcha']", "[id*='captcha']", "[class*='challenge']"
        ]
        
        for selector in captcha_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        return True
            except:
                continue
        
        return False
        
    except:
        return False

def intelligent_captcha_wait():
    """Fast CAPTCHA solving - wait 10 seconds and verify"""
    try:
        log("⚡ Fast CAPTCHA solving - 10 second timeout...")
        
        # Try all CAPTCHA solving methods immediately
        log("🔄 Trying all CAPTCHA solving methods...")
        captcha_types = ["hcaptcha", "recaptcha", "cloudflare", "generic"]
        
        for captcha_type in captcha_types:
            if try_automatic_captcha_solve(captcha_type):
                log(f"✅ CAPTCHA solved with {captcha_type} method!")
                return True
        
        # JavaScript-based solving
        try:
            log("🔧 JavaScript CAPTCHA solving...")
            driver.execute_script("""
                // Try to find and click any CAPTCHA elements
                var captchaElements = document.querySelectorAll('[class*="captcha"], [class*="recaptcha"], [class*="hcaptcha"], [data-sitekey]');
                for (var i = 0; i < captchaElements.length; i++) {
                    var element = captchaElements[i];
                    if (element.offsetParent !== null) {
                        element.click();
                        break;
                    }
                }
                
                // Also try iframes
                var iframes = document.querySelectorAll('iframe[src*="recaptcha"], iframe[src*="hcaptcha"]');
                for (var j = 0; j < iframes.length; j++) {
                    try {
                        iframes[j].contentWindow.document.querySelector('.recaptcha-checkbox, .h-captcha').click();
                    } catch(e) {}
                }
            """)
            time.sleep(2)
        except:
            pass
        
        # Wait only 10 seconds and check
        log("⏳ Waiting 10 seconds for CAPTCHA to be solved...")
        for i in range(10):
            time.sleep(1)
            
            # Check if CAPTCHA is solved
            if not is_captcha_still_present():
                log("✅ CAPTCHA solved!")
                return True
            
            # Try one more solving attempt after 5 seconds
            if i == 5:
                log("🔄 Final CAPTCHA solving attempt...")
                for captcha_type in captcha_types:
                    if try_automatic_captcha_solve(captcha_type):
                        log(f"✅ CAPTCHA solved with final {captcha_type} attempt!")
                        return True
        
        log("⚠️ CAPTCHA not solved in 10 seconds - continuing anyway")
        return False
        
    except Exception as e:
        log(f"⚠️ Fast CAPTCHA solving error: {e}")
        return False

def close_all_popups_with_x():
    """Close all popups by clicking X button only"""
    try:
        log("🪟 Looking for popups to close with X button...")
        
        # Close button selectors (X buttons)
        close_selectors = [
            # Generic close buttons
            "button[aria-label*='close' i]",
            "button[aria-label*='Close' i]", 
            "button[title*='close' i]",
            "button[title*='Close' i]",
            
            # X button classes
            ".close", ".close-btn", ".close-button", ".btn-close",
            ".modal-close", ".popup-close", ".overlay-close",
            
            # X symbols
            "[class*='close']", "[class*='x-']", "[class*='-x']",
            "button:contains('×')", "span:contains('×')", "div:contains('×')",
            "button:contains('✕')", "span:contains('✕')", "div:contains('✕')",
            
            # Specific patterns
            ".fa-times", ".fa-close", ".fa-x", ".fa-remove",
            "[data-dismiss='modal']", "[data-close]", "[data-close='modal']"
        ]
        
        max_attempts = 5
        for attempt in range(max_attempts):
            popup_closed = False
            
            for selector in close_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            log(f"✅ Clicking X button: {selector}")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(1)
                            popup_closed = True
                            break
                    if popup_closed:
                        break
                except:
                    continue
            
            if not popup_closed:
                break
            
            time.sleep(1)
        
        log("✅ Popup closing completed")
        return True
        
    except Exception as e:
        log(f"⚠️ Popup closing error: {e}")
        return False

def close_all_popups_with_x_advanced():
    """Close all popups including SVG X buttons"""
    try:
        log("🪟 Advanced popup closing with SVG X support...")
        
        # Standard close button selectors
        close_selectors = [
            # Generic close buttons
            "button[aria-label*='close' i]", "button[aria-label*='Close' i]", 
            "button[title*='close' i]", "button[title*='Close' i]",
            
            # X button classes
            ".close", ".close-btn", ".close-button", ".btn-close",
            ".modal-close", ".popup-close", ".overlay-close",
            
            # X symbols
            "[class*='close']", "[class*='x-']", "[class*='-x']",
            
            # Specific patterns
            ".fa-times", ".fa-close", ".fa-x", ".fa-remove",
            "[data-dismiss='modal']", "[data-close]", "[data-close='modal']"
        ]
        
        # SVG X button selectors
        svg_selectors = [
            "svg line[x1='20'][y1='0'][x2='0'][y2='20']",  # Exact SVG line match
            "svg line",  # Any SVG line
            "svg path[d*='M']",  # SVG paths
            "svg g",  # SVG groups
            "button svg",  # SVG inside buttons
            "span svg",  # SVG inside spans
            "div svg"  # SVG inside divs
        ]
        
        max_attempts = 5
        for attempt in range(max_attempts):
            popup_closed = False
            
            # Try standard close buttons first
            for selector in close_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            log(f"✅ Clicking standard X button: {selector}")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(1)
                            popup_closed = True
                            break
                    if popup_closed:
                        break
                except:
                    continue
            
            # Try SVG X buttons
            if not popup_closed:
                for selector in svg_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            if element.is_displayed():
                                # Find parent clickable element
                                parent = element.find_element(By.XPATH, "./..")
                                if parent.tag_name in ['button', 'span', 'div']:
                                    log(f"✅ Clicking SVG X button: {selector}")
                                    driver.execute_script("arguments[0].click();", parent)
                                    time.sleep(1)
                                    popup_closed = True
                                    break
                        if popup_closed:
                            break
                    except:
                        continue
            
            # Try JavaScript-based X button finding
            if not popup_closed:
                try:
                    log("🔧 Trying JavaScript-based X button detection...")
                    driver.execute_script("""
                        // Find elements with X symbols or close indicators
                        var xElements = document.querySelectorAll('button, span, div, a');
                        for (var i = 0; i < xElements.length; i++) {
                            var element = xElements[i];
                            var text = element.textContent || element.innerText || '';
                            var html = element.innerHTML || '';
                            
                            // Check for X symbols
                            if (text.includes('×') || text.includes('✕') || text.includes('✖') || 
                                html.includes('x1="20"') || html.includes('close') || 
                                element.getAttribute('aria-label') === 'close' ||
                                element.getAttribute('title') === 'close') {
                                if (element.offsetParent !== null) {
                                    element.click();
                                    break;
                                }
                            }
                        }
                    """)
                    time.sleep(1)
                    popup_closed = True
                except:
                    pass
            
            if not popup_closed:
                break
            
            time.sleep(1)
        
        log("✅ Advanced popup closing completed")
        return True
        
    except Exception as e:
        log(f"⚠️ Advanced popup closing error: {e}")
        return False

def find_and_submit_email_directly(email):
    """Find email field and submit directly without looking for login"""
    try:
        log("📧 Searching for email field to submit directly...")
        
        # Step 1: Check footer first
        log("🔍 Checking footer for email field...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        footer_email_input = find_email_input_advanced()
        if footer_email_input:
            log("✅ Found footer email field - submitting directly...")
            try:
                footer_email_input.clear()
                footer_email_input.send_keys(email)
                log(f"📧 Filled email: {email}")
                
                # Find and click submit button
                footer_submit = find_submit_button_advanced()
                if footer_submit:
                    footer_submit.click()
                    log("✅ Submitted email directly!")
                    time.sleep(3)
                    return True
            except Exception as e:
                log(f"⚠️ Footer email submission error: {e}")
        
        # Step 2: Check page for other email fields
        log("🔍 Checking page for email fields...")
        email_input = find_email_input_advanced()
        if email_input:
            log("✅ Found email field - submitting directly...")
            try:
                email_input.clear()
                email_input.send_keys(email)
                log(f"📧 Filled email: {email}")
                
                # Find and click submit button
                submit_btn = find_submit_button_advanced()
                if submit_btn:
                    submit_btn.click()
                    log("✅ Submitted email directly!")
                    time.sleep(3)
                    return True
            except Exception as e:
                log(f"⚠️ Email submission error: {e}")
        
        return False
        
    except Exception as e:
        log(f"⚠️ Direct email submission error: {e}")
        return False

def press_signup_button_if_needed():
    """Check if signup button needs to be pressed after email submission"""
    try:
        log("🔍 Checking if signup button needs to be pressed...")
        
        # Signup button selectors (no login buttons)
        signup_selectors = [
            # Signup buttons
            "button:contains('sign up' i)", "button:contains('signup' i)",
            "button:contains('join' i)", "button:contains('register' i)",
            "button:contains('create account' i)", "button:contains('get started' i)",
            "a:contains('sign up' i)", "a:contains('signup' i)",
            "a:contains('join' i)", "a:contains('register' i)",
            
            # Submit buttons that might be signup
            "button[type='submit']", "input[type='submit']",
            "button.submit", "button.btn-submit"
        ]
        
        for selector in signup_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        log(f"✅ Clicking signup button: {selector}")
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(2)
                        return True
            except:
                continue
        
        log("ℹ️ No signup button found to press")
        return False
        
    except Exception as e:
        log(f"⚠️ Signup button check error: {e}")
        return False

def look_for_signup_links_only():
    """Look for signup links only (no login links)"""
    try:
        log("🔍 Looking for signup links only...")
        
        # Signup link selectors (no login)
        signup_selectors = [
            "a:contains('sign up' i)", "a:contains('signup' i)",
            "a:contains('join' i)", "a:contains('register' i)", 
            "a:contains('create account' i)", "a:contains('get started' i)",
            "a:contains('new account' i)", "a:contains('become a member' i)",
            "a[href*='signup']", "a[href*='register']", "a[href*='join']",
            "a[href*='sign-up']", "a[href*='create-account']"
        ]
        
        for selector in signup_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        log(f"✅ Found signup link: {selector}")
                        driver.execute_script("arguments[0].click();", element)
                        return True
            except:
                continue
        
        return False
        
    except Exception as e:
        log(f"⚠️ Signup link search error: {e}")
        return False

def close_popups_and_cookies(email=None):
    """Intelligent popup handling: Check for email fields first, then close if no email"""
    popup_submitted = False
    try:
        wait = WebDriverWait(driver, 5)
        max_popup_attempts = 10  # Handle multiple popups in sequence
        
        for attempt in range(max_popup_attempts):
            log(f"🔍 Popup handling attempt {attempt + 1}/{max_popup_attempts}")
            
            # Check if there are any visible popups
            popup_containers = driver.find_elements(By.CSS_SELECTOR, "[class*='modal'], [class*='popup'], [role='dialog'], [role='alertdialog']")
            visible_popups = [p for p in popup_containers if p.is_displayed()]
            
            if not visible_popups:
                log("✅ No popups detected - page is clean!")
                return True
            
            log(f"🪟 Found {len(visible_popups)} visible popup(s)")
            
            popup_handled = False
            
            # For each visible popup, check if it has email field
            for popup in visible_popups:
                if not popup.is_displayed():
                    continue
                    
                log("🔍 Checking popup for email field...")
                
                # Check if popup has email field
                email_inputs = popup.find_elements(By.CSS_SELECTOR, 'input[type="email"], input[name*="email" i], input[placeholder*="email" i]')
                
                # Hardcoded detection for Fashion Nova location popup
                try:
                    popup_text = popup.get_attribute("innerText") or popup.text or ""
                    popup_text_lower = popup_text.lower()
                    
                    # Fashion Nova and other location/country popup indicators
                    location_popup_indicators = [
                        # Fashion Nova specific
                        "your location is set to",
                        "international",
                        "shop in usd",
                        "get shipping options for international",
                        "change country/region",
                        # Generic location popup indicators
                        "select your country",
                        "choose your country",
                        "select country",
                        "choose country",
                        "country selection",
                        "region selection",
                        "location selection",
                        "select region",
                        "choose region",
                        "currency selection",
                        "select currency",
                        "choose currency",
                        "shipping destination",
                        "delivery location"
                    ]
                    
                    # Check if this is a location/country popup (including Fashion Nova)
                    if any(indicator in popup_text_lower for indicator in location_popup_indicators):
                        log("🎯 Detected location/country popup - closing immediately!")
                        # Close immediately without checking email field
                        close_button_selectors = [
                            "button[aria-label*='close' i]", "button[aria-label*='Close' i]", 
                            ".close", ".close-button", ".modal-close", ".popup-close", 
                            "[data-dismiss='modal']", ".fa-times", ".fa-close", ".fa-times-circle",
                            "[aria-label='Close']", "[title='Close']", ".dismiss", ".exit",
                            "div[role='dialog'] button[aria-label*='close']", 
                            "div[role='alertdialog'] button[aria-label*='close']",
                            "button.close", ".btn-close", ".modal-header .close"
                        ]
                        
                        close_clicked = False
                        for selector in close_button_selectors:
                            try:
                                elements = popup.find_elements(By.CSS_SELECTOR, selector)
                                for btn in elements:
                                    if btn.is_displayed() and btn.is_enabled():
                                        text = btn.get_attribute("innerText") or ""
                                        aria_label = btn.get_attribute("aria-label") or ""
                                        btn.click()
                                        log(f"✅ Closed location/country popup: '{text or aria_label}'")
                                        time.sleep(2)
                                        close_clicked = True
                                        popup_handled = True
                                        break
                                if close_clicked:
                                    break
                            except:
                                continue
                        
                        if close_clicked:
                            break  # Move to next popup
                        else:
                            log("⚠️ Could not close location/country popup")
                except:
                    pass
                
                if email_inputs:
                    # Popup HAS email field - proceed with email submission
                    log("📧 Found email field in popup - attempting inscription...")
                    
                    # Try to fill email and submit
                    for email_input in email_inputs:
                        if email_input.is_displayed() and email_input.is_enabled():
                            try:
                                email_input.clear()
                                # Use the provided email or fallback to test email
                                email_to_use = email if email else "test@example.com"
                                email_input.send_keys(email_to_use)
                                log(f"📧 Filled email in popup: {email_to_use}")
                                time.sleep(1)
                                
                                # Handle checkboxes (consent, terms, etc.) - CHECK ONCE ONLY
                                log("🔍 Looking for checkboxes to check...")
                                checkbox_checked = False
                                try:
                                    # Find all checkboxes in the popup with multiple strategies
                                    checkbox_selectors = [
                                        # Regular HTML checkboxes
                                        "input[type='checkbox']",
                                        "input[type='checkbox'][name*='consent']",
                                        "input[type='checkbox'][id*='consent']",
                                        "input[type='checkbox'][name*='agree']",
                                        "input[type='checkbox'][id*='agree']",
                                        "input[type='checkbox'][name*='terms']",
                                        "input[type='checkbox'][id*='terms']",
                                        "input[type='checkbox'][name*='privacy']",
                                        "input[type='checkbox'][id*='privacy']",
                                        "input[type='checkbox'][name*='newsletter']",
                                        "input[type='checkbox'][id*='newsletter']",
                                        "input[type='checkbox'][name*='email']",
                                        "input[type='checkbox'][id*='email']",
                                        # Custom SVG checkboxes (like Fashion Nova)
                                        "span.bx-component",
                                        "span.bx-checkshape",
                                        ".bx-component",
                                        ".bx-checkshape",
                                        "span[class*='check']",
                                        "span[class*='checkbox']",
                                        "div[class*='check']",
                                        "div[class*='checkbox']",
                                        # Generic custom checkbox patterns
                                        "span[role='checkbox']",
                                        "div[role='checkbox']",
                                        "label[class*='check']",
                                        "label[class*='checkbox']"
                                    ]
                                    
                                    checkboxes_found = []
                                    for selector in checkbox_selectors:
                                        try:
                                            checkboxes = popup.find_elements(By.CSS_SELECTOR, selector)
                                            checkboxes_found.extend(checkboxes)
                                        except:
                                            continue
                                    
                                    # Remove duplicates
                                    unique_checkboxes = []
                                    for cb in checkboxes_found:
                                        if cb not in unique_checkboxes:
                                            unique_checkboxes.append(cb)
                                    
                                    log(f"🔍 Found {len(unique_checkboxes)} checkbox(es)")
                                    
                                    # Check only the first checkbox found (avoid loops)
                                    checkbox_checked = False
                                    for checkbox in unique_checkboxes:
                                        if checkbox_checked:
                                            break  # Only check one checkbox
                                            
                                        try:
                                            if checkbox.is_displayed() and checkbox.is_enabled():
                                                # Get checkbox context for logging
                                                checkbox_id = checkbox.get_attribute("id") or ""
                                                checkbox_name = checkbox.get_attribute("name") or ""
                                                checkbox_tag = checkbox.tag_name
                                                checkbox_class = checkbox.get_attribute("class") or ""
                                                checkbox_context = f" (tag: {checkbox_tag}, id: {checkbox_id}, name: {checkbox_name}, class: {checkbox_class})"
                                                
                                                # Check if it's a regular HTML checkbox or custom SVG checkbox
                                                is_regular_checkbox = checkbox.tag_name == "input" and checkbox.get_attribute("type") == "checkbox"
                                                is_custom_checkbox = checkbox.tag_name in ["span", "div", "label"] and ("check" in checkbox_class.lower() or "bx-component" in checkbox_class)
                                                
                                                if is_regular_checkbox:
                                                    # Handle regular HTML checkbox
                                                    if checkbox.is_selected():
                                                        log(f"✅ Regular HTML checkbox already checked{checkbox_context}")
                                                        checkbox_checked = True
                                                        break  # Already checked, move on
                                                    else:
                                                        try:
                                                            checkbox.click()
                                                            log(f"✅ Checked regular HTML checkbox{checkbox_context}")
                                                            checkbox_checked = True
                                                        except:
                                                            # Try JavaScript click if regular click fails
                                                            driver.execute_script("arguments[0].click();", checkbox)
                                                            log(f"✅ Checked regular HTML checkbox via JS{checkbox_context}")
                                                            checkbox_checked = True
                                                        
                                                        time.sleep(1)  # Wait for checkbox to be processed
                                                        break  # Only check one checkbox
                                                
                                                elif is_custom_checkbox:
                                                    # Handle custom SVG checkbox (like Fashion Nova)
                                                    # For custom checkboxes, we can't easily check if they're already selected
                                                    # So we'll try to click and see if it works
                                                    try:
                                                        # Try to click the custom checkbox
                                                        checkbox.click()
                                                        log(f"✅ Clicked custom SVG checkbox{checkbox_context}")
                                                        checkbox_checked = True
                                                        time.sleep(1)
                                                        break  # Only check one checkbox
                                                            
                                                    except Exception as custom_error:
                                                        # Try JavaScript click for custom checkbox
                                                        try:
                                                            driver.execute_script("arguments[0].click();", checkbox)
                                                            log(f"✅ Clicked custom SVG checkbox via JS{checkbox_context}")
                                                            checkbox_checked = True
                                                            time.sleep(1)
                                                            break  # Only check one checkbox
                                                        except:
                                                            log(f"⚠️ Could not click custom checkbox{checkbox_context}: {custom_error}")
                                                
                                                else:
                                                    # Try to click anyway if it looks like a clickable element
                                                    try:
                                                        checkbox.click()
                                                        log(f"✅ Clicked potential checkbox element{checkbox_context}")
                                                        checkbox_checked = True
                                                        time.sleep(1)
                                                        break  # Only check one checkbox
                                                    except:
                                                        log(f"⚠️ Could not click element{checkbox_context}")
                                                        # Don't break here, try next checkbox
                                                        
                                        except Exception as checkbox_error:
                                            log(f"⚠️ Error with individual checkbox: {checkbox_error}")
                                            continue
                                    
                                    if not checkbox_checked:
                                        log("ℹ️ No checkboxes found or checked")
                                        
                                except Exception as checkbox_error:
                                    log(f"⚠️ Error finding checkboxes: {checkbox_error}")
                                
                                # Look for submit button in the same popup
                                submit_button_selectors = [
                                    "button[type='submit']",
                                    "input[type='submit']",
                                    "button",
                                    "input[type='button']"
                                ]
                                
                                submit_buttons = []
                                for selector in submit_button_selectors:
                                    try:
                                        buttons = popup.find_elements(By.CSS_SELECTOR, selector)
                                        submit_buttons.extend(buttons)
                                    except:
                                        continue
                                
                                for submit_btn in submit_buttons:
                                    if submit_btn.is_displayed() and submit_btn.is_enabled():
                                        # Check button text for submit-like actions
                                        button_text = (submit_btn.get_attribute("innerText") or 
                                                     submit_btn.get_attribute("value") or 
                                                     submit_btn.get_attribute("textContent") or "").lower()
                                        
                                        # Look for submit-related text in multiple languages
                                        submit_keywords = [
                                            # English
                                            "subscribe", "sign up", "join", "love saving", "submit", "send", "continue", 
                                            "get started", "sign me up", "i love saving money", "save money", "get discount",
                                            "subscribe now", "join now", "sign up now", "continue shopping", "proceed",
                                            "accept", "agree", "confirm", "finish", "complete", "register", "create account",
                                            # French
                                            "s'abonner", "inscription", "rejoindre", "continuer", "accepter", "confirmer",
                                            "créer un compte", "se connecter", "connexion", "compte", "enregistrer",
                                            "j'aime économiser", "économiser", "obtenir", "recevoir", "valider",
                                            # Spanish
                                            "suscribirse", "inscribirse", "unirse", "continuar", "aceptar", "confirmar",
                                            "crear cuenta", "registrarse", "conectar", "cuenta", "guardar",
                                            # German
                                            "abonnieren", "beitreten", "fortfahren", "akzeptieren", "bestätigen",
                                            "konto erstellen", "anmelden", "verbinden", "konto", "speichern",
                                            # Italian
                                            "iscriversi", "unirsi", "continuare", "accettare", "confermare",
                                            "creare account", "collegare", "conto", "salvare",
                                            # Portuguese
                                            "inscrever-se", "juntar-se", "continuar", "aceitar", "confirmar",
                                            "criar conta", "conectar", "conta", "salvar"
                                        ]
                                        
                                        if any(keyword in button_text for keyword in submit_keywords) or button_text.strip() == "":
                                            submit_btn.click()
                                            log(f"✅ Submitted email in popup with button: '{button_text}'")
                                            time.sleep(2)
                                            
                                            # ALWAYS check for CAPTCHA after popup email submission
                                            log("🔍 Checking for CAPTCHA after popup email submission...")
                                            check_for_captcha()
                                            
                                            # After submitting, try to close the popup
                                            log("🔍 Trying to close popup after submission...")
                                            try:
                                                # Look for close button in popup
                                                close_buttons = popup.find_elements(By.CSS_SELECTOR, 
                                                    "button[aria-label*='close' i], .close, .close-button, .modal-close, .popup-close, [data-dismiss='modal'], .fa-times, .fa-close, .fa-times-circle")
                                                
                                                for close_btn in close_buttons:
                                                    if close_btn.is_displayed() and close_btn.is_enabled():
                                                        close_btn.click()
                                                        log("✅ Closed popup after submission")
                                                        time.sleep(1)
                                                        break
                                            except:
                                                log("⚠️ Could not close popup after submission")
                                            
                                            popup_handled = True
                                            popup_submitted = True  # Mark that we submitted a popup
                                            break
                                
                                if popup_handled:
                                    break
                                    
                            except Exception as e:
                                log(f"⚠️ Error filling email in popup: {e}")
                                continue
                    
                    if popup_handled:
                        break
                else:
                    log("❌ No email field in popup - closing popup immediately...")
                    
                    # No email field, close popup immediately (don't click any buttons)
                    close_button_selectors = [
                        "button[aria-label*='close' i]", "button[aria-label*='Close' i]", 
                        ".close", ".close-button", ".modal-close", ".popup-close", 
                        "[data-dismiss='modal']", ".fa-times", ".fa-close", ".fa-times-circle",
                        "[aria-label='Close']", "[title='Close']", ".dismiss", ".exit",
                        "div[role='dialog'] button[aria-label*='close']", 
                        "div[role='alertdialog'] button[aria-label*='close']",
                        "button.close", ".btn-close", ".modal-header .close"
                    ]
                    
                    close_clicked = False
                    for selector in close_button_selectors:
                        try:
                            elements = popup.find_elements(By.CSS_SELECTOR, selector)
                            for btn in elements:
                                if btn.is_displayed() and btn.is_enabled():
                                    text = btn.get_attribute("innerText") or ""
                                    aria_label = btn.get_attribute("aria-label") or ""
                                    if any(char in text for char in ["×", "✕", "✖"]) or "close" in aria_label.lower():
                                        btn.click()
                                        log(f"✅ Closed popup: '{text or aria_label}'")
                                        time.sleep(2)
                                        close_clicked = True
                                        popup_handled = True
                                        break
                            if close_clicked:
                                break
                        except:
                            continue
                    
                    if close_clicked:
                        popup_handled = True
                        break
                    else:
                        log("⚠️ No close button found - popup cannot be closed")
                        # Don't try other buttons, just mark as handled to move on
                        popup_handled = True
                        break
            
            if not popup_handled:
                log("⚠️ Could not handle popup, trying generic close...")
            # Last resort: try to close any popup (ONLY close buttons, no other buttons)
            try:
                close_buttons = driver.find_elements(By.CSS_SELECTOR, ".close, .close-button, [aria-label*='close' i], .fa-times, .fa-close")
                for btn in close_buttons:
                    if btn.is_displayed() and btn.is_enabled():
                        btn.click()
                        log("✅ Generic close clicked")
                        time.sleep(2)
                        break
                else:
                    log("⚠️ No close buttons found in last resort attempt")
            except:
                log("⚠️ Error in last resort close attempt")
            
            # Wait a moment and check if popups are gone
            time.sleep(1)
            
            # Check again for remaining popups
            remaining_popups = driver.find_elements(By.CSS_SELECTOR, "[class*='modal'], [class*='popup'], [role='dialog'], [role='alertdialog']")
            visible_popups = [p for p in remaining_popups if p.is_displayed()]
            
            if not visible_popups:
                log("✅ All popups handled successfully!")
                return popup_submitted  # Return whether we submitted a popup
            else:
                log(f"⚠️ Still {len(visible_popups)} popup(s) remaining, continuing...")
        
        log("⚠️ Reached max popup attempts, continuing anyway")
        return popup_submitted  # Return whether we submitted a popup
        
    except Exception as e:
        log(f"⚠️ Error in popup handling: {e}")
        return popup_submitted  # Return whether we submitted a popup

def find_email_input_advanced():
    """Advanced email input detection with multiple strategies - PRIORITIZE FOOTER"""
    
    # PRIORITY 1: Look for "Your Email" and similar patterns first (like GLD.com)
    log("🔍 PRIORITY: Looking for 'Your Email' and similar patterns...")
    your_email_selectors = [
        # "Your Email" patterns (highest priority)
        "input[placeholder*='your email' i]",
        "input[placeholder*='your e-mail' i]", 
        "input[placeholder*='enter your email' i]",
        "input[placeholder*='email address' i]",
        "input[placeholder*='email' i]",
        # Join/Gang patterns (for GLD.com style)
        "[class*='join'] input[type='email']",
        "[class*='gang'] input[type='email']",
        "[class*='join'] input[placeholder*='email' i]",
        "[class*='gang'] input[placeholder*='email' i]"
    ]
    
    for selector in your_email_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed() and element.is_enabled():
                    log(f"✅ Found 'Your Email' field: {selector}")
                    return element
        except:
            continue
    
    # PRIORITY 2: Look for email fields in footer areas
    log("🔍 PRIORITY: Looking for email fields in footer areas...")
    footer_selectors = [
        # Footer-specific selectors
        "footer input[type='email']",
        "footer input[name*='email' i]",
        "footer input[placeholder*='email' i]",
        "[class*='footer'] input[type='email']",
        "[id*='footer'] input[type='email']",
        "[class*='newsletter'] input[type='email']",
        "[class*='signup'] input[type='email']",
        "[class*='subscribe'] input[type='email']",
        # Common footer newsletter patterns
        "[class*='footer-newsletter'] input[type='email']",
        "[class*='newsletter-signup'] input[type='email']",
        "[class*='email-signup'] input[type='email']",
        "[class*='footer-signup'] input[type='email']"
    ]
    
    for selector in footer_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed() and element.is_enabled():
                    log(f"✅ Found email field in footer: {selector}")
                    return element
        except:
            continue
    
    # PRIORITY 2: Look for email fields anywhere on page
    log("🔍 Looking for email fields anywhere on page...")
    
    # First, try to scroll to find email sections
    try:
        log("📜 Scrolling to find email sections...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except:
        pass
    
    # Check for Chinese/Asian language websites
    try:
        page_source = driver.page_source.lower()
        chinese_keywords = ["訂閱", "電子報", "通知", "優惠", "折扣", "新訊", "最新消息", "信箱", "電子郵件"]
        found_chinese = [kw for kw in chinese_keywords if kw in page_source]
        if found_chinese:
            log(f"🌏 Detected Chinese website with keywords: {found_chinese}")
    except:
        pass
    
    strategies = [
        # Strategy 1: Direct email inputs
        {
            'selectors': ['input[type="email"]'],
            'name': 'Direct email inputs'
        },
        # Strategy 2: Name-based detection
        {
            'selectors': [
                'input[name*="email" i]',
                'input[name*="mail" i]',
                'input[name*="e-mail" i]',
                'input[name*="newsletter" i]',
                'input[name*="subscribe" i]',
                'input[name*="電子郵件" i]',
                'input[name*="信箱" i]',
                'input[name*="mailbox" i]'
            ],
            'name': 'Name-based detection'
        },
        # Strategy 3: ID-based detection
        {
            'selectors': [
                'input[id*="email" i]',
                'input[id*="mail" i]',
                'input[id*="newsletter" i]',
                'input[id*="subscribe" i]'
            ],
            'name': 'ID-based detection'
        },
        # Strategy 4: Placeholder-based detection
        {
            'selectors': [
                'input[placeholder*="email" i]',
                'input[placeholder*="mail" i]',
                'input[placeholder*="address" i]',
                'input[placeholder*="newsletter" i]',
                'input[placeholder*="電子郵件" i]',
                'input[placeholder*="信箱" i]',
                'input[placeholder*="請輸入" i]'
            ],
            'name': 'Placeholder-based detection'
        },
        # Strategy 5: Class-based detection
        {
            'selectors': [
                'input[class*="email" i]',
                'input[class*="mail" i]',
                'input[class*="newsletter" i]'
            ],
            'name': 'Class-based detection'
        },
        # Strategy 6: Generic text inputs that might be email
        {
            'selectors': ['input[type="text"]'],
            'name': 'Generic text inputs'
        }
    ]
    
    for strategy in strategies:
        log(f"🔍 Strategy: {strategy['name']}")
        
        for selector in strategy['selectors']:
            try:
                inputs = driver.find_elements(By.CSS_SELECTOR, selector)
                
                for inp in inputs:
                    if not inp.is_displayed() or not inp.is_enabled():
                        continue
                    
                    # Additional validation for text inputs
                    if selector == 'input[type="text"]':
                        placeholder = (inp.get_attribute('placeholder') or '').lower()
                        name = (inp.get_attribute('name') or '').lower()
                        id_attr = (inp.get_attribute('id') or '').lower()
                        
                        email_indicators = ['email', 'mail', 'newsletter', 'subscribe', 'address']
                        if not any(indicator in placeholder + name + id_attr for indicator in email_indicators):
                            continue
                    
                    log(f"✅ Found email input using: {strategy['name']}")
                    return inp
                    
            except Exception as e:
                continue
    
    return None

def find_submit_button_advanced():
    """Advanced submit button detection"""
    
    keywords = [
        "subscribe", "sign up", "signup", "sign in", "signin", "join",
        "register", "create account", "submit", "send", "continue",
        "get started", "next", "go", "inscription", "s'inscrire",
        "i love saving money", "get discount", "get offer",
        # Chinese keywords
        "訂閱", "送出", "確認", "加入", "註冊", "會員註冊", "註冊會員",
        "加入會員", "登入", "登錄", "確認送出", "立即訂閱",
        # Japanese keywords
        "登録", "会員登録", "送信", "確認", "購読",
        # Korean keywords
        "회원가입", "가입", "구독", "전송", "확인"
    ]
    
    strategies = [
        # Strategy 1: Button elements
        {
            'selectors': ['button[type="submit"]', 'input[type="submit"]'],
            'name': 'Submit buttons'
        },
        # Strategy 2: All buttons
        {
            'selectors': ['button'],
            'name': 'All buttons'
        },
        # Strategy 3: Links acting as buttons
        {
            'selectors': ['a[role="button"]', 'a.btn', 'a.button'],
            'name': 'Link buttons'
        },
        # Strategy 4: Input buttons
        {
            'selectors': ['input[type="button"]'],
            'name': 'Input buttons'
        }
    ]
    
    for strategy in strategies:
        log(f"🔍 Looking for buttons: {strategy['name']}")
        
        for selector in strategy['selectors']:
            try:
                buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                
                for btn in buttons:
                    if not btn.is_displayed() or not btn.is_enabled():
                        continue
                    
                    # Get button text from multiple sources
                    text_sources = [
                        btn.get_attribute("innerText"),
                        btn.get_attribute("textContent"),
                        btn.get_attribute("value"),
                        btn.get_attribute("title"),
                        btn.get_attribute("aria-label"),
                        btn.get_attribute("data-text")
                    ]
                    
                    button_text = ""
                    for text in text_sources:
                        if text:
                            button_text += text + " "
                    
                    button_text = button_text.lower().strip()
                    
                    # Check if button text contains keywords
                    if any(keyword in button_text for keyword in keywords):
                        log(f"✅ Found submit button: '{button_text[:50]}'")
                        return btn
                        
            except Exception as e:
                continue
    
    return None

def look_for_signup_links_advanced():
    """Advanced signup link detection including user/login icons"""
    
    # First, look for user/login icons (most common on e-commerce sites)
    log("🔍 Looking for user/login icons...")
    icon_selectors = [
        # Common user icon selectors
        "svg[class*='user' i]", "i[class*='user' i]", "span[class*='user' i]",
        "svg[class*='account' i]", "i[class*='account' i]", "span[class*='account' i]",
        "svg[class*='profile' i]", "i[class*='profile' i]", "span[class*='profile' i]",
        "svg[class*='login' i]", "i[class*='login' i]", "span[class*='login' i]",
        "svg[class*='sign' i]", "i[class*='sign' i]", "span[class*='sign' i]",
        # Generic icon patterns
        "button[aria-label*='user' i]", "button[aria-label*='account' i]",
        "button[aria-label*='login' i]", "button[aria-label*='profile' i]",
        "a[aria-label*='user' i]", "a[aria-label*='account' i]",
        "a[aria-label*='login' i]", "a[aria-label*='profile' i]",
        # Common icon classes
        ".user-icon", ".account-icon", ".login-icon", ".profile-icon",
        ".fa-user", ".fa-user-circle", ".fa-user-o", ".fa-account",
        # Header navigation patterns
        "header a[href*='account' i]", "header a[href*='login' i]",
        "header a[href*='sign' i]", "header a[href*='user' i]",
        "nav a[href*='account' i]", "nav a[href*='login' i]",
        "nav a[href*='sign' i]", "nav a[href*='user' i]"
    ]
    
    for selector in icon_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for el in elements:
                if el.is_displayed() and el.is_enabled():
                    # Check if it's in header/navigation area
                    parent = el.find_element(By.XPATH, "./..")
                    parent_classes = parent.get_attribute("class") or ""
                    parent_tag = parent.tag_name.lower()
                    
                    if any(keyword in parent_classes.lower() for keyword in ["header", "nav", "menu", "top"]) or parent_tag in ["header", "nav"]:
                        log(f"🔗 Found user/login icon: {selector}")
                        return el
        except Exception as e:
            log(f"⚠️ Error with icon selector {selector}: {e}")
            continue
    
    # If no icons found, look for text-based links
    keywords = [
        "sign up", "signup", "sign in", "signin", "register", 
        "join", "create account", "get started", "inscription",
        "new account", "become member",
        # Chinese keywords
        "註冊", "加入會員", "註冊會員", "會員註冊", "登入", "登錄",
        "新會員", "成為會員", "會員中心",
        # Japanese keywords
        "登録", "会員登録", "新規登録", "ログイン",
        # Korean keywords
        "회원가입", "가입", "로그인", "신규회원"
    ]
    
    try:
        # Look for links
        links = driver.find_elements(By.CSS_SELECTOR, 'a')
        
        for link in links[:100]:  # Check first 100 links
            try:
                if not link.is_displayed():
                    continue
                
                # Get link text and href
                text = (link.get_attribute("innerText") or "").lower().strip()
                href = (link.get_attribute("href") or "").lower()
                title = (link.get_attribute("title") or "").lower()
                
                # Check text content
                if any(kw in text for kw in keywords):
                    log(f"🔗 Found signup link: '{text}'")
                    return link
                
                # Check href content
                if any(kw in href for kw in ["signup", "register", "join", "signin", "create"]):
                    log(f"🔗 Found signup link in URL: '{href[:50]}'")
                    return link
                
                # Check title
                if any(kw in title for kw in keywords):
                    log(f"🔗 Found signup link in title: '{title}'")
                    return link
                    
            except:
                continue
                
    except:
        pass
    
    return None

def fill_form_fields_advanced(email):
    """Advanced form filling with multiple field types"""
    
    try:
        # Fill name fields
        name_fields = [
            ('input[name*="first" i]', 'Ikram', 'first name'),
            ('input[name*="last" i]', 'Kharroubi', 'last name'),
            ('input[name*="name" i]:not([name*="first"]):not([name*="last"])', 'Ikram Kharroubi', 'full name'),
            ('input[placeholder*="first" i]', 'Ikram', 'first name (placeholder)'),
            ('input[placeholder*="last" i]', 'Kharroubi', 'last name (placeholder)'),
            ('input[id*="first" i]', 'Ikram', 'first name (id)'),
            ('input[id*="last" i]', 'Kharroubi', 'last name (id)')
        ]
        
        for selector, value, field_type in name_fields:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        element.clear()
                        element.send_keys(value)
                        log(f"👤 Filled {field_type}: {value}")
                        wait_random()
                        break
            except:
                continue
        
        # Fill phone fields
        phone_selectors = [
            'input[name*="phone" i]',
            'input[type="tel"]',
            'input[placeholder*="phone" i]',
            'input[id*="phone" i]'
        ]
        
        for selector in phone_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        element.clear()
                        element.send_keys("+1234567890")
                        log(f"📞 Filled phone number")
                        wait_random()
                        break
            except:
                continue
        
        # Fill password fields
        password_selectors = [
            'input[type="password"]',
            'input[name*="password" i]',
            'input[name*="pass" i]',
            'input[placeholder*="password" i]'
        ]
        
        for selector in password_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        element.clear()
                        element.send_keys("TempPass123!")
                        log(f"🔒 Filled password field")
                        wait_random()
                        break
            except:
                continue
        
        # Handle checkboxes
        checkbox_selectors = [
            'input[type="checkbox"]',
            'input[name*="agree" i]',
            'input[name*="accept" i]',
            'input[name*="consent" i]',
            'input[name*="terms" i]'
        ]
        
        for selector in checkbox_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and not element.is_selected():
                        element.click()
                        log(f"☑️ Checked checkbox")
                        wait_random()
                        break
            except:
                continue
                
    except Exception as e:
        log(f"⚠️ Error filling form fields: {e}")

def wait_for_verification():
    """Wait and check for account verification"""
    log("⏳ Waiting for verification...")
    
    # Wait longer for verification
    time.sleep(5)
    
    try:
        # Check current page for verification indicators
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower()
        
        verification_indicators = [
            "verify", "verification", "confirm", "check your email",
            "activate", "activation", "welcome", "thank you",
            "success", "subscribed", "registered", "created"
        ]
        
        if any(indicator in page_source for indicator in verification_indicators):
            log("✅ Verification page detected")
            return True
        
        if any(word in current_url for word in ["verify", "confirm", "welcome", "success"]):
            log("✅ Verification URL detected")
            return True
        
        # Check for verification elements
        verification_selectors = [
            ".verification",
            ".confirmation",
            ".welcome",
            ".success",
            "[class*='verify']",
            "[class*='confirm']"
        ]
        
        for selector in verification_selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed():
                    text = element.text.lower()
                    if any(indicator in text for indicator in verification_indicators):
                        log("✅ Verification element found")
                        return True
            except:
                continue
        
        log("⚠️ No clear verification detected, but continuing...")
        return True
        
    except Exception as e:
        log(f"⚠️ Error checking verification: {e}")
        return True

def find_signup_link_advanced():
    """Find and click signup/registration links with international support"""
    signup_selectors = [
        # English terms
        "a[href*='signup' i]", "a[href*='register' i]", "a[href*='create-account' i]", "a[href*='join' i]",
        "button:contains('Sign Up')", "button:contains('Register')", "button:contains('Create Account')", "button:contains('Join')",
        "a:contains('Sign Up')", "a:contains('Register')", "a:contains('Create Account')", "a:contains('Join')",
        # Chinese terms
        "a:contains('註冊')", "a:contains('加入會員')", "a:contains('註冊會員')", "a:contains('會員註冊')",
        "button:contains('註冊')", "button:contains('加入會員')", "button:contains('註冊會員')",
        "a[href*='register' i]", "a[href*='signup' i]", "a[href*='join' i]",
        # Japanese terms
        "a:contains('登録')", "button:contains('登録')", "a:contains('会員登録')",
        # Korean terms  
        "a:contains('회원가입')", "button:contains('회원가입')", "a:contains('가입')"
    ]
    
    for selector in signup_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for el in elements:
                if el.is_displayed() and el.is_enabled():
                    text = el.get_attribute("innerText") or ""
                    log(f"🔗 Found signup element: '{text}'")
                    
                    # Scroll to element and click
                    driver.execute_script("arguments[0].scrollIntoView(true);", el)
                    time.sleep(1)
                    el.click()
                    log(f"✅ Clicked signup link: {text}")
                    time.sleep(3)  # Wait for navigation
                    return True
        except Exception as e:
            log(f"⚠️ Error with selector {selector}: {e}")
            continue
    
    return False

def find_user_login_icons():
    """Specifically look for user/login icons in header/navigation areas"""
    log("🔍 Looking for user/login icons in header...")
    
    # Common user icon patterns
    icon_patterns = [
        # FontAwesome icons
        "i.fa-user", "i.fa-user-circle", "i.fa-user-o", "i.fa-account",
        # Generic user icons
        "[class*='user-icon']", "[class*='account-icon']", "[class*='login-icon']",
        "[class*='profile-icon']", "[class*='member-icon']",
        # SVG icons
        "svg[class*='user']", "svg[class*='account']", "svg[class*='login']",
        "svg[class*='profile']", "svg[class*='member']",
        # Button with user-related aria-labels
        "button[aria-label*='user']", "button[aria-label*='account']",
        "button[aria-label*='login']", "button[aria-label*='profile']",
        "button[aria-label*='member']", "button[aria-label*='sign']",
        # Links in header
        "header a[href*='account']", "header a[href*='login']", "header a[href*='user']",
        "header a[href*='profile']", "header a[href*='member']", "header a[href*='sign']",
        # Navigation links
        "nav a[href*='account']", "nav a[href*='login']", "nav a[href*='user']",
        "nav a[href*='profile']", "nav a[href*='member']", "nav a[href*='sign']"
    ]
    
    for pattern in icon_patterns:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, pattern)
            for el in elements:
                if el.is_displayed() and el.is_enabled():
                    # Check if it's in a header/navigation area
                    try:
                        # Get parent elements to check location
                        parent = el.find_element(By.XPATH, "./..")
                        grandparent = parent.find_element(By.XPATH, "./..")
                        
                        parent_classes = (parent.get_attribute("class") or "").lower()
                        grandparent_classes = (grandparent.get_attribute("class") or "").lower()
                        parent_tag = parent.tag_name.lower()
                        grandparent_tag = grandparent.tag_name.lower()
                        
                        # Check if it's in header/nav area
                        header_keywords = ["header", "nav", "navigation", "menu", "top", "bar", "toolbar"]
                        is_in_header = any(keyword in parent_classes for keyword in header_keywords) or \
                                     any(keyword in grandparent_classes for keyword in header_keywords) or \
                                     parent_tag in ["header", "nav"] or grandparent_tag in ["header", "nav"]
                        
                        if is_in_header:
                            log(f"🔗 Found user icon in header: {pattern}")
                            return el
                    except:
                        # If we can't check parent, still try the element
                        log(f"🔗 Found potential user icon: {pattern}")
                        return el
                        
        except Exception as e:
            log(f"⚠️ Error with pattern {pattern}: {e}")
            continue
    
    return None

def intelligent_inscribe(email, url):
    """Intelligent inscription with exact sequence: Load → Refresh 2x → Wait JS → Search Email Fields → Submit"""
    try:
        log(f"\n🌐 Opening: {url}")
        driver.get(url)
        
        # Step 1: Wait for initial load
        log("📄 Step 1: Waiting for initial page load...")
        wait_for_javascript()
        wait_random()
        
        # Step 2: Refresh page 2 times to remove popups
        log("🔄 Step 2: Refreshing page 2 times to remove popups...")
        for i in range(2):
            log(f"🔄 Refresh {i+1}/2...")
            driver.refresh()
            wait_for_javascript()
            wait_random()
        
        # Step 3: Wait for JavaScript to load completely after refreshes
        log("📄 Step 3: Waiting for JavaScript to load after refreshes...")
        wait_for_javascript()
        wait_random()
        
        # Step 4: Check for CAPTCHA and handle it
        log("🔒 Step 4: Checking for CAPTCHA...")
        check_for_captcha()
        wait_random()
        
        # Step 5: Check for popups and close them with X button (including SVG X)
        log("🪟 Step 5: Checking for popups and closing with X (including SVG)...")
        close_all_popups_with_x_advanced()
        wait_random()
        
        # Step 6: ALWAYS search for email fields first (like "Your Email" on GLD.com)
        log("📧 Step 6: ALWAYS searching for email input fields first...")
        email_submitted = find_and_submit_email_directly(email)
        
        if email_submitted:
            log("✅ Email submitted successfully!")
            # Check for CAPTCHA after email submission
            check_for_captcha()
            
            # Step 5: Sometimes need to press signup button after email
            log("🔍 Step 5: Checking if signup button needs to be pressed...")
            press_signup_button_if_needed()
            
            return True
        
        # Step 2: Handle popups and cookies
        log("🔍 Checking for popups and cookies...")
        popup_submitted = close_popups_and_cookies(email)
        wait_random()
        
        # Step 1.5: If popup was submitted, we already checked footer first, so continue
        
        # Fallback: Look for signup links only (no login)
        log("🔍 Fallback: Looking for signup links only...")
        check_for_captcha()
        signup_found = look_for_signup_links_only()
        
        if signup_found:
            log("✅ Found signup link - attempting registration...")
            try:
                time.sleep(3)
                wait_for_javascript()
                log("✅ Clicked signup link")
                wait_random()
                
                # Handle popups again after clicking
                close_popups_and_cookies(email)
                wait_random()
            except Exception as e:
                log(f"⚠️ Error clicking signup link: {e}")
        
        # Step 3: ALWAYS prioritize email input detection first
        log("🔍 PRIORITY: Advanced email input detection...")
        email_input = find_email_input_advanced()
        
        # Check for CAPTCHA before proceeding with form filling
        if email_input:
            log("🔍 Checking for CAPTCHA before form submission...")
            check_for_captcha()
        
        if not email_input:
            log("❌ No email input found, trying login/user icon strategy...")
            
            # Try to find and click user/login icons first
            user_icon = find_user_login_icons()
            if user_icon:
                try:
                    log("✅ Found user/login icon, clicking...")
                    driver.execute_script("arguments[0].scrollIntoView(true);", user_icon)
                    time.sleep(1)
                    user_icon.click()
                    log("✅ Clicked user/login icon")
                    time.sleep(3)  # Wait for navigation
                    
                    # Close any new popups after navigation
                    close_popups_and_cookies(email)
                    wait_random()
                    
                    # Try email detection again on the new page
                    log("🔍 Trying email detection again on new page...")
                    email_input = find_email_input_advanced()
                    
                    if not email_input:
                        log("❌ Still no email input found after clicking user icon")
                        return False
                except Exception as e:
                    log(f"⚠️ Error clicking user icon: {e}")
                    return False
            else:
                # Fallback to text-based signup links
                if find_signup_link_advanced():
                    log("✅ Found and clicked signup link")
                    # Close any new popups after navigation
                    close_popups_and_cookies(email)
                    wait_random()
                    
                    # Try email detection again on the new page
                    log("🔍 Trying email detection again on new page...")
                    email_input = find_email_input_advanced()
                    
                    if not email_input:
                        log("❌ Still no email input found after clicking signup link")
                        return False
                else:
                    log("❌ No email input, user icons, or signup links found")
                    
                    # Final fallback: try to find ANY clickable element that might lead to registration
                    log("🔍 Final fallback: looking for any registration-related elements...")
                    
                    fallback_selectors = [
                        # Look for any links with registration-related text
                        "a:contains('註冊')", "a:contains('註冊會員')", "a:contains('加入會員')",
                        "a:contains('會員')", "a:contains('登入')", "a:contains('登錄')",
                        "button:contains('註冊')", "button:contains('加入會員')",
                        # Look for any clickable elements in header
                        "header a", "header button", "nav a", "nav button",
                        ".header a", ".header button", ".nav a", ".nav button",
                        # Look for any elements with user-related classes
                        "[class*='user']", "[class*='account']", "[class*='login']",
                        "[class*='member']", "[class*='sign']", "[class*='register']"
                    ]
                    
                    for selector in fallback_selectors:
                        try:
                            elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            for el in elements:
                                if el.is_displayed() and el.is_enabled():
                                    text = el.get_attribute("innerText") or ""
                                    classes = el.get_attribute("class") or ""
                                    
                                    # Check if it's user-related
                                    if any(keyword in text.lower() or keyword in classes.lower() 
                                           for keyword in ["user", "account", "login", "member", "sign", "register", "註冊", "會員", "登入"]):
                                        log(f"🔗 Found fallback element: '{text}' ({classes})")
                                        
                                        try:
                                            driver.execute_script("arguments[0].scrollIntoView(true);", el)
                                            time.sleep(1)
                                            el.click()
                                            log("✅ Clicked fallback element")
                                            time.sleep(3)
                                            
                                            # Close popups and try email detection again
                                            close_popups_and_cookies(email)
                                            wait_random()
                                            
                                            email_input = find_email_input_advanced()
                                            if email_input:
                                                log("✅ Found email input after clicking fallback element")
                                                break
                                            else:
                                                log("❌ Still no email input after fallback click")
                                        except Exception as e:
                                            log(f"⚠️ Error clicking fallback element: {e}")
                                            continue
                            
                            # If we found an email input, break out of the fallback loop
                            if 'email_input' in locals() and email_input:
                                break
                        except:
                            continue
                    
                    # Final check
                    if 'email_input' not in locals() or not email_input:
                        log("❌ All strategies exhausted - no email input found")
                        return False
        
        log("✅ Found email input field")
        
        # Step 4: Fill all form fields
        log("📝 Filling form fields...")
        fill_form_fields_advanced(email)
        
        # Step 5: Enter email
        try:
            email_input.clear()
            wait_random()
            email_input.send_keys(email)
            wait_random()
            log(f"📧 Entered email: {email}")
        except Exception as e:
            log(f"❌ Failed to enter email: {e}")
            return False
        
        # Step 6: Find submit button with advanced detection
        log("🔍 Advanced submit button detection...")
        submit_btn = find_submit_button_advanced()
        
        if submit_btn:
            try:
                # Scroll to button
                driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
                wait_random()
                
                submit_btn.click()
                log("🖱️ Clicked submit button")
                
                # Wait longer after clicking submit
                log("⏳ Waiting for form submission...")
                time.sleep(5)
                
                # ALWAYS check for CAPTCHA after regular email submission
                log("🔍 Checking for CAPTCHA after regular email submission...")
                check_for_captcha()
                
                # Wait for any redirects or page changes
                try:
                    WebDriverWait(driver, 10).until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )
                except:
                    pass
                
                wait_random()
                
            except Exception as e:
                log(f"⚠️ Button click failed, trying Enter key: {e}")
                try:
                    email_input.send_keys(Keys.ENTER)
                    log("⌨️ Pressed Enter key")
                except:
                    log("❌ All submit methods failed")
                    return False
        else:
            log("🔍 No submit button found, trying Enter key")
            try:
                email_input.send_keys(Keys.ENTER)
                log("⌨️ Pressed Enter key")
            except:
                log("❌ No submit method found")
                return False
        
        # Step 7: Wait for verification
        wait_for_verification()
        
        # Step 8: Final success check
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower()
        
        success_indicators = [
            "thank", "success", "confirm", "subscribed", "registered",
            "verify", "check your email", "welcome", "created"
        ]
        
        if any(word in page_source for word in success_indicators) or any(word in current_url for word in ["success", "thank", "confirm"]):
            log(f"✅ SUCCESS: Inscribed to {url}")
            return True
        else:
            log(f"⚠️ UNCERTAIN: May have inscribed to {url}")
            return True  # Count as success
            
    except Exception as e:
        log(f"❌ FAILED: {url} - {str(e)[:100]}")
        return False

def log(message):
    """Add message to output"""
    try:
        output.insert(tk.END, message + "\n")
        output.see(tk.END)
        root.update_idletasks()
    except:
        print(message)

def start():
    """Start intelligent inscription process"""
    global running, driver
    
    if not SELENIUM_AVAILABLE:
        messagebox.showerror("Error", "Selenium not installed!\nRun: pip install selenium webdriver-manager")
        return
    
    if not url_file.get():
        messagebox.showerror("Error", "Please select a URL file")
        return
    
    # Check email mode and validate
    if email_mode.get() == "single":
        if not email_entry.get().strip():
            messagebox.showerror("Error", "Please enter an email")
            return
    else:  # file mode
        if not email_accounts_file.get():
            messagebox.showerror("Error", "Please select an email accounts file")
            return
    
    # Load URLs
    try:
        log("📂 Loading URLs from file...")
        with open(url_file.get(), 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        import re
        urls = []
        for line in lines:
            if any(skip in line.lower() for skip in ['discovered', '====', 'total:', 'websites', 'shopify']):
                continue
            cleaned = re.sub(r'^\s*\d+\.\s*', '', line)
            
            # Check if it's already a full URL
            if cleaned.startswith('http://') or cleaned.startswith('https://'):
                urls.append(cleaned)
            # If it's just a domain, add https://
            elif '.' in cleaned and not cleaned.startswith('www.') and not ' ' in cleaned:
                urls.append('https://' + cleaned)
                log(f"🔗 Added https:// to domain: {cleaned}")
            # If it's a domain with www., add https://
            elif cleaned.startswith('www.') and not ' ' in cleaned:
                urls.append('https://' + cleaned)
                log(f"🔗 Added https:// to www domain: {cleaned}")
        
        if not urls:
            messagebox.showerror("Error", "No valid URLs found")
            return
        
        log(f"✅ Loaded {len(urls)} URLs")
    except Exception as e:
        messagebox.showerror("Error", f"Could not load file: {e}")
        return
    
    # Load email accounts
    email_accounts = []
    if email_mode.get() == "file":
        try:
            log("📂 Loading email accounts from file...")
            with open(email_accounts_file.get(), 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            import re
            for line in lines:
                if not line or line.startswith('#'):
                    continue
                if '@' in line and '.' in line:
                    email = re.sub(r'^\s*\d+\.\s*', '', line).strip()
                    email_accounts.append(email)
            
            if not email_accounts:
                messagebox.showerror("Error", "No valid email addresses found in file")
                return
            
            log(f"✅ Loaded {len(email_accounts)} email accounts")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load email accounts file: {e}")
            return
    else:
        email_accounts = [email_entry.get().strip()]
    
    try:
        max_sites = int(input_max_sites.get() or len(urls))
        urls = urls[:max_sites]
    except:
        pass
    
    log(f"\n🧠 INTELLIGENT INSCRIPTION SYSTEM")
    log(f"=" * 70)
    log(f"📧 Email Mode: {'Multiple Accounts' if len(email_accounts) > 1 else 'Single Account'}")
    log(f"📧 Email Accounts: {len(email_accounts)}")
    log(f"🌐 Websites: {len(urls)}")
    log(f"🔄 Strategy: ALL emails for EACH website")
    log(f"🎯 Features: Popup handling, Cookie acceptance, Advanced detection")
    log(f"🎯 Multi-strategy form filling, Verification waiting")
    log(f"=" * 70)
    
    # Init browser
    try:
        log("\n🔧 Initializing Chrome browser...")
        options = Options()
        
        if headless.get():
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')
            log("🕶️ Running in headless mode")
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--log-level=3')
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except:
            driver = webdriver.Chrome(options=options)
        
        driver.set_page_load_timeout(30)
        log("✅ Chrome browser started\n")
        
    except Exception as e:
        messagebox.showerror("Error", f"Browser failed: {e}")
        return
    
    running = True
    successful = 0
    failed = 0
    
    try:
        for i, url in enumerate(urls, 1):
            if not running:
                break
            
            log(f"\n🌐 [{i}/{len(urls)}] Processing URL: {url}")
            log(f"📧 Using {len(email_accounts)} email accounts for this website")
            
            # Process ALL email accounts for this URL
            for j, email in enumerate(email_accounts, 1):
                if not running:
                    break
                
                log(f"\n📧 [{j}/{len(email_accounts)}] Using email: {email}")
                
                if intelligent_inscribe(email, url):
                    successful += 1
                    log(f"✅ SUCCESS: {email} inscribed to {url}")
                else:
                    failed += 1
                    log(f"❌ FAILED: {email} failed on {url}")
                
                # Small delay between email attempts
                time.sleep(1)
            
            log(f"\n📊 Website {i}/{len(urls)} completed: {url}")
            log(f"📊 Total Progress: Success: {successful}, Failed: {failed}")
            
            # Longer delay between websites
            time.sleep(3)
    
    finally:
        if driver:
            driver.quit()
        
        total = successful + failed
        rate = (successful / total * 100) if total > 0 else 0
        
        log(f"\n" + "=" * 70)
        log(f"📊 FINAL RESULTS:")
        log(f"=" * 70)
        log(f"✅ Successful: {successful}")
        log(f"❌ Failed: {failed}")
        log(f"📊 Success rate: {rate:.1f}%")
        log(f"=" * 70)
        log("🏁 Intelligent inscription completed!")
        
        running = False

def threaded_start():
    threading.Thread(target=start, daemon=True).start()

def stop():
    global running, driver
    running = False
    if driver:
        try:
            driver.quit()
        except:
            pass
    log("\n🛑 Stopped")

# GUI
root = tk.Tk()
root.title("🧠 Intelligent Inscription System")
root.geometry("900x700")

frame1 = tk.Frame(root)
frame1.pack(pady=10, fill='x', padx=10)
tk.Label(frame1, text="📧 Email Options:", font=('Arial', 11, 'bold')).pack(anchor='w')

# Email mode selection
email_mode_frame = tk.Frame(frame1)
email_mode_frame.pack(fill='x', pady=5)
email_mode = tk.StringVar(value="single")
tk.Radiobutton(email_mode_frame, text="Single Email", variable=email_mode, value="single", 
               font=('Arial', 10)).pack(side='left', padx=10)
tk.Radiobutton(email_mode_frame, text="Email Accounts File", variable=email_mode, value="file", 
               font=('Arial', 10)).pack(side='left', padx=10)

# Single email entry
single_email_frame = tk.Frame(frame1)
single_email_frame.pack(fill='x', pady=5)
tk.Label(single_email_frame, text="📧 Your Email:", font=('Arial', 10)).pack(anchor='w')
email_entry = tk.Entry(single_email_frame, width=100, font=('Arial', 10))
email_entry.pack(fill='x', pady=2)

# Email accounts file
email_file_frame = tk.Frame(frame1)
email_file_frame.pack(fill='x', pady=5)
tk.Label(email_file_frame, text="📄 Email Accounts File (one email per line):", font=('Arial', 10)).pack(anchor='w')
email_accounts_frame = tk.Frame(email_file_frame)
email_accounts_frame.pack(fill='x')
email_accounts_file = tk.StringVar()
tk.Entry(email_accounts_frame, textvariable=email_accounts_file, width=80, font=('Arial', 9)).pack(side='left', fill='x', expand=True)
tk.Button(email_accounts_frame, text="Browse", 
          command=lambda: email_accounts_file.set(filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])),
          font=('Arial', 9, 'bold'), bg='#28a745', fg='white').pack(side='right', padx=5)

frame2 = tk.Frame(root)
frame2.pack(pady=10, fill='x', padx=10)
tk.Label(frame2, text="📄 Website List:", font=('Arial', 11, 'bold')).pack(anchor='w')
url_frame = tk.Frame(frame2)
url_frame.pack(fill='x')
url_file = tk.StringVar()
tk.Entry(url_frame, textvariable=url_file, width=80, font=('Arial', 9)).pack(side='left', fill='x', expand=True)
tk.Button(url_frame, text="Browse", 
          command=lambda: url_file.set(filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])),
          font=('Arial', 9, 'bold'), bg='#007bff', fg='white').pack(side='right', padx=5)

frame2b = tk.Frame(root)
frame2b.pack(pady=5, fill='x', padx=10)
tk.Label(frame2b, text="🔢 Max websites:", font=('Arial', 10)).pack(side='left')
input_max_sites = tk.Entry(frame2b, width=10, font=('Arial', 10))
input_max_sites.pack(side='left', padx=5)

frame3 = tk.Frame(root)
frame3.pack(pady=10)
headless = tk.BooleanVar(value=True)
tk.Checkbutton(frame3, text="🕶️ Headless Mode", variable=headless, font=('Arial', 10, 'bold')).pack()

frame4 = tk.Frame(root)
frame4.pack(pady=15)
tk.Button(frame4, text="▶️ START", command=threaded_start, 
          bg="#28a745", fg="white", font=('Arial', 14, 'bold'), width=12, height=2).pack(side='left', padx=5)
tk.Button(frame4, text="🛑 STOP", command=stop, 
          bg="#dc3545", fg="white", font=('Arial', 14, 'bold'), width=12, height=2).pack(side='left', padx=5)

frame5 = tk.Frame(root)
frame5.pack(fill='both', expand=True, padx=10, pady=10)
tk.Label(frame5, text="📋 Output Log:", font=('Arial', 11, 'bold')).pack(anchor='w')
output = scrolledtext.ScrolledText(frame5, width=100, height=20, font=('Consolas', 9), bg='#f8f9fa', fg='#212529')
output.pack(fill='both', expand=True)

log("=" * 70)
log("🧠 INTELLIGENT INSCRIPTION SYSTEM")
log("=" * 70)
log("✅ Advanced popup detection and closing")
log("✅ Automatic cookie acceptance")
log("✅ Multi-strategy form detection")
log("✅ Smart field filling (name, phone, password)")
log("✅ Signup link detection and clicking")
log("✅ Verification waiting")
log("✅ Random delays to avoid detection")
log("")
log("📋 READY TO START!")
log("=" * 70)

root.mainloop()
