# Analysis Patterns for Blast Radius

This document contains advanced patterns for complex impact analysis scenarios.

## Pattern 1: Multi-File Refactoring

When refactoring spans multiple files, analyze cross-file dependencies:

```
1. Map all files that import/reference the target module
2. For each file, identify specific functions using the target
3. Check for:
   - Type dependencies (interfaces, types)
   - Runtime dependencies (dynamic imports, reflection)
   - Test files that may mock or stub the target
```

**Example output**:
```
Cross-File Impact Analysis: `UserService.authenticate()`

Affected Files (5):
- src/controllers/auth.ts:45 - Direct call in login endpoint
- src/middleware/auth.ts:12 - Validates tokens
- tests/unit/auth.test.ts:78 - Mocked in tests
- src/admin/user-mgmt.ts:134 - Used in admin panel
- src/api/routes.ts:23 - Route handler references
```

## Pattern 2: Breaking Circular Dependencies

When changes might break circular dependencies:

```
1. Identify all modules in the circular chain
2. Mark which direction each dependency flows
3. Determine the "entry point" of the cycle
4. Assess if changes break the cycle
```

**Cycle detection**:
- Module A → Module B → Module C → Module A
- Breaking any link affects ALL modules in the cycle
- Risk level: CRITICAL for all modules

## Pattern 3: API Contract Changes

For public API modifications:

```
1. Search for all external references:
   - OpenAPI/swagger specs
   - Client SDKs
   - Documentation examples
   - Integration tests

2. Classify by breaking change type:
   - Parameter removal: CRITICAL
   - Return type change: HIGH
   - Parameter addition (optional): LOW
   - Behavior change: VARIES
```

**Risk Matrix**:
```
              | Backward Compatible | Breaking Change
--------------|---------------------|-----------------
Internal      | Low Risk            | Medium Risk
Public API    | Low Risk            | Critical Risk
Versioned API | Low Risk            | High Risk
```

## Pattern 4: Database Schema Changes

For database model modifications:

```
1. Find all ORM/Query Builder references
2. Identify migration scripts
3. Check for:
   - Raw SQL queries (string-based, hard to detect)
   - Eager loading relationships
   - Index dependencies
   - Foreign key constraints
```

## Pattern 5: Configuration Changes

When modifying configuration keys:

```
1. Search config file usage:
   - .env files
   - config/*.yml, config/*.json
   - Feature flags

2. Find runtime access:
   - config.get(), process.env, os.Getenv

3. Check default values:
   - Hardcoded defaults vs. required configs
```
