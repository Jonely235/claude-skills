# Tool Patterns for the TRACE Phase

This reference provides detailed patterns for using Glob, Grep, Read, and LSP tools during the **T - Trace** phase of the STOP protocol.

## Core Tools

### 1. Glob - Finding Files by Pattern

**When to use**: You need to find files related to a feature, component, or domain.

**Common Patterns**:

```bash
# Find all files related to authentication
**/*auth*.{ts,js,tsx,jsx}
**/auth/**/*
**/*login* **/*register* **/*session*

# Find test files
**/*.test.{ts,js}
**/*.spec.{ts,js}
**/tests/**/*
**/__tests__/**/*

# Find configuration files
**/*config*.{json,yaml,yml,ts,js}
**/.*rc*

# Find component files
**/components/**/*
**/*.{component,cmp}.{tsx,jsx,ts,js}

# Find API/route files
**/api/**/*
**/routes/**/*
**/controllers/**/*
```

**Tips**:
- Start broad (`**/*keyword*`), then narrow
- Use multiple extensions: `**/*.{ts,tsx,js,jsx}`
- Combine patterns: `**/(user|profile|account)/*`
- Search directories: `**/domain/**/*` is faster than `**/*domain*`

**Examples**:

```bash
# Task: "Add logout functionality"
Glob: **/*session* **/*login* **/*auth*

# Task: "Fix validation bug"
Glob: **/*valid* **/*schema* **/middleware/**/*

# Task: "Update payment flow"
Glob: **/payment/**/* **/checkout/**/* **/stripe/**/*
```

---

### 2. Grep - Searching Code Content

**When to use**: You need to find specific code patterns, function names, or understand how something is implemented.

**Search Strategies**:

#### A. Find Function Implementations

```bash
# Find exact function name
Grep: "function handleLogin"
Grep: "const handleLogin"
Grep: "handleLogin.*=.*\("

# Find class methods
Grep: "class.*AuthController"
Grep: "authenticate\("

# Find error handling
Grep: "throw.*AuthError"
Grep: "catch.*Error"
```

#### B. Find Usage Patterns

```bash
# Find who calls a function (incoming calls)
Grep: "handleLogin\("

# Find imports/requires
Grep: "from.*auth"
Grep: "require.*auth"

# Find API endpoints
Grep: "router\.(get|post|put|delete)"
Grep: "@app\.route"
Grep: "app\.(get|post|put|delete)"
```

#### C. Find Configuration/Constants

```bash
# Find environment variable usage
Grep: "process\.env\."
Grep: "getenv\("
Grep: "os\.getenv"

# Find constants
Grep: "const.*=.*\".*\""
Grep: "MAX_.*MIN_.*DEFAULT_"

# Find database queries
Grep: "SELECT.*FROM"
Grep: "db\.(query|find)"
Grep: "\.find\("
```

#### D. Find Similar Implementations

```bash
# Find similar CRUD operations
Grep: "createUser|deleteUser|updateUser"

# Find all error handling patterns
Grep: "try.*catch"
Grep: "\.catch\("

# Find all middleware
Grep: "middleware|use\(|app\.use"
```

**Grep Options**:

- `-i`: Case insensitive: `Grep: "login" -i`
- `glob`: Filter files: `Grep: "login" glob:**/*.{ts,js}`
- `-C`: Context lines: `Grep: "login" -C:3` (3 lines before/after)
- `output_mode`: Control output
  - `files_with_matches` (default): List matching files
  - `content`: Show matching lines
  - `count`: Count matches per file

**Examples**:

```bash
# Task: "Add logout" - Find how login works
Grep: "handleLogin|loginUser|authenticate" glob:**/*.{ts,js}

# Task: "Fix validation bug" - Find all validation
Grep: "validate|validation|schema" glob:**/*.{ts,js} -i

# Task: "Update payment flow" - Find payment processing
Grep: "payment|stripe|checkout" -C:5
```

---

### 3. Read - Reading File Contents

**When to use**: You found relevant files via Glob/Grep and need to understand the actual implementation.

**Reading Strategy**:

#### A. Read Full File (default)

```bash
Read: src/auth/login.ts
```

**When**: Small-medium files (<500 lines), need complete context

#### B. Read Section (offset + limit)

```bash
# Read specific lines
Read: src/auth/login.ts offset:100 limit:50
```

**When**: Large files, only need specific function

**Tips**:
- Don't skim—actually read the code
- Understand WHY, not just WHAT
- Look for patterns you should follow
- Note dependencies and imports
- Check error handling approach
- Identify edge cases handled

**What to Look For**:

1. **Structure**: How is code organized?
2. **Patterns**: What conventions are used?
3. **Dependencies**: What does this code depend on?
4. **Error handling**: How are errors managed?
5. **Edge cases**: What special cases are handled?
6. **Testing**: How is this tested?

---

### 4. LSP - Language Server Protocol

**When to use**: You need to trace call hierarchies and understand dependencies.

**Operations**:

#### A. incomingCalls - Who Calls This?

```bash
LSP: incomingCalls
  filePath: src/auth/login.ts
  line: 42
  character: 15
```

**Use when**: You want to know what breaks if you change this function.

**Example**:
```
Task: "Refactor authenticate()"
1. Find authenticate() in src/auth/login.ts:42
2. Run incomingCalls
3. See it's called by:
   - src/api/routes/auth.ts:15
   - src/middleware/auth.ts:8
   - src/tests/login.test.ts:23
4. Know: Changing authenticate() affects these 3 places
```

#### B. outgoingCalls - What Does This Call?

```bash
LSP: outgoingCalls
  filePath: src/auth/login.ts
  line: 42
  character: 15
```

**Use when**: You want to understand what this function depends on.

**Example**:
```
Task: "Understand login flow"
1. Find authenticate() in src/auth/login.ts:42
2. Run outgoingCalls
3. See it calls:
   - validateUser() (local)
   - db.users.find() (external)
   - session.create() (external)
4. Know: authenticate() depends on database + session service
```

#### C. goToDefinition - Find Where Something is Defined

```bash
LSP: goToDefinition
  filePath: src/api/routes/auth.ts
  line: 15
  character: 10
```

**Use when**: You see a function/variable call and need to jump to its definition.

#### D. findReferences - Find All Uses

```bash
LSP: findReferences
  filePath: src/auth/login.ts
  line: 42
  character: 15
```

**Use when**: You need to know everywhere a function/variable is used.

**Tips**:
- Requires LSP server configured for your language
- Line/column are 1-indexed (first line = 1, first char = 1)
- More accurate than Grep for finding references (understands scope)

---

## Typical TRACE Workflows

### Workflow 1: Understanding an Existing Feature

**Task**: "Add logout functionality"

**Step 1**: Find related files
```bash
Glob: **/*login* **/*session* **/*auth*
```

**Step 2**: Find login implementation
```bash
Grep: "handleLogin|loginUser" glob:**/*.{ts,js}
```

**Step 3**: Read the code
```bash
Read: src/auth/login.ts
```

**Step 4**: Understand dependencies
```bash
LSP: incomingCalls on handleLogin()
LSP: outgoingCalls on handleLogin()
```

**Result**: You now know:
- How login works
- How sessions are managed
- What pattern to follow for logout
- What will be affected by adding logout

---

### Workflow 2: Debugging a Bug

**Task**: "Fix: User can't update profile"

**Step 1**: Find profile update code
```bash
Glob: **/*profile* **/*user*
Grep: "updateProfile|update.*user" -i
```

**Step 2**: Read the update function
```bash
Read: src/api/users/update.ts
```

**Step 3**: Find validation middleware
```bash
Grep: "validation|validate" glob:**/middleware/**/*
Read: src/middleware/validation.ts
```

**Step 4**: Trace the flow
```bash
LSP: incomingCalls on updateProfile()
LSP: outgoingCalls on updateProfile()
```

**Result**: You discover the validation is too strict, blocking valid updates.

---

### Workflow 3: Finding Similar Patterns

**Task**: "Implement user deletion"

**Step 1**: Find similar CRUD operations
```bash
Grep: "createUser|delete.*|update.*User" glob:**/*.{ts,js}
```

**Step 2**: Read existing implementations
```bash
Read: src/api/users/create.ts
Read: src/api/users/update.ts
```

**Step 3**: Identify the pattern
```bash
# Notice all CRUD functions follow pattern:
# 1. Validate input
# 2. Check permissions
# 3. Execute operation
# 4. Handle errors
# 5. Return response
```

**Result**: Implement deleteUser() following the established pattern.

---

### Workflow 4: Large Codebase Navigation

**Task**: "Understand payment processing"

**Step 1**: Find payment domain
```bash
Glob: **/payment/**/* **/checkout/**/*
```

**Step 2**: Identify entry points
```bash
Grep: "router\.(get|post)" glob:**/payment/**
```

**Step 3**: Trace flow from top
```bash
Read: src/api/payment/routes.ts
LSP: outgoingCalls on payment endpoint
```

**Step 4**: Deep-dive as needed
```bash
Read: src/services/payment/processor.ts
LSP: incomingCalls to understand what uses it
```

**Result**: Map the complete payment flow from API to service to external API.

---

## Pro Tips

### 1. Start Broad, Then Narrow

```bash
# Too specific (might miss files)
Glob: **/auth/login.ts

# Better (find everything, then filter)
Glob: **/*login* **/*auth*
```

### 2. Use Multiple Tools Together

```bash
# Find files
Glob: **/*payment*

# Search within those files
Grep: "stripe|checkout" glob:**/*payment*

# Read the relevant file
Read: src/payment/processor.ts

# Trace dependencies
LSP: outgoingCalls on processPayment()
```

### 3. Search for Concepts, Not Just Names

```bash
# Instead of searching for "authenticate"
Grep: "login|signin|auth|session" -i

# Instead of searching for "validate"
Grep: "check.*input|verify|validate|schema" -i
```

### 4. Look for Tests

```bash
# Tests show how code is supposed to be used
Glob: **/*.test.{ts,js} **/*.spec.{ts,js}

# Search for test cases
Grep: "describe.*login|it.*login" glob:**/*.test.ts
```

### 5. Follow the Error Trail

```bash
# Find error definitions
Grep: "class.*Error|throw new"

# Find error handling
Grep: "catch.*Error|\.catch\("

# Understand error types
Grep: "AuthError|ValidationError"
```

---

## Tool Selection Guide

| Goal | Best Tool | Why |
|------|-----------|-----|
| Find related files | Glob | Fast pattern matching across filenames |
| Find function usage | Grep | Search code content for patterns |
| Understand implementation | Read | See the actual code |
| Trace call hierarchy | LSP incomingCalls | See what depends on this |
| Understand dependencies | LSP outgoingCalls | See what this depends on |
| Find definition | LSP goToDefinition | Jump to where symbol is defined |
| Find all references | LSP findReferences | Find all uses (scope-aware) |
| Quick pattern scan | Grep | Fast, works without LSP |
| Deep investigation | All tools | Combine for complete picture |

---

## Common Pitfalls

### ❌ Don't: Search Too Specifically

```bash
# You might miss the file
Grep: "handleUserLogin"
```

### ✅ Do: Search Broadly

```bash
# You'll find it even if named differently
Grep: "login|signin|auth" -i
```

---

### ❌ Don't: Only Read One File

```bash
Read: src/auth/login.ts
# "I understand it now!" (No, you don't)
```

### ✅ Do: Trace Dependencies

```bash
Read: src/auth/login.ts
LSP: outgoingCalls on handleLogin()
Read: src/utils/session.ts
LSP: incomingCalls on handleLogin()
Read: src/api/routes/auth.ts
```

---

### ❌ Don't: Assume Without Verification

```bash
# "This function must be called by the controller"
# (But you didn't check)
```

### ✅ Do: Verify With Tools

```bash
LSP: incomingCalls on handleLogin()
# Now you KNOW who calls it
```

---

## Quick Reference

```bash
# Find files
Glob: **/*keyword*

# Search code
Grep: "pattern" glob:**/*.{ext} -C:3

# Read file
Read: path/to/file.ts

# Trace calls
LSP: incomingCalls filePath:path line:1 character:1
LSP: outgoingCalls filePath:path line:1 character:1
LSP: goToDefinition filePath:path line:1 character:1
LSP: findReferences filePath:path line:1 character:1
```

---

**Remember**: The TRACE phase is about understanding before acting. These tools are your eyes—use them to see the codebase clearly before you touch it.
