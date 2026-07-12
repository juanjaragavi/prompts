import json

data = [
  {
    "index": 1,
    "company": "Medfar",
    "job_title": "Generative AI (GenAI) | Prompt Engineer",
    "platform": "SmartRecruiters",
    "url": "https://jobs.smartrecruiters.com/oneclick-ui/company/Medfar/publication/962a7b51-8f78-4cac-9914-2d045f619464?dcr_ci=Medfar"
  },
  {
    "index": 2,
    "company": "TherapyNotes.com",
    "job_title": "Senior Software Developer (Agentic Development)",
    "platform": "Workable",
    "url": "https://apply.workable.com/therapynotes/j/2A691CE916/apply/"
  },
  {
    "index": 3,
    "company": "Xsolla",
    "job_title": "Product Owner, DevX and AI — Shop Builder",
    "platform": "Lever",
    "url": "https://jobs.lever.co/xsolla/d1cc3abc-fc26-4732-97ba-49971da226cf/apply"
  },
  {
    "index": 4,
    "company": "Bjak",
    "job_title": "Applied AI Engineer",
    "platform": "Ashby",
    "url": "https://jobs.ashbyhq.com/bjakcareer/0ab4a37a-0779-4480-8d3a-bbaf093c2da8/application"
  },
  {
    "index": 5,
    "company": "Team Red Dog",
    "job_title": "AI Prompt Engineer",
    "platform": "Crelate",
    "url": "https://jobs.crelate.com/portal/teamreddog/job/apply/ny9o6rxqgq7juw8t8z4oo3zp6c"
  },
  {
    "index": 6,
    "company": "Curve Dental",
    "job_title": "AI/ML Platform Software Developer",
    "platform": "Rippling",
    "url": "https://ats.rippling.com/curve-dental/jobs/ef73da8e-d943-4bd0-9921-415901a748aa/apply?jobBoardSlug=curve-dental&jobId=ef73da8e-d943-4bd0-9921-415901a748aa&step=application"
  },
  {
    "index": 7,
    "company": "Netomi",
    "job_title": "Agentic Engineer",
    "platform": "Lever",
    "url": "https://jobs.lever.co/netomi/ba379f47-091b-4f2d-82d3-e97a0821227e/apply"
  },
  {
    "index": 8,
    "company": "WorkBetterNow",
    "job_title": "AI Software Developer (Internal Tools)",
    "platform": "Zoho Recruit",
    "url": "https://workbetternow.zohorecruit.com/jobs/Careers/746650000037462674/AI-Software-Developer-Internal-Tools"
  }
]

file_path = "/Users/macbookpro/GitHub/prompts/prompts/13-job-seeking-prompts/open_applications_inventory.json"
with open(file_path, "w") as f:
    json.dump(data, f, indent=2)

print("Saved to", file_path)
