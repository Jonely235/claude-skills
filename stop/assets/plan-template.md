# STOP Plan Template

Use this template during the **P - Plan** phase to document your approach before coding.

## Metadata

**Date**: YYYY-MM-DD
**Task**: [Brief description of what you're doing]
**Author**: [Your name]
**STOP Duration**: [Total time spent on S-T-O phases]

---

## S - Stop (30 seconds)

**Initial impulse**:
[What did I want to do immediately?]

**STOP checkpoint**:
- [ ] Do I REALLY understand what needs to be done?
- [ ] Have I read the relevant code?
- [ ] What am I missing?

**Self-correction**:
[What did I realize I needed to investigate?]

---

## T - Trace (5-10 minutes)

### 1. Files Found

| File | Relevance | Key Observations |
|------|-----------|------------------|
| [File path] | [High/Medium/Low] | [What did you learn?] |
| [File path] | [High/Medium/Low] | [What did you learn?] |

### 2. Code Patterns Discovered

**Similar existing implementations**:
- [Function/feature 1]: [Location]
- [Function/feature 2]: [Location]

**Common patterns observed**:
- [Pattern 1]: [Description]
- [Pattern 2]: [Description]

### 3. Dependencies Identified

**What does my change depend on?**:
- [Dependency 1]: [Location, what it does]
- [Dependency 2]: [Location, what it does]

**What depends on the code I'm changing?**:
- [Dependent 1]: [Location, how it's affected]
- [Dependent 2]: [Location, how it's affected]

### 4. Architecture Understanding

**Where does my change fit?**
- [Module/Domain]: [Description]
- [Layer]: [Controller/Service/Model/Utility/etc.]

**What's the existing pattern?**
- [Description of how similar things are done]

### 5. Search Commands Used

```bash
# [What you searched for and why]
Glob: [pattern]

# [What you searched for and why]
Grep: [pattern]

# [What you searched for and why]
Read: [file path]

# [What you searched for and why]
LSP: [operation] on [symbol]
```

---

## O - Orient (2-3 minutes)

### 1. Location

**Where does my change fit?**
- File: `[path/to/file.ext]`
- Function/Component: `[name]`
- Line range: `[approximately]`

**What's the existing pattern?**
- [Describe the pattern you should follow]

**Should I follow or create new pattern?**
- [ ] Follow existing pattern
- [ ] Create new pattern (justify: why?)

### 2. Minimal Change

**What's the smallest thing that works?**
- [Description of minimal change]

**Can I reuse existing code?**
- [ ] Yes: [What code can you reuse?]
- [ ] No: [Why not?]

**Should I refactor instead?**
- [ ] Yes: [What should be refactored?]
- [ ] No: [Why not?]

### 3. Risk Assessment

**What depends on this code?**
- [Dependency 1]: [Impact if it breaks]
- [Dependency 2]: [Impact if it breaks]

**What could break?**
- [Risk 1]: [Likelihood: High/Medium/Low]
- [Risk 2]: [Likelihood: High/Medium/Low]

**What tests exist?**
- [Test 1]: [What it covers]
- [Test 2]: [What it covers]

**Do I need to add tests?**
- [ ] Yes: [What tests need to be added?]
- [ ] No: [Existing tests are sufficient]

---

## P - Plan (1-2 minutes)

### 1. The Specific Change

**File**: `path/to/file.ext`

**Function/Component**: `functionName`

**Change Type**: [ ] New feature [ ] Bug fix [ ] Refactor [ ] Optimization [ ] Tests

**Detailed Approach**:
1. [Step 1 - what you'll do]
2. [Step 2 - what you'll do]
3. [Step 3 - what you'll do]
4. [etc.]

**Code changes summary**:
```
[File: path/to/file.ext]
- [What you'll remove/change]
+ [What you'll add/change]

[File: path/to/another-file.ext]
- [What you'll remove/change]
+ [What you'll add/change]
```

### 2. Testing Strategy

**How will you verify it works?**
- [Test method 1]: [What it verifies]
- [Test method 2]: [What it verifies]

**What edge cases exist?**
- [Edge case 1]: [How you'll test it]
- [Edge case 2]: [How you'll test it]

**Manual testing checklist**:
- [ ] [Test case 1]
- [ ] [Test case 2]
- [ ] [Test case 3]

**Automated tests to add**:
- [ ] [Test 1]: [Description]
- [ ] [Test 2]: [Description]

### 3. Rollback Plan

**If it breaks, how do you undo?**
- [Rollback method 1]: [Steps to revert]
- [Rollback method 2]: [Alternative if first doesn't work]

**Git strategy**:
- [ ] Commit in small chunks
- [ ] Create feature branch
- [ ] Keep original code in comments during development

**Verification before commit**:
- [ ] Tests pass
- [ ] Manual testing successful
- [ ] No console errors
- [ ] Code reviewed (if applicable)

### 4. Success Criteria

**Definition of done**:
- [ ] [Criteria 1]
- [ ] [Criteria 2]
- [ ] [Criteria 3]

**How to verify success**:
- [Verification method 1]
- [Verification method 2]

---

## Execution Log

*(Fill this out as you code)*

### Implementation Steps

| Step | Action | Result | Time |
|------|--------|--------|------|
| 1 | [What you did] | [What happened] | [Duration] |
| 2 | [What you did] | [What happened] | [Duration] |
| 3 | [What you did] | [What happened] | [Duration] |

### Issues Encountered

| Issue | Solution | Time to Fix |
|-------|----------|-------------|
| [Issue 1] | [How you fixed it] | [Duration] |
| [Issue 2] | [How you fixed it] | [Duration] |

### Deviations from Plan

| Original Plan | Actual Change | Reason |
|---------------|---------------|--------|
| [What you planned] | [What you actually did] | [Why] |

---

## Post-Implementation Review

### What Went Well

- [Success 1]
- [Success 2]

### What Could Be Improved

- [Improvement 1]
- [Improvement 2]

### Lessons Learned

- [Lesson 1]: [How to apply next time]
- [Lesson 2]: [How to apply next time]

### STOP Effectiveness

**Total time spent**:
- S-T-O phases: [X minutes]
- Planning (P): [X minutes]
- Implementation: [X minutes]
- Testing/Fixing: [X minutes]
- **Total**: [X minutes]

**Time saved estimate**: [How much time did STOP save you?]

**Would this have gone better/worse without STOP?**
- [ ] Better without STOP (why?)
- [ ] Worse without STOP (why?)

**Will you use STOP again?**
- [ ] Yes
- [ ] No (why?)

---

## Notes

[Any additional notes, thoughts, or observations that didn't fit elsewhere]

---

**STOP Protocol Complete** ✓

**Remember**: The best code you write is the code you didn't have to write because you read it first.
