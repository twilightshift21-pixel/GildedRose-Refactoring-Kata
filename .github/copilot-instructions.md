# Gilded Rose Refactoring Kata - Workspace Instructions

## Project Purpose

This is a multi-language refactoring kata designed to practice improving legacy code while maintaining behavior. The exercise involves an inventory management system with complex business logic for different item types (normal items, Aged Brie, Sulfuras, Backstage passes, Conjured items).

**Critical Constraint**: You cannot modify the `Item` class or the `Items` property — these belong to "the goblin in the corner" and are off-limits.

## Repository Structure

```
├── {language}/                 # 50+ language implementations
│   ├── README.md              # Language-specific setup & test commands
│   ├── gilded_rose.(ext)      # Main production code
│   ├── gilded_rose_test.(ext) # Starting unit test (usually failing)
│   ├── texttest_fixture.(ext) # CLI fixture for approval testing
│   └── tests/                 # Test directory (language-dependent)
├── GildedRoseRequirements.md  # Business rules specification
├── texttests/                 # TextTest approval testing framework
└── CONTRIBUTING.md            # Guidelines for adding languages
```

## Business Logic: The Complete Rules

**All Items:**
- Quality ranges: 0-50 (Sulfuras exception: stays at 80)
- Quality degrades by 1 per day normally
- Quality degrades 2x after sell date passes

**Aged Brie:**
- Quality increases (not decreases)
- Increases by 1 per day before sell date
- Increases by 2 per day after sell date

**Sulfuras (Legendary Item):**
- Never changes quality (stays at 80)
- Never needs to be sold (SellIn unchanged)

**Backstage Passes:**
- Quality increases as concert approaches
- Normal: +1 per day
- ≤10 days: +2 per day
- ≤5 days: +3 per day
- After concert (SellIn <= 0): Quality drops to 0

**Conjured Items:**
- Quality degrades 2x as fast as normal items
- Example: Conjured Mana Cake goes -2 per day (or -4 after sell date)

## Development Workflow

### 1. Choosing a Language

The workspace contains setups for:
- **Python**: Simple, clear starting point
- **TypeScript/JavaScript**: Modern, npm-based
- **Java**: Multiple frameworks (JUnit, Cucumber, Spock)
- **C#**: NUnit and xUnit variants
- **Go, Rust, Ruby**: Strong community implementations

Each language's `README.md` contains specific build/test commands.

### 2. Setting Up for Your Language

```bash
cd {language}
# Follow instructions in README.md for that language
```

Common patterns:
- **Python**: `python -m unittest` or `python -m pytest`
- **Node.js**: `npm install && npm test`
- **Java**: `mvn test` or gradle equivalent
- **Go**: `go test ./...`
- **Rust**: `cargo test`

### 3. The Refactoring Process

1. **Run initial tests** to confirm the failing test exists
2. **Write comprehensive tests** covering all item types and edge cases
3. **Refactor incrementally**, running tests after each small change
4. **Use approval testing** (TextTest) as a safety net for behavior

Test Structure Pattern:
- Test normal items (quality decrease, sell date behavior)
- Test Aged Brie (quality increase)
- Test Sulfuras (no change)
- Test Backstage passes (all three quality increase rates)
- Test Conjured items (double degradation)
- Test edge cases (quality bounds, sell date boundaries)

### 4. Approval Testing with TextTest

```bash
# Set up TextTest (Python example)
python texttest_fixture.py 10

# All implementations provide a fixture that outputs item state over N days
# Use this for regression testing and documenting current behavior
```

## Common Implementation Patterns

### Item Quality Update Flow
Most implementations follow this pattern:

```
for each item:
  if special item type:
    apply special logic
  else:
    apply default degradation logic
  ensure quality bounds (0-50) unless Sulfuras
  decrement SellIn
```

### Refactoring Approaches

**Strategy 1: Extract Methods**
- Separate logic for each item type into methods
- Easier to test and maintain

**Strategy 2: Strategy Pattern**
- Create item handler classes
- Polymorphism eliminates if/else chains

**Strategy 3: Functional Approach**
- Pure functions for each item type
- No state mutation

**Strategy 4: Rules Engine**
- Define rules as data structures
- Apply rules in sequence

## Development Guidelines

### Do's ✓
- Add extensive tests before refactoring
- Run tests frequently (after each change)
- Make small, incremental improvements
- Use version control to commit working states
- Test edge cases (quality boundaries, sell date boundaries)
- Document why you chose your refactoring approach

### Don'ts ✗
- Don't modify the `Item` class or `Items` property
- Don't change method signatures without a good reason
- Don't add external dependencies unless genuinely needed
- Don't refactor without tests in place
- Don't ignore failing tests

## Key Files by Language

### Python
- `gilded_rose.py` - Production code
- `tests/` - Test directory
- `texttest_fixture.py` - Approval test fixture
- Run tests: `python -m unittest discover`

### TypeScript/JavaScript
- `src/gilded-rose.ts` or `gilded-rose.js` - Production code
- `test/` - Test files  
- `package.json` - Dependencies and scripts
- Run tests: `npm test`

### Java
- `src/main/java/GildedRose.java` - Production code
- `src/test/java/GildedRoseTest.java` - Tests
- `pom.xml` - Maven configuration
- Run tests: `mvn test`

## Potential Challenges

### 1. Understanding the Quirky Rules
Solution: Read `GildedRoseRequirements.md` carefully, especially the Backstage pass and Sulfuras rules.

### 2. Managing Quality Boundaries
Challenge: Quality bounds vary by item type
Solution: Apply bounds checking at end of each update, with Sulfuras exception

### 3. Testing All Combinations
Challenge: 5+ item types × boundary conditions = many tests needed
Solution: Use parameterized tests or test fixture for each item type + edge cases

### 4. Regression Testing
Challenge: Hard to track behavior changes when refactoring
Solution: Use TextTest approval tests to document current output

## Testing Strategy Recommendations

1. **Unit Tests**: Test each item type individually
2. **Boundary Tests**: Test quality at 0, 50, edge of conditions
3. **Time-based Tests**: Test around sell date (SellIn = 0, transitive states)
4. **Approval Tests**: Compare before/after refactoring with TextTest

Example test cases:
- Normal item with quality 10, SellIn 5 → expect quality 9, SellIn 4
- Aged Brie with quality 49, SellIn 1 → after SellIn=0, quality should increase by 2
- Backstage pass with SellIn 11 → +1 quality, SellIn 6 → +2 quality, SellIn 5 → on boundary between +2 and +3
- Sulfuras with any values → should never change

## Resources

- [Gilded Rose Requirements](../GildedRoseRequirements.md) - Complete specification
- [TextTest Setup](../texttests/README.md) - Approval testing guide
- [Contributing Guide](../CONTRIBUTING.md) - Standards for new language versions
- Original kata: http://iamnotmyself.com/refactor-this-the-gilded-rose-kata/ (via Wayback Machine)

## Quick Command Reference

| Language | Setup | Test | Watch |
|----------|-------|------|-------|
| Python | `pip install -r requirements.txt` | `python -m unittest` | N/A |
| TypeScript | `npm install` | `npm test` | `npm run test:watch` |
| JavaScript | `npm install` | `npm test` | `npm run test:watch` |
| Java (Maven) | `mvn clean install` | `mvn test` | `mvn test -Dtest=...` |
| Go | `go mod tidy` | `go test ./...` | `go test -v ./...` |
| Rust | `cargo build` | `cargo test` | `cargo watch -x test` |
| Ruby | `bundle install` | `bundle exec rspec` | `bundle exec rspec --watch` |

---

**Last Updated**: March 2026 | Multi-language refactoring kata for legacy code practice