---
name: Atmospheric DevOps System
colors:
  surface: '#0e1416'
  surface-dim: '#0e1416'
  surface-bright: '#343a3c'
  surface-container-lowest: '#090f11'
  surface-container-low: '#171d1e'
  surface-container: '#1b2122'
  surface-container-high: '#252b2d'
  surface-container-highest: '#303638'
  on-surface: '#dee3e6'
  on-surface-variant: '#bcc9cd'
  inverse-surface: '#dee3e6'
  inverse-on-surface: '#2b3133'
  outline: '#869397'
  outline-variant: '#3d494c'
  surface-tint: '#4cd7f6'
  primary: '#4cd7f6'
  on-primary: '#003640'
  primary-container: '#06b6d4'
  on-primary-container: '#00424f'
  inverse-primary: '#00687a'
  secondary: '#fbabff'
  on-secondary: '#580065'
  secondary-container: '#ae05c6'
  on-secondary-container: '#ffd8fd'
  tertiary: '#ffb873'
  on-tertiary: '#4b2800'
  tertiary-container: '#e89337'
  on-tertiary-container: '#5b3200'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#acedff'
  primary-fixed-dim: '#4cd7f6'
  on-primary-fixed: '#001f26'
  on-primary-fixed-variant: '#004e5c'
  secondary-fixed: '#ffd6fd'
  secondary-fixed-dim: '#fbabff'
  on-secondary-fixed: '#36003e'
  on-secondary-fixed-variant: '#7c008e'
  tertiary-fixed: '#ffdcbf'
  tertiary-fixed-dim: '#ffb873'
  on-tertiary-fixed: '#2d1600'
  on-tertiary-fixed-variant: '#6a3b00'
  background: '#0e1416'
  on-background: '#dee3e6'
  surface-variant: '#303638'
typography:
  h1:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  h2:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.4'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.1em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  xxl: 64px
---

## Brand & Style

This design system targets high-performance engineering environments, evoking a sense of "mission control" sophistication. The aesthetic is rooted in **Glassmorphism** and **Futurism**, utilizing deep spatial depth and luminous accents to prioritize critical data visualization. 

The brand personality is authoritative yet innovative, designed to make complex DevOps workflows feel tactile and manageable. The emotional response is one of calm focus, achieved through a dark, low-fatigue background contrasted against high-energy neon signals that guide the eye to system statuses and performance metrics.

## Colors

The palette is anchored by a "Deep Midnight" foundation. Backgrounds use a solid `#020617` to ensure infinite depth, while surfaces utilize a semi-transparent slate to support glass effects.

- **Primary Action:** A high-vibrancy Cyan-to-Blue gradient reserved for "Execute" actions, successful deployments, and active states.
- **Alert/Critical:** A Magenta-to-Crimson gradient used sparingly for system failures, breaking changes, or high-priority incident responses.
- **Data Visualization:** Use the specific Neon hex codes for chart paths. Every stroke should include a 4px Gaussian blur "outer glow" of the same color at 30% opacity to simulate light emission.

## Typography

This design system employs a tri-font hierarchy to balance technical precision with readability.

1. **Geist** is used for headlines to provide a sharp, technical "tech-native" feel.
2. **Inter** handles all standard UI text and body copy for maximum legibility during long sessions.
3. **JetBrains Mono** is strictly reserved for technical data, logs, terminal outputs, and metadata labels to reinforce the DevOps aesthetic.

All headings should be rendered in high-contrast white (`#FFFFFF`), while body text should use a slightly muted silver (`#CBD5E1`) to reduce visual noise.

## Layout & Spacing

The system uses a **12-column fluid grid** with generous margins to allow the glassmorphic panels "room to breathe." 

- **Containers:** Content should be grouped into logical "Modules" or "Clusters."
- **Padding:** Use a strict 4px base scale. Standard card internal padding is `24px (lg)`.
- **Density:** Use `md` spacing for interactive controls and `lg` or `xl` for structural separation between different system views.

## Elevation & Depth

Depth is conveyed through **Backdrop Blurs** and **Layered Translucency** rather than traditional drop shadows.

1. **The Floor (Level 0):** Solid `#020617`.
2. **Standard Panels (Level 1):** `rgba(15, 23, 42, 0.6)` with a `20px` backdrop-filter blur. A `1px` border of `rgba(255, 255, 255, 0.08)` must be applied to define edges.
3. **Floating Modals (Level 2):** `rgba(30, 41, 59, 0.8)` with a `40px` backdrop-filter blur. These should include a subtle "Inner Glow" (top-down) using a white-to-transparent linear gradient at 5% opacity to simulate overhead light hitting the glass edge.
4. **Active State Glow:** When an element is focused or active, it emits a `0px 0px 15px` outer glow using its primary accent color.

## Shapes

The shape language is "Soft-Tech." We avoid fully circular edges (except for status pips) and aggressive sharp corners. 

- **Default Radius:** `0.25rem` (4px) for small components like inputs and tags.
- **Large Radius:** `0.75rem` (12px) for main dashboard panels and cards.
- **Status Indicators:** 8px circles with a 100% border radius and a 4px blur glow to represent "living" system statuses (running, failed, pending).

## Components

- **Buttons:** Primary buttons use the Cyan-Blue gradient with white text. Ghost buttons use a `1px` border and no fill, inheriting the text color of the primary gradient.
- **Inputs:** Darker than the panel surface (`rgba(0, 0, 0, 0.3)`) with a subtle `1px` bottom-only border that illuminates to full Cyan on focus.
- **Glass Cards:** The primary container for metrics. Must feature a "Glass Highlight"—a 1px semi-transparent line on the top and left edges to simulate thickness.
- **Charts:** Line charts use a `2px` stroke width. Paths must have a "trailing glow" effect. Area charts use a vertical gradient from the accent color (at 20% opacity) to 0% opacity at the baseline.
- **Status Chips:** Small, pill-shaped indicators. "Healthy" uses a Cyan glow; "Warning" uses a Magenta glow; "Critical" uses a Crimson pulse animation.
- **Terminal/Log View:** High-contrast background (`#000000`) with JetBrains Mono text. Key syntax highlighting should follow the Cyan and Magenta accent palette.