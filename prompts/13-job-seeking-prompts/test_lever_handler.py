import asyncio
import logging

from config import Config
from lever_handler import LeverFormHandler, choose_matching_option
from ollama_field_assistant import OllamaFieldAssistant


def build_handler() -> LeverFormHandler:
    return LeverFormHandler(headless=True)


def test_assess_form_completion_flags_required_unanswered_group() -> None:
    handler = build_handler()
    fields = {
        "field_0": {
            "field_key": "field_0",
            "type": "text",
            "tag": "input",
            "label": "Full name",
            "group_label": "",
            "name": "name",
            "required": True,
            "visible": True,
            "disabled": False,
            "current_value": "Juan",
            "checked": False,
        },
        "field_1": {
            "field_key": "field_1",
            "type": "textarea",
            "tag": "textarea",
            "label": "Describe your AWS services experience",
            "group_label": "",
            "name": "aws_services",
            "required": True,
            "visible": True,
            "disabled": False,
            "current_value": "",
            "checked": False,
        },
        "field_2": {
            "field_key": "field_2",
            "type": "radio",
            "tag": "input",
            "label": "Senior",
            "group_label": "What is your seniority level for this role?",
            "name": "seniority",
            "required": True,
            "visible": True,
            "disabled": False,
            "current_value": "Senior",
            "checked": False,
        },
        "field_3": {
            "field_key": "field_3",
            "type": "radio",
            "tag": "input",
            "label": "Lead",
            "group_label": "What is your seniority level for this role?",
            "name": "seniority",
            "required": True,
            "visible": True,
            "disabled": False,
            "current_value": "Lead",
            "checked": True,
        },
    }

    completion = handler.assess_form_completion(fields)

    assert completion["filled_count"] == 2
    assert len(completion["required_unanswered"]) == 1
    assert "AWS services" in completion["required_unanswered"][0]["label"]


def test_deterministic_answer_covers_prompt_from_screenshot() -> None:
    handler = build_handler()
    field = {
        "label": "Do you have production experience with Gen AI?",
        "group_label": "EXPERIENCE IN GENAI",
        "name": "genai_experience",
        "placeholder": "",
    }
    answer = handler._deterministic_answer(field, "AI Engineer")
    assert answer == "Yes"


def test_choose_matching_option_prefers_exact_or_partial_match() -> None:
    options = ["Trainee", "Junior", "Middle", "Senior", "Lead", "Architect"]
    assert choose_matching_option(options, "Lead") == "Lead"
    assert choose_matching_option(options, "C2 Proficient") == ""


def test_normalize_location_text_strips_accents_and_lowercases() -> None:
    handler = build_handler()
    assert handler._normalize_location_text("Bogotá, Colombia") == "bogota, colombia"
    assert handler._normalize_location_text("Bögöt") == "bogot"
    assert handler._normalize_location_text("  Medellín  ") == "medellin"
    assert handler._normalize_location_text("") == ""


def test_location_search_terms_puts_accent_free_city_first() -> None:
    handler = build_handler()
    terms = handler._location_search_terms("Bogotá, Colombia")
    # The accent-free city must be the first candidate Lever's API can match.
    assert terms[0] == "bogota"
    assert "bogota, colombia" in terms
    assert "colombia" in terms


def test_location_search_terms_single_word_answer() -> None:
    handler = build_handler()
    terms = handler._location_search_terms("Remote")
    assert terms[0] == "remote"


def test_location_search_terms_short_or_empty_answer_has_fallback() -> None:
    handler = build_handler()
    assert handler._location_search_terms("NY") == ["ny"]
    assert handler._location_search_terms("") == [""]


class _StubRow:
    """Minimal stand-in for a Playwright element handle with async inner_text."""

    def __init__(self, text: str):
        self._text = text

    async def inner_text(self) -> str:
        return self._text


def _pick(handler, rows, answer):
    return asyncio.run(handler._pick_location_row(None, rows, answer))


def test_pick_location_row_prefers_colombia_and_token_match() -> None:
    handler = build_handler()
    rows = [
        _StubRow("Bögöt, Sárvári járás, Vas, HUN"),
        _StubRow("Bogotá, Distrito Capital, COL"),
        _StubRow("Bogota, NJ, USA"),
    ]
    picked = _pick(handler, rows, "Bogotá, Colombia")
    assert picked is not None
    assert asyncio.run(picked.inner_text()) == "Bogotá, Distrito Capital, COL"


def test_pick_location_row_rejects_unrelated_suggestions() -> None:
    handler = build_handler()
    rows = [_StubRow("Bögöt, Sárvári járás, Vas, HUN"), _StubRow("Bogot, Ivanovo, RUS")]
    picked = _pick(handler, rows, "Bogotá, Colombia")
    # No row matches the answer or Colombia -> must NOT click an unrelated suggestion.
    assert picked is None


def test_pick_location_row_exact_match_wins() -> None:
    handler = build_handler()
    rows = [_StubRow("Bogotá, Distrito Capital, COL"), _StubRow("Colombia")]
    picked = _pick(handler, rows, "Colombia")
    assert asyncio.run(picked.inner_text()) == "Colombia"


def test_ollama_json_extraction_handles_wrapped_output() -> None:
    assistant = OllamaFieldAssistant({"enabled": True}, logging.getLogger("test-ollama"))
    payload = assistant._extract_json(
        "Here is the answer\n{\"answers\": [{\"field_key\": \"field_9\", \"answer\": \"Colombia\"}]}"
    )
    assert payload["answers"][0]["field_key"] == "field_9"


def test_config_exposes_ollama_section() -> None:
    config = Config()
    ollama = config.get_ollama_config()
    assert ollama["enabled"] is True
    assert ollama["model"]