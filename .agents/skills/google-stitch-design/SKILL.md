---
name: google-stitch-design
description: "Web application and interface design skill using Google Stitch APIs. Uses stored session tokens to authenticate and generate UI/UX designs, layouts, and frontend code directly through the Stitch service."
---

# Google Stitch Design Skill

## Overview

This skill provides guidelines for interacting with Google Stitch to generate, refine, and extract web application and interface designs. It utilizes the session tokens stored in `.agents/credentials/google-stitch.json`.

## Authentication & Quota Management

When an agent or workflow needs to interact with Google Stitch (e.g., via Playwright MCP, curl, or custom script integrations), it MUST select an available token from `repo_root/.agents/credentials/google-stitch.json`. This file contains multiple accounts.

**Quota Limits per Account:**

- 15 designs (pages) OR 400 tokens per day.

**Rotation Strategy:**

- Do not exhaust a single account. The agent must implement a rotation or failover strategy.
- If an account reaches its daily quota (15 designs / 400 tokens), or returns a 401/403 Error/Quota Exceeded error, cycle to the next available token in the JSON array.
- Treat these session tokens as highly sensitive. **Never print them in chat or logs.**

## Usage Scenarios

- **UI/UX Mockup Generation:** When the user requests a new screen or component design (especially premium Brutalism or Apple-style web design).
- **Vibe Coding integration:** Can be used alongside `vibe-coding-ui` skill for generating high-fidelity frontend code based on Stitch outputs.
- **Frontend translation:** Converting Stitch design metadata into React/TypeScript code (such as the SmartMeeting app components).

## Execution Guidelines

1. **Analyze Requirements:** Understand the user's design constraints, color palette, and layout goals.
2. **Access Credentials:** Read `.agents/credentials/google-stitch.json` programmatically.
3. **Execute API/Browser Action:** Call the Stitch service endpoints or use Playwright MCP with the injected session cookie (`__Secure-1PSID` format, depending on the exact Stitch API requirement).
4. **Extract Result:** Capture the generated code or design artifact.
5. **Verify:** Ensure the output aligns with the project's engineering standards (AGENTS.md § 6).

## Security Guardrails

- **Action Tier:** Interacting with external Google APIs via these tokens is considered a **Tier 3 (HIGH RISK)** action according to `safety-guardrails/SKILL.md`.
- Ensure the user is notified if API usage requires costs or significant generation time.
