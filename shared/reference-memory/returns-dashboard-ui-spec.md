# UI Developer Specification: Returns Exception Dashboard

## 1. Overview
This specification covers the **Search Understanding & Scope** view for the Returns/Exception reporting dashboard. The UI is characterized by a dark-mode side navigation, a light-mode main content area with top horizontal routing tabs, and a dense, data-rich 4-column layout focusing on actionable aggregates.

## 2. Global Design Tokens

### Typography
*   **Primary Font:** `Inter` (sans-serif)
*   **Weights:** 
    *   Regular (400) - Body text
    *   Medium (500) - Secondary labels, Tabs
    *   SemiBold/Bold (600/700) - Headers, Primary Metrics

### Color Palette
*   **Brand / Active (Emerald):**
    *   Primary: `#059669` (Emerald 600) - Active states, success indicators.
    *   Background/Subtle: `#D1FAE5` (Emerald 100)
*   **Navigation (Slate):**
    *   Sidebar Background: `#0F172A` (Slate 900)
    *   Sidebar Borders: `#1E293B` (Slate 800)
*   **Alerts & Status:**
    *   Error/Returned (Rose): Text `#E11D48` (Rose 600), Background `#FFE4E6` (Rose 100)
    *   Warning (Amber): Text `#92400E` (Amber 800), Background `#FEF3C7` (Amber 50)
    *   Action/Active Window (Blue): Text `#2563EB` (Blue 600)
*   **Base & Surfaces:**
    *   App Background: `#F9FAFB` (Gray 50)
    *   Card Surfaces: `#FFFFFF` (White)
    *   Text Primary: `#111827` (Gray 900)
    *   Text Secondary: `#6B7280` (Gray 500)

---

## 3. Layout Architecture

### A. App Shell
*   **Sidebar (Left):** 
    *   Fixed width on desktop (e.g., `256px` or `w-64`).
    *   Full height (`h-screen`).
    *   Hidden or collapsed into a hamburger menu on mobile devices (`< md` breakpoint).
*   **Main Workspace (Right):**
    *   Takes remaining width (`flex-1`).
    *   Independent vertical scrolling.
    *   Contains an inner container with a max-width (e.g., `max-w-[1600px]`) to maintain readability on ultra-wide monitors.

### B. Header & Navigation Tabs
*   **Breadcrumbs:** `<Section> / <Category> / <Current Page>` format. Font-size: `sm`.
*   **Page Title:** `text-2xl`, bold.
*   **Horizontal Tabs:**
    *   5 standard tabs: *All Wires, Outgoing Wires, Incoming Wires, International Wires, Alerts & Notifications*.
    *   **Active Tab State:** Bottom border (2px solid Emerald), Emerald text, heavier font weight.
    *   **Inactive Tab State:** Transparent border, Gray text, Medium font weight. Hover state adds a light gray bottom border.

---

## 4. Core Components & "Aggregates"

### 4.1 Item Lifecycle History (4 Step Aggregates)
*   **Position:** Spans the full width of the data container above the grid.
*   **Layout:** Horizontal flex container with a connecting absolute-positioned gray line running through the center of the icons.
*   **The 4 Steps:**
    1.  **Deposited:** Solid green checkmark, `Emerald 100` background.
    2.  **Initially Collected:** Solid green checkmark, `Emerald 100` background.
    3.  **Returned NSF:** Red 'X' icon, `Rose 100` background, red text for timestamps.
    4.  **Eligible For Representment:** Blue indicator (dot), white background with blue ring. This represents the current/active state.

### 4.2 Data Grid (4-Column Desktop Layout)
Below the lifecycle timeline, content is divided into a CSS Grid (`grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6`).

#### Column 1: Item Details & Related Transactions
*   **UI:** Standard Key-Value pairs with horizontal flex layout (`justify-between`).
*   **Return Code Badge:** Requires a specific inline pill badge (Rose background, Rose text, small text size).

#### Column 2: Relationship Insights (4 Metric Aggregates)
*   **UI:** 2x2 CSS Grid inside a white card.
*   **The 4 Metrics:**
    1.  **Relationship:** Blue-tinted box. Big Number: "7 Years".
    2.  **Total Deposits:** Emerald-tinted box. Big Number: "$8.4M".
    3.  **Items Returned:** Amber-tinted box. Big Number: "4". Include subtitle text "NSF Rate".
    4.  **Recent Trend:** Gray-tinted box. Big Text: "Stable".
*   **Alert Box:** Positioned below the 2x2 grid. Amber background, Amber border, contains an alert icon and text regarding threshold limits.

#### Column 3: Recommended Actions
*   **UI:** Vertical list of actionable items.
*   **Styling:** Each item has a thick left border. 
    *   Primary recommendation (Item 1) has an `Emerald 500` left border.
    *   Secondary recommendations have a `Gray 200` border that transitions on hover.
*   **Typography:** Bold title, gray subtitle, and a colored text-link with an arrow (`&rarr;`) for the call to action.

#### Column 4: Quick Recovery Actions (4 Action Aggregates)
*   **UI:** 2x2 Grid of square/rectangular buttons.
*   **The 4 Actions:**
    1.  **Represent Item** (Emerald icon)
    2.  **Suggest Date** (Emerald icon)
    3.  **Alert Me** (Blue icon)
    4.  **Monitor Rule** (Blue icon)
*   **Interaction:** 
    *   Hovering over a button should change the border color to match the icon color.
    *   Apply a slight scaling effect (`scale-110`) to the SVG icon on button hover to encourage clickability.

---

## 5. Responsive Behavior
*   **Mobile (< 768px):** 
    *   Sidebar hides behind a toggle.
    *   Horizontal tabs become scrollable via `overflow-x-auto`.
    *   The 4-column data grid stacks vertically (`grid-cols-1`).
    *   Item Lifecycle History layout must maintain proportions or switch to a vertical timeline if horizontal space is strictly limited.
*   **Tablet (768px - 1280px):** 
    *   Data grid collapses to 2 columns (`grid-cols-2`).
*   **Desktop (> 1280px):** 
    *   Full 4-column display (`xl:grid-cols-4`).