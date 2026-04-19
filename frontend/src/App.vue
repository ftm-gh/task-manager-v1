<!--
  App.vue — The ROOT COMPONENT of the entire application.

  🔑 KEY CONCEPT: What is a Root Component?

  Every Vue application has exactly ONE root component. It's the "outermost shell"
  that wraps everything else. Think of it like the frame of a house:
  - The frame (App.vue) stays the same
  - The rooms inside (pages) change as you navigate

  App.vue typically contains:
  1. Things that appear on EVERY page (like the header/navbar)
  2. A <router-view /> placeholder where page content swaps in and out
  3. Global styles that apply to the whole app

  Component tree:

  App.vue                        ← YOU ARE HERE (the root)
  ├── AppHeader                  ← Always visible (navigation bar)
  └── <router-view />            ← Changes based on URL:
       ├── HomeView       (/)
       ├── LoginView       (/login)
       ├── RegisterView    (/register)
       ├── TasksPage       (/tasks)
       └── NotFoundView    (anything else)
-->

<template>
  <div id="app-root">
    <!--
      We wrap everything in a single root <div>.

      In Vue 3, you CAN have multiple root elements (called "fragments"),
      but wrapping in one div is still common because:
      1. It's easier to apply global layout styles
      2. It avoids edge cases with transitions and teleports
      3. It's a clear visual structure
    -->

    <!-- ── App Header (Navigation Bar) ── -->
    <AppHeader />
    <!--
      The AppHeader component appears at the TOP of every single page.
      It contains the logo, navigation links, and login/logout buttons.

      Because it's here in App.vue (outside <router-view>), it NEVER disappears
      when the user navigates between pages. Only the content below it changes.

      🔑 WHY put it here instead of inside each page?

      BAD approach (duplicating the header in every view):
        LoginView.vue:    <AppHeader /> + login form
        RegisterView.vue: <AppHeader /> + register form
        TasksPage.vue:    <AppHeader /> + task list

      GOOD approach (header once in App.vue):
        App.vue:          <AppHeader /> + <router-view />
        LoginView.vue:    just the login form
        RegisterView.vue: just the register form
        TasksPage.vue:    just the task list

      This follows the DRY principle (Don't Repeat Yourself).
    -->

    <!-- ── Main Content Area ── -->
    <main class="main-content">
      <!--
        <main> is a semantic HTML5 element meaning "the main content of the page."
        Screen readers and search engines use it to identify the primary content.

        It works exactly like a <div>, but with added meaning.
        Other semantic elements: <header>, <nav>, <footer>, <article>, <section>
      -->

      <router-view v-slot="{ Component }">
        <!--
          🔑 <router-view> — The Page Placeholder

          This is where Vue Router renders the current page's component.

          URL: /           → HomeView appears here
          URL: /login      → LoginView appears here
          URL: /tasks      → TasksPage appears here
          URL: /xyz        → NotFoundView appears here

          Everything OUTSIDE <router-view> (like AppHeader) stays the same.
          Only the content INSIDE changes. This is what makes it a
          "Single Page Application" (SPA) — the page never fully reloads.


          🔑 v-slot="{ Component }" — Advanced: Scoped Slot for Transitions

          By default, you can just write <router-view /> and it works.

          But if you want to ADD ANIMATIONS when pages change, you need
          the "scoped slot" syntax. This gives you access to the actual
          component being rendered, so you can wrap it in a <transition>.

          Think of it like:
          - <router-view /> says "show the page"
          - v-slot="{ Component }" says "give me the page, and I'LL decide
            how to show it (with a transition animation)"
        -->

        <transition name="page" mode="out-in">
          <!--
            🔑 <transition> with <router-view>

            This adds a FADE animation when navigating between pages.

            name="page" → CSS classes will be: .page-enter-from, .page-leave-to, etc.

            mode="out-in" → FIRST the old page fades OUT, THEN the new page fades IN.

            Other modes:
            - "in-out": new page fades in first, then old fades out (looks weird usually)
            - (no mode): both happen simultaneously (can cause layout jumps)

            "out-in" is almost always what you want for page transitions.
          -->

          <component :is="Component" />
          <!--
            🔑 <component :is="Component" /> — Dynamic Component

            This is Vue's way of saying "render whatever component this variable holds."

            The "Component" variable comes from the v-slot above — it's whatever
            component Vue Router decided to show based on the current URL.

            It's equivalent to writing <LoginView /> or <TasksPage />,
            but DYNAMICALLY — the actual component changes at runtime.

            Why use this instead of plain <router-view />?
            Because we need to wrap it in <transition>, and <transition>
            needs a SINGLE direct child element — not a <router-view /> tag.
          -->
        </transition>
      </router-view>
    </main>

    <!-- ── Footer ── -->
    <footer class="app-footer">
      <!--
        A simple footer at the bottom of every page.
        Like the header, it's in App.vue so it appears everywhere.
      -->
      <p>
        📋 Task Manager — Built with
        <a href="https://vuejs.org" target="_blank" rel="noopener noreferrer">Vue.js</a>
        &amp;
        <a href="https://flask.palletsprojects.com" target="_blank" rel="noopener noreferrer">Flask</a>
        <!--
          target="_blank" → opens the link in a new tab

          rel="noopener noreferrer" → SECURITY attributes for external links

          🔑 Why noopener noreferrer?

          When you open a link with target="_blank", the NEW page can access
          the ORIGINAL page via window.opener. A malicious site could use this
          to redirect your original page to a phishing site!

          "noopener" prevents this by setting window.opener to null.
          "noreferrer" additionally hides the referrer URL (privacy).

          ALWAYS add these when linking to external sites with target="_blank".

          &amp; is the HTML entity for "&" (ampersand).
          Using & directly in HTML can cause parsing issues in some cases.
        -->
      </p>
    </footer>
  </div>
</template>

<script setup>
/*
  The script section for App.vue is minimal.
  Its only job is to import the AppHeader component.

  All the complex logic lives in the individual page components
  and the stores. App.vue is intentionally simple — it's just
  the layout skeleton.

  🔑 DESIGN PRINCIPLE: Keep the root component thin.
  App.vue should only handle:
  - Layout structure (header, content, footer)
  - Global concerns (maybe a loading overlay or notification system)

  Business logic belongs in views, components, and stores.
*/

import AppHeader from './components/AppHeader.vue'
// Import the navigation header component

import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
/*
  We import the auth store here to do ONE thing on app startup:
  check if a saved token is still valid.
*/

const authStore = useAuthStore()

onMounted(() => { authStore.checkAuth() })

</script>

<style>
/*
  ════════════════════════════════════════════════════════
  GLOBAL STYLES (no "scoped" attribute)
  ════════════════════════════════════════════════════════

  These styles apply to the ENTIRE application — every component.

  🔑 When to use global vs scoped styles:

  GLOBAL (in App.vue, no "scoped"):
  - CSS resets (box-sizing, margin, padding)
  - Base typography (body font, default colors)
  - Layout structure (full-height page, flex container)
  - Utility classes used across many components

  SCOPED (in individual components, with "scoped"):
  - Component-specific styles
  - Anything that should NOT leak to other components

  Rule of thumb: if it affects the whole app → global.
  If it affects one component → scoped.
*/

/* ── CSS Reset ── */
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  /*
    🔑 What is a CSS Reset?

    Every browser applies DEFAULT styles to HTML elements:
    - <body> has 8px margin
    - <h1> has large margin
    - <ul> has left padding
    - etc.

    These defaults are DIFFERENT across browsers (Chrome vs Firefox vs Safari).

    A reset removes all these defaults so you start from a clean slate.
    This way, YOUR styles are the only ones that apply, and the page
    looks the same in every browser.

    * selects ALL elements.
    *::before and *::after select pseudo-elements (decorative elements
    added via CSS, like the bullet points in lists).


    box-sizing: border-box explained:

    WITHOUT border-box (the default):
      width: 200px + padding: 20px + border: 2px = 244px total width 😩
      The padding and border are ADDED to the width.

    WITH border-box:
      width: 200px (includes padding and border) = 200px total width 😊
      What you set is what you get.

    Almost every modern website uses border-sizing: border-box on everything.
  */
}

/* ── Base Styles ── */
html {
  font-size: 16px;
  /*
    Set the base font size.
    All "rem" units are relative to this value:
    1rem = 16px, 1.5rem = 24px, 0.875rem = 14px

    Why rem instead of px?
    If a user has set their browser to use larger text (accessibility),
    rem-based sizes scale up, but px-based sizes don't.
  */

  scroll-behavior: smooth;
  /*
    When clicking an anchor link (#section), the page scrolls smoothly
    instead of jumping instantly. A small but nice touch.
  */
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', Arial, sans-serif;
  /*
    🔑 Font Stack

    This is a list of fonts in order of preference.
    The browser uses the FIRST one it finds on the user's system:

    -apple-system      → macOS/iOS system font (San Francisco)
    BlinkMacSystemFont → Chrome on macOS
    'Segoe UI'         → Windows system font
    Roboto             → Android system font
    Oxygen/Ubuntu      → Linux system fonts
    'Helvetica Neue'   → Older macOS
    Arial              → Universal fallback
    sans-serif         → Ultimate fallback (any sans-serif font)

    This approach uses the user's native OS font, which:
    1. Loads instantly (already on their computer)
    2. Looks familiar and natural to the user
    3. Has excellent readability (optimized by the OS maker)
  */

  background-color: #f0f2f5;
  /* Light gray background — easier on the eyes than pure white */

  color: #333333;
  /* Dark gray text — softer than pure black (#000000) */

  line-height: 1.6;
  /*
    Line height is the space between lines of text.
    1.6 means 1.6 times the font size.
    For 16px font → 25.6px line height.

    Default is about 1.2, which feels cramped.
    1.5 to 1.7 is the sweet spot for readability.
  */

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*
    These make text rendering smoother on macOS/iOS.
    Without them, fonts can look slightly "heavy" or blurry on Retina screens.
    These are vendor-prefixed properties (-webkit for Safari/Chrome, -moz for Firefox).
  */
}

/* ── App Layout ── */
#app-root {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  /*
    🔑 Full-Height Layout with Flexbox

    This creates a layout where:
    - The header sticks to the top
    - The main content fills all available space
    - The footer sticks to the bottom

    Even if the content is very short, the footer stays at the BOTTOM
    of the screen (not floating in the middle).

    min-height: 100vh → the app is AT LEAST as tall as the browser window.
    flex-direction: column → children stack vertically (top to bottom).

    The <main> element gets "flex: 1" (below) to fill remaining space.
  */
}

/* ── Main Content ── */
.main-content {
  flex: 1;
  /*
    flex: 1 means "grow to fill all remaining space."

    If the window is 900px tall:
    - Header: 60px
    - Footer: 50px
    - Main content: 900 - 60 - 50 = 790px (fills the rest)

    This ensures the footer is always pushed to the bottom.
  */

  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  /*
    max-width: 900px → content won't be wider than 900px
    margin: 0 auto → centers the content horizontally

    On a 1920px wide monitor, the content is 900px centered in the middle,
    with empty space on both sides. This is much more readable than
    content stretching the full width.

    On a phone (375px wide), the content fills the whole screen
    because 375px < 900px.
  */

  padding: 24px 16px;
}

/* ── Page Transition Animations ── */
.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
  /*
    New page starts: invisible and 10px below its final position.
  */
}

.page-enter-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
  /*
    Over 0.25 seconds, smoothly animate opacity and position.
    "ease" = start slow, speed up, end slow.
  */
}

.page-leave-from {
  opacity: 1;
  transform: translateY(0);
  /*
    Old page starts: fully visible, in its normal position.
    (This is technically the default, but being explicit is clearer.)
  */
}

.page-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
  /* Leave animation is slightly faster (0.2s) than enter (0.25s).
     This makes the transition feel snappy — the old page leaves quickly,
     and the new page has a moment to settle in. */
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  /*
    Old page ends: invisible and 10px ABOVE (going up as it fades out).

    The old page moves UP and fades out → new page comes from below and fades in.
    This creates a subtle sense of forward motion.
  */
}

/* ── Links ── */
a {
  color: #3498db;
  text-decoration: none;
  /*
    Global link styles:
    - Blue color (the universal "this is clickable" signal)
    - No underline by default (cleaner look)
  */
}

a:hover {
  text-decoration: underline;
  /* Show underline on hover to confirm it's clickable */
}

/* ── Scrollbar Styling (Webkit browsers: Chrome, Safari, Edge) ── */
::-webkit-scrollbar {
  width: 8px;
  /* Thinner than the default scrollbar (usually ~17px) */
}

::-webkit-scrollbar-track {
  background: #f0f0f0;
  /* The "track" is the background of the scrollbar area */
}

::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 4px;
  /* The "thumb" is the draggable part. Rounded corners make it look modern. */
}

::-webkit-scrollbar-thumb:hover {
  background: #aaa;
  /* Slightly darker when hovering over the scrollbar */
}
</style>

<style scoped>
/*
  ════════════════════════════════════════════════════════
  SCOPED STYLES (only apply to App.vue's own elements)
  ════════════════════════════════════════════════════════

  We use a SEPARATE <style scoped> block for styles that should
  only affect elements in THIS component's template.

  Yes, you CAN have both a global <style> and a scoped <style scoped>
  in the same .vue file! Vue processes them both.
*/

.app-footer {
  text-align: center;
  padding: 20px;
  color: #999;
  font-size: 0.85rem;
  border-top: 1px solid #e0e0e0;
  background-color: white;
}

.app-footer a {
  color: #3498db;
  font-weight: 600;
}

.app-footer a:hover {
  color: #2980b9;
}
</style>
