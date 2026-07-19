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