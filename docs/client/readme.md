# 🖥️ Client (Next.js) Setup Guide

## Table of Contents

- [CSS/SCSS Structure & Utilities](#cssscss-structure--utilities)
  - [Color Utility Classes](#-color-utility-classes)
  - [Width & Height Utility Classes](#-width--height-utility-classes)
  - [Border Utility Classes](#-border-utility-classes)
  - [Margin & Padding Utility Classes](#-margin--padding-utility-classes)
  - [Heading Utility Classes](#-heading-utility-classes)
  - [Font Utility Classes](#-font-utility-classes)
  - [Display Utility Classes (Responsive Visibility)](#-display-utility-classes-responsive-visibility)
  - [Other Utility & Customization Classes](#-other-utility--customization-classes)
    - [Scrollbar Customization](#scrollbar-customization)
    - [Text Truncation](#text-truncation)
    - [Form Required Indicator](#form-required-indicator)
    - [Link Styling](#link-styling)
    - [Position Utilities](#position-utilities)
  - [Global and Custom Classes](#-global-and-custom-classes)
  - [Responsive Mixins](#-responsive-mixins)
  - [Component-Level Modular SCSS](#-component-level-modular-scss)
- [Reusable Base Components](#-reusable-base-components)
  - [Div](#-div-component)
  - [Accordion](#-accordion-component)
  - [AnimateContainerOnScroll](#-animatecontaineronscroll-component)
  - [Anchor](#anchor-component)
  - [AppImage](#-appimage-component)
  - [AppVideo](#-appvideo-component)
  - [Button](#-button-component)
  - [Carousel](#-carousel-component)
  - [DivConvertTextToHtml](#-divconverttexttohtml-component)
  - [Heading](#-heading-component)
  - [Icon](#-icon-component)
  - [Paragraph](#-paragraph-component)
  - [SVGIcon](#-svgicon-component)
  - [Table](#-table-component)
- [Form Components](#-form-components)
  - [Form](#-form-component)
  - [TextBox](#-textbox-component)
  - [Select](#-select-component)
  - [DatePicker](#-datepicker-component)
  - [CheckBox](#-checkbox-component)
  - [MediaPicker](#-mediapicker-component)
- [Page Parts](#-page-parts)
  - [Alert](#-alert-component)
  - [Modal & PromptMessage](#-modal--promptmessage-components)
- [Custom React Hooks](#-custom-react-hooks-documentation)
  - [useApiCalls](#-useapicalls)
  - [useDivWidth](#-usedivwidth)
  - [useWebSocket](#-usewebsocket)

This document explains the structure and conventions of the frontend client, built with Next.js and React, including custom SCSS, base components, main components, and Redux state management.

---

## 🎨 SCSS & CSS Class Conventions

# 🏷️ CSS Class Patterns

The project uses a utility-first and BEM-inspired class naming convention. Each pattern is described below with usage and examples.

---

## 🎨 Color Utility Classes

Color-related utility classes allow you to quickly set background, text, and border colors using semantic or palette-based names defined in SCSS variables.

### Background Color

- Pattern: `bg-{color}`
- Example classes: `bg-red`, `bg-blue`, `bg-theme-one`, `bg-primary`, `bg-secondary`

### Text Color

- Pattern: `text-{color}`
- Example classes: `text-primary`, `text-secondary`, `text-theme-two`, `text-white`, `text-black`

### Border Color

- Pattern: `border-{color}`
- Example classes: `border-gray`, `border-theme-three`, `border-primary`, `border-danger`

All available `{color}` values are defined as SCSS variables in `src/assets/styles/`.

- **General colors** (e.g., `red`, `blue`, `gray`) are managed in `src/assets/styles/general/base/_variables.scss` as a SCSS map:
  ```scss
  $colors: (
    "red": red,
    "blue": blue,
    ...,
  );
  ```
- **Branding colors** (e.g., `theme-one`, `theme-two`) are managed in a separate SCSS map, for example:
  ```scss
  $brandingColors: (
    "theme-one": #c5ff4a,
    // Add or update branding colors here
  );
  ```

To add or update a color:

1. Edit the appropriate SCSS map (`$colors` for general, `$brandingColors` for branding).
2. Add or update the color entry (e.g., `'theme-two': #abcdef,`).
3. The utility classes will automatically pick up the new or updated color if the SCSS is set up to loop through these maps.

**Example usage:**

```html
<div class="bg-theme-one text-white border-red">Themed content</div>
```

---

## 📏 Width & Height Utility Classes

Width and height utility classes allow you to set min, max, and fixed sizes using both percentage and pixel values, as well as viewport-based heights.

### Width Patterns

- Percentages (from `$widthPercentages`):
  - `min-width-per-{val}`: Minimum width as a percentage (e.g., `min-width-per-50` → `min-width: 50%;`)
  - `width-per-{val}`: Width as a percentage (e.g., `width-per-75` → `width: 75%;`)
  - `max-width-per-{val}`: Maximum width as a percentage (e.g., `max-width-per-100` → `max-width: 100%;`)
- Pixels (from `$widthPx`):
  - `min-width-px-{val}`: Minimum width in px (e.g., `min-width-px-200` → `min-width: 200px;`)
  - `width-px-{val}`: Width in px (e.g., `width-px-300` → `width: 300px;`)
  - `max-width-px-{val}`: Maximum width in px (e.g., `max-width-px-1200` → `max-width: 1200px;`)
- Inherit: `width-inherit` → `width: inherit;`

### Height Patterns

- Pixels (from `$boxHeighs`):
  - `min-height-px-{val}`: Minimum height in px (e.g., `min-height-px-100` → `min-height: 100px;`)
  - `height-px-{val}`: Height in px (e.g., `height-px-400` → `height: 400px;`)
  - `max-height-px-{val}`: Maximum height in px (e.g., `max-height-px-800` → `max-height: 800px;`)
- Viewport heights:
  - `min-height-vh-full` → `min-height: 100vh;`
  - `min-height-vh-half` → `min-height: 50vh;`
  - `min-height-vh-one-fourth` → `min-height: 25vh;`
  - `min-height-vh-three-fourth` → `min-height: 75vh;`
  - `min-height-vh-one-third` → `min-height: 33.33333333vh;`
  - `min-height-vh-two-third` → `min-height: 66.66666666vh;`
  - (same for `height-vh-*` and `max-height-vh-*`)

### How It Works

- The SCSS loops through all values in `$widthPercentages`, `$widthPx`, and `$boxHeighs` to generate the classes automatically.
- To add or update size options, edit the relevant variable map.

**Example usage:**

```html
<div class="width-per-75 height-px-400">Sized content</div>
<div class="min-height-vh-half max-width-px-1200">Responsive box</div>
```

---

## ⬛ Border Utility Classes

Border utility classes allow you to control border width, style, radius, and direction using variables defined in both general and branding SCSS files.

### Border Class Pattern

- Pattern: `br-{dir}-{type}-{size}`
  - `{dir}`: Direction (`top`, `left`, `right`, `bottom`, or omit for all sides)
  - `{type}`: Border style (`solid`, `dashed`, `dotted`, etc. from `$borderStyles`)
  - `{size}`: Thickness (from `$borderThickness` or branding values)

#### Examples

- `br-top-solid-2` → `border-top: 2px solid;`
- `br-bottom-dashed-4` → `border-bottom: 4px dashed;`
- `br-solid-1` → `border: 1px solid;` (all sides)

### Border Radius

- There are three main patterns for border radius utility classes:

  1. `br-rad-px-{size}`: Sets border-radius in pixels. `{size}` can be any value from `$borderRadius` (e.g., `br-rad-px-5` → `border-radius: 5px;`).
  2. `br-rad-per-{percentage}`: Sets border-radius in percent. `{percentage}` can be any value from `$borderPercentRadius` (e.g., `br-rad-per-50` → `border-radius: 50%;`).
  3. `br-rad-{branding}`: Uses a named value from branding variables in `$brandingBorderRads` (e.g., `br-rad-md` → `border-radius: 8px;`).

**Examples:**

- `br-rad-px-5` → `border-radius: 5px;`
- `br-rad-per-50` → `border-radius: 50%;`
- `br-rad-lg` → `border-radius: 12px;` (from branding)

Branding border radii are defined in `src/assets/styles/branding/base/_variables.scss`:

```scss
$brandingBorderRads: (
  "sm": 4px,
  "md": 8px,
  "lg": 12px,
  "xl": 16px,
  "2xl": 20px,
  "3xl": 24px,
);
```

### Border Color

- Pattern: `border-{color}` (see Color Utility Classes section)
- Example: `border-theme-one` → `border-color: #c5ff4a;`

#### Variables

- General border thickness, radius, and styles are defined in `src/assets/styles/general/base/_variables.scss`:
  - `$borderThickness`, `$borderRadius`, `$borderPercentRadius`, `$borderStyles`, `$directions`
- Branding border radii are defined in `src/assets/styles/branding/base/_variables.scss`:
  - `$brandingBorderRads`

To add or update border options, edit the relevant SCSS variable maps.

---

## 📏 Margin & Padding Utility Classes

Margin and padding utility classes allow you to quickly apply spacing to elements using both general and branding spacing variables.

### General Spacing Patterns

- Sizing values are defined in `$spaceamounts` (from 0 to 100) in `src/assets/styles/general/base/_variables.scss`.
- Patterns:
  - `m-all-{size}`: All margins (e.g., `m-all-2` → `margin: 2px;`)
  - `m-t-{size}`: Top margin
  - `m-b-{size}`: Bottom margin
  - `m-l-{size}`: Left margin
  - `m-r-{size}`: Right margin
  - `m-x-{size}`: Horizontal margins (left & right)
  - `m-y-{size}`: Vertical margins (top & bottom)
  - `p-all-{size}`: All paddings
  - `p-t-{size}`: Top padding
  - `p-b-{size}`: Bottom padding
  - `p-l-{size}`: Left padding
  - `p-r-{size}`: Right padding
  - `p-x-{size}`: Horizontal paddings
  - `p-y-{size}`: Vertical paddings
- Example: `m-x-2` → `margin-left: 2px; margin-right: 2px;`
- Example: `p-y-10` → `padding-top: 10px; padding-bottom: 10px;`
- Special: `m-l-auto`, `m-r-auto` for auto margins.

### Branding Spacing Patterns

- Sizing values are defined in `$brandingSpacings` in `src/assets/styles/branding/base/_variables.scss`.
- Patterns are the same as above, but use branding names (e.g., `temp-1`, `temp-2`, ...):
  - `m-all-{branding}`: All margins (e.g., `m-all-temp-2` → `margin: 8px;`)
  - `p-x-{branding}`: Horizontal paddings (e.g., `p-x-temp-4` → `padding-left: 16px; padding-right: 16px;`)
- Example: `m-y-temp-5` → `margin-top: 20px; margin-bottom: 20px;`

### How It Works

- The SCSS loops through all values in `$spaceamounts` and `$brandingSpacings` to generate the classes automatically.
- To add or update spacing options, edit the relevant variable map.

**Example usage:**

```html
<div class="m-x-2 p-y-temp-4">Spaced content</div>
```

---

## 🅷 Heading Utility Classes

Heading styles are generated for all heading levels (`h1`–`h6`) using responsive font sizes and weights defined in branding variables.

### Pattern

- Each heading (`h1`–`h6`) automatically receives styles for width, font family, and responsive font size.
- Font sizes are set using the `$brandingHeadingFontSizes` map for each heading and breakpoint:
  - `h1-xs`, `h1-sm`, `h1-md`, `h1-lg`, ...
  - `h2-xs`, `h2-sm`, ... up to `h6-lg`
- Font weight is set by `$brandingFontHeadingWeight` (e.g., `bold`).

### Variables

- Font sizes: `$brandingHeadingFontSizes` in `src/assets/styles/branding/base/_variables.scss`
- Font weight: `$brandingFontHeadingWeight`

## To update heading styles, edit the relevant variables in the branding SCSS file.

## 🔤 Font Utility Classes

Font utility classes allow you to control font size and weight using both general and branding variables.

### General Font Patterns

- Font sizes in pixels: `f-s-px-{size}` (from `$fontPxArray`, e.g., `f-s-px-16` → `font-size: 16px;`)
- Font sizes in rem: `f-s-qr-rem-{size}` (from `$fontRemArray`, e.g., `f-s-qr-rem-4` → `font-size: 1rem;`)
- Font weights: `f-w-{weight}` (from `$fontWeightArray`, e.g., `f-w-700` → `font-weight: 700;`)
- Bold: `f-b` → `font-weight: bold;`
- Italic: `f-i` → `font-style: italic;`

General font variables are defined in `src/assets/styles/general/base/_variables.scss`:

```scss
$fontPxArray: $zeroTo100;
$fontRemArray: (1, 2, ..., 16);
$fontWeightArray: (100, 200, ..., 1000);
```

### Branding Font Patterns

- Font sizes: `f-s-{branding}` (from `$brandingFontSizes`, e.g., `f-s-small-xs` → `font-size: 12px;`)
- Font categories (responsive): `f-s-{category}` (from `$brandingFontCategories`, e.g., `f-s-regular`)
  - These use breakpoints (`-xs`, `-sm`, `-md`, `-lg`) and device size mixins (`atSmall`, `atMedium`, `atLarge`).

Branding font variables are defined in `src/assets/styles/branding/base/_variables.scss`:

```scss
$brandingFontSizes: (
  "small-xs": 12px,
  ...,
);
$brandingFontCategories: (
  "small": "small",
  ...,
);
```

**Example usage:**

```html
<span class="f-s-px-18 f-w-700">Bold 18px text</span>
<span class="f-s-regular">Responsive regular text</span>
```

## To add or update font sizes or weights, edit the relevant variable maps.

## 📐 Display Utility Classes (Responsive Visibility)

Display utility classes allow you to control the visibility and display type (flex or block) of elements at different breakpoints. These classes are especially useful for responsive layouts.

### Patterns

- `.show-flex-in-{breakpoints}`: Shows the element as `display: flex` only at the specified breakpoints.
- `.show-block-in-{breakpoints}`: Shows the element as `display: block` only at the specified breakpoints.

#### Supported breakpoint combinations:

- `sm-md-lg`: Show at small, medium, and large sizes
- `md-lg`: Show at medium and large sizes
- `lg`: Show at large size only
- `md-sm-xsm`: Show at medium, small, and extra small (hide at large)
- `sm-xsm`: Show at small and extra small (hide at medium and up)
- `xsm`: Show at extra small only

### How It Works

- By default, the element is hidden (`display: none`).
- At the specified breakpoints, the element is shown as `flex` or `block`.
- Uses SCSS mixins like `@include atSmall`, `@include atMedium`, `@include atLarge` for breakpoints.

### Example usage:

```html
<div class="show-flex-in-sm-md-lg">
  Visible as flex on small, medium, and large screens
</div>
<div class="show-block-in-lg">Visible as block only on large screens</div>
```

## To add or update breakpoints, edit the SCSS mixins and class definitions in the display module.

## 🛠️ Other Utility & Customization Classes

This project includes several additional utility classes for customizing scrollbars, text truncation, form indicators, links, and positioning.

### Scrollbar Customization

- Pattern: `.scroll-type-one`
- Customizes the appearance of scrollbars using branding colors (e.g., `theme-three`, `theme-four`).
- Example SCSS:
  ```scss
  .scroll-type-one {
    &::-webkit-scrollbar {
      width: 20px;
      height: 20px;
    }
    &::-webkit-scrollbar-track {
      box-shadow: inset 0 0 5px map.get($brandingColors, "theme-four");
      border-radius: 10px;
    }
    &::-webkit-scrollbar-thumb {
      background: map.get($brandingColors, "theme-three");
      border-radius: 10px;
    }
  }
  ```

### Text Truncation

- Patterns: `.one-line`, `.two-lines`, `.three-lines`, `.four-lines`
- Truncates text to 1, 2, 3, or 4 lines with ellipsis.
- Example:
  ```html
  <div class="two-lines">This text will be truncated after two lines.</div>
  ```

### Form Required Indicator

- Pattern: `.required` (used on form labels)
- Adds a red asterisk after the label using the `::after` pseudo-element.

### Link Styling

- Pattern: `.link`
- Removes underline and sets pointer cursor for links.

### Position Utilities

- Patterns: `.pos-abs`, `.pos-rel`, `.pos-fix`, `.pos-sticky` (with optional modifiers)
  - Modifiers: `--center`, `--lt`, `--rt`, `--lb`, `--rb` for common positions (center, left-top, right-top, left-bottom, right-bottom)
- Example:
  ```html
  <div class="pos-abs pos-abs--center">Centered absolutely</div>
  <div class="pos-fix pos-fix--lt">Fixed to left top</div>
  ```

## Refer to the corresponding SCSS modules for more details and to add or customize these utilities.

## 🌐 Global and Custom Classes

Some global and custom utility classes are defined in the branding `_global.scss` file. These include base resets, container helpers, and other reusable styles that apply project-wide.

### Examples from `_global.scss`

- `%fontclass`: A placeholder selector for consistent font styling, extended by `body`, `textarea`, `button`, etc.
- `.global-container`: Sets a max width and centers content.
- `.global-min-full-vh`: Sets `min-height: 100vh` for full viewport height sections.
- `html`, `body`, `*`, `img`, `a`, `p`, etc.: Base resets and accessibility improvements.

#### Example usage:

```html
<div class="global-container">Centered content</div>
<div class="global-min-full-vh">Full viewport height section</div>
```

You can add your own customized, reusable classes under the global section in `_global.scss`, or create a new module (e.g., for fonts, widths, etc.) and import it in `main.scss` as shown below:

```scss
@use "sass:math";
// General Classes
@use "general/modules/_alignments";
@use "general/modules/_borders" as general_borders;
@use "general/modules/_colors" as general_colors;
@use "general/modules/_display" as general_display;
@use "general/modules/_font";
@use "general/modules/_form";
@use "general/modules/_heights";
@use "general/modules/_links";
@use "general/modules/_opacity";
@use "general/modules/_others";
@use "general/modules/_position";
@use "general/modules/_spacing";
@use "general/modules/_width";
// Branding Classes
@use "branding/modules/_borders" as branding_borders;
@use "branding/modules/_colors" as branding_colors;
@use "branding/modules/_display" as branding_display;
@use "branding/modules/_date_picker";
@use "branding/modules/_heading";
@use "branding/modules/_row";
@use "branding/modules/_scroll";
@use "branding/modules/spacings";
@use "branding/modules/texts";
@use "branding/modules/_truncate";
@use "branding/base/_global";
```

> **Note:** Classes prefixed with `global-` are intentionally defined in `_global.scss` for easy discoverability. Developers should look for these in the global SCSS file.

---

## 🧩 Responsive Mixins

To support responsive design, the project provides SCSS mixins for common breakpoints. These mixins are defined in the branding `base/_mixins.scss` file and use variables for device sizes:

```scss
@use "variables" as *;

@mixin atSmall {
  @media (min-width: $atSmall) {
    @content;
  }
}

@mixin atMedium {
  @media (min-width: $atMedium) {
    @content;
  }
}

@mixin atLarge {
  @media (min-width: $atLarge) {
    @content;
  }
}
```

Use these mixins in your SCSS to apply styles at different breakpoints:

- `@include atSmall { ... }` for small screens and up
- `@include atMedium { ... }` for medium screens and up
- `@include atLarge { ... }` for large screens and up

## This approach keeps your styles DRY and makes it easy to maintain a responsive design system.

## 🧩 Component-Level Modular SCSS

For highly specific or non-reusable styles, use modular SCSS files scoped to individual components. This keeps your global styles clean and ensures that component-specific styles do not leak into other parts of the app.

- The convention is to create a file named `{ComponentName}.module.scss` in the same folder as the component (e.g., `Header.module.scss`).
- You can import variables, mixins, or helpers as needed using SCSS `@use`:

  ```scss
  @use "@/styles/branding/base/helpers" as *;

  .container {
    height: 100px;
  }
  ```

- These classes are only available to the component that imports them, ensuring encapsulation.

Use modular SCSS for styles that are unique to a component and not intended for reuse elsewhere in the project.

---

## 🧩 Reusable Base Components

After establishing a robust set of CSS utility classes, the project is structured around a set of reusable base components. These components are designed to provide a consistent, modular, and maintainable foundation for building all UI features.

Base components are organized into three main categories under `src/baseComponents/`:

- **formComponents**: Input and form-related elements (e.g., TextBox, Label, Select, MediaPicker, RichTextBox, ...).
- **reusableComponents**: General-purpose UI building blocks (e.g., Button, Card, Carousel, Icon, Row, Column, Table, AppImage, ...).
- **pageParts**: Larger layout or page-level elements (e.g., Alert, Footer, Header, Modal/Popup, ...).

Each category is a folder:

- `src/baseComponents/formComponents`
- `src/baseComponents/reusableComponents`
- `src/baseComponents/pageParts`

**Reusable Components** are those like Button, Card, Carousel, Icon, Row, Column, Table, AppImage, and more. Each will be introduced in detail, one by one, in the following sections.

**Form Components** include TextBox, Label, Select, MediaPicker, RichTextBox, and others, each to be introduced individually.

**Page Parts** are larger, often layout-level components such as Alert, Footer, Header, Modal (Popup), etc., and will also be introduced one by one.

---

### 🟦 Div Component

The `Div` component is a flexible, utility-driven wrapper for building layouts. It abstracts common flexbox and block behaviors, alignment, and responsive visibility into a single, composable component.

#### **Props**

| Prop                 | Type                            | Default                 | Description                                                                                          |
| -------------------- | ------------------------------- | ----------------------- | ---------------------------------------------------------------------------------------------------- |
| `children`           | `ReactNode`                     | —                       | Content to render inside the div.                                                                    |
| `type`               | `"block" \| "flex"`             | `"block"`               | Sets the display type. `"flex"` applies flexbox classes, `"block"` is a normal block element.        |
| `direction`          | `"horizontal" \| "vertical"`    | `"horizontal"`          | Flex direction. `"vertical"` sets column direction, `"horizontal"` is row (default).                 |
| `hAlign`             | `"start" \| "center" \| "end"`  | `"start"`               | Horizontal alignment. For flex, controls `align-items` (vertical) or `justify-content` (horizontal). |
| `vAlign`             | `"start" \| "center" \| "end"`  | `"start"`               | Vertical alignment. For flex, controls `justify-content` (vertical) or `align-items` (horizontal).   |
| `textAlign`          | `"left" \| "center" \| "right"` | `"left"`                | Text alignment. Adds `text-center` or `text-rtl` class.                                              |
| `distributedBetween` | `boolean`                       | `false`                 | If true, applies `flex--jc--between` for space-between distribution.                                 |
| `distributedAround`  | `boolean`                       | `false`                 | If true, applies `flex--jc--around` for space-around distribution.                                   |
| `showIn`             | `string[]`                      | `['xs','sm','md','lg']` | Controls responsive visibility. Uses `showInCssClass` to generate classes for breakpoints.           |
| `className`          | `string`                        | —                       | Additional custom classes.                                                                           |
| `...props`           | `any`                           | —                       | Any other props are spread to the underlying `<div>`.                                                |

#### **How Props Affect the Div**

- **type**: If `"flex"`, applies the `flex` class for flexbox layout.
- **direction**: If `"vertical"`, adds `flex--dir--col` for column direction; otherwise, row.
- **hAlign/vAlign**: Depending on direction, applies alignment classes for flexbox (`flex--ai--*`, `flex--jc--*`).
- **distributedBetween/distributedAround**: Adds flexbox distribution classes for spacing children.
- **textAlign**: Adds `text-center` or `text-rtl` for text alignment.
- **showIn**: Controls which breakpoints the div is visible at, using utility classes.
- **className**: Allows further custom styling.
- **...props**: All other props (e.g., `style`, `id`, etc.) are passed to the `<div>`.

#### **Example Usage**

```jsx
<Div
  type="flex"
  direction="vertical"
  hAlign="center"
  vAlign="center"
  showIn={["md", "lg"]}
  className="custom-class"
>
  <span>Centered content</span>
</Div>
```

This will render a flex column, centered both ways, visible only on medium and large screens, with any additional custom classes.

---

### 🟧 Accordion Component

The `Accordion` component provides a smooth, animated expand/collapse container for showing and hiding content. It is useful for FAQs, collapsible panels, and any UI where content needs to be revealed or hidden with animation.

#### **Props**

| Prop            | Type        | Default | Description                                                                 |
| --------------- | ----------- | ------- | --------------------------------------------------------------------------- |
| `isActive`      | `boolean`   | —       | Controls whether the accordion is expanded (`true`) or collapsed (`false`). |
| `className`     | `string`    | —       | Additional custom classes for the container.                                |
| `onClick`       | `func`      | —       | Callback fired when the accordion is clicked.                               |
| `children`      | `ReactNode` | —       | Content to render inside the accordion.                                     |
| `style`         | `object`    | `{}`    | Inline styles for the container.                                            |
| `initialHeight` | `number`    | `0`     | The height (in px) when collapsed. Usually `0` for fully collapsed.         |
| `animTime`      | `number`    | `0.3`   | Animation duration in seconds for expand/collapse.                          |
| `...props`      | `any`       | —       | Any other props are spread to the underlying Div.                           |

#### **How It Works**

- The accordion animates its height between `initialHeight` (collapsed) and the content’s scroll height (expanded).
- The transition is controlled by the `animTime` prop.
- Clicking the accordion triggers the `onClick` callback and updates the height for smooth animation.
- The `of-hidden` class ensures content is clipped during the transition.

#### **Example Usage**

```jsx
<Accordion
  isActive={open}
  onClick={() => setOpen(!open)}
  className="my-accordion"
  initialHeight={0}
  animTime={0.4}
>
  <div>Accordion content goes here</div>
</Accordion>
```

This will render an accordion that expands and collapses with a 0.4s animation when toggled.

---

### 🟩 AnimateContainerOnScroll Component

The `AnimateContainerOnScroll` component animates its content when it enters the viewport as the user scrolls. It is useful for triggering entrance animations or effects as elements become visible.

#### **Props**

| Prop              | Type        | Default | Description                                                                 |
| ----------------- | ----------- | ------- | --------------------------------------------------------------------------- |
| `className`       | `string`    | —       | Base classes for the container.                                             |
| `activeClassName` | `string`    | —       | Classes to apply when the animation is triggered (element enters viewport). |
| `children`        | `ReactNode` | —       | Content to render inside the container.                                     |
| `...props`        | `any`       | —       | Any other props are spread to the underlying Div.                           |

#### **How It Works**

- Uses a ref to track the container element.
- Listens to the global `scrollPos` state (from Redux) to detect scroll events.
- When the top of the container enters the viewport, applies the `activeClassName` for animation.
- The animation only triggers once per mount.

#### **Example Usage**

```jsx
<AnimateContainerOnScroll className="my-section" activeClassName="fade-in-up">
  <div>Animated content appears here</div>
</AnimateContainerOnScroll>
```

This will apply the `fade-in-up` class to the container when it enters the viewport, triggering your animation.

---

### Anchor Component

The `Anchor` component is a flexible, accessible link component that supports both internal (Next.js routing) and external navigation, with optional visual effects and custom styling.

#### **Props**

| Prop         | Type        | Default    | Description                                                                            |
| ------------ | ----------- | ---------- | -------------------------------------------------------------------------------------- |
| `anchorType` | `string`    | `"scale"`  | Visual style/effect for the anchor. See below for available types.                     |
| `to`         | `string`    | —          | The URL or path to link to.                                                            |
| `internal`   | `boolean`   | `true`     | If true, uses Next.js `<Link>` for internal routing; otherwise, uses a standard `<a>`. |
| `target`     | `string`    | `"_blank"` | Target for external links (e.g., `_blank`, `_self`).                                   |
| `ariaLabel`  | `string`    | `""`       | Optional ARIA label for accessibility.                                                 |
| `className`  | `string`    | —          | Additional custom classes.                                                             |
| `children`   | `ReactNode` | —          | Content to render inside the anchor.                                                   |
| `...props`   | `any`       | —          | Any other props are spread to the underlying element.                                  |

#### **anchorType Options**

- `"scale"`: Adds a scaling effect on hover (default).
- `"internal-routing"`: Applies theme color classes for internal navigation.
- `"no-effect"`: No special effect or color.

You can update the code to customize the effect for each type, add new types, or remove any existing types as needed for your project.

#### **How It Works**

- If `internal` is true, renders a Next.js `<Link>` for client-side routing.
- If `internal` is false, renders a standard `<a>` tag for external links.
- Applies the appropriate classes and effects based on `anchorType`.
- Supports accessibility via `aria-label`.

#### **Example Usage**

```jsx
<Anchor to="/about" anchorType="internal-routing" internal>
  Go to About Page
</Anchor>

<Anchor to="https://example.com" anchorType="scale" internal={false}>
  External Link
</Anchor>
```

---

### 🟩 AppImage Component

The `AppImage` component is a responsive, feature-rich image wrapper built on top of Next.js's legacy `Image` component. It provides automatic width/height handling, a loading spinner, and easy integration with modular SCSS for custom styles.

#### **Props**

| Prop          | Type       | Default   | Description                                                              |
| ------------- | ---------- | --------- | ------------------------------------------------------------------------ |
| `src`         | `string`   | —         | The image source URL.                                                    |
| `alt`         | `string`   | —         | The alt text for accessibility.                                          |
| `width`       | `number`   | —         | The width of the image (in px). If omitted, uses parent width.           |
| `height`      | `number`   | —         | The height of the image (in px). If omitted, uses parent height or auto. |
| `layout`      | `string`   | `"fill"`  | Next.js Image layout mode (`"fill"`, `"fixed"`, `"responsive"`, etc.).   |
| `objectFit`   | `string`   | `"cover"` | CSS object-fit property for image scaling.                               |
| `className`   | `string`   | —         | Additional custom classes for the wrapper.                               |
| `imgClass`    | `string`   | —         | Custom classes for the `<img>` element.                                  |
| `showSpinner` | `boolean`  | `true`    | If true, shows a loading spinner until the image loads.                  |
| `priority`    | `boolean`  | `false`   | If true, uses Next.js priority loading.                                  |
| `onClick`     | `function` | —         | Click handler for the image.                                             |
| `...props`    | `any`      | —         | Any other props are spread to the underlying Image.                      |

#### **How It Works**

- Uses a custom hook (`useDivWidth`) to auto-detect parent width if not provided.
- Shows a spinner overlay (using SCSS module) while the image is loading.
- Supports all Next.js legacy Image props, plus custom styling via `className` and `imgClass`.
- Handles responsive layouts and object-fit for modern UI needs.

#### **Example Usage**

```jsx
<AppImage
  src="/images/sample.jpg"
  alt="Sample image"
  width={400}
  height={300}
  layout="responsive"
  objectFit="cover"
  className="my-image-wrapper"
  imgClass="rounded shadow"
  showSpinner={true}
  onClick={() => alert("Image clicked!")}
/>
```

This renders a responsive image with a loading spinner, custom wrapper and image classes, and a click handler.

---

### 🟧 AppVideo Component

The `AppVideo` component is a simple, reusable wrapper for rendering HTML5 videos with customizable width, height, and additional props. It is designed for easy integration and extension in React projects.

#### **Props**

| Prop       | Type     | Default | Description                                                     |
| ---------- | -------- | ------- | --------------------------------------------------------------- |
| `width`    | `number` | —       | The width of the video in pixels.                               |
| `height`   | `number` | —       | The height of the video in pixels.                              |
| `src`      | `string` | —       | The video source URL.                                           |
| `...props` | `any`    | —       | Any other props are spread to the underlying `<video>` element. |

#### **How It Works**

- Renders a native HTML5 `<video>` element with the provided `width`, `height`, and `src`.
- The `controls` attribute is always enabled for user playback controls.
- Any additional props (such as `autoPlay`, `loop`, `muted`, etc.) are passed directly to the `<video>` element.
- Includes a fallback message for browsers that do not support the video tag.

#### **Example Usage**

```jsx
<AppVideo
  width={640}
  height={360}
  src="/videos/sample.mp4"
  autoPlay={false}
  loop={false}
  muted={false}
  style={{ borderRadius: 8 }}
/>
```

This will render a 640x360 video player with standard controls and any additional props you provide.

---

### 🟦 Button Component

The `Button` component is a reusable, style-driven button for consistent UI actions. It supports two visual types, customizable text, and all standard button props, making it easy to use and extend across the project.

#### **Props**

| Prop        | Type     | Default | Description                                                            |
| ----------- | -------- | ------- | ---------------------------------------------------------------------- |
| `btnText`   | `string` | —       | The text to display inside the button.                                 |
| `btnType`   | `number` | `1`     | Visual style: `1` for primary (themed), any other value for secondary. |
| `className` | `string` | —       | Additional custom classes for the button.                              |
| `...props`  | `any`    | —       | Any other props are spread to the underlying `<button>` element.       |

#### **How It Works**

- Renders a native `<button>` element with utility and theme classes for padding, border, and rounded corners.
- `btnType` determines the color scheme:
  - `1`: Themed background, border, and hover effects (primary style).
  - Other: Outlined style with border only (secondary style).
- All additional props (e.g., `onClick`, `type`, `disabled`, etc.) are passed to the button.
- Uses the `classnames` (`cx`) library for conditional class composition.

#### **Example Usage**

```jsx
<Button btnText="Submit" btnType={1} onClick={handleSubmit} />
<Button btnText="Cancel" btnType={2} className="m-l-8" type="button" />
```

This renders a primary and a secondary button with custom text and props.

#### **Customization & Notes**

- You can extend the component to support icons, loading states, or additional button types as needed.
- All standard HTML button attributes are supported via props.
- For accessibility, ensure to provide descriptive `btnText` and use semantic button types (`type="submit"`, etc.).

---

### 🟨 Carousel Component

The `Carousel` component is a flexible, reusable slider for displaying a horizontal list of items with navigation controls. It supports two types: manual navigation (type 1) and auto-sliding with indicators (type 2). The component is modular, with each type implemented as a separate subcomponent.

#### **Props**

| Prop              | Type          | Default | Description                                                                |
| ----------------- | ------------- | ------- | -------------------------------------------------------------------------- |
| `type`            | `number`      | `1`     | Carousel style: `1` for manual navigation, `2` for auto-sliding with dots. |
| `itemWidth`       | `number`      | —       | Width of each carousel item in pixels.                                     |
| `gapBetweenItems` | `number`      | —       | Gap between carousel items in pixels.                                      |
| `numberOfItems`   | `number`      | —       | Total number of items in the carousel.                                     |
| `children`        | `ReactNode[]` | —       | Carousel items to display.                                                 |
| `...props`        | `any`         | —       | Any other props are spread to the underlying carousel type component.      |

#### **How It Works**

- The main `Carousel` component delegates rendering to either `CarouselType1` or `CarouselType2` based on the `type` prop.
- Both types use a responsive container and horizontal scrolling logic, but differ in navigation:
  - **Type 1**: Manual navigation with left/right arrow buttons. Users can scroll through items by clicking the arrows.
  - **Type 2**: Auto-sliding carousel with dot indicators. Slides advance automatically every few seconds, and users can jump to a slide by clicking a dot.
- Both types use a custom hook (`useDivWidth`) to determine the visible area and calculate how many items fit per view.
- The carousel is fully responsive and supports any number of items.

#### **Example Usage**

```jsx
<Carousel type={1} numberOfItems={9} itemWidth={500} gapBetweenItems={20}>
  <Div className="width-px-500 height-px-300 bg-green m-r-20">Hello 1</Div>
  <Div className="width-px-500 height-px-300 bg-green m-r-20">Hello 2</Div>
  {/* ...more items... */}
</Carousel>

<Carousel type={2} numberOfItems={6} itemWidth={400} gapBetweenItems={16}>
  {/* ...carousel items... */}
</Carousel>
```

#### **Type 1: Manual Navigation**

- Shows left/right arrow buttons to scroll through items.
- Calculates how many items fit in the visible area and scrolls by that amount.
- Disables arrows when at the start/end of the carousel.

#### **Type 2: Auto-Sliding with Dots**

- Automatically advances to the next slide every few seconds.
- Shows dot indicators for each slide; clicking a dot jumps to that slide.
- Loops back to the first slide after the last.

#### **Customization & Notes**

- You can extend the carousel to support more types, custom animations, or additional controls.
- All layout and style props are passed to the underlying type component.
- For accessibility, ensure carousel items are focusable and provide alt text for images/videos.

---

### 🟫 DivConvertTextToHtml Component

The `DivConvertTextToHtml` component safely renders raw HTML content from a string, using DOMPurify to sanitize the input and prevent XSS attacks. It is useful for displaying user-generated or CMS-provided HTML in a React application.

#### **Props**

| Prop       | Type     | Default | Description                                                   |
| ---------- | -------- | ------- | ------------------------------------------------------------- |
| `text`     | `string` | —       | The raw HTML string to render.                                |
| `...props` | `any`    | —       | Any other props are spread to the underlying `Div` component. |

#### **How It Works**

- Uses the `DOMPurify` library to sanitize the `text` prop, removing any potentially dangerous HTML or scripts.
- Stores the sanitized HTML in state and updates it whenever `text` changes.
- Renders a `Div` component with `dangerouslySetInnerHTML`, passing all other props through.
- Ensures that only safe, sanitized HTML is rendered to the DOM.

#### **Example Usage**

```jsx
<DivConvertTextToHtml
  text="<h2>Welcome</h2><p>This is <b>safe</b> HTML!</p>"
  className="my-html-content"
/>
```

This will render the provided HTML string as real HTML, with all tags and formatting, but sanitized for safety.

#### **Customization & Notes**

- You can pass any additional props (such as `className`, `style`, etc.) to the underlying `Div`.
- Always sanitize user-generated HTML before rendering to prevent XSS vulnerabilities.

---

### 🟪 Heading Component

The `Heading` component is a simple, semantic wrapper for rendering headings (`h1`–`h6`) based on a numeric `type` prop. It ensures consistent heading usage and makes it easy to apply custom props or classes to any heading level.

#### **Props**

| Prop       | Type        | Default | Description                                                   |
| ---------- | ----------- | ------- | ------------------------------------------------------------- |
| `type`     | `number`    | `1`     | Heading level: 1 for `<h1>`, 2 for `<h2>`, ..., 6 for `<h6>`. |
| `children` | `ReactNode` | —       | Content to render inside the heading.                         |
| `...props` | `any`       | —       | Any other props are spread to the underlying heading element. |

#### **How It Works**

- Renders the appropriate heading tag (`<h1>`–`<h6>`) based on the `type` prop.
- Passes all additional props (such as `className`, `style`, `id`, etc.) to the heading element.
- If `type` is not 1–6, renders nothing.

#### **Example Usage**

```jsx
<Heading type={1} className="main-title">Main Title</Heading>
<Heading type={3} style={{ color: 'red' }}>Section Heading</Heading>
```

This will render an `<h1>` and an `<h3>` with the provided content and props.

---

### 🟫 Icon Component

The `Icon` component is a flexible wrapper for rendering FontAwesome icons with customizable type, color, size, and scale. It supports a wide range of icon types, including both solid and brand icons, and is designed for consistent icon usage throughout the project.

#### **Props**

| Prop     | Type     | Default | Description                                                    |
| -------- | -------- | ------- | -------------------------------------------------------------- |
| `type`   | `string` | "close" | The icon type to render (see list below for supported values). |
| `color`  | `string` | "black" | The color of the icon (any valid CSS color value).             |
| `width`  | `string` | "16px"  | The width of the icon (e.g., `30`).                            |
| `height` | `string` | "16px"  | The height of the icon (e.g., `30`).                           |
| `scale`  | `number` | `1`     | Scale factor for the icon (applies CSS `transform: scale()`).  |

#### **Supported `type` Values**

- `close`, `left`, `right`, `play-circle`, `instagram`, `linkedin`, `youtube`, `telegram`, `github`, `circle-user`, `calendar-days`, `angle-up`, `search`, `check-mark`, `eye`, `eye-slash`, `upload`, `circle-play`

#### **How It Works**

- Renders a `FontAwesomeIcon` with the specified icon, color, width, height, and scale.
- Only the icon matching the `type` prop is rendered; all others return an empty string.
- You can add more icon types by extending the icon imports and the component logic.

#### **Example Usage**

```jsx
<Icon type="close" color="#f00" width={30} height={30} />
<Icon type="instagram" color="#833AB4" scale={1.5} />
<Icon type="left" />
```

This will render a red close icon, a scaled Instagram icon, and a default left arrow icon.

#### **Customization & Notes**

- You can add more icon types by importing additional FontAwesome icons and extending the component.
- All standard FontAwesomeIcon props (such as `spin`, `pulse`, etc.) can be added as needed.
- For accessibility, consider adding `aria-label` or `title` props to describe the icon's purpose.

---

### 🟫 Paragraph Component

The `Paragraph` component is a simple wrapper for rendering a semantic `<p>` element with any children and custom props. It ensures consistent paragraph usage and makes it easy to apply custom classes, styles, or attributes.

#### **Props**

| Prop       | Type        | Default | Description                                                 |
| ---------- | ----------- | ------- | ----------------------------------------------------------- |
| `children` | `ReactNode` | —       | Content to render inside the paragraph.                     |
| `...props` | `any`       | —       | Any other props are spread to the underlying `<p>` element. |

#### **How It Works**

- Renders a native `<p>` element with all provided children and props.
- Passes all additional props (such as `className`, `style`, `id`, etc.) to the paragraph element.

#### **Example Usage**

```jsx
<Paragraph className="my-paragraph" style={{ color: "blue" }}>
  This is a styled paragraph.
</Paragraph>
```

This will render a `<p>` with the provided content, class, and style.

#### **Customization & Notes**

- You can pass any valid HTML attributes or custom classes/styles to the paragraph.
- Use this component for consistent paragraph rendering and easy extension.

---

### 🟫 SVGIcon Component

The `SVGIcon` component is a flexible wrapper for rendering custom SVG icons as React components. It supports dynamic icon selection via a `type` prop and allows customization of fill, stroke, width, and height. This approach enables scalable, themeable SVG icons throughout the project.

#### **Props**

| Prop     | Type     | Default | Description                                                  |
| -------- | -------- | ------- | ------------------------------------------------------------ |
| `type`   | `string` | —       | The icon type to render (must match a key in the `iconMap`). |
| `fill`   | `string` | "none"  | The fill color for the SVG icon.                             |
| `stroke` | `string` | "black" | The stroke color for the SVG icon.                           |
| `width`  | `number` | `30`    | The width of the SVG icon in pixels.                         |
| `height` | `number` | `30`    | The height of the SVG icon in pixels.                        |

#### **How It Works**

- Looks up the icon component in the `iconMap` object using the `type` prop.
- If a matching icon is found, renders it with the specified `fill`, `stroke`, `width`, and `height` props.
- If no matching icon is found, renders nothing.
- You can add more SVG icons by importing them and adding to the `iconMap`.

#### **Example Usage**

```jsx
<SVGIcon type="google" fill="#4285F4" width={40} height={40} />
```

This will render the Google SVG icon with a blue fill and 40x40 size.

#### **Customization & Notes**

- Add more SVG icon components to the `iconMap` for easy expansion.
- All standard SVG props (such as `viewBox`, `className`, etc.) can be supported by updating the icon components.
- Use this component for scalable, themeable icons that are not available in FontAwesome or other icon libraries.

---

### 🟫 Table Component

The `Table` component is a flexible, responsive table for displaying tabular data with custom headers, multi-row headings, and cell rendering. It is designed for advanced layouts, dynamic column widths, and integration with the project's utility and base components.

#### **Props**

| Prop               | Type      | Default | Description                                                           |
| ------------------ | --------- | ------- | --------------------------------------------------------------------- |
| `headingTitleRows` | `array`   | —       | Array of objects for the first header row (supports colSpan/rowSpan). |
| `headingData`      | `array`   | —       | Array of objects for the second header row and column definitions.    |
| `bodyData`         | `array`   | —       | Array of row objects, each mapping column identifiers to cell data.   |
| `useFullWidth`     | `boolean` | `true`  | If true, stretches columns to fill the container width.               |
| `className`        | `string`  | —       | Additional custom classes for the table.                              |

#### **How It Works**

- Uses a custom hook (`useDivWidth`) to measure the container and adjust column widths responsively.
- Supports multi-row headers with `colSpan` and `rowSpan` for complex table layouts.
- Each cell and header can render custom React nodes (e.g., styled `Div`s, icons, etc.).
- Column widths are calculated from the `headingData` array, and can stretch to fit the container if `useFullWidth` is true.
- The table is horizontally scrollable on small screens.

#### **Example Usage**

```jsx
import Table from "@/baseComponents/reusableComponents/Table";
import { HEADING_TITLE_ROWS, HEADING_DATA, BODY_DATA } from "./utils";
import { MOCK_DATA } from "./constants";

const bodyData = useMemo(() => BODY_DATA(MOCK_DATA), [MOCK_DATA]);

<Table
  headingTitleRows={HEADING_TITLE_ROWS()}
  headingData={HEADING_DATA()}
  bodyData={bodyData}
  useFullWidth={true}
  className="bg-orange"
/>;
```

#### **Supporting Utility Functions**

- `HEADING_TITLE_ROWS()`: Returns an array of objects for the first header row, each with `identifier`, `display`, `colSpan`, and optional `rowSpan`.
- `HEADING_DATA()`: Returns an array of objects for the second header row, each with `identifier`, `name`, `display`, and `width`.
- `BODY_DATA(MOCK_DATA)`: Maps an array of data objects to the table's row format, with custom cell rendering.

---

## 🧩 Form Components

### 🟦 Form Component

The `Form` component is a simple wrapper for the native `<form>` element, providing a consistent API for handling form submissions in React.

#### **Props**

| Prop       | Type        | Default | Description                                                    |
| ---------- | ----------- | ------- | -------------------------------------------------------------- |
| `onSubmit` | `function`  | —       | Callback fired on form submission. Receives the event object.  |
| `children` | `ReactNode` | —       | Content to render inside the form.                             |
| `...props` | `any`       | —       | Any other props are spread to the underlying `<form>` element. |

#### **How It Works**

- Prevents the default form submission behavior.
- Calls the `onSubmit` callback if provided.
- Passes all other props to the `<form>` element.

#### **Example Usage**

```jsx
<Form onSubmit={handleSubmit}>
  <input type="text" name="name" />
  <button type="submit">Submit</button>
</Form>
```

This will render a form that prevents default submission and calls your `handleSubmit` function.

---

### 🟦 TextBox Component

The `TextBox` component is a flexible, styled input field with label, password visibility toggle, and value management. It supports both controlled and read-only modes, and is styled with utility classes.

#### **Props**

| Prop          | Type      | Default | Description                                                     |
| ------------- | --------- | ------- | --------------------------------------------------------------- |
| `label`       | `string`  | —       | The label text to display above the input.                      |
| `val`         | `string`  | —       | The current value of the input (controlled).                    |
| `placeHolder` | `string`  | —       | Placeholder text for the input.                                 |
| `isRequired`  | `boolean` | `false` | If true, shows a required indicator on the label.               |
| `...props`    | `any`     | —       | Any other props are spread to the underlying `<input>` element. |

#### **How It Works**

- Renders a label using the `Label` component.
- Renders an input field with utility classes and controlled value.
- If `type="password"`, shows an eye icon to toggle visibility.
- Prevents editing if `isNotEditable` is true.
- Passes all other props to the `<input>` element.

#### **Example Usage**

```jsx
<TextBox
  label="Password"
  val={password}
  onChange={(e) => setPassword(e.target.value)}
  placeHolder="Enter your password"
  isRequired
  type="password"
/>
```

This will render a password input with a label, required indicator, and a toggle for visibility.

---

### 🟦 Select Component

The `Select` component is a custom dropdown/select input with styled options, label, and placeholder. It supports absolute or relative dropdown positioning and is fully controlled.

#### **Props**

| Prop                         | Type       | Default  | Description                                                        |
| ---------------------------- | ---------- | -------- | ------------------------------------------------------------------ |
| `options`                    | `array`    | —        | Array of option objects `{ value, shownText }` to display.         |
| `val`                        | `string`   | —        | The currently selected value.                                      |
| `optionChanged`              | `function` | —        | Callback fired when an option is selected. Receives the new value. |
| `placeHolder`                | `string`   | —        | Placeholder text when no value is selected.                        |
| `label`                      | `string`   | —        | The label text to display above the select.                        |
| `isRequired`                 | `boolean`  | —        | If true, shows a required indicator on the label.                  |
| `optionsContainerIsAbsolute` | `boolean`  | `true`   | If true, dropdown is absolutely positioned; else, relatively.      |
| `optionsContainerWidth`      | `string`   | `"100%"` | Width of the dropdown options container.                           |

#### **How It Works**

- Renders a label using the `Label` component.
- Renders a styled select box that shows the selected value or placeholder.
- Clicking the select toggles the dropdown of options.
- Options are rendered in a scrollable container, absolute or relative.
- Clicking an option calls `optionChanged` and closes the dropdown.
- Clicking outside (when absolute) closes the dropdown.

#### **Example Usage**

```jsx
<Select
  label="Country"
  options={[
    { value: "us", shownText: "United States" },
    { value: "ca", shownText: "Canada" },
  ]}
  val={country}
  optionChanged={setCountry}
  placeHolder="Select a country"
  isRequired
/>
```

This will render a select input with a label, required indicator, and a dropdown of options.

---

### 🟦 DatePicker Component

The `DatePicker` component is a styled wrapper around `react-datepicker` for selecting dates (and optionally times), with label, placeholder, and dropdown controls for year/month.

#### **Props**

| Prop                     | Type      | Default        | Description                                                      |
| ------------------------ | --------- | -------------- | ---------------------------------------------------------------- |
| `className`              | `string`  | —              | Additional custom classes for the outer container.               |
| `isRequired`             | `boolean` | —              | If true, shows a required indicator on the label.                |
| `label`                  | `string`  | —              | The label text to display above the picker.                      |
| `chosenDate`             | `Date`    | —              | The currently selected date.                                     |
| `setChosenDate`          | `func`    | —              | Callback to update the selected date.                            |
| `dateFormat`             | `string`  | `"dd-MM-yyyy"` | Format string for the displayed date.                            |
| `yearDropdownItemNumber` | `number`  | `100`          | Number of years to show in the year dropdown.                    |
| `showYearDropdown`       | `boolean` | `true`         | If true, shows a year dropdown.                                  |
| `showMonthDropdown`      | `boolean` | `false`        | If true, shows a month dropdown.                                 |
| `placeHolder`            | `string`  | —              | Placeholder text for the input.                                  |
| `showTimeSelect`         | `boolean` | `false`        | If true, enables time selection.                                 |
| `showTimeSelectOnly`     | `boolean` | `false`        | If true, only time selection is shown.                           |
| `hasMarginBottom`        | `boolean` | `true`         | If true, adds bottom margin to the container.                    |
| `...props`               | `any`     | —              | Any other props are spread to the underlying `react-datepicker`. |

#### **How It Works**

- Renders a label using the `Label` component (if provided).
- Renders a styled `react-datepicker` input with utility classes.
- Supports year/month dropdowns, time selection, and custom formats.
- Calls `setChosenDate` when a date is picked.
- Passes all other props to the underlying `react-datepicker`.

#### **Example Usage**

```jsx
<DatePicker
  label="Birthday"
  chosenDate={birthday}
  setChosenDate={setBirthday}
  placeHolder="Select your birthday"
  showYearDropdown
  showMonthDropdown
  dateFormat="yyyy/MM/dd"
  isRequired
/>
```

This will render a date picker with a label, required indicator, and dropdowns for year and month.

---

### 🟦 CheckBox Component

The `CheckBox` component is a styled, controlled checkbox with a label and required indicator, using utility classes and custom icons for a modern look.

#### **Props**

| Prop         | Type       | Default | Description                                       |
| ------------ | ---------- | ------- | ------------------------------------------------- |
| `label`      | `string`   | —       | The label text to display next to the checkbox.   |
| `val`        | `boolean`  | —       | The current checked state (controlled).           |
| `setVal`     | `function` | —       | Function to update the checked state.             |
| `isRequired` | `boolean`  | `false` | If true, shows a required indicator on the label. |

#### **How It Works**

- Renders a flex container with a styled box and label.
- Clicking the box toggles the checked state by calling `setVal(!val)`.
- If `val` is true, shows a check-mark icon inside the box (using the `Icon` component and theme color).
- The label is displayed to the right, with a required indicator if `isRequired` is true.
- Uses utility classes for size, border, background, and spacing.

#### **Example Usage**

```jsx
<CheckBox label="Accept Terms" val={accepted} setVal={setAccepted} isRequired />
```

This will render a checkbox with a label and required indicator, updating `accepted` when clicked.

---

### 🟦 MediaPicker Component

The `MediaPicker` component is a flexible, feature-rich file input for images and videos, supporting cropping, resizing, preview, and custom file handling. It is designed for profile photos, avatars, and video uploads, with optional cropper and resizer dialogs.

#### **Props**

| Prop                           | Type       | Default   | Description                                                             |
| ------------------------------ | ---------- | --------- | ----------------------------------------------------------------------- |
| `label`                        | `string`   | —         | The label text to display above the picker.                             |
| `isRequired`                   | `boolean`  | `false`   | If true, shows a required indicator on the label.                       |
| `setFile`                      | `function` | —         | Callback to update the selected file (image or video).                  |
| `hasCropper`                   | `boolean`  | `true`    | If true, enables the cropper dialog for images.                         |
| `cropInfo`                     | `object`   | —         | Cropper config: `{ minWidth, maxWidth, minHeight, maxHeight, aspect }`. |
| `hasResizer`                   | `boolean`  | `false`   | If true, enables the resizer dialog for images.                         |
| `maxWidth`                     | `number`   | —         | Maximum width for resizing/cropping.                                    |
| `type`                         | `string`   | "default" | Picker type (for custom picker UI, usually leave as default).           |
| `initialSrc`                   | `string`   | ""        | Initial image/video source (for editing or preview).                    |
| `setInitialSrc`                | `function` | —         | Callback to update the initial source.                                  |
| `initialSrcComesFromOurServer` | `boolean`  | `false`   | If true, prepends the app domain to `initialSrc`.                       |
| `previewer`                    | `string`   | "default" | Previewer type (for custom preview UI).                                 |
| `className`                    | `string`   | —         | Additional custom classes for the outer container.                      |
| `hasMarginBottom`              | `boolean`  | —         | If true, adds bottom margin to the container.                           |
| `fileType`                     | `string`   | "image"   | File type: "image" or "video".                                          |

#### **How It Works**

- Renders an image or video picker with label and preview.
- Handles file selection, preview, and state management for the file and its name.
- If `hasCropper` is true and fileType is image, shows a cropper dialog for cropping the image to the specified aspect ratio and size.
- If `hasResizer` is true and fileType is image, shows a resizer dialog for resizing the image to `maxWidth`.
- Supports initial source for editing existing images/videos, with optional server domain prefix.
- Uses subcomponents for image and video picking, cropping, resizing, and preview.
- All file changes are propagated via `setFile`.

#### **Example Usage**

```jsx
<MediaPicker
  label="Profile Photo"
  isRequired
  file={profilePhoto}
  setFile={setProfilePhoto}
  id="profilePhotoFieldHomePage"
  hasCropper={true}
  hasResizer={true}
  maxWidth={400}
  cropInfo={{
    minWidth: 50,
    maxWidth: 400,
    minHeight: 50,
    maxHeight: 400,
    aspect: 1,
  }}
/>
```

This will render a profile photo picker with cropping and resizing enabled, enforcing a square aspect ratio and size limits.

## 🧩 Page Parts

### 🟥 Alert Component

The `Alert` component is a global notification system for displaying success and error messages at the top-right of the screen. It is integrated with Redux and provides animated entry/exit, custom styling, and close controls.

#### **How It Works**

- The component listens to the Redux `alert` state (an array of alert items).
- Each alert item has a `type` ("success" or "error"), a unique `key`, a `message`, and a `display` flag for animation.
- Alerts slide in from the right and can be dismissed by clicking the close button or automatically after 15 seconds.
- The border color and close button color reflect the alert type (green for success, red for error).
- Uses utility classes for layout, animation, and styling.

#### **Props**

The `Alert` component does not take any props directly. It is connected to Redux and displays all current alert items.

#### **Helper Functions**

- `addNewAlertItem(dispatch, type, message)`: Adds a new alert to the Redux state. Type is "success" or "error".
- `removeAnAlertItem(dispatch, key)`: Animates and removes an alert by key.

#### **Example Usage**

```jsx
import { useDispatch } from "react-redux";
import Button from "@/baseComponents/reusableComponents/Button";
import { addNewAlertItem } from "@/utils/alert";

const DisplayAlert = () => {
  const dispatch = useDispatch();
  return (
    <>
      <Button
        btnText="Alert of type success"
        onClick={() =>
          addNewAlertItem(
            dispatch,
            "success",
            "This is a sample success message"
          )
        }
      />
      <Button
        btnText="Alert of type error"
        onClick={() =>
          addNewAlertItem(dispatch, "error", "This is a sample error message")
        }
      />
    </>
  );
};
```

---

### 🟦 Modal & PromptMessage Components

The `Modal` component provides a flexible modal dialog system, integrated with Redux for global state management. It is designed to display various modal types, such as prompt messages, and can be extended for more complex modal content.

#### **Modal Component**

**How It Works:**

- Listens to the Redux `modal` state to determine the modal type and props.
- Renders a fixed-position container with a close button.
- The close button dispatches `clearModal()` to hide the modal.
- The modal content area conditionally renders subcomponents based on the `type` (e.g., `PromptMessage`).
- Uses utility classes and a CSS module for styling and animation.

#### **Example Usage**

To display a prompt message modal, dispatch the `setModal` action with the appropriate type and props:

```jsx
import { useDispatch } from "react-redux";

import Button from "@/baseComponents/reusableComponents/Button";

import { setModal } from "@/reducer/subs/modal";

const DisplayModal = () => {
  const dispatch = useDispatch();

  return (
    <>
      <Button
        btnText="Modal of type prompt-message"
        className="width-px-350"
        onClick={() => {
          dispatch(
            setModal({
              type: "prompt-message",
              props: {
                message: "This is a sample message",
              },
            })
          );
        }}
      />
    </>
  );
};

export default DisplayModal;
```

This will open a modal with your custom message and an OK button to close it.

---

# 📦 Custom React Hooks Documentation

This document introduces custom React hooks designed for scalable, maintainable, and DRY code in your project. Each hook is fully integrated with Redux and provides a clean API for common frontend needs.

---

## 🪝 useApiCalls

A powerful hook for making HTTP API requests (GET, POST, PUT, DELETE) with built-in loading, error handling, and authentication support.

### **Props**

| Prop                | Type     | Default | Description                                                                           |
| ------------------- | -------- | ------- | ------------------------------------------------------------------------------------- |
| `method`            | string   | —       | HTTP method: `"GET"`, `"POST"`, `"PUT"`, or `"DELETE"`.                               |
| `url`               | string   | —       | API endpoint (relative path).                                                         |
| `bodyData`          | object   | —       | Data to send in the request body (for POST/PUT).                                      |
| `headers`           | object   | —       | Custom headers. If not provided, JWT auth header is added automatically if available. |
| `sendReq`           | boolean  | —       | When set to `true`, the request is triggered.                                         |
| `setSendReq`        | function | —       | Function to reset `sendReq` to `false` after the request.                             |
| `handleError`       | function | —       | Optional callback for custom error handling.                                          |
| `useDefaultHeaders` | boolean  | `true`  | Whether to use default headers (including JWT auth).                                  |
| `showLoading`       | boolean  | `true`  | Whether to show loading state via Redux.                                              |
| `showErrerMessage`  | boolean  | `true`  | Whether to show error messages via alert system.                                      |

### **Returns**

- `data`: The response data from the API.
- `status`: The HTTP status code.

### **Example Usage**

```jsx
const [sendReq, setSendReq] = useState(false);
const { data, status } = useApiCalls({
  method: "POST",
  url: "/api/login",
  bodyData: { username, password },
  sendReq,
  setSendReq,
  showLoading: true,
  showErrerMessage: true,
});
```

---

## 🪝 useDivWidth

A utility hook for measuring the width of a DOM element (usually a div) and updating it on window resize. Optionally dispatches the width to Redux for layout management.

### **Props**

| Prop              | Type    | Default | Description                                                                  |
| ----------------- | ------- | ------- | ---------------------------------------------------------------------------- |
| `isMainContainer` | boolean | `false` | If `true`, dispatches the width to Redux for main container layout tracking. |

### **Returns**

- `containerRef`: Attach this ref to the element you want to measure.
- `width`: The current width of the element.

### **Example Usage**

```jsx
const { containerRef, width } = useDivWidth();
return <div ref={containerRef}>Width: {width}px</div>;
```

---

## 🪝 useWebSocket

A robust hook for managing WebSocket connections, sending/receiving messages, and handling connection events with Redux integration.

### **Props**

| Prop               | Type     | Default | Description                                                       |
| ------------------ | -------- | ------- | ----------------------------------------------------------------- |
| `sendReq`          | boolean  | —       | When set to `true`, opens a new WebSocket connection.             |
| `setSendReq`       | function | —       | Function to reset `sendReq` to `false` after connection.          |
| `url`              | string   | —       | WebSocket endpoint (relative path).                               |
| `onOpen`           | function | —       | Callback when the connection opens. Receives the socket instance. |
| `onMessage`        | function | —       | Callback for incoming messages. Receives the event object.        |
| `onError`          | function | —       | Callback for errors. Receives the error object.                   |
| `onClose`          | function | —       | Callback when the connection closes.                              |
| `showLoading`      | boolean  | `true`  | Whether to show loading state via Redux.                          |
| `showErrerMessage` | boolean  | `true`  | Whether to show error messages via alert system.                  |

### **Returns**

- `socketRef`: Ref to the WebSocket instance.
- `send`: Function to send data through the socket (`send(data)`).

### **Example Usage**

```jsx
const [sendReq, setSendReq] = useState(false);
const { socketRef, send } = useWebSocket({
  sendReq,
  setSendReq,
  url: "/ws/chat/",
  onMessage: (event) => {
    const data = JSON.parse(event.data);
    // handle incoming data
  },
});
```

---

## 📁 Location

All hooks are located in `src/hooks/`. See the source code for advanced usage and customization.

---
