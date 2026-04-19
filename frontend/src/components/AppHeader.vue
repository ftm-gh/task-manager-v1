<!--
  AppHeader (also called NavBar) — the top navigation bar.

  This is a more refined version with:
  - Logo/brand area
  - Navigation links
  - User info dropdown area
  - Responsive-friendly layout

  🔑 DESIGN PATTERN: "Container/Presentational" Components

  AppHeader is mostly "presentational" — it displays things and emits events.
  It reads from the auth store but doesn't do heavy logic.

  This makes it easy to test, reuse, and understand.
-->

<template>
  <header class="app-header">
    <div class="header-content">
      <!-- Left side: Logo/Brand -->
      <router-link to="/" class="brand">
        <span class="brand-icon">📋</span>
        <span class="brand-text">TaskManager</span>
      </router-link>

      <!-- Right side: Navigation -->
      <nav class="header-nav">
        <template v-if="authStore.isLoggedIn">
          <router-link to="/dashboard" class="nav-link" active-class="nav-link-active">
            <!--
              🔑 active-class="nav-link-active"

              Vue Router automatically adds a CSS class to a <router-link>
              when its destination matches the CURRENT URL.

              By default, it adds "router-link-active".
              active-class lets you customize the class name.

              So when the user is on /tasks, this link gets the class
              "nav-link nav-link-active" — and we can style it differently
              (e.g., bold or underlined) to show which page they're on.
            -->
            📝 My Tasks
          </router-link>

          <div class="user-section">
            <span class="user-greeting">
              Hello, <strong>{{ authStore.user?.username }}</strong>
            </span>
            <button @click="handleLogout" class="btn-logout">
              Logout
            </button>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="nav-link" active-class="nav-link-active">
            Login
          </router-link>
          <router-link to="/register" class="nav-link nav-link-register" active-class="nav-link-active">
            Sign Up
          </router-link>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

function handleLogout() {
  authStore.logout()
  router.push({ name: 'Login' })
}
</script>

<style scoped>
.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 0 24px;
  /*
    Padding 0 on top/bottom because we set height with min-height.
    24px on left/right for breathing room from the edges.
  */

  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  /*
    A subtle shadow below the header.
    This gives it a sense of depth — the header feels like it's
    "floating" above the page content.
  */

  position: sticky;
  top: 0;
  z-index: 100;
  /*
    🔑 position: sticky + top: 0

    This makes the header "stick" to the top of the page when scrolling.
    As you scroll down, the header stays visible.

    Without sticky: the header scrolls away with the rest of the content.
    With sticky: the header locks in place at the top.

    z-index: 100 ensures the header appears ON TOP of other content.
    Higher z-index = closer to the viewer (like layers in Photoshop).
    Other elements default to z-index: 0, so 100 puts the header above everything.
  */
}

.header-content {
  max-width: 1100px;
  margin: 0 auto;
  /* Center the header content, matching the main content width */

  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 60px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: white;
}

.brand-icon {
  font-size: 1.5rem;
}

.brand-text {
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: -0.5px;
  /*
    Negative letter-spacing brings letters closer together.
    This is a common design trick for bold headings — it makes them
    look tighter and more professional.
  */
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  color: rgba(255, 255, 255, 0.8);
  /*
    rgba with 0.8 opacity = slightly transparent white.
    The active link will be fully opaque (1.0), creating contrast.
  */
  text-decoration: none;
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background-color 0.2s, color 0.2s;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-link-active {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
  /* The active page link is brighter and has a background */
}

.nav-link-register {
  background-color: #3498db;
  color: white;
}

.nav-link-register:hover {
  background-color: #2980b9;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-left: 8px;
  padding-left: 14px;
  border-left: 1px solid rgba(255, 255, 255, 0.2);
  /* A subtle vertical line separating nav links from user info */
}

.user-greeting {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.85rem;
}

.btn-logout {
  background-color: rgba(231, 76, 60, 0.8);
  color: white;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-logout:hover {
  background-color: #e74c3c;
}
</style>
