# Handoff: myBuilds — Technical Submittal Automation System (Phase 1 MVP)

## Overview
myBuilds is a web application that lets building-materials suppliers generate
compliant, consultant-ready technical submittal packages automatically. Staff
pull datasheets, certificates and AI-drafted compliance statements from a
document library into branded PDF packages.

This handoff covers the **Phase 1 MVP** screen set:
1. Authentication (Login / Register / Password reset)
2. Main Dashboard
3. Documents Library + Upload + (version history reference)
4. Templates list + drag-and-drop Template Builder
5. Submittal Generator wizard (multi-step)
6. Submittals list + detail slide-over
7. User Profile / Settings

## About the Design Files
The file in this bundle (`myBuilds.dc.html`) is a **design reference created in
HTML** — a working prototype that demonstrates the intended look, layout, copy,
and interactions. **It is not production code to copy directly.**

The task is to **recreate these designs in the target codebase's environment**.
The intended stack (per the original spec) is **React + Vite**. Use the project's
established component library, routing, state management, and data layer; wire
the screens to real APIs. If no frontend environment exists yet, React + Vite is
the recommended choice. The HTML/inline-style approach in the prototype is a
fidelity reference only — translate it into idiomatic components and a real
stylesheet / design-token system.

## Fidelity
**High-fidelity.** Final colors, typography, spacing, component styling, and
interaction states are all represented. Recreate the UI to match, using the
codebase's existing primitives where they exist (buttons, inputs, tables,
modals) styled to these tokens.

---

## Design Tokens

### Color
| Token | Hex | Usage |
|---|---|---|
| Primary | `#0066cc` | Buttons, active nav, links, focus rings |
| Primary hover | `#0052a3` | Button hover |
| Primary tint | `#e8f1fd` | Active nav background, info chips |
| Primary tint 2 | `#f4f9ff` / `#f7fafe` | Selected cards, soft panels |
| Accent (orange) | `#ff6b35` | Notification dot, draft accents |
| Success | `#28a745` (text `#1e7a32`, bg `#eaf6ec`) | Approved, completed |
| Purple | `#6b4ed8` (bg `#f0ecfd`) | Reviewed, template icon |
| Warning/Draft | `#c2620f` (bg `#fef0e6`) | Draft, optional, mid-confidence |
| Error | `#dc3545` (bg `#fdf2f2`/`#fdecea`) | Destructive, errors, required `*` |
| Text primary | `#1a1a1a` | Headings |
| Text body | `#333` / `#374151` | Body text |
| Text muted | `#6b7685` / `#8a94a2` | Secondary text |
| Text faint | `#9aa3ad` | Placeholders, meta, icons |
| Border | `#e6eaef` / `#e9edf2` / `#eef1f5` | Card borders, dividers |
| Input border | `#d4dae1` | Form field borders |
| App background | `#f5f7fa` | Main canvas |
| Surface | `#ffffff` | Cards, bars, modals |
| Subtle surface | `#fafbfc` / `#f7f9fc` | Table headers, inset panels |

Status badge map (bg / text):
- Approved / Active → `#eaf6ec` / `#1e7a32`
- Generated → `#e8f1fd` / `#0066cc`
- Reviewed → `#f0ecfd` / `#6b4ed8`
- Draft → `#fef0e6` / `#c2620f`
- Archived / Inactive → `#eef0f3` / `#6b7685`

Document-type badge map (bg / text):
- Datasheet → `#e8f1fd` / `#0066cc`
- Certificate → `#eaf6ec` / `#1e7a32`
- Compliance → `#fdf0e9` / `#c2620f`
- Manual → `#f0ecfd` / `#6b4ed8`
- Catalogue → `#e7f6f7` / `#0a8a93`
- Vendor List → `#fdf2f7` / `#bd2a72`

### Typography
- Font family: **Inter** (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto` fallback), antialiased.
- Page title (h1): 25px / 700 / letter-spacing -0.02em
- Auth headline (h2): 26px / 700
- Section/card title: 15–17px / 700
- Body: 14–14.5px / 400–500, line-height ~1.5
- Secondary / meta: 12–13px / 500, color muted
- Table header: 11.5px / 600 / uppercase / letter-spacing 0.05em / color `#9aa3ad`
- Badge: 11.5–12px / 600
- Eyebrow labels: 11px / 700 / uppercase / letter-spacing 0.08–0.09em

### Spacing & Radius
- Base unit 8px (use 8 / 12 / 16 / 18 / 22 / 26 / 28 / 32).
- Screen padding: `28px 32px 48px`.
- Card padding: 16–24px.
- Radius: inputs/buttons 6–8px, cards 10–14px, pills/badges 20px, avatars 50%.
- Card shadow (hover): `0 6px 20px rgba(20,40,70,.10)` to `0 8px 24px rgba(20,40,70,.10)`.
- Modal shadow: `0 24px 60px rgba(10,25,50,.3)`.
- Focus ring: `border-color:#0066cc; box-shadow:0 0 0 3px rgba(0,102,204,.12)`.

### Controls
- Primary button: bg `#0066cc`, white, 40–46px tall, radius 7–8px, weight 600; hover `#0052a3`.
- Secondary button: white bg, `#374151` text, `1px #d4dae1` border; hover bg `#f5f7fa`.
- Icon button: 32px square, transparent, radius 7px, muted icon; hover tint bg + colored icon.
- Inputs: 40–44px tall, `1px #d4dae1`, radius 6–7px, 14–14.5px text.
- Toggle switch: 42×24px track, radius 13px, 20px white knob; on = `#0066cc`, off = `#cdd6e0`.
- Checkbox: 18px, radius 5px, checked = `#0066cc` fill + white check.

---

## App Shell (persistent after login)

**Sidebar** — 232px fixed, white, right border `#e6eaef`, sticky full-height.
- Logo lockup: 30px rounded-square `#0066cc` mark with white "m" + "myBuilds" 17px/700.
- Full-width "New Submittal" primary button (opens wizard).
- "Workspace" eyebrow, then nav items: Dashboard, Documents (badge "1.2k"), Templates, Submittals (blue badge "47"). Active item = `#e8f1fd` bg, `#0066cc` text/600; hover `#f1f5f9`.
- Footer: storage card (`#f1f6fd` bg) with 64% progress bar, "6.4 GB of 10 GB used".

**Topbar** — 62px, white, bottom border, sticky, z-index 30.
- Left: search input (max 440px, `#f3f5f8` bg pill, search icon) — "Search submittals, documents, templates…".
- Right: bell button (40px, with orange unread dot), divider, user chip (34px `#0066cc` avatar "SC", name "Sarah Chen", role "Operator", chevron). Clicking the chip opens a dropdown (My Profile, Preferences, divider, Sign out in red).

---

## Screens

### 1. Authentication
Split layout: left **brand panel** (flex:1) on a `linear-gradient(135deg,#0066cc,#003d80)` with logo, eyebrow "Technical Submittal Automation", headline "Generate compliant submittals in minutes, not days.", supporting copy, and 3 stats (12k+ submittals / 98.4% accuracy / 6 min avg). Right **form panel** 520px white, vertically centered, `fadeIn`.

Three views toggled in place:
- **Login**: "Welcome back". Email (mail icon, prefilled `sarah.chen@acmebuild.com`), Password (lock icon + show/hide eye toggle), "Forgot password?" link, "Remember me for 30 days" checkbox, full-width "Sign in" button (shows spinner + "Signing in…" for ~850ms, then enters app), "Create an account" link. Error area renders above form when present (red `#fdecea`).
- **Register**: "Create your account". Two-column Full name / Username, then Work email, Company, Password (with live 4-segment strength meter colored red→orange→yellow→green and label Too weak/Weak/Fair/Good/Strong), Terms checkbox, "Create account", "Sign in" link.
- **Password reset**: "Reset your password". Email field + "Send reset link"; on submit replaces form with green success confirmation. "← Back to sign in".

### 2. Dashboard
- Header: "Good morning, Sarah" + subtitle; right actions "Upload Document" (secondary) and "New Submittal" (primary).
- **KPI row** — 4 cards (grid 1fr×4). Each: tinted icon chip (38px) + trend pill, big 27px value, label. Values: 47 Submittals this month (+18%), 1,284 Documents in library (+64), 38 Templates created (+3), 12 Compliance pending (Review).
- **Charts row** — grid 1.7fr / 1fr.
  - Bar chart "Submittals generated / Last 30 days": 14 bars, last bar `#0066cc`, others `#aecbf0`, radius 4px top.
  - Donut "Status distribution": `conic-gradient(#0066cc 0-46%, #6b4ed8 46-64%, #28a745 64-86%, #cdd6e0 86-100%)` with white center hole (312 Total). Legend: Generated 144, Reviewed 56, Approved 68, Draft/Archived 44.
- **Recent submittals** table (6 rows): Submittal (blue/600), Product, Consultant, Status badge, Date, chevron. Row click opens detail slide-over; "View all →" goes to Submittals.

### 3. Documents Library
- Header + "Upload Document" primary.
- Two-column grid `220px / 1fr`.
  - **Left filter card**: "Filter by type" list (All types 1284, Datasheets 312, Certificates 188, Compliance docs 264, Manuals 142, Catalogues 96). Active = blue tint; filters the table by type.
  - **Right**: toolbar (search, "Filters" button, list/grid segmented toggle in a `#eef1f5` pill), then either:
    - **List view** (default): table — Document (file icon + name + product), Type badge, Version, Size, Uploaded date, and row Actions (Preview/Download/Versions/Delete icon buttons). 8 rows of seed data.
    - **Grid view**: 3-col cards with striped placeholder thumbnail, type badge, name, version/size.

**Upload modal** (600px, centered, `pop` in): header "Upload Document" + close X. Stages:
1. *Idle* — dashed dropzone "Drag & drop a PDF, or click to browse / PDF only · up to 50 MB". Click advances to:
2. *Selected* — selected-file row (red doc icon, `AcoustiClad-50mm-Datasheet-v3.3.pdf`, 2.6 MB, green check) + form: Product select, Document type select, Title input, auto Version chip "v3.3 (new)".
3. *Uploading* — primary button shows spinner "Uploading…" (~1.1s).
4. *Done* — green check, "Upload complete"; modal auto-closes (~1s) and a success toast appears.
Footer (Cancel / Upload document) hidden on the Done stage.

> Version history (per spec 3.3) is referenced via the row "Versions" action — implement as a timeline modal: current version highlighted blue, past versions gray, restore/download/preview per entry.

### 4. Templates
- **List**: header + "Create Template". Search + Filters. 3-col grid of template cards: purple layers icon + status badge, name (16/700), product, type badge + "N sections", footer with consultant + Edit/Duplicate/Delete icon buttons. Clicking a card (or Edit) opens the Builder. Seed: 6 templates (Active/Draft/Inactive).
- **Template Builder** — full-height (`calc(100vh - 62px)`), three regions:
  - **Top bar**: back button, template title "Standard Facade Submittal / AcoustiClad 50mm Panel · Hassell Studio", Preview (secondary) + Save Template (primary, toasts + returns to list).
  - **Grid `252px / 1fr / 300px`**:
    - *Left* "Available Sections" (`#fafbfc`): clickable cards (Vendor List, Installation Manual, Test Reports, Drawings & Schematics) with type badge + plus icon; clicking appends to the canvas.
    - *Center* canvas (`#f5f7fa`): "Drag the handle to reorder · N active sections". Each section card is **draggable** (HTML5 drag-and-drop reorders the list), shows drag handle, name, type badge, Required/Optional pill, "N docs", and a delete icon. Selected card = blue border + ring. 6 default sections.
    - *Right* "Section Properties": editable Section name, read-only Section type, "Mandatory section" toggle (writes back to the selected section), "Linked documents" panel.

### 5. Submittal Generator Wizard
Centered (max 760px). 5-step progress bar with numbered circles (done = green w/ check, current = blue, upcoming = gray) and connecting lines. Card body per step; footer Cancel / Back / Continue (Back hidden on step 1; final button "Generate Submittal").
1. **Template** — select Product (3 cards) and Template (2 cards), selection = blue ring.
2. **Project info** — Project name/code, Consultant name/code, description textarea (prefilled).
3. **Sections** — review list of template sections with Required/Optional pills and on toggles.
4. **Compliance** — two big choice cards: "Yes, generate with AI" (sparkle icon) vs "No, skip". When Yes, reveals a panel: requirements-doc upload + AI model select (Claude 4.5 Sonnet / GPT-4o).
5. **Review** — summary table (Product, Template, Project, Consultant, Compliance).

On Generate: button spinner ~1.6s → **success view**: green check, "Submittal generated", file card (`SUB-2026-0148.pdf`) with Pages/File size/Gen time stats, and actions Download PDF / View details / Generate another.

### 6. Submittals list + detail
- **List**: header + "New Submittal", search + "Status" filter, full table — Submittal (blue), Product, Consultant, Project, Status badge, Pages, Generated, row download button. 8 rows. Row click opens detail.
- **Detail slide-over** — right panel 540px, scrim overlay (click to close), `slideIn`. Header: submittal number + status badge, product · project, close X, and a 4-tab bar:
  - *Overview*: key/value rows (number, product, consultant, project, pages, generated by/on).
  - *Files*: full-width "Download full package (PDF)" + list of included files with type badges and download buttons.
  - *Compliance*: cards with requirement (bold), AI statement in a blue-left-border quote box, and a colored confidence-score pill (96% / 91% green, 74% amber).
  - *Audit*: vertical timeline with colored dots — approved, reviewed, generated, created, each with actor + timestamp.

### 7. Profile / Settings
Max 820px, 4-tab bar (Profile / Security / Preferences / Notifications):
- **Profile**: 76px avatar + "Change photo"; card with Full name, Username (read-only), Email, Phone, Department, Role badge; Cancel / Save changes (toast).
- **Security**: Change-password card (current + new) → "Update password" (toast); Two-factor card with "Enable 2FA".
- **Preferences**: toggle rows — Compact sidebar, Remember filters, Default to grid view.
- **Notifications**: toggle rows — Submittal generated, Compliance review needed, Weekly digest, Security alerts.

---

## Interactions & Behavior
- **Routing**: single-page; sidebar + buttons swap the active screen. Builder and wizard are full routes (not modals). Reset scroll to top on navigation.
- **Auth**: "Sign in" / "Create account" set a loading state for ~850ms then mark the session logged-in and render the shell. "Sign out" returns to login.
- **Transitions**: screens `fadeIn .3s`; modals/cards `pop .15–.2s`; slide-over + toast `slideIn .25s`; spinners `spin .7s linear infinite`; button/hover transitions ~.12–.15s.
- **Drag & drop** (builder): native `draggable` cards; `dragstart` records index, `drop` splices/reorders and selects the moved section.
- **Toasts**: dark pill bottom-right with green check, auto-dismiss ~2.6s. Triggered by uploads, saves, downloads, section add/remove, etc.
- **Loading states**: login button, upload submit, wizard generate all show inline spinners.
- **Form validation** (to implement against real APIs): required fields marked with red `*`; password strength meter; email format; username availability.
- **Responsive**: desktop-first. Below ~1024px collapse the sidebar to a hamburger drawer and stack KPI/chart/grid columns; the auth brand panel hides under ~860px (form panel goes full-width). Tables become horizontally scrollable or card-stacked on mobile.

## State Management
- `session` (logged in/out, current user), `authView` (login/register/reset), auth loading/error, password-strength.
- `route` (dashboard | documents | templates | builder | submittals | wizard | profile).
- `userMenuOpen`.
- Documents: `docView` (list/grid), `docFilter` (type).
- Upload modal: `uploadOpen`, `uploadStage` (idle/selected/uploading/done).
- Builder: ordered `sections` array, `dragIndex`, `selectedSection`; section mandatory flags.
- Wizard: `step` (1–5), selected product/template indices, compliance on/off, generating flag, generated result.
- Detail: `detailOpen`, current submittal, `detailTab`.
- Profile: `profileTab`, preference/notification toggle map.
- Transient `toast` message.

Real implementation should fetch: KPIs/charts, documents (paginated, filterable), templates, products, submittals (paginated + detail incl. files/compliance/audit), and wire upload + generate + save endpoints. Replace all seed arrays in the prototype with API data.

## Assets
- **Icons**: line icons (≈1.7 stroke, 24-box) drawn inline in the prototype — replace with the codebase's icon set (e.g. Lucide/Feather, which these match): mail, lock, eye, search, bell, plus, chevron, user, settings, log-out, grid, file/doc, layers, stack, upload, download, edit, copy, trash, more (dots), history, filter, shield, clock, sparkles, check, x, drag-grid.
- **Logo**: placeholder "m" mark — swap for the real myBuilds logo.
- **Images**: document thumbnails are CSS striped placeholders; wire real PDF previews.
- **Fonts**: Inter via Google Fonts.

## Files
- `myBuilds.dc.html` — the full high-fidelity prototype (all 7 screen areas, mock data, interactions). Open in a browser to explore every state. This is the single source of truth for visual + behavioral intent.
