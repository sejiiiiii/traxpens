# Traxpens — Design System & Product Architecture Specification
*Document Version: 1.0.0 | Date: October 2026*
*Platform Target: Android Mobile & Responsive Web*

---

## 1. Executive Design Read & Philosophy

### Design Read Statement
> **Reading this as:** A daily financial utility and intelligent wealth allocation product for working professionals and salary earners, engineered with a minimal, modular, tactile, and Linear-tier precision aesthetic. It operates with zero visual clutter, absolute rejection of AI purple/violet gradients, and typography anchored by **Plus Jakarta Sans** and **JetBrains Mono**.

### Dial Configuration
| Dial | Level | Rationale |
| :--- | :---: | :--- |
| **`DESIGN_VARIANCE`** | **6 / 10** | Structured modularity with asymmetric bento cards; avoids chaotic layouts while rejecting boring cookie-cutter 3-column rows. |
| **`MOTION_INTENSITY`** | **5 / 10** | Purposeful spring physics (`stiffness: 120, damping: 22`) for feedback, sheets, and progress meters. Zero gratuitous looping animations. |
| **`VISUAL_DENSITY`** | **5 / 10** | Balanced daily utility; high numeric legibility without cramped cockpit overload. Whitespace is used as an active divider. |

### Core Tenets
1. **The 3-Second Frictionless Log:** Adding an expense must require no more than two taps and numeric input. Financial apps die when entry takes more than 5 seconds.
2. **Modular Paycheck-First Mental Model:** Money is not an abstract infinite stream. It begins with the monthly salary paycheck, partitioned via the **50/30/20 Rule** (Needs, Wants, Savings) while allowing user-defined custom categories and dynamic allocation.
3. **Adaptive Daily Spending Cap:** Budgets fail when users look at monthly lump sums. Traxpens recalculates an adaptive daily spending cap that adjusts daily based on current burn rate, remaining cycle days, and user-specified active timeframes (e.g., weekday vs weekend weighting).
4. **Economic Reality & Intelligent Insights:** Financial advice is contextualized with real-world macroeconomic guidance (inflation hedges, emergency cash yield, debt avoidance, index fund discipline).
5. **No AI Clichés:** Zero purple/violet gradients, zero floating stamps, zero unlabelled buttons, zero emojis in core system UI, zero generic system fonts (`Inter`, `Roboto`, `Arial` banned).

---

## 2. Color System & Surface Architecture

### Absolute Palette Rules
- **Single Accent Discipline:** The solitary accent is **Precision Emerald Teal** (`#0D9488` in light mode, `#14B8A6` in dark mode). It conveys financial security, liquidity, and growth without aggression.
- **Strict Prohibition:** All purple/violet/magenta/neon gradients are strictly banned.
- **Surface Depth:** No pure black (`#000000`). Dark mode utilizes rich OLED Charcoal (`#090A0F`), and light mode uses Clinical Canvas Mist (`#F8F9FA`).

### Semantic Color Tokens

```
/* ==========================================================================
   TRAXPENS DESIGN SYSTEM TOKENS
   ========================================================================== */

:root {
  /* LIGHT MODE (Clean, Clinical, Architectural) */
  --bg-canvas: #F8F9FA;
  --bg-surface: #FFFFFF;
  --bg-subtle: #F1F3F5;
  --bg-surface-elevated: #FFFFFF;

  --border-hairline: rgba(0, 0, 0, 0.07);
  --border-bezel: rgba(0, 0, 0, 0.04);
  --border-focus: #0D9488;

  --text-primary: #11141A;
  --text-secondary: #5A6270;
  --text-tertiary: #8C95A6;
  --text-inverse: #FFFFFF;

  /* Accent: Emerald Teal */
  --accent-primary: #0D9488;
  --accent-hover: #0F766E;
  --accent-subtle: #CCFBF1;
  --accent-contrast: #FFFFFF;

  /* Functional Status (Color-blind safe + backed by shape/copy) */
  --status-safe: #10B981;       /* Under 75% cap */
  --status-warning: #F59E0B;    /* 75% - 95% cap */
  --status-critical: #EF4444;   /* Exceeded cap */
  --status-neutral: #64748B;    /* Unallocated */

  /* 50/30/20 Categories */
  --cat-needs: #2563EB;         /* 50% Needs - Steady Azure */
  --cat-wants: #F59E0B;         /* 30% Wants - Vibrant Amber */
  --cat-savings: #0D9488;       /* 20% Savings - Precision Emerald */
  --cat-custom: #64748B;        /* Custom Buckets - Slate */
}

[data-theme="dark"] {
  /* DARK MODE (OLED, Restrained, High-Contrast) */
  --bg-canvas: #090A0F;
  --bg-surface: #12141C;
  --bg-subtle: #191C26;
  --bg-surface-elevated: #1F2330;

  --border-hairline: rgba(255, 255, 255, 0.08);
  --border-bezel: rgba(255, 255, 255, 0.03);
  --border-focus: #14B8A6;

  --text-primary: #F3F4F6;
  --text-secondary: #94A3B8;
  --text-tertiary: #64748B;
  --text-inverse: #090A0F;

  /* Accent: Precision Mint Teal */
  --accent-primary: #14B8A6;
  --accent-hover: #2DD4BF;
  --accent-subtle: rgba(20, 184, 166, 0.15);
  --accent-contrast: #090A0F;

  /* Functional Status */
  --status-safe: #34D399;
  --status-warning: #FBBF24;
  --status-critical: #F87171;
  --status-neutral: #94A3B8;

  /* 50/30/20 Categories */
  --cat-needs: #3B82F6;
  --cat-wants: #FBBF24;
  --cat-savings: #14B8A6;
  --cat-custom: #94A3B8;
}
```

---

## 3. Typography Architecture

### Font Stack Specification
- **Primary Display & Interface:** `Plus Jakarta Sans`, sans-serif.
  - *Weights:* Medium (500), SemiBold (600), Bold (700).
  - *Tracking:* `-0.02em` for headlines; `0` for body.
  - *Rationale:* Geometric clarity with generous x-height, distinct letterforms, and zero generic "Inter" fatigue.
- **Numerical & Financial Data:** `JetBrains Mono`, monospace.
  - *Weights:* Regular (400), SemiBold (600).
  - *Tracking:* `-0.01em`, tabular numbers (`font-variant-numeric: tabular-nums`).
  - *Rationale:* Ensures financial columns align with millimeter precision; eliminates number shifting during dynamic updates.

### Type Scale

| Level | Size (rem / px) | Line Height | Weight | Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Display H1** | `2.25rem / 36px` | `1.15` | 700 Bold | App dashboard balance hero, monthly salary total |
| **Headline H2** | `1.5rem / 24px` | `1.25` | 600 SemiBold | Section headings, module titles |
| **Subhead H3** | `1.125rem / 18px` | `1.35` | 600 SemiBold | Bento card titles, modal headers |
| **Body Large** | `1rem / 16px` | `1.5` | 500 Medium | Primary inputs, main list labels |
| **Body Regular** | `0.875rem / 14px` | `1.4` | 400 Regular | Supporting copy, economic guide text |
| **Caption/Micro** | `0.75rem / 12px` | `1.3` | 600 SemiBold | Category badges, timestamp metadata, percentage chips |
| **Mono Primary** | `1.25rem / 20px` | `1.2` | 600 SemiBold | Expense amount numbers, remaining daily cap |
| **Mono Micro** | `0.8125rem / 13px` | `1.2` | 500 Medium | Split ratios (50% / 30% / 20%), date counters |

---

## 4. Hardware-Inspired Component Architecture (The Double-Bezel)

To achieve the tactile "$150k agency finish" outlined in the `high-end-visual-design` skill:

### The Doppelrand (Double-Bezel) Card Structure
Cards are never flat rectangles. They are engineered like machined hardware trays:
1. **Outer Shell (`tray`):**
   - Padding: `p-1.5` (6px) or `p-2` (8px).
   - Radius: `rounded-[20px]`.
   - Border: Hairline stroke `border border-[var(--border-bezel)]`.
   - Background: `bg-[var(--bg-subtle)]`.
2. **Inner Core (`plate`):**
   - Radius: `rounded-[14px]` (concentric with outer shell).
   - Background: `bg-[var(--bg-surface)]`.
   - Inner Highlight: `shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]` (dark) or `shadow-[inset_0_1px_0_rgba(255,255,255,0.8)]` (light).
   - Padding: `p-4` to `p-5`.

### Button-in-Button CTA
Primary action buttons utilize nested trailing glyph containers:
- Base: Fully rounded pill `rounded-full px-5 py-3 font-semibold text-sm bg-[var(--accent-primary)] text-[var(--accent-contrast)]`.
- Nested Trailing Capsule: `ml-3 w-7 h-7 rounded-full bg-black/10 dark:bg-white/15 flex items-center justify-center transition-transform group-hover:translate-x-0.5`.

---

## 5. Core Feature Specifications

### A. The Monthly Salary & Modular Allocation Engine (50/30/20 + Custom)
- **Base Anchor:** User defines Monthly Net Paycheck (e.g., $5,000 / €4,200 / ₹1,00,000) and Payday Cycle (1st of month, 25th, or custom interval).
- **Default 50/30/20 Partition:**
  1. **Needs (50%):** Fixed essentials — Rent/Mortgage, Utilities, Groceries, Insurance, Commute.
  2. **Wants (30%):** Discretionary — Dining out, Streaming/Subscriptions, Shopping, Hobbies, Leisure.
  3. **Savings & Investments (20%):** Future wealth — Emergency cushion, Index funds (S&P 500 / Total Market), Retirement, Debt payoff.
- **Modular Customization:**
  - Dynamic Slider & Direct % / $ inputs: Adjust to 60/20/20, 40/30/30, or custom proportions.
  - Custom Category Creator: Add custom buckets (e.g., "Kids Education", "Side Project", "Vacation Fund") with custom color tags and allocation rules.
  - Overspend Spillover Protection: If "Needs" swell beyond 50%, the engine prompts automated deduction from "Wants" to preserve the 20% Savings floor.

### B. Dynamic Daily Spending Cap
- **Formula:**
  $$\text{Daily Cap} = \frac{\text{Remaining Unallocated Discretionary (Wants)} - \text{Planned Upcoming Bills}}{\text{Days Remaining Until Payday}}$$
- **Time-Period Customization:**
  - *Standard Mode:* Equal division across remaining days.
  - *Weekend Weighted Mode:* Automatically allocates 1.5× budget to Friday–Sunday and compresses Monday–Thursday.
  - *Custom Date Range:* Allows locking a specific event window (e.g., "3-day trip" cap without breaking monthly baseline).
- **Visual Gauge:** Circular or bar progress meter with tactile threshold states:
  - 0–75% spent: Safe (Emerald)
  - 75–95% spent: Caution (Amber)
  - 100%+ spent: Cap Exceeded (Coral Red with smart recalculation showing tomorrow's revised lowered allowance).

### C. The 2-Tap Frictionless Expense Logger
- **Tap 1:** Tap persistent floating quick-action pill or press `N` shortcut.
- **Entry:** Large keypad-friendly numeric input (`JetBrains Mono` 32px), pre-focused.
- **Category Selection:** 4 immediate pill chips (Needs, Wants, Custom, or recent categories like "Lunch", "Coffee", "Transit").
- **Tap 2:** Tap "Log Expense" or press Enter. Immediate haptic tick, sheet slides away, daily cap recalculates instantly.

### D. Economic Reality Guides & Intelligent Insights
- Real-world, non-gimmicky financial intelligence cards updated based on current economic trends:
  1. *Cash Optimization:* "High-Yield Cash vs Inflation: Keep 3–6 months of Needs in 4.5%+ liquid cash; route excess to diversified index funds."
  2. *Subscription Audit:* "Phantom Bleed: You have 6 recurring digital subscriptions totaling $84/mo ($1,008/yr). Review usage."
  3. *50/30/20 Health Score:* Benchmark comparing actual monthly velocity against the planned baseline.
  4. *Payday Projection:* Forecast showing projected surplus balance on day 30 if current spending rate continues.

---

## 6. Multi-Platform Ergonomics (Android Mobile & Responsive Web)

### Android Mobile (360px – 430px)
- **Thumb Zone Compliance:**
  - All high-frequency actions (Quick Log CTA, Navigation Tabs, Date filter toggles) live in the bottom 35% of the screen.
  - Minimum touch target: `48dp × 48dp` (minimum 8dp spacing between targets).
  - Bottom navigation bar with 4 core views: **Dashboard**, **Allocations (50/30/20)**, **Activity Log**, **Guides & Insights**.
  - Bottom Sheet drawer for manual expense logging with swipe-down-to-dismiss gesture.

### Responsive Web (768px – 1440px+)
- **Desktop Layout:**
  - Left persistent minimal rail (collapsed to 72px icons or expanded 240px drawer).
  - Central 2-column or Asymmetric Bento Grid:
    - *Column 1 (Span 7):* Salary Breakdown card + Dynamic Daily Spending Cap gauge + Real-time Expense Timeline.
    - *Column 2 (Span 5):* 50/30/20 Modular Allocator + Economic Guides & Macro Insights.
  - Keyboard Navigation: `Cmd/Ctrl + N` for quick log, `1-4` for category selection, `Esc` to dismiss modals.

---

## 7. Motion Choreography & Transitions
- **Spring Curve:** `cubic-bezier(0.32, 0.72, 0, 1)` (snappy entry, gentle settle).
- **Duration Scale:**
  - Micro-interactions (button press, toggle): `150ms`.
  - Sheet slide-up / modal fade: `280ms`.
  - Progress bar width / gauge fill: `600ms ease-out`.
- **Accessibility:** Full support for `prefers-reduced-motion: reduce`. All transforms fall back to instantaneous opacity shifts.
