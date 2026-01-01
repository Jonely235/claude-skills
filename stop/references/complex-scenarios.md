# Complex Scenarios for STOP Protocol

This reference covers advanced scenarios where the basic STOP protocol needs adaptation or additional strategies.

## Scenarios Covered

1. [Large Codebases (>100k lines)](#large-codebases)
2. [Legacy Code with No Tests](#legacy-code-no-tests)
3. [Microservices/Distributed Systems](#microservices)
4. [Multiple Valid Approaches](#multiple-approaches)
5. [Emergency/Hotfix Situations](#emergency-hotfix)
6. [Foreign/Unfamiliar Codebase](#foreign-codebase)
7. [Performance Optimization](#performance-optimization)

---

## Large Codebases (>100k lines)

### Challenge

Too many files, overwhelming amount of code, don't know where to start.

### STOP Adaptation

**S - Stop**: Don't try to understand everything. Focus on the relevant slice.

**T - Trace (Strategic Scoping)**:

1. **Start from the entry point**
   ```bash
   # User-facing: Find the route/endpoint
   Grep: "router\.(get|post)" glob:**/routes/**/*
   Grep: "@app\.route.*user" glob:**/*.{py,ts,js}

   # Library: Find the public API
   Glob: **/index.{ts,js,py}
   Glob: **/api/**/*
   ```

2. **Trace downward, not outward**
   ```bash
   # Follow the call stack DOWN into implementation
   LSP: outgoingCalls on the entry point function
   Read: the immediate dependencies only

   # Don't: Read all sibling files
   # Do: Read only files in the call chain
   ```

3. **Use domain boundaries**
   ```bash
   # Find domain-specific directories
   Glob: **/payment/**/*
   Glob: **/user/**/*
   Glob: **/auth/**/*

   # Work within one domain at a time
   ```

**O - Orient**: Draw a mini-map of just the relevant slice.

```
┌─────────────────────────────────────┐
│  Your Change Scope (10 files)       │
├─────────────────────────────────────┤
│  routes/user.ts                     │
│    ↓                                │
│  controllers/userController.ts      │
│    ↓                                │
│  services/userService.ts            │
│    ↓                                │
│  models/user.ts                     │
└─────────────────────────────────────┘

      (Ignore the other 9,990 files)
```

**P - Plan**: Focus changes on the identified slice.

### Example

**Task**: "Add email confirmation to user registration"

**Bad approach**: Try to understand the entire authentication system (3 days).

**STOP approach**:
```bash
# 1. Find registration endpoint
Grep: "register|signup" -i glob:**/routes/**/*

# 2. Read registration handler
Read: src/routes/auth.ts
# Found: registerUser() controller

# 3. Trace just this flow
LSP: outgoingCalls on registerUser()
# Calls: validateUser(), createUser(), sendWelcomeEmail()

# 4. Focus on email service
Read: src/services/email.ts
# Found: sendEmail() function pattern

# 5. Plan
# - Add sendConfirmationEmail() using existing email pattern
# - Call it after createUser()
# - Add confirmEmail endpoint
```

**Time**: 2 hours (vs 3 days for full understanding).

---

## Legacy Code with No Tests

### Challenge

No tests to show expected behavior, code is unclear, afraid to break things.

### STOP Adaptation

**S - Stop**: Accept that you won't fully understand everything. Focus on risk containment.

**T - Trace (Archaeology Mode)**:

1. **Find the business logic**
   ```bash
   # Look for the "meat" of the code
   Grep: "if.*else|for|while|switch" glob:**/legacy/**/*

   # Find data transformations
   Grep: "\.map\(|\.filter\(|\.reduce\(" glob:**/legacy/**/*
   ```

2. **Find the data flow**
   ```bash
   # Trace where data comes from
   Grep: "SELECT|INSERT|UPDATE|db\.|query\(" glob:**/legacy/**/*

   # Trace where data goes
   Grep: "return|res\.|response\." glob:**/legacy/**/*
   ```

3. **Look for comments and TODOs**
   ```bash
   # Sometimes there are clues
   Grep: "//|// TODO|// FIXME|// HACK" glob:**/legacy/**/* -C:2
   ```

4. **Search for related files**
   ```bash
   # Find database schema
   Glob: **/schema*.sql **/migrations/**/*

   # Find documentation
   Glob: **/*.md **/docs/**/*
   ```

**O - Orient**: Identify risks.

```
High Risk Areas:
- Direct database queries (can't easily test)
- Global state (hard to predict)
- No input validation (security risk)
- Complex conditionals (business logic)

Low Risk Areas:
- Pure functions (input → output)
- Formatting/presentation code
- Logging/metrics code
```

**P - Plan (Containment Strategy)**:

1. **Add characterization tests first**
   ```bash
   # Before changing anything, add tests that capture current behavior
   # Even if the behavior is wrong, tests prevent regression
   ```

2. **Create a safety net**
   ```bash
   # Add extensive logging around the change
   # Add feature flag to disable if needed
   # Plan rollback procedure
   ```

3. **Make smallest possible change**
   ```bash
   # Don't refactor, just add the new feature
   # Leave ugly code alone if it works
   # "When in doubt, do nothing"
   ```

### Example

**Task**: "Fix: Legacy user export is broken"

**Bad approach**: Rewrite the export system (2 weeks, high risk).

**STOP approach**:
```bash
# 1. Find the export code
Grep: "export.*user|user.*export" -i glob:**/legacy/**

# 2. Read the legacy export function
Read: src/legacy/exportUsers.js
# Found: 500-line function, no tests, unclear logic

# 3. Trace data flow
# - Reads from MySQL
# - Transforms data
# - Writes to CSV file
# - Has error handling but unclear

# 4. Look for clues
Grep: "//.*export|TODO.*export" -C:3
# Found comment: "FIXME: export fails for users with special chars"

# 5. Plan (containment)
# - DON'T rewrite the function
# - Add logging to understand the failure
# - Fix only the specific issue (special chars)
# - Add test to prevent regression
# - Leave rest of ugly code alone
```

**Time**: 3 hours (vs 2 weeks for rewrite).

---

## Microservices/Distributed Systems

### Challenge

Code is split across multiple repositories/services, hard to understand the full flow.

### STOP Adaptation

**S - Stop**: Identify which service(s) are relevant to your change.

**T - Trace (Service Boundary Mapping)**:

1. **Map the service topology**
   ```bash
   # Find service definitions
   Glob: **/docker-compose*.yml
   Glob: **/kubernetes/**/*
   Glob: **/services/**/*

   # Find API gateways/routers
   Glob: **/gateway/**/*
   Glob: **/api-gateway/**/*
   ```

2. **Trace inter-service communication**
   ```bash
   # Find HTTP calls to other services
   Grep: "fetch\(|axios\.|http\.|request\(" glob:**/*.{ts,js}

   # Find message queue calls
   Grep: "publish|subscribe|emit|send.*queue" glob:**/*.{ts,js}

   # Find gRPC calls
   Grep: "grpc|\.call\(|rpc\(" glob:**/*.{ts,js}
   ```

3. **Find service ownership**
   ```bash
   # Look for service-specific patterns
   Glob: **/package.json **/composer.json
   # Check service names in configs

   # Find API definitions
   Glob: **/openapi.yaml **/swagger.yaml **/api-spec.yaml
   ```

**O - Orient**: Draw the service interaction diagram.

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Frontend    │ ──→  │ API Gateway  │ ──→  │ User Service │
└──────────────┘      └──────────────┘      └──────────────┘
                             │                      │
                             ↓                      ↓
                      ┌──────────────┐      ┌──────────────┐
                      │ Auth Service │      │   Database   │
                      └──────────────┘      └──────────────┘

Your change: Add email confirmation
Affected services: User Service + Email Service (new)
```

**P - Plan**: Consider cross-service impacts.

```
Questions:
1. Which service owns the data? (User Service)
2. Which service sends emails? (Need to check/create)
3. What's the communication protocol? (REST? Queue? gRPC?)
4. What happens if email service is down? (Need retry logic)
5. Do we need to update API gateway? (Maybe new endpoint)
```

### Example

**Task**: "Add user email verification across microservices"

**STOP approach**:
```bash
# 1. Find user service
Glob: **/user-service/**/*

# 2. Check if email service exists
Glob: **/email-service/**/* **/notification-service/**/*
# Found: notification-service exists

# 3. Understand current flow
Read: services/user-service/src/routes.ts
# User registration currently returns 200 immediately

# 4. Check how services communicate
Grep: "axios|fetch|http" glob:services/user-service/**/*
# Found: Services use HTTP client library

# 5. Check notification service API
Read: services/notification-service/routes.ts
# Has /send-email endpoint

# 6. Plan cross-service change
# User Service:
#   - Add "email_verified" flag to user model
#   - On registration: generate token, call notification service
#   - Add /verify-email endpoint
# Notification Service:
#   - Already has send-email, just use it
#   - Add email template for verification
# API Gateway:
#   - No changes needed (internal communication)
```

**Key insight**: Existing notification service can be reused, no new service needed.

---

## Multiple Valid Approaches

### Challenge

There are several ways to solve the problem, and it's unclear which is best.

### STOP Adaptation

**S - Stop**: Don't pick an approach yet. First understand the options.

**T - Trace (Comparative Analysis)**:

1. **Find existing patterns in the codebase**
   ```bash
   # How are similar problems currently solved?
   Grep: "similar.*function|pattern.*like" -i

   # Search for the different approaches
   # Example: State management
   Grep: "useState|useReducer|Context|Redux" glob:**/*.{tsx,ts}
   ```

2. **Find precedents**
   ```bash
   # Look for recent similar changes
   # Check git history for similar features
   # Read PR discussions for architectural decisions
   ```

3. **Understand trade-offs**
   ```bash
   # For each approach, trace:
   - Complexity: How hard to implement?
   - Maintainability: How easy to understand?
   - Performance: Does it scale?
   - Testability: Can we test it?
   - Compatibility: Does it fit existing architecture?
   ```

**O - Orient**: Create a decision matrix.

```
Approach              | Complexity | Maintainability | Performance | Fit
----------------------|------------|-----------------|-------------|-------
1. Add to existing    | Low        | High            | Medium      | ★★★
2. Create new service | High       | Medium          | High        | ★★
3. Use library        | Low        | Low             | High        | ★
```

**P - Plan**: Use AskUserQuestion to decide.

```bash
# When multiple valid approaches exist, ask the user:
# - Which approach do you prefer?
# - What are your priorities? (Speed vs maintainability vs performance)
# - Are there constraints I should know about?
```

### Example

**Task**: "Add real-time notifications"

**Possible approaches**:
1. WebSocket (direct connection)
2. Server-Sent Events (SSE)
3. Polling (simplest)
4. Use third-party service (Pusher, Firebase)

**STOP approach**:
```bash
# 1. Check existing patterns
Grep: "websocket|sse|polling|socket\.io" -i
# No existing real-time features

# 2. Check infrastructure
Glob: **/nginx.conf **/docker-compose.yml
# Found: Single server, no load balancer

# 3. Check requirements
# Read the ticket/requirement
# - Need real-time for < 1000 users
# - Messages should appear within 1 second
# - Budget constrained

# 4. Decision matrix
Approach   | Setup | Scaling | Cost | Fit
-----------|-------|---------|------|-----
WebSocket  | Hard  | Complex | Low  | ★
SSE        | Easy  | Medium  | Low  | ★★★
Polling    | Trivial| Poor   | Medium| ★
Pusher     | Easy  | Auto    | High | ★

# 5. Plan
# Recommend SSE: Simple, fits infrastructure, meets requirements
# If user wants different trade-offs, use their preference
```

---

## Emergency/Hotfix Situations

### Challenge

Production is broken, need to fix NOW, no time for thorough analysis.

### STOP Adaptation

**S - Stop**: Take 30 seconds (not 5-10 minutes).

**T - Trace (Emergency Mode - Focused Investigation)**:

1. **Find the error**
   ```bash
   # Search for error logs/stack traces
   Grep: "ERROR|Exception|TypeError" -C:5

   # Find recent changes
   # Check git log for recent commits
   # Check deployment logs
   ```

2. **Trace only the broken path**
   ```bash
   # Don't understand the whole system
   # Just trace the specific error path
   Read: the file mentioned in stack trace
   LSP: incomingCalls on the broken function
   ```

3. **Find what changed**
   ```bash
   # Git diff recent changes
   # Compare with last known good version
   ```

**O - Orient**: Identify the quickest fix.

```
Options (fastest to slowest):
1. Revert last commit (1 minute)
2. Hotfix the specific line (5 minutes)
3. Add defensive check (10 minutes)
4. Proper fix (hours - do this after emergency)
```

**P - Plan**: Fix → Test → Deploy → Document.

```
Emergency Plan:
1. Fix the immediate issue (revert or hotfix)
2. Add test to prevent regression
3. Deploy hotfix
4. AFTER emergency: Plan proper fix using full STOP protocol
```

### Example

**Task**: "PRODUCTION DOWN: 500 errors on user profile"

**STOP (Emergency Mode)**:
```bash
# 1. Find the error
Grep: "500|ERROR.*profile" -C:5
# Found: TypeError in src/user/profile.ts:45

# 2. Read the broken code
Read: src/user/profile.ts offset:40 limit:10
# Line 45: user.name.toLowerCase()
# Error: user.name is null

# 3. Find what changed
git log --oneline -10
# Recent commit: "Add user profile optimization"
git show HEAD --stat
# Changed: src/user/profile.ts

# 4. Quick decision
# Option A: Revert commit (1 minute, safe)
# Option B: Add null check (5 minutes, risk of other issues)
# Decision: REVERT (safest in emergency)

# 5. Plan
# Now: Revert commit, deploy
# Later: Fix the null check properly with full STOP + tests
```

**Time**: 5 minutes (vs 1 hour for "proper fix" in emergency).

---

## Foreign/Unfamiliar Codebase

### Challenge

First time working with this codebase, don't understand the architecture or conventions.

### STOP Adaptation

**S - Stop**: Acknowledge what you don't know.

**T - Trace (Learning Mode)**:

1. **Start with project documentation**
   ```bash
   # Read the README
   Read: README.md

   # Find architecture docs
   Glob: **/docs/**/*.{md,txt}

   # Find setup/development docs
   Glob: **/{CONTRIBUTING,DEVELOPMENT,DEVELOPER}.md
   ```

2. **Understand the project structure**
   ```bash
   # Look at directory structure
   Bash: ls -la

   # Find the main entry points
   Glob: **/index.{ts,js,py,go,java}
   Glob: **/main.{ts,js,py,go,java}
   Glob: **/app.{ts,js,py,go,java}

   # Find package/dependency info
   Read: package.json / requirements.txt / go.mod / pom.xml
   ```

3. **Learn the conventions**
   ```bash
   # Find existing implementations of common patterns
   # How do they handle errors?
   Grep: "try.*catch|throw new" -C:2

   # How do they structure API responses?
   Grep: "return.*res\.|response\." -C:2

   # How do they name things?
   Glob: **/*controller* **/*service* **/*model*
   ```

4. **Find examples**
   ```bash
   # Find test files (they show how code is used)
   Glob: **/*.test.{ts,js,py}

   # Read a simple test to understand the pattern
   Read: tests/simple-example.test.ts
   ```

**O - Orient**: Create a mental model of the codebase.

```
Project Structure:
├── src/
│   ├── controllers/  (Request handlers)
│   ├── services/     (Business logic)
│   ├── models/       (Data models)
│   ├── middleware/   (Auth, validation, logging)
│   └── utils/        (Helper functions)
├── tests/            (Test files)
└── docs/             (Documentation)

Conventions observed:
- Controllers are thin, just call services
- Services contain business logic
- All errors go through error middleware
- Async functions use try-catch
- Functions use camelCase
```

**P - Plan**: Follow conventions, don't introduce new patterns.

### Example

**Task**: "Add password reset (first time in this codebase)"

**STOP (Learning Mode)**:
```bash
# 1. Read project docs
Read: README.md
Read: docs/ARCHITECTURE.md
# Learned: MVC architecture, Express + TypeScript

# 2. Understand existing patterns
Read: src/controllers/authController.ts
# Pattern: Controller validates input, calls service, returns response

Read: src/services/authService.ts
# Pattern: Service contains logic, uses models

# 3. Find similar feature (email confirmation)
Read: src/services/emailService.ts
# Pattern: Uses Nodemailer, has sendEmail() function

# 4. Plan (following conventions)
# - Create resetPassword() in authService (follows existing pattern)
# - Create POST /reset-password route in authRoutes (follows existing pattern)
# - Use existing emailService for sending emails (reuse, don't create new)
# - Add tests following pattern from tests/auth.test.ts
```

**Result**: Feature fits seamlessly into existing architecture.

---

## Performance Optimization

### Challenge

Need to optimize performance, but don't know where the bottleneck is.

### STOP Adaptation

**S - Stop**: Don't optimize anything until you measure.

**T - Trace (Profiling Mode)**:

1. **Find the suspected slow code**
   ```bash
   # Search for database queries
   Grep: "SELECT|INSERT|UPDATE|db\.|query\(" -C:3

   # Search for loops
   Grep: "for\s*\(.*\{|while\s*\(.*\{|\.forEach\(" -C:2

   # Search for expensive operations
   Grep: "JSON\.parse|JSON\.stringify|deepCopy|clone" -C:2
   ```

2. **Find N+1 query problems**
   ```bash
   # Look for queries inside loops
   Grep: "for.*{.*db\.|while.*{.*query\(" -A:10

   # Look for ORM calls inside loops
   Grep: "forEach.*{.*\.find\(|forEach.*{.*\.save\(" -A:5
   ```

3. **Find caching opportunities**
   ```bash
   # Search for repeated expensive calls
   Grep: "getUser|getConfig|fetchData"

   # Check if caching is already used
   Grep: "cache|redis|memcached" -i
   ```

**O - Orient**: Profile before optimizing.

```
Measurement Tools:
- Database: EXPLAIN query plans
- Application: Add timing logs
- Network: Browser DevTools / curl with timing
- Memory: Heap profilers

Rules:
1. Measure first
2. Find the actual bottleneck (not what you assume)
3. Optimize the bottleneck, not everything
4. Measure after to confirm improvement
```

**P - Plan**: Optimize based on data, not guesses.

### Example

**Task**: "Optimize slow user profile loading"

**Bad approach**: Cache everything without measuring (might not help).

**STOP approach**:
```bash
# 1. Find the code
Grep: "profile|getUserProfile" -i glob:**/*.{ts,js}

# 2. Read the profile endpoint
Read: src/api/users/profile.ts

# 3. Add timing logs (before optimizing!)
console.time('profileLoad');
// ... existing code ...
console.timeEnd('profileLoad');
# Result: 2500ms

# 4. Measure each operation
console.time('dbQuery');
const user = await db.findUser(id);
console.timeEnd('dbQuery');
# Result: 2300ms (this is the bottleneck!)

# 5. Investigate database query
# Add EXPLAIN
EXPLAIN SELECT * FROM users WHERE id = ?;
# Result: Full table scan, no index on id

# 6. Plan optimization
# - Add index on users.id (fixes root cause)
# - NOT: Cache the result (band-aid)
# - NOT: Use different database (overkill)

# 7. After optimization: 45ms (55x faster)
```

**Key insight**: Measurement revealed the real bottleneck, avoiding wasted effort.

---

## Summary: Adapting STOP to Complexity

| Scenario | Key Adaptation | Time Investment |
|----------|----------------|-----------------|
| Large codebase | Scope to relevant slice, ignore rest | 10-15 min |
| Legacy code no tests | Risk containment, characterization tests | 15-20 min |
| Microservices | Map service boundaries, trace communication | 15-20 min |
| Multiple approaches | Comparative analysis, decision matrix | 10-15 min |
| Emergency/hotfix | Focused 30s investigation, revert first | 1-5 min |
| Foreign codebase | Learn conventions first, follow patterns | 20-30 min |
| Performance | Measure before optimizing, profile first | 15-30 min |

**Core Principle**: STOP saves time in ALL scenarios, but the execution adapts to context.

---

**Remember**: Even in complex scenarios, the fundamental rule holds: **Read before you write.** The more complex the situation, the more you need STOP.
