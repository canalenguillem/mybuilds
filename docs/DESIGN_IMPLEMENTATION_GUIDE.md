# Design Implementation Guide - myBuilds Phase 1 MVP

## Overview

This document integrates the **high-fidelity design prototype** (`myBuilds.dc.html`) with the technical specifications. The design is a working HTML prototype that demonstrates the complete Phase 1 MVP visual design, interactions, and component behavior.

**Important**: The prototype is a **reference for visual design and UX flow**, not production code. Implement using React + Vite with the design tokens specified below.

---

## Design Files & References

### Primary Design Reference
- **File**: `myBuilds_dc.html` (124 KB)
- **Format**: High-fidelity interactive HTML prototype
- **Coverage**: All 7 Phase 1 MVP screens with interactions
- **How to use**: Open in browser to explore every screen state, interaction, and animation

### Design Documentation
- **Colors**: Complete token map with hex codes
- **Typography**: Font sizes, weights, letter-spacing for all text levels
- **Spacing**: Base unit and all measurements
- **Components**: Button, input, badge, toggle styles with states
- **Animations**: Timing, easing, and transition specifications

---

## Design Tokens - Complete Reference

### Color Palette

#### Primary Colors
| Token | Hex | Usage |
|-------|-----|-------|
| Primary | `#0066cc` | Buttons, active nav, links, focus rings |
| Primary hover | `#0052a3` | Button hover states |
| Primary tint | `#e8f1fd` | Active nav backgrounds, info chips |
| Primary tint 2 | `#f4f9ff` / `#f7fafe` | Selected cards, soft panels |

#### Secondary Colors
| Token | Hex | Usage |
|-------|-----|-------|
| Accent (orange) | `#ff6b35` | Notification dot, draft accents |
| Success | `#28a745` | Approved, completed states |
| Success text | `#1e7a32` | Success text color |
| Success bg | `#eaf6ec` | Success background |
| Purple | `#6b4ed8` | Reviewed, template icon |
| Purple bg | `#f0ecfd` | Purple background |
| Warning/Draft | `#c2620f` | Draft, optional, mid-confidence |
| Warning bg | `#fef0e6` | Warning background |
| Error | `#dc3545` | Destructive, errors, required indicator |
| Error bg light | `#fdf2f2` / `#fdecea` | Error background |

#### Neutral Colors
| Token | Hex | Usage |
|-------|-----|-------|
| Text primary | `#1a1a1a` | Headings, primary text |
| Text body | `#333` / `#374151` | Body text, default |
| Text muted | `#6b7685` / `#8a94a2` | Secondary text, metadata |
| Text faint | `#9aa3ad` | Placeholders, icons, subtle |
| Border | `#e6eaef` / `#e9edf2` / `#eef1f5` | Card borders, dividers |
| Input border | `#d4dae1` | Form field borders |
| App background | `#f5f7fa` | Main canvas, default background |
| Surface | `#ffffff` | Cards, bars, modals |
| Subtle surface | `#fafbfc` / `#f7f9fc` | Table headers, inset panels |

#### Status Badge Colors (background / text)
| Status | Background | Text |
|--------|-----------|------|
| Approved / Active | `#eaf6ec` | `#1e7a32` |
| Generated | `#e8f1fd` | `#0066cc` |
| Reviewed | `#f0ecfd` | `#6b4ed8` |
| Draft | `#fef0e6` | `#c2620f` |
| Archived / Inactive | `#eef0f3` | `#6b7685` |

#### Document Type Badge Colors (background / text)
| Type | Background | Text |
|------|-----------|------|
| Datasheet | `#e8f1fd` | `#0066cc` |
| Certificate | `#eaf6ec` | `#1e7a32` |
| Compliance | `#fdf0e9` | `#c2620f` |
| Manual | `#f0ecfd` | `#6b4ed8` |
| Catalogue | `#e7f6f7` | `#0a8a93` |
| Vendor List | `#fdf2f7` | `#bd2a72` |

### Typography

#### Font Family
- **Primary**: Inter
- **Fallback**: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto`
- **Rendering**: Antialiased
- **Import**: Google Fonts

#### Type Scale
| Level | Size | Weight | Line Height | Letter Spacing | Usage |
|-------|------|--------|-------------|----------------|-------|
| Page title (h1) | 25px | 700 | auto | -0.02em | Screen headings |
| Auth headline (h2) | 26px | 700 | auto | auto | Login/register headings |
| Section title | 15-17px | 700 | auto | auto | Card titles, headers |
| Body | 14-14.5px | 400-500 | 1.5 | auto | Regular text, descriptions |
| Secondary/Meta | 12-13px | 500 | auto | auto | Timestamps, helper text |
| Table header | 11.5px | 600 | auto | 0.05em | Table column headers |
| Badge | 11.5-12px | 600 | auto | auto | Status, type badges |
| Eyebrow labels | 11px | 700 | auto | 0.08-0.09em | Section labels |

### Spacing

#### Base Unit
- **8px grid system** - all spacing multiples of 8
- Common values: 8, 12, 16, 18, 22, 26, 28, 32, 40, 48, 56, 64

#### Screen & Container Spacing
| Area | Value | Notes |
|------|-------|-------|
| Screen padding | 28px 32px 48px | Horizontal 32px, vertical 28px top / 48px bottom |
| Card padding | 16-24px | Usually 20px |
| Section gap | 24px | Between major content blocks |
| Row gap | 16px | Between rows/items |
| Column gap | 16px | Between columns |

#### Component Spacing
| Component | Value | Notes |
|-----------|-------|-------|
| Sidebar width | 248px | Fixed width |
| Topbar height | 62px | Sticky header |
| Button height | 40-46px | Typically 40px |
| Input height | 40-44px | Typically 40px |
| Card radius | 10-14px | Typically 12px |
| Button radius | 6-8px | Typically 7px |
| Badge/Pill radius | 20px | Fully rounded |
| Avatar radius | 50% | Circular |

### Controls & Components

#### Primary Button
- **Background**: `#0066cc`
- **Text**: White
- **Height**: 40-46px (typically 40px)
- **Padding**: `0 24px`
- **Radius**: 7-8px (typically 7px)
- **Font weight**: 600
- **Font size**: 14px
- **Hover**: Background `#0052a3`
- **Active**: Background darker
- **Disabled**: Opacity 50%, cursor not-allowed
- **Loading**: Show spinner icon, text "...ing"

#### Secondary Button
- **Background**: White
- **Text**: `#374151`
- **Border**: `1px #d4dae1`
- **Height**: 40px
- **Padding**: `0 24px`
- **Radius**: 7px
- **Font weight**: 500
- **Hover**: Background `#f5f7fa`
- **Border hover**: `1px #c4cdd8`

#### Icon Button
- **Size**: 32px square
- **Background**: Transparent
- **Radius**: 7px
- **Icon**: Muted color (`#6b7685`)
- **Hover**: Background `#e8f1fd`, icon `#0066cc`
- **Padding**: 0 (center icon)

#### Text Input / Select
- **Height**: 40-44px (typically 40px)
- **Border**: `1px #d4dae1`
- **Radius**: 6-7px
- **Padding**: `0 12px`
- **Font size**: 14-14.5px
- **Font weight**: 400
- **Placeholder color**: `#9aa3ad`
- **Focus**: Border `#0066cc`, shadow `0 0 0 3px rgba(0,102,204,.12)`
- **Error**: Border `#dc3545`, background `#fdf2f2`
- **Icon position**: Left side padding

#### Toggle Switch
- **Track**: 42px × 24px
- **Track radius**: 13px
- **Knob**: 20px circle, white
- **Track on**: `#0066cc`
- **Track off**: `#cdd6e0`
- **Transition**: 0.2s ease

#### Checkbox
- **Size**: 18px × 18px
- **Radius**: 5px
- **Checked**: `#0066cc` background, white checkmark
- **Unchecked**: `#d4dae1` border
- **Transition**: 0.15s ease

#### Badge/Pill
- **Padding**: 4-6px 10-12px (typically 5px 12px)
- **Radius**: 20px (fully rounded)
- **Font size**: 11.5-12px
- **Font weight**: 600
- **Height**: 24-28px (typically 26px)

#### Card
- **Background**: White
- **Border**: `1px #e6eaef`
- **Radius**: 10-14px (typically 12px)
- **Padding**: 16-24px (typically 20px)
- **Shadow**: `0 1px 2px rgba(20,40,70,.08)`
- **Shadow hover**: `0 6px 20px rgba(20,40,70,.10)` to `0 8px 24px rgba(20,40,70,.10)`

#### Modal
- **Background**: White
- **Border**: `1px #e6eaef`
- **Radius**: 12px
- **Padding**: 24-28px
- **Shadow**: `0 24px 60px rgba(10,25,50,.3)`
- **Overlay**: `rgba(0,0,0,.4)` semi-transparent background
- **Width**: 520px (auth) / 600px (upload) / 760px (wizard) / 540px (detail)

#### Form
- **Label color**: `#1a1a1a`
- **Label weight**: 500
- **Label size**: 13-14px
- **Label margin bottom**: 8px
- **Required indicator**: Red `*` after label text
- **Helper text**: 12px, `#6b7685`
- **Error text**: 12px, `#dc3545`, margin top 4px

### Animations & Transitions

#### Timing
| Purpose | Duration | Easing |
|---------|----------|--------|
| Button/hover | 0.12-0.15s | ease |
| Card transitions | 0.15-0.2s | ease |
| Modal/toast entrance | 0.25s | ease-out |
| Screen fade | 0.3s | ease |
| Spinner | 0.7s | linear infinite |

#### Specific Animations
- **Screen transitions**: `fadeIn 0.3s ease`
- **Modal pop-in**: `pop 0.15-0.2s cubic-bezier(0.34, 1.56, 0.64, 1)`
- **Toast slide-in**: `slideIn 0.25s ease-out`
- **Slide-over**: `slideIn 0.25s ease-out` (from right)
- **Spinner**: `spin 0.7s linear infinite` (360° rotation)
- **Button hover scale**: Optional subtle scale up

#### Focus Ring
- **Color**: `#0066cc`
- **Style**: `box-shadow: 0 0 0 3px rgba(0,102,204,.12)`
- **Width**: 3px with 0px spread
- **Applied to**: All interactive elements on tab/focus

---

## Screen Specifications

### 1. Authentication Screens

#### Layout
- **Split layout**: Left brand panel (flex 1) | Right form panel (520px)
- **Brand panel gradient**: `linear-gradient(135deg, #0066cc, #003d80)`
- **Form panel**: White, vertically centered
- **Transition**: Content fades in 0.3s

#### Brand Panel Content
- **Logo**: Placeholder "m" mark (swap for real myBuilds logo)
- **Eyebrow**: "Technical Submittal Automation" - 11px, 700, uppercase, letter-spacing 0.08em
- **Headline**: "Generate compliant submittals in minutes, not days." - 28px, 700
- **Supporting copy**: Body text explaining benefits
- **Stats section**:
  - "12,000+" submittals generated
  - "98.4%" accuracy rate
  - "6 min" average generation time
  - Each stat: large number + small label

#### Login Form
- **Heading**: "Welcome back" - 26px, 700
- **Fields**:
  - Email (mail icon) - prefilled `sarah.chen@acmebuild.com`
  - Password (lock icon) + show/hide eye toggle
- **Options**:
  - "Forgot password?" link (primary color)
  - "Remember me for 30 days" checkbox
- **Button**: Full-width "Sign in" primary button
  - Shows spinner + "Signing in…" for ~850ms
  - Then navigates to dashboard
- **Error display**: Red `#fdecea` box above form if present
- **Footer link**: "Create an account" links to register view

#### Register Form
- **Heading**: "Create your account" - 26px, 700
- **Fields**:
  - Two-column: Full name | Username
  - Work email
  - Company
  - Password with 4-segment strength meter
    - Segment colors: red → orange → yellow → green
    - Labels: Too weak / Weak / Fair / Good / Strong
- **Checkbox**: Agree to Terms & Conditions
- **Button**: Full-width "Create account" primary
- **Footer link**: "Sign in" links to login view

#### Password Reset Form
- **Heading**: "Reset your password" - 26px, 700
- **Step 1 - Email request**:
  - Email input field
  - "Send reset link" button
  - "← Back to sign in" link
- **Step 2 - Success confirmation**:
  - Green checkmark icon
  - Success message
  - Email confirmation text
  - Countdown or "Resend" option

#### Responsive Behavior
- **Below 860px**: Brand panel hides, form panel goes full width
- **Mobile**: Stack layout, adjust padding to 16px

---

### 2. Dashboard

#### Header
- **Left**: "Good morning, [Name]" (25px, 700) + "Dashboard" subtitle (12px, muted)
- **Right**: Two action buttons:
  - "Upload Document" (secondary, 40px)
  - "New Submittal" (primary, 40px)

#### KPI Cards Row
- **Layout**: 4-column grid (1fr each)
- **Cards**: 
  - Icon chip (38px, tinted background)
  - Trend pill (e.g., "+18%", green for positive)
  - Large value (27px, 700)
  - Label text
- **Values**:
  1. Submittals this month: 47 (+18%)
  2. Documents in library: 1,284 (+64)
  3. Templates created: 38 (+3)
  4. Compliance pending: 12 (Review button)

#### Charts Row
- **Layout**: 2-column grid (1.7fr / 1fr)
- **Left - Bar chart** "Submittals generated / Last 30 days":
  - 14 bars, heights vary
  - Last bar: `#0066cc`
  - Previous bars: `#aecbf0`
  - Bar radius: 4px top
  - Y-axis labels
  - X-axis (dates)
- **Right - Donut chart** "Status distribution":
  - Conic gradient: Generated 46% blue | Reviewed 18% purple | Approved 22% green | Draft 14% gray
  - White center hole with "312 Total"
  - Legend below: color dot + label + count

#### Recent Submittals Table
- **Columns**: Submittal (blue link), Product, Consultant, Status badge, Date, chevron (action)
- **Rows**: 8 rows of seed data
- **Row styling**: 
  - Border-bottom: `1px #e6eaef`
  - Padding: 16px vertical
  - Hover: Subtle background tint
- **Row interaction**: Click opens detail slide-over
- **Footer**: "View all →" link to full Submittals list

---

### 3. Documents Library

#### Header
- **Left**: Page title "Documents" + search bar integrated in topbar
- **Right**: "Upload Document" primary button

#### Layout
- **Two-column**: 220px left filter | 1fr right content

#### Left Filter Card
- **Title**: "Filter by type"
- **Items**: (expandable/collapsible)
  - All types - 1,284
  - Datasheets - 312
  - Certificates - 188
  - Compliance docs - 264
  - Manuals - 142
  - Catalogues - 96
- **Active**: Blue tint background
- **Click**: Filters the table/grid
- **Card styling**: Subtle bg, padding 16px, radius 12px

#### Toolbar
- **Order**: Search (topbar), Filter button, List/Grid toggle
- **Toggle**: Segmented control in `#eef1f5` pill
  - Icon buttons: list icon | grid icon
  - Selected: Blue background

#### List View (Default)
- **Table columns**: Document | Type badge | Version | Size | Uploaded | Actions
- **Document column**: File icon + name (blue link)
- **Type badge**: Color-coded per type
- **Actions**: Preview icon | Download icon | Versions icon | Delete icon
  - Hover: Colored, tooltips appear
- **Rows**: 8 rows of seed data
- **Pagination**: Below table (if >8)

#### Grid View
- **Layout**: 3-column auto-fit grid (220px basis)
- **Cards**:
  - Striped placeholder thumbnail (CSS pattern)
  - Type badge (top-right)
  - Document name (14px, 500)
  - Version/size (12px, muted)
  - Hover: Blue border, action icons overlay

#### Upload Modal

**Stage 1: Idle**
- **Dropzone**: Dashed border `#d4dae1`, `#f5f7fa` background
- **Icon**: Upload icon, muted color
- **Text**: "Drag & drop a PDF, or click to browse"
- **Subtext**: "PDF only · up to 50 MB" (12px, muted)
- **Click**: Browse file system

**Stage 2: Selected**
- **File row**: Doc icon + name + size + green checkmark
- **Form fields**:
  - Product select dropdown (required)
  - Document type select (required)
  - Title input (required)
  - Version chip (auto-filled, e.g., "v3.3 (new)")
- **Buttons**: Cancel (secondary) | Upload document (primary)

**Stage 3: Uploading**
- **Button**: Shows spinner + "Uploading…" (~1.1s)
- **Progress**: Optional progress bar

**Stage 4: Done**
- **Icon**: Green checkmark, large
- **Message**: "Upload complete" heading
- **Auto-close**: Modal closes after ~1s
- **Toast**: Success notification appears

---

### 4. Templates

#### List View

**Header**
- **Title**: "Templates"
- **Button**: "Create Template" (primary)

**Toolbar**
- **Search**: By name or product
- **Filters**: By status (Active/Draft/Inactive), product, type
- **View**: Cards (grid) or list

**Card Grid** (3 columns)
- **Card**:
  - Icon (purple layers) + status badge (top-right)
  - Template name (16px, 700)
  - Product name (13px, muted)
  - Type badge (e.g., "Generic", "Consultant-specific")
  - Section count (e.g., "6 sections")
  - Footer row: Consultant name | Action icons (Edit, Duplicate, Delete)
- **Hover**: Blue border, shadow
- **Click**: Opens Builder

#### Template Builder

**Layout**: Full viewport (`calc(100vh - 62px)`), 3-column grid

**Top Bar** (62px, sticky, white, bottom border)
- **Left**: Back button | Template title
  - Title: "Standard Facade Submittal / AcoustiClad 50mm Panel · Hassell Studio" (16px, 500)
- **Right**: Preview button (secondary) | Save Template button (primary)
  - Save: Shows spinner then toast "Saved", returns to list

**Grid** `252px / 1fr / 300px`

**Left Column: Available Sections** (`#fafbfc` background)
- **Title**: "Available Sections" (13px, 700, muted)
- **Scrollable list** of clickable cards:
  - Card: Icon (muted) + name (14px, 500) + plus icon (blue hover)
  - Examples: Vendor List, Installation Manual, Test Reports, Drawings & Schematics
  - Click: Appends to canvas (animates)
- **Padding**: 16px

**Center Column: Canvas** (`#f5f7fa` background)
- **Helper text**: "Drag the handle to reorder · N active sections" (12px, muted)
- **Section cards** (draggable):
  - Drag handle (≡) on left (muted)
  - Section name (14px, 700)
  - Type badge (compact)
  - Required/Optional pill (blue outline if required, gray if optional)
  - Document count (12px, muted)
  - Delete icon (red hover)
  - **Dragging state**: Opacity 50%, shadow
  - **Drop target**: Blue dashed border highlight
  - **Selected**: Blue border + ring
  - **Reorder**: HTML5 drag-and-drop splices array
- **Padding**: 16px | Gap between sections: 12px

**Right Column: Section Properties** (`#fafbfc` background)
- **Title**: "Section Properties" (13px, 700, muted)
- **Fields**:
  - Section name (editable input, current selection)
  - Section type (read-only dropdown or text)
  - "Mandatory section" toggle switch (writes back)
  - "Linked documents" panel (read-only list of included doc IDs)
- **Padding**: 16px | Scrollable

---

### 5. Submittal Generator Wizard

#### Container
- **Max width**: 760px
- **Centered on screen**
- **Background**: `#f5f7fa` canvas

#### Progress Bar (Top)
- **5 steps**: Numbered circles (1–5)
- **States**:
  - Done: Green `#28a745` background, white check icon
  - Current: Blue `#0066cc` background, white number
  - Upcoming: Gray `#cdd6e0` background, gray number
- **Connecting lines**: Vertical lines between circles
- **Labels** (optional): "Template" / "Project Info" / "Sections" / "Compliance" / "Review"

#### Card Body (Per Step)

**Step 1: Select Template & Product**
- **Instruction**: "What product and template?"
- **Product cards** (3 cards):
  - Image/icon + Product name + SKU
  - Selected: Blue ring border
- **Template cards** (2-3 cards below):
  - Icon (purple layers) + Template name + Section count + Consultant
  - Selected: Blue ring border
- **Buttons**: Continue (primary) | Cancel (secondary)

**Step 2: Project Information**
- **Form fields** (vertical stack):
  - Project name (required, red `*`)
  - Project code (required, red `*`)
  - Consultant name (required, red `*`)
  - Consultant code (optional)
  - Description textarea (optional, prefilled with example)
- **Validation**: Red border + error text below if invalid
- **Buttons**: Back (secondary, enabled) | Continue (primary) | Cancel

**Step 3: Review Sections**
- **Instruction**: "Review template sections"
- **Section list**:
  - Each row: Toggle switch | Section name | Type badge | Required/Optional pill
  - Mandatory sections: Toggle disabled, always on
  - Optional sections: Toggle enabled, user can exclude
- **Buttons**: Back | Continue | Cancel

**Step 4: Compliance Options**
- **Instruction**: "Generate AI-assisted compliance statements?"
- **Choice cards** (2 large cards):
  - Left: "No, skip for now" (gray bg)
  - Right: "Yes, generate with AI" (blue bg, sparkle icon)
  - Selected: Blue border + ring
- **If Yes selected, reveals panel**:
  - "Upload consultant requirements document" (upload dropzone)
  - "AI model" dropdown:
    - Claude 4.5 Sonnet (default)
    - GPT-4o
  - Helpful explanation: "AI will extract requirements and draft statements for review"
- **Buttons**: Back | Continue | Cancel

**Step 5: Review & Summary**
- **Summary table** (2-column key/value):
  - Product | [selected product name]
  - Template | [selected template]
  - Project | [name + code]
  - Consultant | [name + code]
  - Sections | [N sections included]
  - Compliance | [Yes with model] or [No]
- **Edit links** (pencil icon): Click to jump back to that step
- **Buttons**: Back | Generate Submittal (primary, large) | Cancel

#### Post-Generation Success Screen
- **Icon**: Large green checkmark
- **Heading**: "Submittal generated" (25px, 700)
- **File card**:
  - File icon + "SUB-2026-0148.pdf"
  - Pages: 156 pages
  - File size: 12.3 MB
  - Generation time: 2m 14s
- **Action buttons**:
  - Download PDF (primary, large)
  - View details (secondary)
  - Generate another (link)

---

### 6. Submittals List & Detail

#### List View

**Header**
- **Title**: "Submittals"
- **Button**: "New Submittal" (primary)

**Toolbar**
- **Search**: "Search submittals…"
- **Filter**: "Status" dropdown (All | Generated | Reviewed | Approved | Archived)

**Table**
- **Columns**: Submittal (blue link) | Product | Consultant | Project | Status badge | Pages | Generated date | Action (download icon)
- **Rows**: 8 rows of seed data
- **Row styling**:
  - Padding: 16px vertical | 14px horizontal
  - Border-bottom: `1px #e6eaef`
  - Hover: Subtle tint background
- **Row click**: Opens detail slide-over
- **Download action**: Download PDF directly

#### Detail Slide-Over (540px)

**Header**
- **Submittal number** (25px, 700): "SUB-2026-0148"
- **Status badge**: Color-coded (Approved/Generated/Reviewed/Draft)
- **Product & project** (12px, muted): "AcoustiClad 50mm Panel · Downtown Office Complex"
- **Close button** (X icon, right)

**Tab Bar** (4 tabs)
- Tabs: Overview | Files | Compliance | Audit
- **Styling**: Bottom border indicator, primary blue for active

#### Overview Tab
- **Key/value rows** (gray alternating bg):
  - Submittal number | SUB-2026-0148
  - Product | AcoustiClad 50mm Panel
  - Consultant | Hassell Studio
  - Project | Downtown Office Complex
  - Pages | 156
  - Generated by | Sarah Chen
  - Generated on | Jan 15, 2024 at 2:34 PM
  - Status | Approved (badge)

#### Files Tab
- **Full-width button**: "Download full package (PDF)" (primary, 48px height)
  - Icon: Download icon
  - Text: File name + size + pages
- **Included files list**:
  - File card rows:
    - File icon + Name
    - Type badge (Datasheet / Certificate / etc.)
    - Size (12px, muted)
    - Download icon button (blue hover)
  - 8-12 files

#### Compliance Tab
- **Cards** (vertical stack):
  - Each card shows:
    - **Requirement** (bold, 14px)
    - **Statement** (body text in left-border quote box, blue `#0066cc` border)
    - **Confidence pill** (color-coded):
      - 90%+ = Green `#28a745`
      - 70-89% = Amber `#c2620f`
      - <70% = Orange/red (if any)
  - **Example values**: 96% / 91% / 74%
  - Scrollable if many statements

#### Audit Tab
- **Vertical timeline**:
  - Colored dots (left side)
  - Activity lines connecting dots
  - Content: Action | Actor | Timestamp
  - **Timeline entries** (bottom to top, most recent first):
    - Approved by Sarah Chen on Jan 15, 2024
    - Reviewed by John Smith on Jan 14, 2024
    - Generated by system on Jan 14, 2024
    - Created by Sarah Chen on Jan 14, 2024
  - **Colors**: Green for approved, purple for reviewed, blue for generated, gray for created

---

### 7. Profile / Settings

#### Container
- **Max width**: 820px
- **Left padding/margin**: Optional sidebar navigation

#### Tab Bar
- **4 tabs**: Profile | Security | Preferences | Notifications
- **Styling**: Bottom border indicator, primary blue for active

#### Profile Tab

**Avatar Section**
- **Avatar**: 76px circular, blue `#0066cc` background + initials
- **Button**: "Change photo" (secondary, small)

**Information Card**
- **Fields**:
  - Full name (editable input)
  - Username (read-only, grayed text)
  - Email (editable input)
  - Phone (editable input)
  - Department (editable dropdown)
  - Role (read-only badge, e.g., "Operator")
- **Buttons**: Cancel (secondary) | Save changes (primary)
- **Toast**: "Profile updated" on save

#### Security Tab

**Change Password Card**
- **Title**: "Change password"
- **Fields**:
  - Current password (input)
  - New password (input) with strength meter
  - Confirm password (input)
  - Show/hide toggle (eye icon)
- **Strength meter**: 4 segments, colors red→orange→yellow→green
- **Button**: "Update password" (primary)
- **Toast**: "Password updated" on save

**Two-Factor Authentication Card**
- **Title**: "Two-factor authentication"
- **Status**: Currently disabled (gray)
- **Button**: "Enable 2FA" (primary)
- **On enable**: Modal with QR code + backup codes

#### Preferences Tab

**Toggle Rows** (vertical stack)
- **Compact sidebar** toggle
  - Description: "Use compact sidebar navigation"
  - Default: Off
- **Remember filters** toggle
  - Description: "Remember document / template filters on return"
  - Default: On
- **Default to grid view** toggle
  - Description: "Show documents and templates in grid view by default"
  - Default: Off
- **Auto-archive** toggle (optional)
  - Description: "Auto-archive submittals older than [X days]"
  - Number input: 90 days (default)

**Auto-save**: Changes apply immediately, optional toast

#### Notifications Tab

**Toggle Rows** (vertical stack)
- **Submittal generated** toggle
  - Description: "Notify when submittals are generated"
  - Default: On
- **Compliance review needed** toggle
  - Description: "Notify when compliance statements need review"
  - Default: On
- **Weekly digest** toggle
  - Description: "Receive weekly summary of activities"
  - Default: On
- **Security alerts** toggle
  - Description: "Notify on login from new device"
  - Default: On

**Email Frequency Selector** (optional)
- Radio buttons: Immediate | Daily | Weekly
- Default: Immediate

**Auto-save**: Changes apply immediately

---

## App Shell (Persistent After Login)

### Sidebar (248px fixed width)

**Logo & brand** (top, 62px)
- Logo mark + "myBuilds" text (14px, 700)

**Navigation menu**
- Items (vertical stack, 8px gap):
  - Dashboard (icon + "Dashboard")
  - Documents (icon + "Documents")
  - Templates (icon + "Templates")
  - Submittals (icon + "Submittals")
  - Compliance (icon + "Compliance") [optional for phase 1]
  - Analytics (icon + "Analytics") [optional for phase 1]
  - ─────────── divider
  - Settings (icon + "Settings")
  - Help (icon + "Help") [optional]
- **Active**: Blue `#e8f1fd` background + blue text
- **Hover**: Light tint background
- **Icons**: 20px, muted (gray) default, blue when active
- **Text**: 14px, 500

**Sidebar collapse** (responsive)
- Below 1024px: Hamburger menu (3 lines icon)
- Click: Slides out left drawer modal overlay
- Mobile-friendly touch targets

### Topbar (62px sticky, z-index 30)

**Left section**
- **Search input**: Max 440px, `#f3f5f8` pill background, search icon left
  - Placeholder: "Search submittals, documents, templates…"
  - On focus: Border `#0066cc`, shadow
  - Results: Dropdown with recent items

**Right section**
- **Bell icon button** (32px):
  - Icon: Bell outline
  - Unread dot: Orange `#ff6b35` (top-right)
  - Click: Dropdown notification panel (optional)
- **Divider**: `#e6eaef`, vertical
- **User chip** (34px, pill, `#0066cc` background):
  - Avatar: 34px circular with "SC" initials
  - Name: "Sarah Chen" (13px, 600)
  - Role: "Operator" (11px, muted)
  - Chevron: Indicates dropdown
  - Click: Opens dropdown menu:
    - My Profile (click → Profile tab)
    - Preferences (click → Preferences tab)
    - ─────────── divider
    - Sign out (red text)

---

## Interactions & Behavior

### Routing
- **Single-page application**
- Sidebar/buttons toggle active screen
- **Builder and Wizard**: Full-height routes (not modals)
- **Detail slide-over**: Overlay modal for submittal details
- **Reset scroll**: Scroll to top (0, 0) on navigation

### Authentication Flow
- **Login/Register**: Buttons show spinner for ~850ms
- **Session**: Once logged in, render app shell + dashboard
- **Sign out**: Return to login screen, clear session
- **Password reset**: Multi-step form with success confirmation

### Upload Modal
- **Stages**: Idle → Selected → Uploading → Done
- **Auto-close**: Modal closes after Done stage (~1s)
- **Toast**: Success notification appears bottom-right
- **Form validation**: Required fields marked with red `*`

### Template Builder
- **Drag & drop**: Native `draggable` attribute on section cards
- **Events**:
  - `dragstart`: Record source index
  - `dragover`: Highlight drop zone (blue dashed border)
  - `drop`: Reorder array, re-render, select moved section
- **Visual feedback**: Dragged card opacity 50%, drop target highlights

### Wizard Navigation
- **Step progression**: Back/Continue buttons
- **Step 1**: Back button hidden
- **Final step**: Button text "Generate Submittal"
- **Form validation**: All required fields (marked `*`) must be filled
- **Error display**: Red border + text below field
- **Progress visual**: Step circles + connecting lines update

### Toasts
- **Appearance**: Dark pill, bottom-right corner
- **Content**: Green checkmark icon + message text (white)
- **Auto-dismiss**: ~2.6s
- **Triggered by**:
  - Upload complete
  - Template saved
  - Submittal generated
  - Download started
  - Section reordered
  - Password updated
  - Profile saved

### Loading States
- **Login button**: Show spinner + "Signing in…" text
- **Upload button**: Show spinner + "Uploading…" text
- **Wizard generate**: Show spinner + "Generating…" text
- **Spinner animation**: Rotating circle, 0.7s linear infinite

### Form Validation
- **Required fields**: Red `*` after label
- **Email format**: Validate on blur, show error if invalid
- **Password strength**: 4-segment colored meter (red→orange→yellow→green)
- **Username availability**: Optional async check (green checkmark if available)
- **On submit**: Prevent if invalid, show error messages

### Responsive Behavior
- **Desktop (1024px+)**: Full layout as designed
- **Tablet (768-1023px)**:
  - Sidebar collapses to hamburger
  - KPI cards stack 2×2
  - Chart row stacks vertically (chart over donut)
  - Grid columns reduce to 2 or 1
- **Mobile (<768px)**:
  - Full-width sidebar drawer (slide-in)
  - Single-column layout
  - Tables scroll horizontally OR convert to card-stack view
  - Auth brand panel hides (form full-width)
  - Buttons/inputs scaled for touch (48px+ height)

---

## Implementation Checklist

### Phase 1 MVP Screens (All required)
- [ ] Authentication (Login, Register, Password Reset)
- [ ] Dashboard
- [ ] Documents Library (List, Grid, Upload modal)
- [ ] Templates (List, Builder with drag-drop)
- [ ] Submittal Wizard (5 steps)
- [ ] Submittals List & Detail (slide-over)
- [ ] Profile / Settings (4 tabs)

### Design System Components
- [ ] Primary, secondary, icon buttons with all states
- [ ] Text inputs, selects, dropdowns
- [ ] Checkboxes, toggle switches
- [ ] Badges (status, document type)
- [ ] Cards, modals, toasts
- [ ] Tables with hover/select states
- [ ] Progress bars, spinners
- [ ] Color tokens CSS variables or SCSS
- [ ] Typography scale system

### Interactions
- [ ] Form validation + error display
- [ ] Login/register form submission (850ms delay)
- [ ] File upload stages (idle → selected → uploading → done)
- [ ] Drag-and-drop section reordering
- [ ] Modal transitions (fade, pop, slide-in)
- [ ] Toast notifications auto-dismiss
- [ ] Spinner animations
- [ ] Focus rings on all interactive elements

### Responsive
- [ ] Desktop (1024px+) layout verified
- [ ] Tablet (768-1023px) sidebar/grid collapse
- [ ] Mobile (<768px) stacked layout, touch-friendly sizes
- [ ] Landscape/portrait orientation

### Accessibility
- [ ] Keyboard navigation (Tab through all elements)
- [ ] Focus visible (focus ring on all buttons/inputs)
- [ ] Color contrast ≥4.5:1 for text
- [ ] Semantic HTML (buttons, inputs, labels, links)
- [ ] Icon buttons have aria-labels
- [ ] Form labels associated with inputs
- [ ] Error messages linked to fields

---

## References

### Design File
- **myBuilds_dc.html** - Open in browser to explore all screens, interactions, hover states, and animations in real-time.

### Specification Files (From Original Docs)
- **API_SPECIFICATIONS.md** - REST endpoints for fetching/updating data
- **DATABASE_SCHEMA.md** - Data models for all entities
- **PROJECT_STRUCTURE.md** - File organization for React components
- **DEVELOPMENT_WORKFLOW.md** - Development standards, testing, Git workflow

### External Resources
- **Inter font**: https://fonts.google.com/specimen/Inter
- **Lucide Icons**: https://lucide.dev/ (matches the 24-box stroke weight)
- **React Documentation**: https://react.dev/
- **Vite Documentation**: https://vitejs.dev/

---

## Notes for Developers

1. **The prototype is a visual reference.** Do not copy the HTML/inline styles directly. Instead, recreate the UI using React components and a proper CSS or CSS-in-JS system.

2. **Replace seed data** in the prototype with real API calls to the backend (see API_SPECIFICATIONS.md).

3. **Match the design tokens exactly** — use CSS custom properties (variables) to define colors, spacing, typography so they can be maintained centrally.

4. **Implement form validation** against real API requirements (unique email, username availability, password policies, etc.).

5. **Test responsive behavior** below 1024px to ensure sidebar collapses and layouts stack properly.

6. **Accessibility is mandatory.** Every interactive element must be keyboard-accessible and have visible focus rings. All icons must have labels. Ensure color contrast meets WCAG AA standards.

7. **Use the design as your source of truth** for visual decisions. If you have questions about spacing, colors, or component behavior, refer back to the prototype or this guide.

---

**Ready to implement? Open myBuilds_dc.html in your browser and start coding!** 🚀
