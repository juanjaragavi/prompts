#!/usr/bin/env python3
"""
Human-in-the-loop Lever batch runner.

Flow:
1) Open each target job page in a visible browser.
2) Wait for user to solve CAPTCHA/challenge manually.
3) When form fields become detectable, bot auto-fills and submits.
4) Save per-job status artifacts.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import List, Dict, Any

from playwright.async_api import async_playwright, Page

from config import Config
from lever_handler import LeverFormHandler


TARGET_INDEXES = [3, 5, 6, 7, 8, 16, 17, 18, 19, 20]
CAPTCHA_WAIT_SECONDS = 420
CAPTCHA_POLL_INTERVAL_SECONDS = 4
MANUAL_COMPLETION_WAIT_SECONDS = 600


def load_target_jobs(inventory_path: str, indexes: List[int]) -> List[Dict[str, Any]]:
    with open(inventory_path, "r") as f:
        inventory = json.load(f)
    selected = [item for item in inventory if item.get("index") in indexes and item.get("platform", "").lower() == "lever"]
    return sorted(selected, key=lambda x: x["index"])


async def wait_until_form_detected(bot: LeverFormHandler, page: Page, timeout_seconds: int) -> Dict[str, Any]:
    waited = 0
    while waited < timeout_seconds:
        form_fields = await bot.detect_lever_form_fields(page)
        if form_fields:
            return form_fields

        await asyncio.sleep(CAPTCHA_POLL_INTERVAL_SECONDS)
        waited += CAPTCHA_POLL_INTERVAL_SECONDS

    return {}


async def wait_until_required_fields_resolved(
    bot: LeverFormHandler,
    page: Page,
    job_title: str,
    timeout_seconds: int,
) -> Dict[str, Any]:
    waited = 0
    latest_report: Dict[str, Any] = {"completion": {"required_unanswered": []}, "filled_count": 0}

    while waited < timeout_seconds:
        fields = await bot.detect_lever_form_fields(page)
        if not fields:
            await asyncio.sleep(CAPTCHA_POLL_INTERVAL_SECONDS)
            waited += CAPTCHA_POLL_INTERVAL_SECONDS
            continue

        latest_report = await bot.fill_lever_form(page, fields, job_title=job_title)
        if not latest_report["completion"]["required_unanswered"]:
            return latest_report

        await asyncio.sleep(CAPTCHA_POLL_INTERVAL_SECONDS)
        waited += CAPTCHA_POLL_INTERVAL_SECONDS

    return latest_report


async def process_job(bot: LeverFormHandler, page: Page, app: Dict[str, Any]) -> Dict[str, Any]:
    index = app["index"]
    company = app["company"]
    job_title = app["job_title"]
    platform = app["platform"]
    url = app["url"]

    bot.logger.info("=" * 80)
    bot.logger.info(f"HIL Processing {index}: {company} - {job_title}")
    bot.logger.info(f"URL: {url}")

    loaded = await bot.load_page(page, url)
    if not loaded:
        return {
            "index": index,
            "company": company,
            "job_title": job_title,
            "platform": platform,
            "url": url,
            "status": "Failed to Load",
            "details": "Could not load target page",
            "screenshot_path": await bot.take_screenshot(page, f"hil_failed_load_{index}"),
            "timestamp": datetime.now().isoformat(),
        }

    bot.logger.info(
        f"If CAPTCHA/challenge is visible, solve it now in the opened browser window. Waiting up to {CAPTCHA_WAIT_SECONDS}s..."
    )

    form_fields = await wait_until_form_detected(bot, page, CAPTCHA_WAIT_SECONDS)
    if not form_fields:
        return {
            "index": index,
            "company": company,
            "job_title": job_title,
            "platform": platform,
            "url": url,
            "status": "Requires Manual Action",
            "details": f"Form fields were not detectable after waiting {CAPTCHA_WAIT_SECONDS}s (likely unresolved CAPTCHA/challenge)",
            "screenshot_path": await bot.take_screenshot(page, f"hil_no_form_{index}", full_page=True),
            "timestamp": datetime.now().isoformat(),
        }

    fill_report = await bot.fill_lever_form(page, form_fields, job_title=job_title)
    if fill_report["filled_count"] <= 0:
        return {
            "index": index,
            "company": company,
            "job_title": job_title,
            "platform": platform,
            "url": url,
            "status": "Form Detection Failed",
            "details": "Form detected but bot could not fill required fields",
            "screenshot_path": await bot.take_screenshot(page, f"hil_unfilled_{index}", full_page=True),
            "timestamp": datetime.now().isoformat(),
        }

    completion = fill_report["completion"]
    if completion["required_unanswered"]:
        unresolved = ", ".join(
            field.get("label") or field.get("group_label") or field.get("name") or "field"
            for field in completion["required_unanswered"][:6]
        )
        bot.logger.info(
            "Manual completion required for unresolved fields. "
            f"Please complete them in the browser now. Waiting up to {MANUAL_COMPLETION_WAIT_SECONDS}s. "
            f"Fields: {unresolved}"
        )
        await bot.take_screenshot(page, f"hil_incomplete_{index}", full_page=True)
        fill_report = await wait_until_required_fields_resolved(
            bot,
            page,
            job_title,
            MANUAL_COMPLETION_WAIT_SECONDS,
        )
        completion = fill_report["completion"]
        if completion["required_unanswered"]:
            unresolved = ", ".join(
                field.get("label") or field.get("group_label") or field.get("name") or "field"
                for field in completion["required_unanswered"][:6]
            )
            return {
                "index": index,
                "company": company,
                "job_title": job_title,
                "platform": platform,
                "url": url,
                "status": "Incomplete Required Fields",
                "details": f"Required questions still remained unanswered after manual-assist window: {unresolved}",
                "screenshot_path": await bot.take_screenshot(page, f"hil_incomplete_final_{index}", full_page=True),
                "timestamp": datetime.now().isoformat(),
            }

    await bot.take_screenshot(page, f"hil_filled_{index}", full_page=True)

    submitted = await bot.find_and_click_submit(page)
    if not submitted:
        return {
            "index": index,
            "company": company,
            "job_title": job_title,
            "platform": platform,
            "url": url,
            "status": "Form Filled",
            "details": "Form filled but submit button was not clicked",
            "screenshot_path": await bot.take_screenshot(page, f"hil_no_submit_{index}", full_page=True),
            "timestamp": datetime.now().isoformat(),
        }

    verified, reason = await bot.verify_submission(page)
    status = "Submitted" if verified else "Submission Uncertain"
    details = reason

    return {
        "index": index,
        "company": company,
        "job_title": job_title,
        "platform": platform,
        "url": url,
        "status": status,
        "details": details,
        "screenshot_path": await bot.take_screenshot(page, f"hil_submitted_{index}", full_page=True),
        "timestamp": datetime.now().isoformat(),
    }


async def main() -> None:
    config = Config()
    bot = LeverFormHandler(headless=False)

    inventory_path = os.path.join(config.get_output_dirs()["status_dir"], "open_applications_inventory_expanded.json")
    targets = load_target_jobs(inventory_path, TARGET_INDEXES)

    if len(targets) != len(TARGET_INDEXES):
        bot.logger.warning(
            f"Expected {len(TARGET_INDEXES)} target jobs but found {len(targets)} Lever targets in inventory"
        )

    run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "run_id": f"human_in_loop_lever_{run_stamp}",
        "mode": "human_in_loop",
        "targets": [t["index"] for t in targets],
        "results": [],
    }

    async with async_playwright() as p:
        browser_cfg = config.get_browser_config()
        browser = await p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(
            user_agent=browser_cfg["user_agent"],
            viewport={
                "width": browser_cfg["viewport_width"],
                "height": browser_cfg["viewport_height"],
            },
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        page = await context.new_page()

        for app in targets:
            result = await process_job(bot, page, app)
            report["results"].append(result)

            status_file = os.path.join(
                config.get_output_dirs()["status_dir"],
                f"hil_application_{app['index']}_status.json",
            )
            with open(status_file, "w") as sf:
                json.dump(result, sf, indent=2)
            bot.logger.info(f"Saved HIL status file: {status_file} -> {result['status']}")

        await context.close()
        await browser.close()

    summary = {
        "total": len(report["results"]),
        "submitted": sum(1 for r in report["results"] if r["status"] == "Submitted"),
        "submission_uncertain": sum(1 for r in report["results"] if r["status"] == "Submission Uncertain"),
        "form_filled": sum(1 for r in report["results"] if r["status"] == "Form Filled"),
        "manual_action": sum(1 for r in report["results"] if "Manual Action" in r["status"]),
        "failed": sum(1 for r in report["results"] if r["status"] == "Failed to Load"),
    }

    report["summary"] = summary
    report_path = os.path.join(
        config.get_output_dirs()["status_dir"],
        f"hil_batch_report_{run_stamp}.json",
    )
    with open(report_path, "w") as rf:
        json.dump(report, rf, indent=2)

    bot.logger.info("=" * 80)
    bot.logger.info(f"HIL batch completed. Summary: {summary}")
    bot.logger.info(f"Report: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())
