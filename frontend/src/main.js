/*
╔══════════════════════════════════════════════════════════════╗
║  main.js — The VERY FIRST JavaScript file that runs         ║
╚══════════════════════════════════════════════════════════════╝

🔑 KEY CONCEPT: What does "entry point" mean?

When you open a book, you start at page 1.
When a browser loads your app, it starts at main.js.

In index.html, we have:
<script type="module" src="/src/main.js"></script>

That tells the browser: "Start here." Everything else in the app
is loaded BECAUSE main.js imports it (directly or indirectly).

The chain of imports:
main.js
→ imports App.vue
→ imports AppHeader.vue
→ imports router/index.js
→ imports LoginView.vue, RegisterView.vue, TasksPage.vue, etc.
→ imports Pinia (state management)

So main.js is the root of a tree — it pulls in everything the app needs.


🔑 What does main.js actually DO? (4 steps)

1. CREATE the Vue app instance
2. INSTALL plugins (router for navigation, Pinia for state)
3. (Optional) Set up any global configurations
4. MOUNT the app to the DOM (attach it to the HTML page)

After step 4, the app is alive and the user can see it.
*/


// ════════════════════════════════════════════════════
// STEP 0: IMPORTS — Gather all the tools we need
// ════════════════════════════════════════════════════

import { createApp } from 'vue'
/*
🔑 What is createApp?

createApp is a FUNCTION provided by the Vue library.
It creates a new Vue application instance.

Think of it like:
- Vue is a car factory
- createApp() builds one specific car
- You then customize the car (add GPS, add trunk storage)
- Finally you drive it (mount it)

We import it using "destructuring":
{ createApp } means "from the vue module, give me JUST the createApp function."

The vue module exports MANY things (ref, computed, watch, etc.),
but we only need createApp here.

This is called a "named import" — you specify exactly what you want.
The alternative is a "default import":
import something from 'vue'  ← gets the default export
import { createApp } from 'vue'  ← gets a specific named export
*/

import { createPinia } from 'pinia'
/*
🔑 What is Pinia? (Recap with more detail)

Pinia is a STATE MANAGEMENT library for Vue.

"State" = data that your app needs to remember.

Types of state:
1. LOCAL state — data used by ONE component only
   Example: whether a dropdown is open or closed
   → Use ref() inside the component

2. SHARED state — data used by MULTIPLE components
   Example: the logged-in user's info, the JWT token
   → Use a Pinia store

Without Pinia, sharing data between unrelated components is painful:

┌─────────┐
│ App.vue  │  ← You'd have to store everything HERE
│          │     and pass it down through EVERY level
├──────────┤
│ Header   │  ← needs user info (passed down from App)
├──────────┤
│ TaskPage │  ← needs user info (passed down from App)
│  └ TaskItem │  ← needs user info (passed down from TaskPage from App)
└──────────┘

With Pinia:

┌────────────────┐
│  Auth Store 📦  │  ← ANY component can access directly
└────────────────┘
↕    ↕    ↕
Header TaskPage TaskItem   ← all read from the store directly

createPinia() creates the Pinia instance (the "store manager").
Individual stores (like useAuthStore) are defined in /stores/auth.js.
*/

import App from './App.vue'
/*
🔑 Importing a .vue file

This imports our root component — the outer shell of the app.

When you import a .vue file:
1. Vite (our build tool) sees the .vue extension
2. The @vitejs/plugin-vue plugin processes it
3. It splits the file into:
    - JavaScript (from <script>)
    - HTML template (from <template>) → compiled into a render function
    - CSS (from <style>) → injected into the page
4. The result is a JavaScript object (a "component definition")

So "App" here is not HTML — it's a JavaScript object that Vue
knows how to turn into HTML.

"Default import" — App.vue exports itself as the default export,
so we import it without curly braces: import App from './App.vue'
*/

import router from './router'
/*
🔑 Importing the router

This imports from ./router/index.js
(When you import a folder, JavaScript automatically looks for index.js inside it)

The router object knows:
- All the routes (URL → component mappings)
- The navigation guards (e.g., redirect to /login if not authenticated)
- The history mode (clean URLs vs hash URLs)

We'll install it as a plugin so that:
- <router-link> and <router-view> work in templates
- useRouter() and useRoute() work in scripts
- Navigation guards run before every page change
  */


// ════════════════════════════════════════════════════
// STEP 1: CREATE the Vue application
// ════════════════════════════════════════════════════

const app = createApp(App)
/*
This creates the Vue application instance.

"App" (our root component) is passed as the argument.
This tells Vue: "When you render, start with App.vue."

At this point:
✅ The app object exists in memory
❌ Nothing is visible on the page yet
❌ No plugins are installed yet
❌ The app is not connected to the HTML page yet

The "app" variable is the heart of your application.
Everything gets attached to it.

🔑 ANALOGY:
Think of building a sandwich:
- createApp(App) = you have the bread (the base)
- app.use(...)   = you add toppings (plugins)
- app.mount(...) = you serve it (make it visible)
  */


// ════════════════════════════════════════════════════
// STEP 2: INSTALL plugins
// ════════════════════════════════════════════════════

const pinia = createPinia()
/*
Create the Pinia instance.
This is the "store manager" that keeps track of all your stores.

You only create ONE Pinia instance for the entire app.
Individual stores (auth, tasks, etc.) register themselves with
this instance when they're first used.
*/

app.use(pinia)
/*
🔑 What does app.use() do?

app.use(plugin) INSTALLS a plugin into the Vue app.

A plugin is a piece of code that adds GLOBAL functionality:
- New components available everywhere
- New methods available in every component
- Hooks into Vue's internal systems

app.use(pinia) does:
1. Makes Pinia available throughout the entire app
2. Every component can now call useAuthStore(), useTaskStore(), etc.
3. Pinia injects itself into Vue's reactivity system

ORDER MATTERS: Install Pinia BEFORE the router, because
the router's navigation guards might use Pinia stores.
If the router runs before Pinia is installed, the stores
won't be available yet, and you'll get an error.
*/

app.use(router)
/*
Install the Vue Router plugin.

This does several things:
1. Registers <router-link> as a global component
   (so you can use it in any .vue file without importing)
2. Registers <router-view> as a global component
3. Makes useRouter() and useRoute() available in any component
4. Starts watching the browser's URL for changes
5. Runs navigation guards on every route change

After this line, the router is "alive" and listening for URL changes.
*/


// ════════════════════════════════════════════════════
// STEP 3: GLOBAL CONFIGURATIONS (Optional)
// ════════════════════════════════════════════════════

/*
🔑 You can add global configurations here if needed.
Some common examples (NOT required for our app, just for learning):
*/

// Example 1: Global error handler
app.config.errorHandler = (err, instance, info) => {
/*
This catches errors that occur ANYWHERE in the Vue app.
Without this, errors would just show in the browser console.

    In a production app, you might send these to an error tracking
    service like Sentry or LogRocket.

    Parameters:
    - err: the Error object
    - instance: the Vue component where the error occurred
    - info: a string describing where the error happened
            (e.g., "render function", "watcher callback")
*/
console.error('🚨 Global Vue Error:', err)
console.error('   Component:', instance)
console.error('   Info:', info)

// In production, you'd send this to an error tracking service:
// errorTrackingService.captureException(err, { extra: { info } })
}

// Example 2: Performance warnings during development
app.config.performance = false
/*
When set to true, Vue tracks component render performance
and shows it in the browser's DevTools (Performance tab).

Useful for finding slow components during development.
NEVER enable in production (it adds overhead).

We keep it false here, but you can try setting it to true
and checking the browser DevTools.
*/

// Example 3: Global properties (available in every component)
app.config.globalProperties.$appName = 'Task Manager'
/*
🔑 What is globalProperties?

It lets you add variables/functions accessible in EVERY component's template.

In any component's template, you could now do:
<h1>{{ $appName }}</h1>  → renders "Task Manager"

The $ prefix is a convention for global properties to distinguish them
from the component's own data.

⚠️ Use sparingly! Overusing global properties makes code hard to trace.
For most cases, Pinia stores are a better choice for shared data.

This is shown here for educational purposes.
*/


// ════════════════════════════════════════════════════
// STEP 4: MOUNT the app to the DOM
// ════════════════════════════════════════════════════

app.mount('#app')
/*
🔑 THE MOST IMPORTANT LINE IN THIS FILE

This connects the Vue app to the actual HTML page.

'#app' is a CSS selector that targets <div id="app"></div> in index.html.

What happens when mount() runs:
1. Vue finds the <div id="app"></div> in the HTML
2. Vue renders App.vue's template into HTML
3. Vue replaces the empty div's content with the rendered HTML
4. Vue sets up reactivity — now when data changes, the HTML auto-updates
5. The app is LIVE — the user can see and interact with it!

Before mount():
<div id="app"></div>  ← empty

After mount():
<div id="app">
<header class="app-header">...</header>    ← AppHeader
<main class="main-content">
<div class="home">Welcome!</div>          ← HomeView (from router)
</main>
<footer class="app-footer">...</footer>     ← Footer
</div>

🔑 IMPORTANT: mount() should be the LAST thing you call.
All plugins must be installed BEFORE mounting.
Once the app is mounted, you can't install more plugins.

It's like sealing an envelope:
- Put everything inside first (plugins, configs)
- Then seal it (mount)
- You can't add more stuff after sealing


🔑 TIMELINE OF WHAT HAPPENS:

1. Browser loads index.html
2. Browser sees <script src="/src/main.js">
3. Browser downloads and runs main.js
4. main.js imports all dependencies (Vue, Pinia, Router, App.vue, etc.)
5. createApp(App) creates the app instance
6. app.use(pinia) installs state management
7. app.use(router) installs navigation
8. app.mount('#app') renders everything to the page
9. Router checks the current URL and renders the matching page
10. onMounted() in App.vue checks if saved token is still valid
11. ✨ App is ready! User can interact with it.

All of this happens in about 100-300 milliseconds.
*/


/*
════════════════════════════════════════════════════
📝 SUMMARY
════════════════════════════════════════════════════

This file does 4 things:

1. IMPORTS everything the app needs:
    - createApp from Vue (to create the app)
    - createPinia (for shared state)
    - App.vue (the root component)
    - router (for page navigation)

2. CREATES the Vue app with App.vue as the root

3. INSTALLS plugins:
    - Pinia (state management — shared data across components)
    - Router (URL-based navigation between pages)

4. MOUNTS the app to <div id="app"> in index.html

After these 4 steps, the application is fully running.


════════════════════════════════════════════════════
🧠 CONCEPTS COVERED IN THIS FILE
════════════════════════════════════════════════════

- Entry point / bootstrapping
- ES Module imports (named vs default)
- Vue application instance
- Plugin system (app.use())
- State management (Pinia)
- Client-side routing (Vue Router)
- DOM mounting
- Global configuration
- Application lifecycle
  */
