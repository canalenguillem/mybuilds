# Claude Design Prompts - Complete UI/UX Design Package

## Introduction

These are comprehensive prompts for Claude Design to create mockups for all pages of the AI-Powered Technical Submittal Automation System. Use these prompts to generate professional designs for the React + Vite frontend.

---

## 1. AUTH PAGES

### Prompt 1.1: Login Page Design

```
Based on the technical specification for an AI-Powered Technical Submittal Automation System,
design a professional login page with the following requirements:

**Layout & Components:**
- Header with company logo (top left) and application name
- Centered login form with email and password fields
- "Remember me" checkbox
- "Forgot Password?" link
- Login button (primary action)
- Sign up link for new users
- Footer with copyright

**Styling:**
- Professional corporate design
- Color scheme: Blue (#0066cc) as primary, white background
- Form width: ~400px, centered on page
- Use clean, modern typography
- Subtle background gradient or pattern
- Input fields with placeholder text
- Button should be full width with hover effects

**UI Elements:**
- Email input with email icon
- Password input with show/hide toggle
- Loading state for login button
- Error message area above form (red text)
- Success/info messages if needed

**State Variations:**
- Default state
- Hover states on buttons and links
- Focus states on inputs
- Loading state (spinner in button)
- Error state (red border on inputs, error message)
- Empty state

**Accessibility:**
- Clear labels for all inputs
- Proper form structure
- Keyboard navigation friendly
- Color contrast compliance

Design this page as a high-fidelity mockup suitable for development handoff.
```

---

### Prompt 1.2: Registration Page Design

```
Design a professional user registration/signup page for the Technical Submittal Automation System.

**Layout & Components:**
- Header with logo and app name
- Multi-step form OR single-page form
- Fields: Email, Full Name, Username, Password, Confirm Password, Company Name
- Password strength indicator
- Terms & Conditions checkbox
- Create Account button
- Login link for existing users
- Progress indicator if multi-step

**Styling:**
- Consistent with login page design
- Professional, clean appearance
- Blue primary color (#0066cc)
- White or light gray background
- Password strength meter with color coding (red/orange/yellow/green)

**Validation:**
- Real-time validation indicators
- Password requirements display (8+ chars, uppercase, number, etc.)
- Email format validation
- Username availability check (visual feedback)
- Required field indicators

**State Variations:**
- Empty state
- Typing/input state
- Validation states (valid/invalid)
- Loading state (during registration)
- Success state with redirect prompt
- Error states with helpful messages

Design a modern, user-friendly registration experience.
```

---

### Prompt 1.3: Password Reset Page Design

```
Design a password reset flow for the Technical Submittal Automation System with multiple screens.

**Screen 1: Request Password Reset**
- Email input field
- Submit button
- Back to login link
- Info message about reset email

**Screen 2: Reset Password via Link**
- New password input
- Confirm password input
- Password strength indicator
- Reset button
- Show password toggle

**Styling:**
- Consistent with auth pages
- Clean, minimal design
- Professional appearance
- Clear instructions for user

**Messages:**
- Success message after email submission
- Confirmation message after password reset
- Error messages for invalid email or token
- Password requirements information

Design both screens of the password reset flow.
```

---

## 2. DASHBOARD & MAIN PAGES

### Prompt 2.1: Main Dashboard Design

```
Design a comprehensive dashboard for the Technical Submittal Automation System showing KPIs and recent activity.

**Layout:**
- Top navigation bar with user menu (profile, settings, logout)
- Left sidebar with navigation menu
- Main content area with grid layout

**Key Sections:**

1. **Welcome Header**
   - Greeting message with user name
   - Quick action buttons (New Submittal, Upload Document, Create Template)

2. **KPI Cards (Top Section)** - 4 cards in a row:
   - Submittals Generated (This Month): Large number with trend up/down
   - Documents in Library: Total count
   - Templates Created: Number of templates
   - Compliance Review Pending: Number requiring review

3. **Charts Section** (2 columns):
   - Left: Line chart showing submittals generated over last 30 days
   - Right: Pie chart showing submittal status distribution (draft, completed, archived)

4. **Recent Activity Table**
   - Columns: Submittal Number, Product, Consultant, Status, Date, Actions
   - Show last 10 recent submittals
   - Pagination controls
   - Sort and filter options

5. **Quick Links/Shortcuts**
   - Most used templates
   - Recent documents
   - Recent submittals

**Sidebar Navigation:**
- Dashboard (active)
- Documents
- Products
- Templates
- Submittals
- Compliance
- Analytics
- Admin (if authorized)

**Styling:**
- Professional corporate dashboard
- White background
- Blue primary color (#0066cc)
- Gray secondary elements (#f5f5f5)
- Clear typography hierarchy
- Icons for each menu item and card

**Responsive:**
- Desktop-first design
- Cards stack on tablet/mobile
- Sidebar collapses to hamburger on mobile

Design this as the main landing page after login.
```

---

### Prompt 2.2: Analytics Dashboard Design

```
Design a comprehensive analytics dashboard for the Technical Submittal Automation System.

**Layout:**
- Full width with sidebar navigation
- Multiple sections with various visualizations

**Key Sections:**

1. **Date Range Selector** (Top)
   - Preset ranges: Last 7 days, Last 30 days, Last 90 days, Custom range
   - Export button (PDF, Excel)

2. **KPI Row** (4 cards):
   - Total Submittals Generated
   - Average Generation Time
   - Compliance Accuracy Rate
   - Documents Processed

3. **Charts** (2 columns, multiple rows):
   - Column 1:
     * Line chart: Submittals generated daily
     * Bar chart: Submittals by product
   - Column 2:
     * Pie chart: Submittals by status
     * Line chart: Compliance review pending vs completed

4. **Tables**:
   - Top products by submittal count (with rankings)
   - Top templates by usage
   - Compliance statements accuracy breakdown
   - Page generation metrics

5. **Filters Section**:
   - Filter by product, consultant, template, date range
   - Active filter tags with remove option
   - Apply/Reset buttons

**Design Elements:**
- Multiple chart types (line, bar, pie, table)
- Color-coded data (green for success, red for pending, blue for active)
- Hover tooltips on charts
- Responsive chart sizing
- Professional color palette

**Styling:**
- Clean, data-focused design
- White background
- Blue primary, gray accents
- Clear typography for readability
- Grid layout for charts

Design a professional analytics dashboard suitable for management review.
```

---

## 3. DOCUMENT MANAGEMENT

### Prompt 3.1: Documents List Page Design

```
Design the document management/library page for the Technical Submittal Automation System.

**Layout:**
- Sidebar navigation
- Main content area

**Header Section:**
- Page title: "Documents Library"
- Upload button (primary)
- Search bar with filter icon
- View toggle (List/Grid views)

**Filter & Search Section:**
- Search input field with placeholder "Search documents..."
- Filter by:
  * Document Type (dropdown): datasheets, certificates, manuals, catalogues, vendor lists, compliance docs
  * Product (dropdown or multi-select)
  * Date Range (from/to)
  * Status (all, active, archived)
- Clear filters button

**Documents List/Grid:**
- Columns (List View): Document Name, Type, Product, Version, Size, Uploaded By, Date, Actions
- Grid View: Document cards with preview
- Pagination at bottom (20 items per page)

**Row Actions:**
- Preview (eye icon)
- Download (download icon)
- View Versions (history icon)
- Delete (trash icon)
- More options (three dots)

**Card View (Grid):**
- Document preview/thumbnail
- Document name
- Type badge (color-coded)
- Product name
- Latest version number
- Hover shows actions

**Sidebar (Optional):**
- Document count by type
- Recent uploads
- Most used documents
- Storage usage indicator

**Empty State:**
- Large upload icon
- Message: "No documents yet. Upload your first document!"
- Upload button

**Dialogs/Modals:**
- Upload document form (when clicking Upload button)
- Document details modal
- Delete confirmation

**Styling:**
- Professional document management interface
- White background
- Blue primary color
- Document type badges with distinct colors
- Clean typography
- Icons throughout

Design this as the main document library management page.
```

---

### Prompt 3.2: Document Upload Modal/Form Design

```
Design a document upload form/modal for the Technical Submittal Automation System.

**Modal Structure:**
- Header: "Upload Document"
- Close button (X)
- Main form
- Footer with Cancel and Upload buttons

**Form Fields:**
1. **File Upload Area** (Drag & Drop)
   - Large drop zone with dashed border
   - Icon and text: "Drag and drop PDF or click to browse"
   - Browse button
   - File info after selection: name, size, type

2. **Select Product** (Required)
   - Dropdown with product list
   - Search within dropdown
   - "Create new product" option

3. **Document Type** (Required)
   - Radio buttons or dropdown:
     * Datasheet
     * Certificate
     * Manual
     * Catalogue
     * Vendor List
     * Compliance Document
     * Other

4. **Document Title** (Required)
   - Text input
   - Placeholder: "Enter document title"

5. **Description** (Optional)
   - Text area
   - Placeholder: "Add notes or description"
   - Character counter

6. **Version Number** (Auto-filled)
   - Read-only field showing next version
   - Tooltip explaining versioning

7. **Checkboxes:**
   - Replace existing version (if document exists)
   - Make current version (checkbox)

**Form States:**
- Empty state (initial)
- File selected state (shows file info)
- Loading state (during upload)
- Success state (shows checkmark, closes after delay)
- Error state (shows error message, allows retry)

**Validation:**
- File type validation (PDF only)
- File size limit (show max size allowed)
- All required fields indicated
- Error messages below fields

**Styling:**
- Clean modal design
- White background
- Blue buttons and accents
- Professional appearance
- Clear form layout
- Helpful hints below fields

**Size:**
- 600px width
- Center on screen
- Responsive on smaller screens

Design a professional document upload experience.
```

---

### Prompt 3.3: Document Versions History Design

```
Design a document version history/timeline view for the Technical Submittal Automation System.

**Layout:**
- Modal or side panel view
- Header with document name and close button

**Content:**

1. **Document Info Header**
   - Document name
   - Product name
   - Total versions count
   - Current version indicator

2. **Current Version Section**
   - Green "Current Version" badge
   - Version number
   - File size
   - Upload date/time
   - Uploaded by user
   - Preview button
   - Download button
   - Actions menu

3. **Version Timeline** (Vertical timeline)
   Each version shows:
   - Version number
   - Upload/modified date and time
   - Uploaded by
   - File size
   - Change summary/reason (if provided)
   - Actions:
     * Download icon
     * Preview icon
     * Restore to this version (if not current)
     * Delete icon

4. **Timeline Styling:**
   - Vertical line connecting versions
   - Dots/circles for each version
   - Current version highlighted in blue
   - Past versions in gray
   - Alternating left/right layout or single column

5. **Comparison Feature** (Optional):
   - Checkboxes to select two versions
   - Compare button to show differences

**Empty State:**
- Only one version created message
- No version history to display

**Styling:**
- Professional timeline design
- White/light background
- Blue primary color for current version
- Gray for past versions
- Clear typography
- Hover effects on actions

**Size:**
- Modal: 700px width
- Or side panel: 400-500px width
- Scrollable if many versions

Design a clear, professional version history interface.
```

---

## 4. TEMPLATE MANAGEMENT

### Prompt 4.1: Templates List Page Design

```
Design the submittal templates management page for the Technical Submittal Automation System.

**Layout:**
- Sidebar navigation
- Main content area

**Header Section:**
- Page title: "Submittal Templates"
- Create New Template button (primary)
- Search bar
- Filter icon
- View toggle (List/Grid)

**Filter Section:**
- Search: "Search templates..."
- Filter by:
  * Product (multi-select)
  * Consultant/Client (dropdown)
  * Template Type (all, generic, specific, custom)
  * Status (active, inactive)
- Clear filters button

**Templates List View:**
- Columns: Template Name, Product, Consultant, Type, Sections, Modified, Status, Actions
- Pagination (20 per page)
- Sortable columns (click header to sort)

**Row Actions:**
- Edit (pencil icon)
- Duplicate (copy icon)
- View Details (eye icon)
- Delete (trash icon)
- More options (three dots)

**Template Card (Grid View):**
- Template name (large text)
- Product name (badge)
- Consultant name (if specific)
- Template type badge (color-coded)
- Section count
- Last modified date
- Status indicator (active/inactive)
- Hover shows Edit, Duplicate, Delete buttons

**Status Indicators:**
- Active (green check)
- Inactive (gray)
- Draft (orange)

**Sidebar (Optional):**
- Templates by product
- Recently modified
- Template usage statistics
- Filter shortcuts

**Empty State:**
- Large template icon
- Message: "No templates created yet."
- Create Template button
- Link to documentation

**Styling:**
- Professional template management interface
- White background
- Blue primary color
- Type badges with distinct colors
- Clean grid layout
- Icons throughout

Design the main template management page.
```

---

### Prompt 4.2: Template Builder - Drag & Drop Design

```
Design a template builder with drag-and-drop section reordering for the Technical Submittal Automation System.

**Layout:**
- Left sidebar: Available sections panel
- Center: Template builder canvas
- Right sidebar: Section properties/settings

**Left Sidebar - Available Sections:**
- Search input: "Search sections..."
- Expandable categories:
  * Company Info (company profile, vendor list)
  * Product Details (datasheets, specifications)
  * Compliance (compliance statements, certificates)
  * Custom (user-defined sections)
- Each section as a draggable card:
  * Section icon
  * Section name
  * Description (tooltip)

**Center Canvas - Template Structure:**
- Header with template name and consultant
- Breadcrumb or tabs for navigation
- Droppable area for sections
- Sections displayed as cards in order:
  * Drag handle (six dots) on left
  * Section name (large)
  * Section type badge
  * Description
  * Document count
  * Conditional rules indicator (if any)
  * Actions menu (edit, duplicate, delete)
- Add section button between sections (+ icon)
- Visual feedback while dragging (highlighting drop zones)

**Right Sidebar - Section Properties:**
- Shows properties of selected section
- Properties include:
  * Section Name (editable)
  * Section Type (dropdown)
  * Description (textarea)
  * Mandatory/Optional toggle
  * Documents included (multi-select list)
  * Conditional Logic (if applicable)
  * Document source (current/inherited)

**Top Action Bar:**
- Save Template button (primary)
- Preview button (secondary)
- Discard button
- Publish/Activate toggle
- More options (three dots)

**States:**
- Section dragging (lifted, opacity reduced, shadow)
- Drop zone highlight (blue dashed border)
- Hover states on sections
- Selected section (blue border, properties shown)

**Responsive:**
- On smaller screens, sidebars may stack or hide
- Full-width canvas with collapsible panels

**Styling:**
- Clean, professional builder interface
- White background
- Blue primary color
- Drag handles distinct
- Clear visual hierarchy
- Smooth animations during drag
- Undo/Redo friendly

Design an intuitive, professional template builder.
```

---

### Prompt 4.3: Branding & Configuration Design

```
Design the branding and configuration panel for the Template Builder in the Technical Submittal Automation System.

**Modal/Panel Structure:**
- Header: "Branding & Configuration"
- Close button
- Tabs: General, Branding, Header/Footer, Advanced

**Tab 1: General**
- Template name (text input)
- Description (textarea)
- Product selection (dropdown, multi-select)
- Consultant/Client (dropdown, multi-select)
- Template type (radio: generic, consultant-specific, custom)
- Status (active/inactive toggle)

**Tab 2: Branding**
- Company Logo
  * Logo upload (drag & drop or browse)
  * Logo preview
  * Logo size slider
  * Logo position (left, center, right)
  * Logo removal button

- Colors
  * Primary color picker
  * Secondary color picker
  * Accent color picker
  * Preview of colors applied

- Typography
  * Font family selector
  * Heading font size
  * Body font size
  * Preview text

- Background
  * Color picker
  * Pattern selector (optional)
  * Image upload (optional)

**Tab 3: Header & Footer**
- Header Content Area
  * Add/edit company name
  * Add/edit company address
  * Add/edit contact info
  * Logo placement options

- Footer Content Area
  * Page number format selector
  * Date format selector
  * Add custom text (textarea)
  * Add company info toggle
  * Copyright text

- Preview of header/footer layout

**Tab 4: Advanced**
- Page size (A4, Letter, etc.)
- Margin settings (top, bottom, left, right)
- Font embedding options
- Metadata (author, subject, keywords)
- Security options (password protect)

**Bottom Section:**
- Preview button (shows how template will look)
- Save button (primary)
- Cancel button
- Reset to defaults button

**Preview Section (Right Side or Modal):**
- Live preview of configuration
- Shows how branding will appear
- Toggleable for each section

**Styling:**
- Clean, professional configuration interface
- White background with gray sections
- Blue primary color
- Form validation with helpful messages
- Color swatches for quick selection
- Live preview updates as you change settings

Design a comprehensive branding and configuration panel.
```

---

## 5. SUBMITTAL GENERATION

### Prompt 5.1: Submittal Generator Wizard Design

```
Design a multi-step submittal generation wizard for the Technical Submittal Automation System.

**Wizard Structure:** 4-5 Steps

**Step 1: Select Template & Product**
- Page title: "Generate New Submittal"
- Progress bar at top showing step 1/4 or 1/5
- Breadcrumb navigation: Step 1 > Step 2 > Step 3 > Step 4

- Content:
  * Question: "What product and template?"
  * Product selector (large cards or dropdown with search)
    - Show product name, SKU, category
    - Show relevant templates below
  * Template selector (cards showing template name, consultant, section count)
  * Next button (primary, disabled until selections made)
  * Back button (disabled on first step)
  * Cancel button (secondary)

**Step 2: Project & Consultant Information**
- Progress bar
- Form with fields:
  * Project Name (required)
  * Project Code (required)
  * Consultant Name (required)
  * Consultant Code (optional)
  * Project Description (optional)
  * Custom fields (if template has any)
- Validation messages below fields
- All fields required indicator (*)
- Next/Back/Cancel buttons

**Step 3: Review Template Sections**
- Progress bar
- Current template sections displayed as list or cards
- Each section shows:
  * Section name
  * Section type
  * Number of documents
  * Mandatory indicator
- Toggle switches to include/exclude optional sections
- Edit link to modify sections (opens builder in modal)
- Option to generate compliance statements (checkbox)
- Next/Back/Cancel buttons

**Step 4: Compliance Options** (if applicable)
- Progress bar
- Question: "Generate AI compliance statements?"
- Yes/No radio buttons
- If Yes:
  * Upload consultant requirements document
  * AI model selector (GPT-4, Claude)
  * Review statements checkbox
  * Analysis type selector (full, requirements-only, gaps-only)
- Helpful explanation text
- Next/Back/Cancel buttons

**Step 5: Review & Generate**
- Progress bar (or "Final Review")
- Summary of all selections:
  * Product
  * Template
  * Project info
  * Sections included (count)
  * Compliance generation (yes/no)
- Edit links next to each section to go back and change
- Large red warning if required fields are missing
- Generate button (primary, large)
- Back/Cancel buttons

**Post-Generation Screen:**
- Success message with checkmark
- Generated submittal details:
  * Submission number
  * File size
  * Page count
  * Generation time
- Action buttons:
  * Download PDF (primary)
  * View Details
  * Generate Another
  * Close/Go to Dashboard

**Design Elements:**
- Progress bar with step indicators
- Color-coded steps (completed: green, current: blue, upcoming: gray)
- Card-based layout for selections
- Clean, organized forms
- Helpful labels and descriptions
- Keyboard navigation support
- Responsive on all screen sizes

**Styling:**
- Professional wizard interface
- White background
- Blue primary color
- Progress indicators prominent
- Clear navigation between steps
- Helpful hints throughout
- Validation feedback

Design an intuitive, user-friendly submission wizard.
```

---

### Prompt 5.2: Submittal List & Details Page Design

```
Design the submittal list page and detail view for the Technical Submittal Automation System.

**List Page Layout:**
- Sidebar navigation
- Main content area

**Header:**
- Page title: "Submittals"
- New Submittal button (primary)
- Search bar with icon
- Filter icon

**Filter Section:**
- Search: "Search submittals..."
- Filter by:
  * Status (dropdown): all, draft, generated, reviewed, approved, archived
  * Product (multi-select)
  * Consultant (multi-select)
  * Date Range (from/to)
  * Created By (dropdown)
- Clear filters button
- Saved filters (optional)

**Submittals List:**
- Table with columns:
  * Checkbox (for bulk actions)
  * Submission Number (sortable)
  * Product (sortable)
  * Consultant (sortable)
  * Project Name
  * Status (with badge/color)
  * Pages
  * Generated Date (sortable)
  * Actions
- Pagination (20 per page)
- Bulk action toolbar (appears when items selected):
  * Delete selected
  * Archive selected
  * Export selected
  * Change status

**Row Actions:**
- View details (eye icon)
- Download (download icon)
- Duplicate/Generate Similar (copy icon)
- Delete (trash icon)
- More options (three dots):
  * Archive
  * Move to another product
  * Resend email
  * Change status

**Status Badges:**
- Draft: Orange
- Generated: Blue
- Reviewed: Purple
- Approved: Green
- Archived: Gray

**Empty State:**
- Large document icon
- Message: "No submittals generated yet."
- Generate Submittal button
- Link to templates

**Detail View (Modal or Side Panel):**
- Header with submission number and status badge
- Close button
- Tabs: Overview, Files, Compliance, Audit Trail

**Tab 1: Overview**
- Submission Number
- Product Name
- Consultant
- Project Name
- Project Code
- Status
- Generated Date/Time
- Generated By
- File Size
- Page Count
- Total Sections Included
- Edit metadata button (pencil icon)

**Tab 2: Files**
- Main PDF download button (large)
- Generated file info:
  * Filename
  * Size
  * Pages
  * Download button
  * Preview button
- Included documents list:
  * Document name
  * Type
  * Status
  * Download link

**Tab 3: Compliance**
- If compliance statements generated:
  * List of compliance statements
  * Each statement shows:
    - Requirement
    - Statement text
    - Confidence score (%)
    - Review status
    - Reviewer name
    - Actions: Edit, Delete

**Tab 4: Audit Trail**
- Timeline of all actions on this submittal:
  * Action (created, generated, reviewed, approved, downloaded, etc.)
  * Actor (user name)
  * Date/Time
  * Details
  * Timestamp

**Styling:**
- Professional list and detail views
- White background
- Blue primary color
- Status badges color-coded
- Clean typography
- Icons throughout
- Hover effects on rows

Design a comprehensive submittal management interface.
```

---

## 6. COMPLIANCE MANAGEMENT

### Prompt 6.1: Compliance Review Dashboard Design

```
Design a compliance review dashboard for the Technical Submittal Automation System.

**Layout:**
- Sidebar navigation
- Main content area

**Header:**
- Page title: "Compliance Review"
- Filter icon
- Stats summary bar showing:
  * Pending Review: X statements
  * Approved: X statements
  * Changes Needed: X statements

**Filter Section:**
- Filter by:
  * Status (pending review, approved, changes needed)
  * Submittal ID or Product
  * Confidence Score range (slider or range input)
  * Date range
  * Reviewer
- Clear filters button

**Compliance Statements Queue/List:**

**Card/Row Format for Each Statement:**
- Submittal reference:
  * Submission number (link to submittal)
  * Product name
  * Consultant name

- Statement content:
  * Requirement (bold)
  * AI-Generated Statement (quoted or boxed)
  * Confidence Score (visual indicator: percentage + color bar)
    - 90-100%: Green
    - 70-89%: Yellow/Amber
    - Below 70%: Red

- Metadata:
  * AI Model used (GPT-4, Claude, etc.)
  * Generated date
  * Source documents (list of documents used)

- Status badge and Actions:
  * Current status button/badge
  * Action buttons:
    - Approve (checkmark icon, green)
    - Request Changes (pencil icon, orange)
    - Reject (X icon, red)
  * View details button (arrow)

**Pagination:** 10-20 statements per page

**Empty State:**
- Checkmark icon
- Message: "All compliance statements reviewed!"
- Link to view approved statements

**Detail View (Modal):**
- Full statement content
- Confidence score with reasoning
- Source documents (expandable list)
- Suggested changes or issues (if any)
- Comments section
- Action buttons at bottom:
  * Approve
  * Request Changes
  * Reject
  * Cancel

**Request Changes Modal:**
- Text area for reviewer comments
- Dropdown for change type (minor, major, additional research needed)
- Button to return to author with changes

**Styling:**
- Clean, focused compliance review interface
- White background
- Blue primary color
- Confidence scores with visual indicators
- Color-coded status badges
- Professional typography
- Clear visual hierarchy

Design a streamlined compliance review interface.
```

---

### Prompt 6.2: Compliance Analysis Results Design

```
Design the compliance analysis results page/modal for the Technical Submittal Automation System.

**Layout:**
- Full page or large modal
- Header with back button, close button
- Main content area with tabs and sections

**Header:**
- Page title: "Compliance Analysis Results"
- Submittal reference (number, product, consultant)
- Analysis date and time
- AI model used badge

**Summary Section:**
- Overview cards:
  * Total Requirements Found: X
  * Compliance Statements Generated: X
  * Gaps Identified: X
  * Confidence Average: X%

**Tabs:**

**Tab 1: Extracted Requirements**
- Table with columns:
  * # (row number)
  * Requirement Text
  * Category (color badge)
  * Confidence (%)
  * Source Document
  * Actions (view, edit, delete)
- Expandable rows to see full requirement text
- Categories include: quality, safety, compliance, performance, etc.

**Tab 2: Compliance Statements**
- Each statement shows:
  * Requirement (bold)
  * Generated Statement (in box)
  * Source Documents (list with links)
  * Confidence Score (visual bar)
  * Status (pending, approved, rejected)
  * Actions: Edit, Approve, Reject, View Details

**Tab 3: Gap Analysis**
- Issues/Gaps Identified (if any)
- Each gap shows:
  * Requirement
  * Issue description
  * Risk level (High: red, Medium: orange, Low: yellow)
  * Recommended action
  * Possible solutions (if available)
- Empty state: "No gaps identified!"

**Tab 4: Source Documents**
- List of consultant requirement documents used
- For each document:
  * Document name
  * Upload date
  * File size
  * Download link
  * View metadata

**Bottom Action Bar:**
- Use Selected Statements button (primary)
- Edit Mode toggle
- Export Results button
- Back/Close button

**Styling:**
- Clean, analytical interface
- White background with light gray sections
- Blue primary, color-coded risk levels
- Confidence scores with visual indicators
- Professional typography
- Tables with alternating row colors
- Clear visual hierarchy

Design a comprehensive analysis results interface.
```

---

## 7. ADMIN & SETTINGS

### Prompt 7.1: User Management Page Design

```
Design a user management/admin page for the Technical Submittal Automation System.

**Layout:**
- Sidebar navigation (Admin section)
- Main content area

**Header:**
- Page title: "User Management"
- Add New User button (primary)
- Search bar
- Filter icon
- Export Users button (secondary)

**Filter Section:**
- Search: "Search users..."
- Filter by:
  * Role (dropdown: Admin, Operator, Reviewer, Viewer)
  * Status (active, inactive)
  * Department (if applicable)
- Clear filters button

**Users Table:**
- Columns:
  * Checkbox (bulk select)
  * Name (sortable)
  * Email (sortable)
  * Username (sortable)
  * Role (sortable, badge color-coded)
  * Status (active/inactive badge, sortable)
  * Last Login (sortable)
  * Actions

- Pagination (20 per page)

**Row Actions:**
- Edit (pencil icon) - opens edit modal
- View Profile (eye icon)
- Reset Password (key icon)
- Deactivate/Activate (toggle or button)
- Delete (trash icon) - with confirmation
- More options (three dots)

**Bulk Actions Toolbar** (when items selected):
- Change Role
- Change Status (activate/deactivate)
- Export Selected
- Delete Selected
- Send Message (email)

**User Roles Badges (Color-Coded):**
- Admin: Red/Purple
- Operator: Blue
- Reviewer: Orange
- Viewer: Gray

**Empty State:**
- Person icon
- Message: "No users yet. Invite your first user!"
- Add New User button

**Add/Edit User Modal:**
- Form fields:
  * Full Name (required)
  * Email (required, unique)
  * Username (required, unique)
  * Role (dropdown: required)
  * Status (active/inactive toggle)
  * Department (optional)
  * Phone (optional)
- Action buttons:
  * Save (primary)
  * Cancel
- For new users: Send invite email checkbox

**Reset Password Modal:**
- Message explaining action
- Option to:
  * Generate temporary password
  * Send reset link to email
- Show generated password (with copy button) or confirmation message

**Styling:**
- Professional admin interface
- White background
- Blue primary color
- Role badges color-coded
- Status indicators
- Clean table layout
- Professional typography

Design a comprehensive user management interface.
```

---

### Prompt 7.2: System Settings Page Design

```
Design a comprehensive system settings page for the Technical Submittal Automation System.

**Layout:**
- Sidebar navigation (Admin section)
- Left panel with settings categories
- Right panel with settings form

**Left Panel - Settings Categories:**
- General
- Company Information
- Database & Storage
- Email Configuration
- AI/LLM Integration
- Security
- API Keys
- Logs & Monitoring
- About

**Main Content Area:**

**Section 1: General Settings**
- Application Name (text input)
- Default Language (dropdown: English, Arabic)
- Time Zone (dropdown)
- Theme (toggle: Light/Dark)
- Date Format (dropdown)
- Number Format (dropdown)
- Save button

**Section 2: Company Information**
- Company Name (text input)
- Company Logo (upload)
- Company Email (text input)
- Company Phone (text input)
- Company Address (textarea)
- Company Website (text input)
- Save button

**Section 3: Storage Configuration**
- Storage Type (radio: Local, AWS S3, MinIO)
- For Local:
  * Storage Path (read-only)
  * Max Upload Size (MB)
- For AWS S3:
  * AWS Access Key (password input)
  * AWS Secret Key (password input)
  * S3 Bucket Name (text input)
  * AWS Region (dropdown)
  * Test Connection button
- For MinIO:
  * MinIO Host (text input)
  * MinIO Port (number input)
  * Bucket Name (text input)
  * Access Key (password input)
  * Secret Key (password input)
  * Test Connection button
- Storage Usage indicator (progress bar showing used/total)
- Backup settings:
  * Auto-backup enabled (toggle)
  * Backup frequency (dropdown)
  * Backup retention days (number)

**Section 4: Email Configuration**
- Email Service Type (radio: SMTP, SendGrid, Other)
- For SMTP:
  * SMTP Server (text input)
  * SMTP Port (number input)
  * Use TLS (toggle)
  * Username (text input)
  * Password (password input)
  * From Email (text input)
  * Test Email button
- Email templates selection (expandable)

**Section 5: AI/LLM Configuration**
- AI Provider (radio: OpenAI, Claude, Other)
- API Key (password input)
- Model Selection (dropdown):
  * For OpenAI: gpt-4, gpt-3.5-turbo, etc.
  * For Claude: claude-3-opus, claude-3-sonnet, etc.
- Temperature (slider: 0.0 - 1.0)
- Max Tokens (number input)
- Test API button
- Cost tracking (optional):
  * Show total API spend
  * Cost per operation

**Section 6: Security**
- Password Policy:
  * Minimum length (number input)
  * Require uppercase (toggle)
  * Require numbers (toggle)
  * Require special characters (toggle)
  * Password expiration days (number input)
- Session Timeout (minutes, number input)
- Enable Two-Factor Auth (toggle)
- IP Whitelist (textarea with IPs)
- Rate Limiting (toggle with limit input)
- CORS Allowed Origins (textarea)

**Section 7: API Keys**
- List of API Keys:
  * Key name
  * Created date
  * Last used date
  * Status (active/inactive)
  * Actions: View (masked), Regenerate, Delete
- Generate New Key button
- Secret display modal (show once, with copy button)

**Section 8: Logs & Monitoring**
- Log Level (dropdown: Debug, Info, Warning, Error)
- Enable Audit Logging (toggle)
- Log Retention Days (number input)
- View Logs button (opens logs page)
- Enable System Monitoring (toggle)
- Alert Email (text input)

**Section 9: About**
- Application Version
- Database Version
- API Documentation Link
- Support Contact
- License Information

**General Styling:**
- Professional admin interface
- White background
- Left sidebar with categories
- Settings grouped logically
- Form validation with helpful messages
- Required field indicators (*)
- Help text below key settings
- Save buttons at bottom or inline
- Unsaved changes warning

**Status Indicators:**
- Green checkmark for successful connections/tests
- Red X for failed connections
- Loading spinner during tests

Design a comprehensive system settings interface.
```

---

## 8. ADDITIONAL PAGES

### Prompt 8.1: Products Management Page Design

```
Design a products management page for the Technical Submittal Automation System.

**Layout:**
- Sidebar navigation
- Main content area

**Header:**
- Page title: "Products"
- Add New Product button (primary)
- Search bar
- Filter icon
- Bulk actions

**Filter Section:**
- Search: "Search products..."
- Filter by:
  * Category (dropdown)
  * Status (active/inactive)
  * Vendor (dropdown)
- Clear filters button

**Products Table/Grid:**
- Table Columns:
  * Checkbox
  * Product Name (sortable)
  * SKU (sortable)
  * Category (sortable, badge)
  * Vendor
  * Document Count
  * Template Count
  * Status (badge)
  * Last Updated
  * Actions

- OR Grid View:
  * Product cards with:
    - Product name
    - SKU
    - Category badge
    - Icon/image
    - Document count
    - Template count
    - Status
    - Hover: Edit, Delete, View Details buttons

**Row/Card Actions:**
- Edit (pencil)
- View Details (eye)
- Manage Documents (document icon)
- Manage Templates (template icon)
- Delete (trash)
- More options (three dots)

**Add/Edit Product Modal:**
- Form fields:
  * Product Name (required)
  * SKU/Code (required, unique)
  * Category (dropdown: required)
  * Description (textarea)
  * Vendor (dropdown)
  * Status (active/inactive)
  * Image Upload (optional)
- Save/Cancel buttons

**Product Details View:**
- Basic info
- Documents count and list
- Templates count and list
- Edit/Delete options

**Styling:**
- Professional product management
- White background
- Blue primary color
- Category badges color-coded
- Clean layout
- Icons throughout

Design a product management interface.
```

---

### Prompt 8.2: User Profile & Settings Page Design

```
Design a user profile and personal settings page for the Technical Submittal Automation System.

**Layout:**
- Sidebar navigation (User menu)
- Main content area

**Header:**
- Page title: "My Profile"
- Tabs: Profile, Preferences, Security, Notifications

**Tab 1: Profile**
- Profile Picture:
  * Current picture (circular)
  * Change/Upload button
  * Delete button

- Personal Information:
  * Full Name (editable text input)
  * Email (read-only or editable)
  * Username (read-only)
  * Phone (editable)
  * Department (editable dropdown)
  * Job Title (editable)
  * Bio (editable textarea)

- Account Information:
  * User ID (read-only)
  * Role (read-only with badge)
  * Account Created Date
  * Last Login Date/Time
  * Status (Active indicator)

- Save button
- Cancel button

**Tab 2: Preferences**
- Display Preferences:
  * Language (dropdown: English, Arabic)
  * Theme (radio: Light, Dark)
  * Time Zone (dropdown)
  * Date Format (dropdown)
  * Items per page (number input)

- Default Settings:
  * Default view on dashboard (dropdown)
  * Remember filters (toggle)
  * Default document view (list/grid)
  * Auto-archive old submittals (toggle with days)

- Notification Preferences:
  * Email on submittal generated (toggle)
  * Email on compliance review needed (toggle)
  * Digest frequency (dropdown: immediate, daily, weekly)

- Save button

**Tab 3: Security**
- Password Section:
  * Current password (password input)
  * New password (password input)
  * Confirm password (password input)
  * Password strength indicator
  * Password requirements (list)
  * Change Password button

- Two-Factor Authentication:
  * Status (enabled/disabled)
  * If enabled:
    - Show backup codes (protected)
    - Disable 2FA button
  * If disabled:
    - Enable 2FA button (opens setup flow)

- Active Sessions:
  * List of active sessions:
    - Device/Browser
    - Location
    - IP Address
    - Last active
    - Sign Out button
  * Sign Out All Other Sessions button

- Login History:
  * Table of recent logins:
    - Date/Time
    - Device
    - IP Address
    - Location

**Tab 4: Notifications**
- Notification Channels (toggles):
  * Email notifications
  * In-app notifications
  * SMS notifications (if available)

- Notification Types (checkboxes):
  * Submittal Generated
  * Compliance Review Needed
  * Document Uploaded
  * Template Modified
  * Security Alerts
  * System Maintenance
  * Weekly Digest
  * Monthly Report

- Notification Frequency (radio buttons for each type)

- Save button

**Styling:**
- Clean, professional profile interface
- White background
- Blue primary color
- Tabs clearly visible
- Form validation
- Success/error messages
- Required field indicators
- Help text where needed

Design a comprehensive user profile interface.
```

---

## DESIGN GUIDELINES

### General Styling Requirements for All Pages

```
**Color Palette:**
- Primary: #0066cc (Blue)
- Secondary: #f5f5f5 (Light Gray)
- Accent: #ff6b35 (Orange)
- Success: #28a745 (Green)
- Warning: #ffc107 (Yellow/Amber)
- Error: #dc3545 (Red)
- Text: #333333 (Dark Gray)
- Light Text: #666666 (Medium Gray)
- Background: #ffffff (White)
- Border: #e0e0e0 (Light Border)

**Typography:**
- Font Family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto
- Headings: Bold, line-height 1.2
- Body Text: Regular, line-height 1.5
- Buttons: Medium weight
- Monospace (for code): 'Courier New', monospace

**Spacing:**
- Use 8px base unit (8px, 16px, 24px, 32px, etc.)
- Padding: 16px for containers, 12px for inputs
- Margin: 16px between sections, 24px between major blocks

**Buttons:**
- Primary: Blue background, white text, rounded corners (4px)
- Secondary: Gray background, dark text
- Danger: Red background, white text
- Outline: Border only, no background
- Sizes: Small, Medium (default), Large
- States: Default, Hover, Active, Disabled, Loading

**Forms:**
- Input height: 40-44px
- Label above input, 8px gap
- Error state: Red border, red text below
- Success state: Green checkmark
- Placeholder text: Light gray (#999)
- Required indicator: Red asterisk *

**Tables:**
- Alternating row colors (white, #f9f9f9)
- Header row: Dark background, white text
- Hover row: Light blue background
- 1px gray borders between rows
- Padding: 12px per cell
- Sortable headers: Cursor pointer, hover effect

**Cards/Containers:**
- White background
- 1px border (#e0e0e0)
- Box shadow: 0 2px 4px rgba(0,0,0,0.1)
- Rounded corners: 4-8px
- Padding: 16-24px
- Hover: Slight shadow increase, cursor changes

**Responsive Design:**
- Mobile: < 768px - Stack columns, hide non-essential sidebars
- Tablet: 768px - 1024px - Adjusted spacing, collapsible sidebars
- Desktop: > 1024px - Full layout as designed

**Accessibility:**
- Minimum contrast ratio: 4.5:1 for text on background
- Focus states: Visible blue outline (2px)
- All images: Alt text
- Form labels: Properly associated with inputs
- Icons: Have aria-labels when used alone
- Keyboard navigation: Tab through all interactive elements

**Icons:**
- Size: 16px (small), 20px (medium), 24px (large)
- Use consistent icon set throughout
- Color: Match text color or use primary color
- Stroke width: Consistent across all icons

**Animations:**
- Transitions: 0.2s ease for hover effects
- Loading: Spinner animation
- Modal: Fade in with scale animation
- Sidebar: Slide in from left
- Notifications: Slide in from top right
- Keep animations smooth, not distracting

**Dark Mode (Optional):**
- Dark background: #1a1a1a
- Cards: #2a2a2a
- Text: #ffffff
- Adjust colors for contrast
```

---

## HOW TO USE THESE PROMPTS

### Step 1: Choose Your Pages
Select which pages you want to design first (start with auth and dashboard)

### Step 2: Copy the Prompt
Copy the entire prompt for that page

### Step 3: Paste into Claude Design
Open Claude Design and paste the prompt with this instruction:

```
"You are designing a professional web application. Please create a high-fidelity 
mockup following all specifications. Use the design guidelines provided. Create a 
professional, user-friendly interface suitable for a business application in the 
construction/material supply industry. Ensure all interactive elements are clearly 
shown with appropriate states."
```

### Step 4: Review & Iterate
Review the design and ask Claude Design for adjustments:
- "Make the buttons larger"
- "Change the color scheme"
- "Add more whitespace"
- "Make it more professional"
- "Add icons to the sidebar"

### Step 5: Export & Use
Export the design and share with your development team

---

## RECOMMENDED DESIGN ORDER

**Phase 1 (MVP):**
1. Login & Registration (Auth Pages)
2. Main Dashboard
3. Documents List & Upload
4. Templates List & Builder
5. Submittal Generator Wizard
6. Submittal List & Details
7. User Profile/Settings

**Phase 2 (Enhancements):**
8. Analytics Dashboard
9. Compliance Review Dashboard
10. Products Management
11. System Settings
12. User Management

**Phase 3 (Advanced):**
13. Compliance Analysis Results
14. Additional admin pages
15. Mobile responsive versions
16. Dark mode (optional)

---

**All prompts are ready to use with Claude Design. Start with the auth pages and dashboard for best results!**
