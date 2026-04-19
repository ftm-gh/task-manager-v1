/**
 * router/index.js — Vue Router Configuration
 *
 * WHAT IS ROUTING?
 * In a traditional website, each page is a separate HTML file:
 *   /login  → login.html
 *   /dashboard → dashboard.html
 *   Clicking a link loads a WHOLE NEW PAGE from the server.
 *
 * In a Single Page Application (SPA), there's only ONE HTML file.
 * The router SIMULATES multiple pages by swapping Vue components
 * without reloading the page. This makes the app feel FAST and smooth.
 *
 *   URL: /login      → Show LoginView component
 *   URL: /dashboard  → Show DashboardView component
 *   URL: /register   → Show RegisterView component
 */

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NotFoundView from '../views/NotFoundView.vue'


// Define the routes: which URL shows which component
const routes = [
  {
    path: '/',
    redirect: '/dashboard'
    //   When user visits the root URL, redirect to dashboard
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    //   () => import() is called LAZY LOADING
    //   The component's code is only downloaded when the user visits this page
    //   This makes the initial page load faster
    meta: { requiresGuest: true }
    //   meta is custom data we attach to the route
    //   requiresGuest: only for NOT logged-in users (logged-in users get redirected)
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true }
    //   requiresAuth: only for logged-in users (guests get redirected to login)
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue')
    //   This matches ANY URL that doesn't match the above routes
    //   It's a "catch-all" that shows a 404 page
  }
]

const router = createRouter({
  history: createWebHistory(),
  //   createWebHistory() uses clean URLs like /dashboard
  //   (as opposed to hash-based URLs like /#/dashboard)
  routes
})

// NAVIGATION GUARD: Code that runs BEFORE every page change
// This is how we protect pages that require authentication
router.beforeEach(async (to, from) => {
  //   to   = the route the user is trying to go TO
  //   from = the route the user is coming FROM

  const authStore = useAuthStore()

  // If we haven't checked authentication yet, do it now
  if (authStore.user === null && !authStore.loading) {
    await authStore.checkAuth()
  }

  // If the page requires login and user is NOT logged in → go to login
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return { name: 'Login' }
    //   Returning an object tells the router to go there instead
  }

  // If the page is for guests only and user IS logged in → go to dashboard
  if (to.meta.requiresGuest && authStore.isLoggedIn) {
    return { name: 'Dashboard' }
  }

  // Otherwise, allow the navigation
  // (returning nothing = "proceed normally")
})

export default router