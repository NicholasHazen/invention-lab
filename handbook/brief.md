# Invention Lab handbook — authoring contract

Goal: develop the existing guide into a substantive college-text-meets-maker-workbench learning system. Teach foundations AND how to begin independent projects. Preserve the existing 52-step pivot tutorial and 3D viewer as a detailed case study.

Reader: motivated adult beginner with a little Fusion experience, a Bambu X1 Carbon, ordinary hand tools, optional low-voltage electronics. Do not assume calculus, EE vocabulary or shop certification. Give a no-purchase/simulation route where practical. Deeper paths can require algebra, physics or coding, but state those prerequisites.

Voice: connected original prose, concrete mechanisms and causal explanations. Read TutorBro tutorial-writing skill and prose guide. No fabricated build history or physical test results. Neither an outline nor a link directory is enough.

Each chapter should contain substantive explanation, explicit outcomes/prerequisites, one numerically worked or traced example, a reproducible bench/paper/software lab with materials/actions/expected observations and diagnostics, prediction questions with answers, an adjacent independent-project challenge, and precise references to primary sources. Target roughly 1,500–2,200 useful words; length is not a substitute for coverage. Avoid generic repeated scaffolding where it adds nothing. Use tables/diagrams/code when they explain a relationship. Label expected observations versus tests actually run. No unverified promise that old external software/course examples work on current versions.

Keep labs low-energy and beginner-appropriate. Put specific safety instructions beside the relevant action. Do not provide unsupervised mains, lithium-pack fabrication, laser-material guessing, or unreviewed CNC operation recipes. Teach the reasoning and direct machine-specific operation to training/manufacturer instructions. Distinguish prototypes from rated devices.

Stable project spine: (1) sensor bracket and fit coupon; (2) low-voltage bench sensor/logger; (3) small tabletop positioning rig/simulation. The existing pivot has NOT been physically printed or load-tested; electronics remain a future project extension, not a newly validated design.

Recommendations: research current primary sources (university/course owner, author, publisher, official project docs). Record what a resource teaches, who it suits, prerequisites, free/paid/access uncertainty, a specific starting task, and limitations. Include courses, books and videos across the collection. Avoid affiliate links and exact prices. Distinguish free archived course materials from certificates or live instruction. Do not list a resource you have not opened/verified. Prefer a few useful choices over a long undifferentiated list. Recommendations reflect syllabus/contents/documentation review, not a claim of personally completing each course.

Resource JSON schema (array): id, title, creator, url, format (course|book|video|documentation|project), topics (array), level, prerequisites, access, why (short original assessment), first_task (actionable), limitations, verified_on ('2026-11-04'), evidence_url, evidence_note (what the official page verified). IDs lowercase hyphenated. Use absolute external URLs; internal chapter links will be inserted by root. Cite sources near supported claims as normal Markdown links.

Chapter files: one H1 title, H2 sections and H3 subsections. No metadata frontmatter; root keeps navigation in curriculum.json. Keep worksheet and code files in handbook/worksheets or handbook/examples, with relative links from chapter outputs coordinated with root. Source prose remains in this repository for maintenance. Do not alter the pivot geometry, source guide or publishing tools unless explicitly assigned.
