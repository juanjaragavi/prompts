"""Local Ollama helper for unresolved application form questions."""

from __future__ import annotations

import json
import re
import subprocess
from subprocess import TimeoutExpired
from typing import Any, Dict, List


class OllamaFieldAssistant:
    """Suggest answers for unresolved form fields using a local Ollama model."""

    def __init__(self, config: Dict[str, Any], logger: Any):
        self.config = dict(config)
        self.logger = logger

    def is_enabled(self) -> bool:
        return bool(self.config.get("enabled", False))

    def suggest_answers(
        self,
        fields: List[Dict[str, Any]],
        candidate: Dict[str, Any],
        job_context: Dict[str, Any],
    ) -> Dict[str, str]:
        """Return `{field_key: answer}` suggestions for unresolved fields."""
        if not self.is_enabled() or not fields:
            return {}

        model = str(self.config.get("model", "llama3-groq-tool-use:8b"))
        if not re.fullmatch(r"[A-Za-z0-9._:-]+", model):
            self.logger.warning(f"Rejected invalid Ollama model name: {model}")
            return {}

        timeout_seconds = int(self.config.get("timeout_seconds", 45))
        resolved: Dict[str, str] = {}
        for field in fields:
            field_key = str(field.get("field_key", "")).strip()
            if not field_key:
                continue

            prompt = self._build_single_field_prompt(field, candidate, job_context)
            try:
                result = subprocess.run(
                    ["ollama", "run", model],
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=timeout_seconds,
                    check=False,
                )
            except TimeoutExpired:
                self.logger.warning(f"Ollama timed out after {timeout_seconds} seconds")
                continue
            except Exception as exc:
                self.logger.warning(f"Ollama invocation failed: {exc}")
                continue

            if result.returncode != 0:
                self.logger.warning(f"Ollama returned non-zero exit code: {result.stderr.strip()}")
                continue

            answer = self._extract_answer(result.stdout)
            if answer:
                resolved[field_key] = answer

        return resolved

    def _build_single_field_prompt(
        self,
        field: Dict[str, Any],
        candidate: Dict[str, Any],
        job_context: Dict[str, Any],
    ) -> str:
        options = field.get("options", [])
        option_lines = []
        for option in options:
            if isinstance(option, dict):
                option_lines.append(str(option.get("text", "")).strip())
            else:
                option_lines.append(str(option).strip())

        candidate_summary = {
            "full_name": candidate.get("full_name"),
            "title": candidate.get("title"),
            "location": candidate.get("location"),
            "current_company": candidate.get("current_company"),
            "years_experience": candidate.get("years_experience"),
            "years_ai_experience": candidate.get("years_ai_experience"),
            "linkedin": candidate.get("linkedin"),
            "github": candidate.get("github"),
            "portfolio": candidate.get("portfolio"),
            "notice_period": candidate.get("notice_period"),
            "target_range_monthly": candidate.get("target_range_monthly"),
            "target_range_annual": candidate.get("target_range_annual"),
            "country": candidate.get("country"),
            "city": candidate.get("city"),
            "english_level": candidate.get("english_level"),
            "requires_visa_sponsorship": candidate.get("requires_visa_sponsorship"),
            "summary_medium": candidate.get("summary_medium"),
        }

        rules = [
            "Answer only with the final answer text.",
            "Do not explain your reasoning.",
            "Do not add prefixes, bullet points, or JSON.",
            "Be truthful to the candidate profile.",
        ]
        if option_lines:
            rules.append("If options are provided, answer with exactly one of the option texts.")

        prompt_payload = {
            "task": "Answer one job application field.",
            "rules": rules,
            "job_context": job_context,
            "candidate": candidate_summary,
            "field": {
                "label": field.get("label"),
                "group_label": field.get("group_label"),
                "type": field.get("type"),
                "placeholder": field.get("placeholder"),
                "options": option_lines,
            },
        }
        return json.dumps(prompt_payload, ensure_ascii=False, indent=2)

    def _build_prompt(
        self,
        fields: List[Dict[str, Any]],
        candidate: Dict[str, Any],
        job_context: Dict[str, Any],
    ) -> str:
        candidate_summary = {
            "full_name": candidate.get("full_name"),
            "title": candidate.get("title"),
            "location": candidate.get("location"),
            "current_company": candidate.get("current_company"),
            "years_experience": candidate.get("years_experience"),
            "years_ai_experience": candidate.get("years_ai_experience"),
            "linkedin": candidate.get("linkedin"),
            "github": candidate.get("github"),
            "portfolio": candidate.get("portfolio"),
            "notice_period": candidate.get("notice_period"),
            "target_range_monthly": candidate.get("target_range_monthly"),
            "target_range_annual": candidate.get("target_range_annual"),
            "country": candidate.get("country"),
            "city": candidate.get("city"),
            "english_level": candidate.get("english_level"),
            "requires_visa_sponsorship": candidate.get("requires_visa_sponsorship"),
            "summary_medium": candidate.get("summary_medium"),
        }
        instructions = {
            "task": "Answer unresolved job application questions accurately and conservatively.",
            "rules": [
                "Do not invent certifications or experience not present in the candidate summary.",
                "If a select/radio field has options, answer using the exact option text when possible.",
                "Use concise professional text for textarea/text questions.",
                "Return strict JSON only.",
                "Schema: {\"answers\": [{\"field_key\": \"...\", \"answer\": \"...\"}]}",
            ],
            "job_context": job_context,
            "candidate": candidate_summary,
            "fields": fields,
        }
        return json.dumps(instructions, ensure_ascii=False, indent=2)

    def _extract_json(self, raw_text: str) -> Dict[str, Any]:
        text = raw_text.strip()
        if not text:
            return {}

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            return {}

        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {}

    def _extract_answer(self, raw_text: str) -> str:
        text = raw_text.strip()
        if not text:
            return ""

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return ""

        answer = lines[-1]
        answer = re.sub(r"^['\"]|['\"]$", "", answer).strip()
        return answer