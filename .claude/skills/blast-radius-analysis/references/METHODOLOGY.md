# Risk Assessment Methodology

Detailed criteria for quantifying and categorizing risk levels in blast radius analysis.

## Risk Level Quantification

### Critical Risk (🔴)

**Criteria** (any of these):
- Called by ≥5 unrelated modules
- Part of public API surface
- In hot path (request handler, main loop)
- Has state dependencies shared across modules
- Breaking changes require system-wide restart

**Examples**:
- `User.authenticate()` - used in auth, sessions, API, admin, tests
- `Database.connect()` - singleton connection pool
- HTTP middleware - processes every request

**Mitigation Strategy**:
- Require code review from multiple teams
- Create feature flag for gradual rollout
- Maintain backward compatibility for ≥1 version
- Update all downstream code in single PR

### High Risk (🟡)

**Criteria** (any of these):
- Called by 2-4 modules
- Internal API used by multiple features
- Moderate complexity (5-10 conditional branches)
- Some state dependencies

**Examples**:
- `EmailService.send()` - used by notifications, password reset, marketing
- `Utils.formatDate()` - helper used by several display components
- Cache layer functions - shared across features

**Mitigation Strategy**:
- Update all direct callers before merging
- Add integration tests for affected paths
- Document breaking changes clearly
- Coordinate with team

### Medium Risk (🟢)

**Criteria** (any of these):
- Called by 1-2 modules
- Self-contained logic
- No shared state
- Pure function or clear side effects

**Examples**:
- `MathUtils.calculatePercentage()` - used by 2 dashboard widgets
- `Validator.validateEmail()` - called by registration form only
- Local helper functions within a module

**Mitigation Strategy**:
- Update direct callers
- Add unit tests
- Standard PR review sufficient

### Low Risk (⚪)

**Criteria**:
- Single caller
- No external dependencies affected
- Pure function
- Well-tested

**Examples**:
- Private methods with single usage
- Dead code (no callers)
- Utility functions in tests

**Mitigation Strategy**:
- Standard PR review
- Consider deleting if unused

## Dependency Depth vs Breadth

### Depth Analysis

```
Depth 0: Target function
Depth 1: Direct callers (immediate impact)
Depth 2: Callers of direct callers (cascading impact)
Depth 3+: Transitive dependencies
```

**Rule**: Each depth level increases risk exponentially.
- Depth 1: 1x risk
- Depth 2: 2x risk (cascading failures)
- Depth 3+: 3x-5x risk (unpredictable interactions)

### Breadth Analysis

```
Breadth = Number of modules at each depth level

Breadth 1: 1-2 modules (low breadth)
Breadth 2: 3-5 modules (medium breadth)
Breadth 3: 6+ modules (high breadth)
```

**Risk Formula**: `Risk = Depth × Breadth × Criticality_Multiplier`

| Criticality | Multiplier |
|-------------|------------|
| Public API  | 3.0        |
| Internal API| 1.5        |
| Private     | 1.0        |

**Example**:
- Function at Depth 2, Breadth 4, Internal API
- Risk = 2 × 4 × 1.5 = **12 (High Risk)**

## Module Coupling Analysis

### Coupling Types

1. **Data Coupling** (Low Risk):
   - Passes primitive data only
   - No knowledge of internal structure

2. **Stamp Coupling** (Medium Risk):
   - Passes complex data structures
   - Partial knowledge of structure

3. **Control Coupling** (High Risk):
   - One module controls logic of another
   - Flags/parameters control flow

4. **Content Coupling** (Critical Risk):
   - Direct access to internal data
   - Modifies internal state
   - Breaks encapsulation

### Cohesion Assessment

**High Cohesion** (Low Risk):
- Related functions grouped together
- Single responsibility
- Changes are localized

**Low Cohesion** (High Risk):
- Unrelated functions in same module
- Multiple responsibilities
- Changes ripple unpredictably

## Quick Risk Calculator

```
Score = (N_Callers × 0.5) + (Depth × 2) + (Breadth × 1.5) + (Public_API × 3) + (Stateful × 2)

Score Interpretation:
0-5:   Low Risk
6-15:  Medium Risk
16-25: High Risk
26+:   Critical Risk
```
