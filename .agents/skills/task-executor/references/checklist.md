# Task Executor Checklist

Use this checklist to verify task execution completeness.

## Pre-Execution

- [ ] Goal extracted and clear
- [ ] Scope defined (files/systems)
- [ ] Success criteria established
- [ ] Plan created with risk assessment
- [ ] User approved the plan

## During Execution

- [ ] Each step logged (success/failure)
- [ ] Safety guardrails consulted before destructive ops
- [ ] Checkpoints saved after major steps
- [ ] Retries attempted on failures (max 2)

## Post-Execution

- [ ] Success criteria re-checked
- [ ] Automated tests run (if applicable)
- [ ] Output manually verified
- [ ] Report sent to user
- [ ] Self-evaluation logged

## Risk Assessment Guide

| Action | Risk Level | Confirmation |
|--------|-----------|-------------|
| Read files | LOW | Not needed |
| Create new files | LOW | Not needed |
| Edit existing files | MEDIUM | Not needed if reversible |
| Delete files | HIGH | Required |
| API calls with cost | HIGH | Required |
| System configuration changes | HIGH | Required |
| Install packages | MEDIUM | Not needed |
| Send external messages | MEDIUM | Required for first time |
