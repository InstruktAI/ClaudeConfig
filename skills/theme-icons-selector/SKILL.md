---
name: Theme Icons Selector
description: Helps select matching icon sets for website themes from curated icon catalog at ~/Documents/Icons. Use when designing websites, selecting icons for themes, matching visual styles, or recommending icons for wellness, nature, spa, or spiritual projects.
---

# Theme Icons Selector

## Instructions

This skill helps select appropriate icon sets from a curated catalog to match website themes and visual styles.

### Icon Catalog Location

**Path**: `/Users/Morriz/Documents/Icons/`

Available icon sets include wellness, spa, nature, floral, herbal, and spiritual themes with various styles (outlined, filled, colored, minimal, detailed).

### Workflow

#### Step 1: Understand Theme Requirements

Identify the project's visual characteristics:
- **Theme**: Wellness, spa, nature, spiritual, alternative, professional
- **Style**: Minimal, detailed, outlined, filled, geometric
- **Color preference**: Monochrome, pastel, colored, earthy tones
- **Audience**: Professional, alternative/new-age, mainstream, spiritual

#### Step 2: View Icon Catalog Overview

Read the composite image showing all available sets:

```
Read: /Users/Morriz/Documents/Icons/all_icon_sets.png
```

This displays all icon sets stacked vertically with labels, allowing visual comparison of:
- Style variations (outlined vs filled, minimal vs detailed)
- Color palettes (monochrome, blue accents, pastels)
- Thematic focus (flowers, trees, spa, herbs, mandalas)
- Icon quantity and variety

#### Step 3: Match Sets to Theme

Based on the composite view, identify 2-3 icon sets that align with theme requirements.

**Matching guidelines**:

**For natural/earthy themes**:
- `113863-flowers` - Detailed floral icons
- `111025-tree-icons` - Tree and nature elements
- `4787730-herbs-and-spices-outline` - Herbal/organic outlined style

**For wellness/spa themes**:
- `1499705-massage-and-spa` - Spa and massage focused
- `3057311-spa` - Minimal spa line art
- `2943524-selfcare-outline` - Clean outlined self-care icons
- `2943555-selfcare-solid` - Bold filled self-care icons
- `2943615-selfcare-blue` - Colored self-care with blue accents

**For spiritual/alternative themes**:
- `4587380-pastel-mandala` - Soft pastel mandalas
- `4721277-mandalas-flat-3-of-3` - Flat mandala designs
- `112005-detailed-flowers` - Ornate floral patterns

**For minimal/modern themes**:
- `2943524-selfcare-outline` - Very clean outlined style
- `1185116-trees` - Simple tree silhouettes

#### Step 4: Review Specific Icon Set

Once sets are narrowed down, view the full icon collection:

```
Read: /Users/Morriz/Documents/Icons/{set-name}.png
```

Or read the interactive HTML catalog:

```
Read: /Users/Morriz/Documents/Icons/{set-name}.html
```

#### Step 5: Recommend Specific Icons

Based on site sections and content needs, recommend specific icons by their display names. Reference the set's directory for SVG files:

```
/Users/Morriz/Documents/Icons/{set-name}/svg/{icon-name}.svg
```

### Output Format

Provide recommendations structured as:

**Recommended Icon Sets**:

1. **Primary Set**: `{set-name}`
   - Style: {outlined/filled/colored/etc}
   - Count: {number} icons
   - Why: {matches theme because...}
   - Best for: {which site sections/elements}

2. **Alternative Set**: `{set-name}`
   - Style: {description}
   - Count: {number} icons
   - Why: {reasoning}
   - Best for: {use cases}

**Specific Icon Recommendations**:

For each major site section, suggest specific icons:
- **Hero/Header**: {icon names}
- **Services/Features**: {icon names}
- **About/Contact**: {icon names}
- **Navigation**: {icon names}

**Implementation Notes**:
- SVG files located at: `/Users/Morriz/Documents/Icons/{set-name}/svg/`
- Icons can be used inline or as icon components
- Recommend consistent style across site (stick to one set or complementary sets)

## Examples

### Example 1: Minimal Wellness Site

User request:
```
I need icons for a clean, minimal wellness website with an earthy vibe
```

You would:
1. Read `/Users/Morriz/Documents/Icons/all_icon_sets.png`
2. Identify earthy + minimal sets
3. Recommend:
   - **Primary**: `2943524-selfcare-outline` (clean outlined, wellness focused)
   - **Alternative**: `4787730-herbs-and-spices-outline` (earthy, natural elements)
4. Read the selfcare-outline PNG to see all icons
5. Suggest specific icons:
   - Hero: Meditation, Lotus Flower
   - Services: Yoga, Massage, Aromatherapy
   - Contact: Location pin, Calendar

### Example 2: Spiritual/Alternative Theme

User request:
```
Building a site for alternative healing - looking for spiritual, new-age feel without heavy symbolism
```

You would:
1. Read composite image
2. Focus on soft, organic styles avoiding overt spiritual symbols
3. Recommend:
   - **Primary**: `113863-flowers` (natural, organic patterns)
   - **Accent**: `4587380-pastel-mandala` (subtle spiritual, soft colors)
4. Review flower set for nature-based icons
5. Suggest using floral elements for section dividers and accent graphics
6. Recommend pastel mandalas sparingly for backgrounds or subtle decorative elements

### Example 3: Professional Spa Business

User request:
```
Icon set for a professional massage therapy practice - needs to look credible and calming
```

You would:
1. View all sets via composite
2. Focus on professional spa sets
3. Recommend:
   - **Primary**: `3057311-spa` (professional, minimal line art)
   - **Alternative**: `1499705-massage-and-spa` (direct massage/spa focus)
4. Read spa set details
5. Provide specific icon matches:
   - Services: Hot stones, Massage table, Essential oils
   - Benefits: Relaxation, Muscle relief
   - Info: Clock, Location, Phone

### Example 4: Multi-Theme Comparison

User request:
```
Show me 3 different icon styles for a wellness site - I want to see variety before deciding
```

You would:
1. Read composite image
2. Select three contrasting wellness sets:
   - **Outlined/Minimal**: `2943524-selfcare-outline`
   - **Filled/Bold**: `2943555-selfcare-solid`
   - **Colored/Vibrant**: `2943615-selfcare-blue`
3. Read all three set images
4. Present side-by-side comparison showing how each would look:
   - Outlined: Clean, modern, works with any color scheme
   - Filled: Strong visual presence, bold statements
   - Colored: Adds personality, blue calming theme
5. Let user choose based on their brand direction
