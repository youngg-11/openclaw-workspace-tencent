---
name: daily-report
description: 工作日报生成。触发场景：用户要求整理日报、梳理工作。
---

# Daily Report

## Format

Group by time period, list work items for each period.

Each item includes:
- What was done
- 2 pros ✅
- 2 cons ❌ (auto-logged to self-improving-agent)

## Structure

```
# YYYY-MM-DD Work Report

**08:00-09:00**
- Work item
  - ✅ Pro 1
  - ✅ Pro 2
  - ❌ Con 1 → Next time improve
  - ❌ Con 2 → Next time improve
```

## Con Handling

Log each ❌ to:
- `.learnings/ERRORS.md` (error reflection)
- `.learnings/LEARNINGS.md` (improvement guide)

Format:
```
## Improvement Log
- Time: YYYY-MM-DD
- Scenario: Work item
- Issue: Con description
- Fix: How to avoid
```

## Rules
- Concise, max 20 chars/point
- Time order
- Must have 2 pros + 2 cons
- Cons auto-logged to self-improving
