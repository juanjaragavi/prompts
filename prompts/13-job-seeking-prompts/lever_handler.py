from __future__ import annotations

from typing import Any, Dict, List, Tuple

from playwright.async_api import Page

from job_application_bot import JobApplicationBot
from ollama_field_assistant import OllamaFieldAssistant


class LeverFormHandler(JobApplicationBot):
    """Lever application handler with deterministic and LLM-assisted completion."""

    def __init__(self, headless: bool = True):
        super().__init__(headless=headless)
        self.ollama_assistant = OllamaFieldAssistant(self.config.get_ollama_config(), self.logger)

    async def detect_lever_form_fields(self, page: Page) -> Dict[str, Dict[str, Any]]:
        """Collect rich metadata for all visible Lever form controls."""
        try:
            self.logger.info("Detecting Lever form fields dynamically...")
            form_data = await page.evaluate(
                r"""
                () => {
                  const cssEscape = (value) => {
                    if (!value) return '';
                    if (window.CSS && typeof window.CSS.escape === 'function') {
                      return window.CSS.escape(value);
                    }
                    return String(value).replace(/([ #;?%&,.+*~\':"!^$[\]()=>|/@])/g, '\\$1');
                  };

                  const detectLabel = (control) => {
                    const id = control.getAttribute('id');
                    if (id) {
                      const byFor = document.querySelector(`label[for="${cssEscape(id)}"]`);
                      if (byFor) return byFor.textContent.trim();
                    }
                    const parentLabel = control.closest('label');
                    if (parentLabel) return parentLabel.textContent.trim();
                    const labelledBy = control.getAttribute('aria-labelledby');
                    if (labelledBy) {
                      const parts = labelledBy.split(/\s+/).map((labelId) => document.getElementById(labelId)).filter(Boolean);
                      if (parts.length) return parts.map((node) => node.textContent.trim()).join(' ');
                    }
                    const group = control.closest('[data-qa], .application-question, .application-field, .postings-input-wrapper, fieldset, .application-page');
                    if (group) {
                      const labelNode = group.querySelector('label, legend, h4, h3, .application-label, .postings-label');
                      if (labelNode) return labelNode.textContent.trim();
                    }
                    return control.getAttribute('aria-label') || control.getAttribute('placeholder') || control.getAttribute('name') || id || '';
                  };

                  const detectSelector = (control, idx) => {
                    const id = control.getAttribute('id');
                    if (id) return `#${cssEscape(id)}`;
                    const name = control.getAttribute('name');
                    const tag = control.tagName.toLowerCase();
                    const type = (control.getAttribute('type') || '').toLowerCase();
                    const value = control.getAttribute('value');
                    if (name) {
                      let selector = `${tag}[name="${cssEscape(name)}"]`;
                      if (type === 'radio' || type === 'checkbox') {
                        if (value) selector += `[value="${cssEscape(value)}"]`;
                      }
                      return selector;
                    }
                    return `${tag}:nth-of-type(${idx + 1})`;
                  };

                                    const controls = Array.from(document.querySelectorAll('input, textarea, select, [role="combobox"], button[aria-haspopup="listbox"]'));
                  const fields = {};

                  controls.forEach((control, idx) => {
                    const tag = control.tagName.toLowerCase();
                                        const role = (control.getAttribute('role') || '').toLowerCase();
                                        const type = role === 'combobox'
                                            ? 'combobox'
                                            : ((control.getAttribute('type') || tag).toLowerCase());
                    const selector = detectSelector(control, idx);
                    const questionContainer = control.closest('[data-qa], .application-question, .application-field, .postings-input-wrapper, fieldset, .application-page');
                                        const optionNodes = tag === 'select'
                      ? Array.from(control.options || []).map((option) => ({ text: option.textContent.trim(), value: option.value || '' }))
                      : [];

                    const errorNodes = questionContainer
                      ? Array.from(questionContainer.querySelectorAll('.error, [aria-invalid="true"], .application-error, [data-error]'))
                      : [];

                                        const optionLikeTexts = new Set(['yes', 'no', 'us', 'senior', 'lead', 'junior', 'middle', 'trainee', 'architect']);
                                        const questionHeading = questionContainer
                                            ? Array.from(questionContainer.querySelectorAll('legend, h4, h3, h2, p, .application-label, .postings-label, strong, span, div'))
                                                    .map((node) => (node.textContent || '').replace(/\s+/g, ' ').trim())
                                                    .filter((text) => text && text.length > 5)
                                                    .filter((text) => !optionLikeTexts.has(text.toLowerCase()))
                                                    .sort((a, b) => b.length - a.length)[0] || ''
                                            : '';

                                        const widgetText = questionContainer
                                            ? (questionContainer.textContent || '').replace(/\s+/g, ' ').trim()
                                            : '';
                                        const currentValue = (() => {
                                            if (type === 'file') {
                                                return widgetText;
                                            }
                                            if (type === 'combobox') {
                                                return (control.textContent || control.getAttribute('aria-label') || '').trim();
                                            }
                                            if (tag === 'select') {
                                                return (control.selectedOptions[0]?.textContent || control.value || '').trim();
                                            }
                                            return (control.value || '').trim();
                                        })();
                                        const explicitRequired = control.required || control.getAttribute('aria-required') === 'true';
                                        const impliedRequired = /\*/.test(detectLabel(control)) || /\*/.test(questionHeading || '');

                                        fields[`field_${idx}`] = {
                      field_key: `field_${idx}`,
                      selector,
                      tag,
                      role,
                      type,
                      label: detectLabel(control),
                                            group_label: questionHeading || '',
                      name: control.getAttribute('name') || '',
                      id: control.getAttribute('id') || '',
                      placeholder: control.getAttribute('placeholder') || '',
                                            required: explicitRequired || impliedRequired,
                      disabled: !!control.disabled,
                      visible: control.offsetParent !== null,
                      checked: !!control.checked,
                                            current_value: currentValue,
                      option_value: control.getAttribute('value') || '',
                      options: optionNodes,
                      error_text: errorNodes.map((node) => (node.textContent || '').trim()).filter(Boolean).join(' | '),
                                            widget_text: widgetText,
                    };
                  });

                  return fields;
                }
                """
            )
            return form_data or {}
        except Exception as exc:
            self.logger.error(f"Error detecting form fields: {exc}")
            return {}

    def assess_form_completion(self, form_fields: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Classify fields into completed and unresolved required groups."""
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for field in form_fields.values():
            group_name = field.get("name") or field.get("id") or field.get("group_label") or field.get("label") or field.get("field_key")
            group_key = f"{field.get('type')}::{group_name}"
            grouped[group_key] = [*grouped.get(group_key, []), dict(field)]

        filled: List[Dict[str, Any]] = []
        required_unanswered: List[Dict[str, Any]] = []
        optional_unanswered: List[Dict[str, Any]] = []

        for fields in grouped.values():
            representative = dict(fields[0])
            field_type = representative.get("type", "")
            is_required = any(bool(item.get("required")) for item in fields)
            is_visible = any(bool(item.get("visible")) for item in fields)
            if not is_visible:
                continue

            if field_type == "radio":
                is_answered = any(bool(item.get("checked")) for item in fields)
                representative["options"] = [item.get("label") or item.get("option_value") for item in fields]
            elif field_type == "checkbox" and len(fields) > 1:
                is_answered = any(bool(item.get("checked")) for item in fields)
                representative["options"] = [item.get("label") or item.get("option_value") for item in fields]
            else:
                is_answered = any(self._has_meaningful_value(item) for item in fields) or any(bool(item.get("checked")) for item in fields)

            if is_answered:
                filled.append(representative)
            elif is_required:
                required_unanswered.append(representative)
            else:
                optional_unanswered.append(representative)

        return {
            "filled_count": len(filled),
            "required_unanswered": required_unanswered,
            "optional_unanswered": optional_unanswered,
            "filled": filled,
        }

    def _has_meaningful_value(self, field: Dict[str, Any]) -> bool:
        value = str(field.get("current_value", "")).strip()
        if not value:
            return False

        normalized = value.lower()
        placeholder_tokens = {
            "select",
            "select...",
            "choose",
            "choose...",
            "loading",
            "loading...",
            "type your response",
            "type response",
        }
        if normalized in placeholder_tokens:
            return False
        if field.get("type") == "combobox" and normalized.startswith("select"):
            return False
        if field.get("type") == "file":
            file_success_tokens = ["success", ".pdf", ".doc", ".docx", "uploaded", "attach"]
            return any(token in normalized for token in file_success_tokens) and "success" in normalized
        return True

    def _candidate_field_mapping(self) -> Dict[str, str]:
        candidate = self.candidate
        return {
            "full name": str(candidate.get("full_name") or "").strip(),
            "name": str(candidate.get("full_name") or "").strip(),
            "email": str(candidate.get("email") or "").strip(),
            "phone": str(candidate.get("phone_with_cc") or candidate.get("phone") or "").strip(),
            "current location": str(candidate.get("location") or "").strip(),
            "location": str(candidate.get("location") or "").strip(),
            "current company": str(candidate.get("current_company") or "").strip(),
            "linkedin": str(candidate.get("linkedin") or "").strip(),
            "github": str(candidate.get("github") or "").strip(),
            "website": str(candidate.get("portfolio") or "").strip(),
            "portfolio": str(candidate.get("portfolio") or "").strip(),
        }

    def _deterministic_answer(self, field: Dict[str, Any], job_title: str) -> str:
        candidate = self.candidate
        options = [str(option.get("text", option)).strip() if isinstance(option, dict) else str(option).strip() for option in field.get("options", [])]
        haystack = " ".join(
            [
                str(field.get("label") or "").lower(),
                str(field.get("group_label") or "").lower(),
                str(field.get("name") or "").lower(),
                str(field.get("placeholder") or "").lower(),
            ]
        )

        for token, value in self._candidate_field_mapping().items():
            if token in haystack:
                return value

        option_answer = self._deterministic_answer_from_options(options, job_title)
        if option_answer:
            return option_answer

        if "which location are you applying for" in haystack or "apply for" in haystack and "location" in haystack:
            return "Colombia"
        if "current location" in haystack or "location" in haystack:
            return str(candidate.get("location") or "Bogotá, Colombia")
        if "salary b2b gross" in haystack or "gross monthly usd" in haystack or "minimum amount" in haystack:
            return str(candidate.get("target_monthly_usd") or "4500")
        if "salary" in haystack and "usd" in haystack:
            return str(candidate.get("target_range_monthly") or "$3,500 - $4,500 USD / month")
        if "aws/gcp certification" in haystack:
            return "No formal AWS or GCP certification yet. My strongest production cloud experience is on Google Cloud, including Vertex AI, Cloud Run, BigQuery, Compute Engine, and Cloud Armor."
        if "experience working with aws" in haystack or "aws services" in haystack:
            return "My deepest production cloud experience is on Google Cloud rather than AWS. I have built and operated AI systems with Vertex AI, Cloud Run, BigQuery, Compute Engine, and Cloud Armor, and I can transfer that architecture experience quickly to AWS environments."
        if "aws bedrock" in haystack:
            return "No"
        if "production experience with gen ai" in haystack or "experience in genai" in haystack:
            return "Yes"
        if "rag" in haystack or "retrieval-augmented generation" in haystack:
            return "Yes. I have worked on retrieval-augmented AI workflows and context-grounded LLM systems as part of enterprise AI product development, combining retrieval, prompt orchestration, and evaluation guardrails to improve answer quality and reduce hallucination risk."
        if "mlops pipelines" in haystack or "training, validation, deployment" in haystack:
            return "Yes. I have worked across production ML and AI delivery workflows including model integration, evaluation, deployment orchestration, monitoring, and iterative improvement in real business environments."
        if "full-stack applications or dashboards that integrate ai" in haystack or "integrate ai functionality" in haystack:
            return "Yes. At TopNetworks I designed and shipped AI-enabled full-stack products and internal SaaS tools, including interfaces, backend services, orchestration layers, and production integrations for LLM-powered workflows."
        if "experience in ai/ml areas" in haystack or "experience in ml areas" in haystack:
            return str(candidate.get("summary_medium") or "")
        if "ai adoption" in haystack or "frustrating thing you were happy doing manually" in haystack:
            return "Before adopting modern AI-assisted workflows, one frustrating manual task was repeatedly drafting and restructuring complex technical and product content from scratch. AI-assisted development and prompt-driven workflows dramatically reduced that friction by speeding up ideation, implementation, and iteration while still keeping human technical judgment in control."
        if "region" in haystack and "provide your region" in haystack:
            return "Colombia"
        if "pre-sales" in haystack:
            return "Yes"
        if "provide your region" in haystack or "region" == haystack.strip():
            return "Colombia"
        if "b2b contract" in haystack or "gross monthly usd" in haystack or "salary" in haystack:
            return str(candidate.get("target_range_monthly") or "$3,500 - $4,500 USD / month")
        if "seniority level" in haystack:
            title = job_title.lower()
            if "architect" in title:
                return "Architect"
            if "lead" in title:
                return "Lead"
            return "Senior"
        if "conversational english level" in haystack or "english level" in haystack:
            return "C2 Proficient"
        if "city of residence" in haystack or "city" in haystack and "residence" in haystack:
            return str(candidate.get("city") or "Bogotá")
        if "current notice period" in haystack or "notice period" in haystack:
            return str(candidate.get("notice_period") or "Immediate")
        if "pre-sales" in haystack:
            return "Yes"
        if "country" in haystack:
            return str(candidate.get("country") or "Colombia")
        if "visa" in haystack or "sponsorship" in haystack:
            return "Yes" if candidate.get("requires_visa_sponsorship") else "No"
        if "years" in haystack and "experience" in haystack:
            return str(candidate.get("years_experience") or "17")
        return ""

    def _deterministic_answer_from_options(self, options: List[str], job_title: str) -> str:
        normalized_options = [option.strip() for option in options if option and option.strip()]
        lowered = {option.lower(): option for option in normalized_options}

        seniority_scale = ["trainee", "junior", "middle", "senior", "lead", "architect"]
        if all(item in lowered for item in seniority_scale[:4]):
            title = job_title.lower()
            if "architect" in title and "architect" in lowered:
                return lowered["architect"]
            if "lead" in title and "lead" in lowered:
                return lowered["lead"]
            if "senior" in lowered:
                return lowered["senior"]

        preferred_seniority = ["architect", "lead", "senior", "staff principal", "head", "director and higher"]
        if any(option in lowered for option in preferred_seniority):
            title = job_title.lower()
            if "architect" in title and "architect" in lowered:
                return lowered["architect"]
            if "lead" in title and "lead" in lowered:
                return lowered["lead"]
            if "senior" in lowered:
                return lowered["senior"]
            for fallback in ["lead", "architect", "senior", "staff principal", "head"]:
                if fallback in lowered:
                    return lowered[fallback]

        if set(lowered).issubset({"yes", "no"}) and len(lowered) == 2:
            return ""

        for candidate_value in ["c2 proficient", "full professional proficiency", "advanced", "fluent", "professional", "expert"]:
            if candidate_value in lowered:
                return lowered[candidate_value]

        for candidate_value in ["colombia", "remote", "latam", "latin america", "bogotá, colombia", "bogota, colombia"]:
            if candidate_value in lowered:
                return lowered[candidate_value]

        for candidate_value in ["bogotá", "bogota"]:
            if candidate_value in lowered:
                return lowered[candidate_value]

        if "yes" in lowered and "pre-sales" in job_title.lower():
            return lowered["yes"]

        return ""

    async def _upload_resume_if_needed(self, page: Page, field: Dict[str, Any]) -> bool:
        field_type = str(field.get("type") or "").lower()
        if field_type != "file":
            return False

        haystack = " ".join(
            [
                str(field.get("label") or "").lower(),
                str(field.get("group_label") or "").lower(),
                str(field.get("name") or "").lower(),
            ]
        )
        if "resume" not in haystack and "cv" not in haystack:
            return False

        selector = str(field.get("selector") or "").strip()
        if not selector:
            return False

        lever_cfg = self.config.get_platform_config("lever") or {}
        resume_variant = lever_cfg.get("resume_variant", "master")
        resume_path = self.config.get_resume_path(resume_variant)
        return await self.upload_file(page, selector, resume_path, "resume")

    async def _fill_location_autocomplete(self, page: Page, selector: str, answer: str) -> bool:
        try:
            element = await page.query_selector(selector)
            if not element:
                return False

            await element.click()
            await page.wait_for_timeout(250)
            try:
                await page.keyboard.press("Meta+A")
            except Exception:
                pass
            await page.keyboard.press("Backspace")
            await page.type(selector, answer, delay=25)
            await page.wait_for_timeout(1000)

            suggestion_selectors = [
                '[role="option"]',
                '[role="listbox"] [role="option"]',
                'li[role="option"]',
                '.select__option',
                '.autocomplete__option',
            ]
            for suggestion_selector in suggestion_selectors:
                options = await page.query_selector_all(suggestion_selector)
                for option in options:
                    try:
                        text = (await option.inner_text()).strip().lower()
                    except Exception:
                        continue
                    if "colombia" in text or "bogot" in text or answer.lower() in text:
                        await option.click()
                        await page.wait_for_timeout(self.browser_config["action_wait_ms"])
                        return True

            await page.keyboard.press("ArrowDown")
            await page.wait_for_timeout(250)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(self.browser_config["action_wait_ms"])
            return True
        except Exception as exc:
            self.logger.warning(f"Location autocomplete failed for {selector}: {exc}")
            return False

    async def _select_combobox_option(self, page: Page, selector: str, answer: str) -> bool:
        try:
            element = await page.query_selector(selector)
            if not element:
                return False

            await element.click()
            await page.wait_for_timeout(500)

            option_selectors = [
                '[role="option"]',
                'li[role="option"]',
                '[role="listbox"] li',
                '[role="listbox"] [id]',
            ]
            normalized_answer = answer.strip().lower()
            for option_selector in option_selectors:
                options = await page.query_selector_all(option_selector)
                for option in options:
                    try:
                        text = (await option.inner_text()).strip()
                    except Exception:
                        continue
                    lowered = text.lower()
                    if normalized_answer == lowered or normalized_answer in lowered:
                        await option.click()
                        await page.wait_for_timeout(self.browser_config["action_wait_ms"])
                        return True

            await page.keyboard.type(answer, delay=20)
            await page.wait_for_timeout(500)
            await page.keyboard.press("ArrowDown")
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(self.browser_config["action_wait_ms"])
            return True
        except Exception as exc:
            self.logger.warning(f"Combobox selection failed for {selector}: {exc}")
            return False

    async def _apply_answer(self, page: Page, field: Dict[str, Any], answer: str) -> bool:
        selector = str(field.get("selector") or "").strip()
        if not selector or not answer:
            return False

        field_type = str(field.get("type") or "").lower()
        tag = str(field.get("tag") or "").lower()
        haystack = " ".join(
            [
                str(field.get("label") or "").lower(),
                str(field.get("group_label") or "").lower(),
                str(field.get("name") or "").lower(),
                str(field.get("placeholder") or "").lower(),
            ]
        )
        try:
            if field_type == "radio":
                candidates = await page.query_selector_all(f"input[name=\"{field.get('name', '')}\"]")
                normalized = answer.lower()
                for candidate in candidates:
                    text = await page.evaluate(
                        """
                        (el) => {
                          const label = el.closest('label');
                          if (label) return label.textContent || '';
                          const forLabel = el.id ? document.querySelector(`label[for="${el.id}"]`) : null;
                          return (forLabel && forLabel.textContent) || el.value || '';
                        }
                        """,
                        candidate,
                    )
                    candidate_text = str(text).strip().lower()
                    if normalized == candidate_text:
                        await candidate.click()
                        await page.wait_for_timeout(self.browser_config["action_wait_ms"])
                        return True
                return False

            if field_type == "checkbox":
                candidates = await page.query_selector_all(f"input[name=\"{field.get('name', '')}\"]")
                normalized = answer.lower()
                for candidate in candidates:
                    text = await page.evaluate(
                        """
                        (el) => {
                          const label = el.closest('label');
                          if (label) return label.textContent || '';
                          const forLabel = el.id ? document.querySelector(`label[for="${el.id}"]`) : null;
                          return (forLabel && forLabel.textContent) || el.value || '';
                        }
                        """,
                        candidate,
                    )
                    candidate_text = str(text).strip().lower()
                    if normalized == candidate_text:
                        await candidate.check()
                        await page.wait_for_timeout(self.browser_config["action_wait_ms"])
                        return True
                element = await page.query_selector(selector)
                if element and normalized_truthy(answer):
                    await element.check()
                    return True
                return False

            if tag == "select" or field_type == "select-one":
                options = [item.get("text", "") for item in field.get("options", [])]
                selected = choose_matching_option(options, answer)
                if not selected:
                    return False
                return await self.select_option(page, selector, selected, "lever_select")

            if field_type == "combobox":
                return await self._select_combobox_option(page, selector, answer)

            if "location" in haystack:
                return await self._fill_location_autocomplete(page, selector, answer)

            return await self.fill_field(page, selector, answer, "lever_field")
        except Exception as exc:
            self.logger.warning(
                f"Failed to apply answer for field {field.get('field_key')} "
                f"(type={field.get('type')}, answer={answer[:60]!r}): {exc}"
            )
            return False

    async def fill_lever_form(
        self,
        page: Page,
        form_fields: Dict[str, Dict[str, Any]],
        job_title: str = "",
    ) -> Dict[str, Any]:
        """Fill Lever form with deterministic answers first, then Ollama suggestions."""
        self.logger.info("Filling Lever form with candidate data...")
        deterministic_fills = 0
        latest_fields = {key: dict(value) for key, value in form_fields.items()}

        for field in latest_fields.values():
            if field.get("disabled") or not field.get("visible"):
                continue
            if await self._upload_resume_if_needed(page, field):
                deterministic_fills += 1
                continue
            answer = self._deterministic_answer(field, job_title)
            if answer and await self._apply_answer(page, field, answer):
                deterministic_fills += 1

        await page.wait_for_timeout(750)
        latest_fields = await self.detect_lever_form_fields(page)
        completion = self.assess_form_completion(latest_fields)

        ollama_answers: Dict[str, str] = {}
        if completion["required_unanswered"]:
            prompt_fields = [
                {
                    "field_key": field["field_key"],
                    "label": field.get("label", ""),
                    "group_label": field.get("group_label", ""),
                    "type": field.get("type", ""),
                    "options": field.get("options", []),
                    "placeholder": field.get("placeholder", ""),
                }
                for field in completion["required_unanswered"]
            ]
            ollama_answers = self.ollama_assistant.suggest_answers(
                prompt_fields,
                self.candidate,
                {"job_title": job_title},
            )
            for field in completion["required_unanswered"]:
                answer = ollama_answers.get(field["field_key"], "")
                if answer:
                    await self._apply_answer(page, field, answer)

            await page.wait_for_timeout(750)
            latest_fields = await self.detect_lever_form_fields(page)
            completion = self.assess_form_completion(latest_fields)

        total_fills = deterministic_fills + len(ollama_answers)
        self.logger.info(
            f"Form fill summary: deterministic={deterministic_fills}, ollama={len(ollama_answers)}, unresolved_required={len(completion['required_unanswered'])}"
        )
        return {
            "filled_count": total_fills,
            "completion": completion,
            "used_ollama": bool(ollama_answers),
            "ollama_answers": ollama_answers,
        }

    async def find_and_click_submit(self, page: Page) -> bool:
        """Find and click the submit button on Lever form."""
        try:
            self.logger.info("Locating submit button...")
            submit_selectors = [
                'button:has-text("Submit application")',
                'button:has-text("Apply")',
                'button[type="submit"]',
                'button[class*="submit"]',
                'button[class*="apply"]',
                'button[class*="primary"]',
            ]
            for selector in submit_selectors:
                button = await page.query_selector(selector)
                if button and await button.is_visible():
                    self.logger.info(f"Found submit button: {selector}")
                    await button.scroll_into_view_if_needed()
                    await page.wait_for_timeout(500)
                    await button.click()
                    self.logger.info("Clicked submit button")
                    await page.wait_for_timeout(3000)
                    return True
            self.logger.warning("Could not find visible submit button")
            return False
        except Exception as exc:
            self.logger.error(f"Error clicking submit button: {exc}")
            return False

    async def verify_submission(self, page: Page) -> Tuple[bool, str]:
        """Require explicit success evidence and reject incomplete on-page forms."""
        try:
            self.logger.info("Verifying submission...")
            await page.wait_for_timeout(2000)

            current_url = page.url
            content_lower = (await page.content()).lower()
            error_patterns = [
                "there was an error sending your application",
                "please try again",
                "this field is required",
            ]
            if any(pattern in content_lower for pattern in error_patterns):
                matched = next(pattern for pattern in error_patterns if pattern in content_lower)
                return False, f"Submission blocked by on-page error: {matched}"

            success_patterns = [
                "thank you",
                "application received",
                "thank you for your interest",
                "successfully submitted",
                "we have received your application",
            ]
            if any(pattern in content_lower for pattern in success_patterns):
                return True, "Success text detected"

            if "thank" in current_url.lower() or "confirm" in current_url.lower() or "submitted" in current_url.lower():
                return True, f"Confirmation URL detected: {current_url}"

            latest_fields = await self.detect_lever_form_fields(page)
            completion = self.assess_form_completion(latest_fields)
            if completion["required_unanswered"]:
                labels = ", ".join(field.get("label") or field.get("group_label") or field.get("name") or "field" for field in completion["required_unanswered"][:5])
                return False, f"Required fields remain unanswered: {labels}"

            submit_button = await page.query_selector('button:has-text("Submit application"), button[type="submit"]')
            if submit_button and await submit_button.is_visible():
                return False, f"Still on application form at {current_url}"

            return False, f"No explicit confirmation found after submit at {current_url}"
        except Exception as exc:
            self.logger.warning(f"Error verifying submission: {exc}")
            return False, str(exc)

    async def handle_lever_with_javascript(
        self,
        page: Page,
        index: int,
        company: str,
        job_title: str,
    ) -> Tuple[str, str, str]:
        """Complete Lever form filling and submission with strict completion checks."""
        try:
            self.logger.info(f"Starting Lever JavaScript form handler for {company}")
            form_fields = await self.detect_lever_form_fields(page)
            if not form_fields:
                return "Requires Manual Action", "Could not detect form fields", ""

            fill_report = await self.fill_lever_form(page, form_fields, job_title=job_title)
            completion = fill_report["completion"]
            if completion["required_unanswered"]:
                labels = ", ".join(field.get("label") or field.get("group_label") or field.get("name") or "field" for field in completion["required_unanswered"][:6])
                screenshot = await self.take_screenshot(page, f"incomplete_{index}", full_page=True)
                return "Incomplete Required Fields", f"Required questions remain unanswered: {labels}", screenshot

            screenshot = await self.take_screenshot(page, f"filled_{index}", full_page=True)
            submitted = await self.find_and_click_submit(page)
            if not submitted:
                return "Form Filled", "Form filled but could not locate submit button", screenshot

            verified, reason = await self.verify_submission(page)
            screenshot = await self.take_screenshot(page, f"submitted_{index}", full_page=True)
            if verified:
                return "Submitted", reason, screenshot
            return "Submission Uncertain", reason, screenshot
        except Exception as exc:
            self.logger.error(f"Error in Lever JavaScript handler: {exc}")
            screenshot = await self.take_screenshot(page, f"error_{index}", full_page=True)
            return "Error", str(exc), screenshot


def choose_matching_option(options: List[str], answer: str) -> str:
    normalized = answer.strip().lower()
    for option in options:
        if normalized == option.strip().lower():
            return option
    for option in options:
        if normalized in option.strip().lower() or option.strip().lower() in normalized:
            return option
    return ""


def normalized_truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "yes", "y", "1", "check", "checked"}