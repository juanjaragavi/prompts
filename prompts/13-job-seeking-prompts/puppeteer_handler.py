"""
Production-grade pyppeteer form handler with robust state and retry behavior.
"""

import asyncio
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse


class FormState(Enum):
    """Tracks form processing state."""

    UNINITIALIZED = "uninitialized"
    LOADED = "loaded"
    FIELDS_DETECTED = "fields_detected"
    FILLING = "filling"
    FILLED = "filled"
    SUBMITTING = "submitting"
    SUBMITTED = "submitted"
    FAILED = "failed"


class PuppeteerFormHandler:
    """Advanced form handler built on pyppeteer."""

    def __init__(self, logger: logging.Logger, config: Any):
        self.logger = logger
        self.config = config
        self.state = FormState.UNINITIALIZED
        self.attempts = 0
        self.max_attempts = 3
        self.timeout_ms = 30000
        self.form_data: Dict[str, Any] = {}
        self.browser = None
        self.page = None
        self._launch = None

    async def init_browser(self) -> bool:
        """Initialize browser lazily and safely."""
        if self.browser:
            return True

        try:
            from pyppeteer import launch
        except ImportError:
            self.logger.error("pyppeteer not installed. Install: pip install pyppeteer")
            return False

        self._launch = launch

        browser_cfg = {}
        try:
            browser_cfg = self.config.get_browser_config() or {}
        except Exception:
            browser_cfg = {}

        headless = bool(browser_cfg.get("headless", True))
        self.timeout_ms = int(browser_cfg.get("default_timeout_ms", self.timeout_ms))

        try:
            extra_args = ["--disable-gpu", "--disable-blink-features=AutomationControlled"]
            browser_cfg = browser_cfg or {}
            if browser_cfg.get("allow_no_sandbox", True):
                extra_args.extend(["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"])

            self.browser = await self._launch(
                headless=headless,
                args=extra_args,
            )
            self.logger.info("Puppeteer browser initialized")
            return True
        except Exception as exc:
            self.logger.error(f"Failed to initialize pyppeteer: {exc}")
            if self.browser:
                try:
                    await self.browser.close()
                except Exception as close_err:
                    self.logger.warning(f"Error closing failed browser instance: {close_err}")
                self.browser = None
            return False

    def _validate_url(self, url: str) -> bool:
        """Allow only absolute HTTP(S) URLs."""
        try:
            parsed = urlparse(url)
            return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
        except Exception:
            return False

    async def load_page(self, url: str, retry_count: int = 0) -> bool:
        """Load target URL with timeout and exponential backoff."""
        self.attempts = retry_count + 1

        if not self._validate_url(url):
            self.logger.error(f"Refusing to load non-http(s) URL: {url}")
            self.state = FormState.FAILED
            return False

        try:
            if not await self.init_browser():
                self.state = FormState.FAILED
                return False

            if self.page:
                try:
                    await self.page.close()
                except Exception as close_err:
                    self.logger.warning(f"Error closing previous page: {close_err}")

            self.page = await self.browser.newPage()
            await self.page.setViewport({"width": 1365, "height": 900})
            await self.page.setDefaultNavigationTimeout(self.timeout_ms)
            await self.page.setDefaultTimeout(self.timeout_ms)

            await self.page.goto(url, waitUntil="networkidle2", timeout=self.timeout_ms)
            self.state = FormState.LOADED
            return True
        except Exception as exc:
            self.logger.warning(
                f"Load page failed (attempt {retry_count + 1}/{self.max_attempts}): {exc}"
            )
            if retry_count < self.max_attempts - 1:
                await asyncio.sleep(2 ** retry_count)
                return await self.load_page(url, retry_count + 1)

            self.state = FormState.FAILED
            return False

    async def detect_form_fields_advanced(self) -> Dict[str, Any]:
        """Analyze forms and collect concrete selectors for each field."""
        if not self.page:
            return {}

        try:
            form_analysis = await self.page.evaluate(
                r"""
                () => {
                  const forms = Array.from(document.querySelectorAll('form'));
                  const output = {};

                  const cssEscape = (v) => {
                    if (!v) return '';
                    if (window.CSS && typeof window.CSS.escape === 'function') {
                      return window.CSS.escape(v);
                    }
                    return String(v).replace(/([ #;?%&,.+*~\\':\"!^$[\]()=>|/@])/g, '\\\\$1');
                  };

                  const computeSelector = (el, fallbackIndex) => {
                    const id = el.getAttribute('id');
                    if (id) return `#${cssEscape(id)}`;

                    const name = el.getAttribute('name');
                    const tag = el.tagName.toLowerCase();
                    if (name) return `${tag}[name="${cssEscape(name)}"]`;

                    return `${tag}:nth-of-type(${fallbackIndex + 1})`;
                  };

                  forms.forEach((form, formIdx) => {
                    const formKey = form.getAttribute('id') || `form_${formIdx}`;
                    const controls = Array.from(form.querySelectorAll('input, textarea, select'));
                    const fieldMap = {};

                    controls.forEach((control, idx) => {
                      const tag = control.tagName.toLowerCase();
                      const type = (control.getAttribute('type') || tag).toLowerCase();
                      const selector = computeSelector(control, idx);

                      let label = '';
                      const controlId = control.getAttribute('id');
                      if (controlId) {
                        const forLabel = form.querySelector(`label[for="${cssEscape(controlId)}"]`);
                        if (forLabel) label = (forLabel.textContent || '').trim();
                      }
                      if (!label) {
                        const parentLabel = control.closest('label');
                        if (parentLabel) label = (parentLabel.textContent || '').trim();
                      }

                      const options = [];
                      if (tag === 'select') {
                        Array.from(control.options || []).forEach((opt) => {
                          options.push({ text: (opt.textContent || '').trim(), value: opt.value || '' });
                        });
                      }

                      fieldMap[`field_${idx}`] = {
                        type,
                        tag,
                        name: control.getAttribute('name') || '',
                        id: controlId || '',
                        selector,
                        label,
                        required: !!control.required,
                        disabled: !!control.disabled,
                        visible: control.offsetParent !== null,
                        placeholder: control.getAttribute('placeholder') || '',
                        options,
                      };
                    });

                    const submitCandidates = Array.from(
                      form.querySelectorAll('button[type="submit"], input[type="submit"], button:not([type])')
                    ).map((btn, idx) => ({
                      text: ((btn.textContent || btn.value || '') + '').trim(),
                      selector: computeSelector(btn, idx),
                    }));

                    output[formKey] = {
                      fieldCount: Object.keys(fieldMap).length,
                      fields: fieldMap,
                      submitButtons: submitCandidates,
                    };
                  });

                  return output;
                }
                """
            )

            self.form_data = form_analysis or {}
            self.state = FormState.FIELDS_DETECTED
            return self.form_data
        except Exception as exc:
            self.logger.error(f"Error detecting form fields: {exc}")
            self.state = FormState.FAILED
            return {}

    def _candidate_field_mapping(self, candidate_data: Dict[str, Any]) -> Dict[str, str]:
        return {
            "name": str(candidate_data.get("full_name") or "").strip(),
            "first": str(candidate_data.get("first_name") or "").strip(),
            "last": str(candidate_data.get("last_name") or "").strip(),
            "email": str(candidate_data.get("email") or "").strip(),
            "phone": str(candidate_data.get("phone_with_cc") or candidate_data.get("phone") or "").strip(),
            "location": str(candidate_data.get("location") or candidate_data.get("city") or "").strip(),
            "address": str(candidate_data.get("address") or "").strip(),
            "city": str(candidate_data.get("city") or "").strip(),
            "country": str(candidate_data.get("country") or "").strip(),
            "linkedin": str(candidate_data.get("linkedin") or "").strip(),
            "github": str(candidate_data.get("github") or "").strip(),
            "portfolio": str(candidate_data.get("portfolio") or "").strip(),
            "company": str(candidate_data.get("current_company") or candidate_data.get("company") or "").strip(),
            "years": str(candidate_data.get("years_experience") or "").strip(),
        }

    async def fill_form_intelligent(self, candidate_data: Dict[str, Any]) -> bool:
        """Fill detected form fields using label/name semantic matching."""
        if not self.page or not self.form_data:
            return False

        self.state = FormState.FILLING
        value_map = self._candidate_field_mapping(candidate_data)
        filled_count = 0

        try:
            for form_info in self.form_data.values():
                fields = form_info.get("fields", {})

                for field_info in fields.values():
                    if field_info.get("disabled") or not field_info.get("visible"):
                        continue

                    field_type = (field_info.get("type") or "").lower()
                    selector = field_info.get("selector")
                    if not selector or field_type in {"hidden", "submit", "button", "file"}:
                        continue

                    haystack = " ".join(
                        [
                            str(field_info.get("label") or "").lower(),
                            str(field_info.get("name") or "").lower(),
                            str(field_info.get("id") or "").lower(),
                            str(field_info.get("placeholder") or "").lower(),
                        ]
                    )

                    chosen = ""
                    for token, value in value_map.items():
                        if value and token in haystack:
                            chosen = value
                            break

                    if not chosen:
                        continue

                    if field_type == "select-one" or field_info.get("tag") == "select":
                        if await self._select_option(selector, chosen, field_info.get("options", [])):
                            filled_count += 1
                    elif field_type in {"checkbox", "radio"}:
                        if await self._click_if_exists(selector):
                            filled_count += 1
                    else:
                        if await self._fill_text_field(selector, chosen):
                            filled_count += 1

            self.state = FormState.FILLED if filled_count > 0 else FormState.FAILED
            self.logger.info(f"Filled {filled_count} field(s)")
            return filled_count > 0
        except Exception as exc:
            self.logger.error(f"Error filling form: {exc}")
            self.state = FormState.FAILED
            return False

    async def _fill_text_field(self, selector: str, value: str) -> bool:
        element = await self.page.querySelector(selector)
        if not element:
            return False

        await element.focus()
        await self.page.evaluate("(el) => { el.value = ''; }", element)
        await self.page.type(selector, value, {"delay": 10})
        await asyncio.sleep(0.05)
        return True

    async def _select_option(self, selector: str, value: str, options: list) -> bool:
        select_value = value
        lowered = value.lower()

        if options:
            best = None
            for opt in options:
                txt = str(opt.get("text", "")).lower()
                val = str(opt.get("value", ""))
                if lowered in txt or lowered == val.lower():
                    best = val
                    break
            if best:
                select_value = best

        try:
            changed = await self.page.select(selector, select_value)
            return len(changed) > 0
        except Exception:
            return False

    async def _click_if_exists(self, selector: str) -> bool:
        element = await self.page.querySelector(selector)
        if not element:
            return False
        await element.click()
        await asyncio.sleep(0.05)
        return True

    async def submit_form(self) -> Tuple[bool, str]:
        """Locate submit button and verify likely success."""
        if not self.page:
            return False, "Page is not initialized"

        self.state = FormState.SUBMITTING

        selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:not([type])',
            '[role="button"]',
        ]

        submit_button = None
        try:
            for selector in selectors:
                elements = await self.page.querySelectorAll(selector)
                for element in elements:
                    label = await self.page.evaluate(
                        "(el) => ((el.textContent || el.value || '') + '').trim().toLowerCase()",
                        element,
                    )
                    if any(k in label for k in ["submit", "apply", "send", "confirm", "continue"]):
                        submit_button = element
                        break
                if submit_button:
                    break

            if not submit_button:
                return False, "Submit button not found"

            await self.page.evaluate("(el) => el.scrollIntoView({block: 'center'})", submit_button)
            await asyncio.sleep(0.2)
            await submit_button.click()

            try:
                await self.page.waitForNavigation({"waitUntil": "networkidle2", "timeout": 12000})
                self.state = FormState.SUBMITTED
                return True, "Form submitted and navigation detected"
            except Exception:
                await asyncio.sleep(2)
                content = (await self.page.content()).lower()
                if any(s in content for s in ["thank you", "application received", "success", "submitted"]):
                    self.state = FormState.SUBMITTED
                    return True, "Form submitted and confirmation text detected"

                self.state = FormState.SUBMITTED
                return True, "Form submitted (no explicit confirmation detected)"
        except Exception as exc:
            self.state = FormState.FAILED
            self.logger.error(f"Error submitting form: {exc}")
            return False, str(exc)

    async def cleanup(self) -> None:
        """Close page/browser resources."""
        try:
            if self.page:
                await self.page.close()
        except Exception as close_page_err:
            self.logger.warning(f"Error closing page: {close_page_err}")
        finally:
            self.page = None

        try:
            if self.browser:
                await self.browser.close()
        except Exception as close_browser_err:
            self.logger.warning(f"Error closing browser: {close_browser_err}")
        finally:
            self.browser = None

    async def get_state(self) -> Dict[str, Any]:
        """Return current runtime state useful for diagnostics."""
        return {
            "state": self.state.value,
            "attempts": self.attempts,
            "form_data_count": len(self.form_data),
            "timestamp": datetime.now().isoformat(),
        }