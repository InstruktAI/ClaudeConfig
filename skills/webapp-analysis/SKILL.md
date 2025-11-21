---
name: Web Application Analysis
description: Comprehensive analysis for local web projects and live websites. Identifies improvement opportunities, captures design systems and visual aesthetics for revamping/modernizing, and audits architecture, performance, accessibility, SEO, and code quality. Use when analyzing projects, examining codebases, auditing websites, planning redesigns, or modernizing web applications.
---

# Web Application Analysis

## Instructions

This skill performs comprehensive analysis of web projects (local codebases) and live websites to identify improvement opportunities across all facets.

### Analysis Types

**Local Projects**: Analyze codebase structure, architecture, code quality, dependencies, testing infrastructure, and deployment configuration.

**Live Websites**:
- **Redesign/Modernization**: Capture visual design (colors, typography, layout), content and messaging, images and assets - everything users see to inform building a new site
- **Technical Audit**: Identify user-facing issues like accessibility gaps or critical errors (not implementation details)

### Workflow

#### For Local Projects

1. **Determine project root and type**:
   - Identify package manager files (package.json, pyproject.toml, etc.)
   - Determine framework/stack from configuration
   - Locate source and test directories

2. **Launch parallel analysis agents**:

   Execute all five agents concurrently using the Task tool:

   - **Architecture Explorer** (`subagent_type: Explore`, `thoroughness: medium`)
     - Directory structure and organization
     - Separation of concerns (business logic, infrastructure, UI)
     - Design patterns and architectural layers
     - Module boundaries and dependencies

   - **Data Flow Analyzer** (`subagent_type: Explore`, `thoroughness: medium`)
     - Data models and schemas
     - State management patterns
     - API contracts and persistence patterns
     - Data validation and transformation

   - **Dependency Auditor** (`subagent_type: Explore`, `thoroughness: quick`)
     - Package dependencies and management
     - External service integrations
     - Circular dependency detection
     - Import pattern analysis
     - Unused dependency identification

   - **Testing & Quality Analyzer** (`subagent_type: Explore`, `thoroughness: quick`)
     - Test organization and coverage
     - Linting and formatting configuration
     - Type checking setup
     - CI/CD pipeline analysis
     - Pre-commit hooks and quality gates

   - **Configuration Reviewer** (`subagent_type: Explore`, `thoroughness: quick`)
     - Environment variables and secrets management
     - Build configuration and tooling
     - Deployment setup (containerization, hosting config)
     - Development vs production differences

3. **Wait for all agents to complete**:
   - Collect findings from each agent
   - Review reports for common themes

4. **Synthesize findings**:
   - Combine insights into coherent assessment
   - Identify priority issues and opportunities
   - Create actionable recommendations

#### For Live Websites

1. **Initialize browser and navigate**:
   ```
   Use mcp__playwright__browser_navigate to visit the URL
   ```

2. **Capture initial state**:
   ```
   Use mcp__playwright__browser_take_screenshot with fullPage: true
   Use mcp__playwright__browser_snapshot for accessibility tree and content extraction
   ```

3. **Visual & UX Analysis**:
   - Take screenshots at multiple viewport sizes (desktop, tablet, mobile)
   - Document navigation patterns and user flows
   - Capture design system elements:
     - Color palette (primary, secondary, accent colors, backgrounds)
     - Typography (font families, sizes, weights, line heights)
     - Spacing and layout grid patterns
     - UI components (buttons, forms, cards, modals)
     - Iconography and visual style
     - Imagery style (photography vs illustrations, filters, treatments)
   - Note responsive behavior and breakpoints
   - Identify visual hierarchy and content organization patterns
   - Document animation and interaction patterns

4. **Content & Structure Audit**:
   - Extract page content from accessibility snapshot
   - Analyze heading hierarchy (h1-h6 structure)
   - Document semantic HTML usage
   - Capture content strategy:
     - Tone and voice (formal, casual, technical, friendly)
     - Messaging patterns and value propositions
     - Content types (hero sections, feature lists, testimonials, blog posts)
     - Copy length and readability
   - Identify forms, CTAs, and interactive elements
   - Map site structure via navigation analysis
   - Document information architecture and content organization

5. **Asset Collection**:
   - Capture all visible images (hero images, product photos, illustrations, icons, logos)
   - Identify media files if present (videos, audio)
   - Note image usage contexts and visual styles

6. **Additional Context** (if needed for technical audit):
   - Check console for critical errors
   - Review accessibility from snapshots
   - Note any obvious technical issues affecting user experience

7. **Navigate to key pages**:
   - Repeat capture and analysis for important pages
   - Build comprehensive site understanding

8. **Close browser**:
   ```
   Use mcp__playwright__browser_close
   ```

9. **Synthesize findings**:
    - Combine data from all pages analyzed
    - Identify patterns and inconsistencies
    - Create prioritized recommendations

### Output Format

Provide structured analysis with these sections:

#### Executive Summary
- Target type (local project or live website)
- Primary purpose and target audience
- Technology stack identified
- Overall architecture or design pattern
- Current state assessment (production, development, experimental)

#### Strengths
- Well-implemented patterns and practices
- Quality attributes observed
- Notable features or innovations
- Performance or accessibility wins

#### Concerns
- Anti-patterns or design issues
- Missing best practices or quality gates
- Performance bottlenecks or inefficiencies
- Accessibility gaps or violations
- Security considerations
- Technical debt or maintenance issues

#### Improvement Recommendations

Organize by priority:

**High Priority** - Critical issues affecting functionality, security, accessibility, or core user experience

**Medium Priority** - Quality improvements, optimization opportunities, minor UX enhancements

**Low Priority** - Nice-to-have refinements, future considerations

For each recommendation:
- Specific issue identified with evidence
- Impact on users or development team
- Suggested solution or approach
- Estimated complexity (simple / moderate / complex)

#### Next Steps
- Actionable tasks to address high-priority items
- Suggested tools, libraries, or approaches
- Migration paths if major changes needed
- Alignment with workspace standards (for local projects)

#### Design System Inventory (For Redesign/Modernization Projects)

When analysis is for revamping or modernizing:

**Visual Design**:
- Color palette with hex codes
- Typography system (font stacks, scale, usage)
- Spacing scale and layout grid
- Border radius and shadow patterns
- Component inventory with visual examples

**Content & Messaging**:
- Tone and voice characteristics
- Key messaging themes
- Content type patterns
- Call-to-action styles and language

**Asset Catalog**:
- Images (hero images, product photos, illustrations, icons, logos)
- Font families used
- Media assets (videos, animations) if present

**User Experience Patterns**:
- Navigation structure and patterns
- Interaction patterns (hover states, transitions, animations)
- Form designs and validation approaches
- Responsive breakpoints and mobile adaptations

**Modernization Opportunities**:
- Outdated visual patterns to refresh
- Modern design trends to consider
- Enhanced user experience possibilities
- Content and messaging improvements

### Implementation Notes

**Efficiency**:
- Always execute multiple independent agents in parallel
- For local projects: launch all 5 agents in a single message with multiple Task tool calls
- For websites: batch Playwright operations where possible

**Evidence**:
- Reference specific file paths and line numbers for local projects
- Include screenshot filenames and URLs for websites
- Quote relevant code or content excerpts

**Scope Management**:
- Tailor analysis depth to project complexity
- For simple static sites, focus on essentials (performance, accessibility, SEO)
- For complex applications, deep-dive architecture and code quality
- For redesign/modernization requests, include full Design System Inventory section
- For technical audits, focus on Concerns and Recommendations sections

**Website Analysis**:
- Respect robots.txt and rate limits
- Save screenshots to organized directory (e.g., `analysis-output/screenshots/`)
- Focus on capturing what users see: visuals, content, and images
- For redesign work, ignore technical implementation details (bundles, CSS architecture, etc.)
- Keep browser sessions focused and close properly
- Document which pages were analyzed

## Examples

### Example 1: Analyzing a Local Next.js Project

User request:
```
Analyze this Next.js project and tell me what could be improved
```

You would:
1. Identify project root by finding package.json
2. Check framework from next.config.js or package.json dependencies
3. Launch 5 analysis agents in parallel using Task tool:
   - Architecture Explorer examining app/, components/, lib/ structure
   - Data Flow Analyzer reviewing API routes and data fetching patterns
   - Dependency Auditor checking package.json and imports
   - Testing & Quality Analyzer looking for test files and config
   - Configuration Reviewer examining next.config.js, .env files, deployment setup
4. Wait for all agents to complete
5. Synthesize findings into comprehensive report with:
   - Executive summary identifying it as Next.js 13+ App Router project
   - Strengths like good component organization
   - Concerns like missing tests or unoptimized images
   - Prioritized recommendations
   - Next steps with specific files to modify

### Example 2: Auditing a Live Website

User request:
```
Audit https://example.com for performance and accessibility issues
```

You would:
1. Navigate to https://example.com using Playwright
2. Take full-page screenshot and capture accessibility snapshot
3. Capture network requests to analyze loaded resources
4. Resize browser to mobile viewport and capture again
5. Analyze console messages for errors or warnings
6. Navigate to 2-3 key pages (e.g., /about, /products) and repeat captures
7. Close browser
8. Synthesize findings:
   - Executive summary noting it's a static marketing site
   - Strengths like responsive design
   - Concerns like large unoptimized images, missing alt text
   - High priority: optimize images, add alt attributes
   - Medium priority: implement lazy loading
   - Low priority: consider modern image formats (WebP, AVIF)
9. Provide evidence with screenshot paths and specific issues found

### Example 3: Examining a Python API Project

User request:
```
Examine this FastAPI codebase
```

You would:
1. Identify project root via pyproject.toml or requirements.txt
2. Confirm FastAPI from dependencies
3. Launch 5 parallel agents analyzing:
   - Architecture: API route organization, business logic separation
   - Data Flow: Pydantic models, database connections, validation
   - Dependencies: Third-party packages, circular imports
   - Testing: pytest setup, coverage, fixtures
   - Configuration: Environment variables, Docker setup, CI/CD
4. Synthesize findings focused on API-specific concerns:
   - Route organization and OpenAPI docs
   - Request/response validation
   - Error handling patterns
   - Database migration strategy
   - Testing coverage for endpoints
5. Provide FastAPI-specific recommendations

### Example 4: Analyzing Website for Redesign

User request:
```
Analyze https://oldcompany.com - we want to modernize and revamp the design
```

You would:
1. Navigate to https://oldcompany.com
2. Take full-page screenshots at desktop (1920x1080), tablet (768x1024), mobile (375x667)
3. Capture accessibility snapshot and network requests
4. Document design system:
   - Extract color palette from screenshots (primary blue #2E5C8A, secondary gray #707070, etc.)
   - Identify fonts (Arial, Georgia) and usage patterns
   - Note button styles, spacing patterns, component designs
   - Capture visual hierarchy and layout approach
5. Analyze content strategy:
   - Note formal, corporate tone
   - Identify messaging themes (reliability, experience, trust)
   - Document content types (hero + 3-column features pattern)
6. Catalog assets:
   - Stock photography (business, handshake images)
   - Simple icon graphics
   - Multiple logo variations
   - Fonts: Arial and Georgia
7. Navigate to /about, /services, /contact and repeat captures
8. Synthesize findings with Design System Inventory section:
   - Current visual design (dated gradients, drop shadows, centered layouts)
   - Content patterns (heavy text blocks, formal language)
   - Asset inventory (stock photography, simple icons, traditional fonts)
   - UX patterns (traditional navigation, limited mobile optimization)
   - Modernization opportunities (flat design, modern typography, improved mobile UX, content refresh, updated imagery)
9. Provide actionable redesign roadmap

### Example 5: Quick Static Site Analysis

User request:
```
Quick analysis of this simple portfolio site
```

You would:
1. Recognize it's a simple project (static HTML/CSS or basic Astro)
2. Scale analysis appropriately - skip heavy architectural analysis
3. Launch subset of agents or use quick thoroughness:
   - Quick architecture review (file organization)
   - Skip data flow (no complex state)
   - Quick dependency check
   - Skip testing (may not have tests for static site)
   - Configuration review (build process, deployment)
4. Focus findings on:
   - Asset optimization
   - Accessibility
   - SEO basics
   - Performance
5. Keep recommendations lightweight and actionable
