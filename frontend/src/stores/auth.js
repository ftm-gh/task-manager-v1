/**
 * stores/auth.js — Authentication Store (Pinia)
 *
 * WHAT IS STATE MANAGEMENT?
 * "State" is all the data your app is currently tracking:
 *   - Is the user logged in? (auth state)
 *   - What tasks are loaded? (task state)
 *   - Which filter is active? (UI state)
 *
 * Without a store, each component manages its own data.
 * Problem: if ComponentA and ComponentB both need user info,
 * how do they share it? Passing data through many layers of
 * components is messy (called "prop drilling").
 *
 * A STORE (Pinia) is a SINGLE SOURCE OF TRUTH — one central place
 * where shared data lives. Any component can read from it or update it.
 *
 *     ┌─────────┐     ┌─────────┐     ┌─────────┐
 *     │ Header  │     │ Sidebar │     │ TaskList│
 *     │ (needs  │     │ (needs  │     │ (needs  │
 *     │  user)  │     │  user)  │     │  tasks) │
 *     └────┬────┘     └────┬────┘     └────┬────┘
 *          │               │               │
 *          ▼               ▼               ▼
 *     ┌──────────────────────────────────────────┐
 *     │          Pinia Store (central)           │
 *     │   user: {id: 1, name: "alice"}           │
 *     │   tasks: [{...}, {...}]                  │
 *     └──────────────────────────────────────────┘
 */

import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', {
  // STATE: The data this store manages
  // Think of it as the "variables" for authentication
  state: () => ({
    user: null,       // null = not logged in, object = logged in
    loading: false,   // true while a request is in progress
    error: null       // error message if something went wrong
  }),

  // GETTERS: Computed values derived from the state
  // They automatically recalculate when the state changes
  // (like formulas in a spreadsheet)
  getters: {
    isLoggedIn: (state) => state.user !== null,
    //   Simple check: if user object exists, they're logged in
    username: (state) => state.user?.username || ''
    //   The ?. is "optional chaining" — if user is null, returns undefined
    //   instead of crashing with "Cannot read property of null"
  },

  // ACTIONS: Functions that can change the state
  // Usually involve calling the API and then updating the state
  actions: {
    async register(username, email, password) {
      /**
       * WHAT IS ASYNC/AWAIT?
       * HTTP requests take time (the server needs to respond).
       * "async/await" lets us write code that WAITS for the response
       * without freezing the entire page.
       *
       * Without async/await:
       *   api.post('/auth/register', data)
       *     .then(response => { ... })    ← "callback" style, gets messy
       *     .catch(error => { ... })
       *
       * With async/await:
       *   const response = await api.post('/auth/register', data)
       *   Much cleaner! Reads like normal code.
       */
      this.loading = true
      this.error = null
      try {
        await api.post('/auth/register', { username, email, password })
        // If we get here, registration succeeded.
        // Now log them in automatically:
        await this.login(username, password)
        return {success: true}
      } catch (err) {
        const message = err.response?.data?.error || 'Registration failed'
        this.error = message
        return { success: false, message }
      } finally {
        // "finally" runs no matter what — success or error
        this.loading = false
      }
    },

    async login(username, password) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('/auth/login', { username, password })
        this.user = response.data.user
        //   Store the user info in our state
        //   Now EVERY component can access this.user
        return { success: true }
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        await api.post('/auth/logout')
      } finally {
        this.user = null    // Clear user state regardless of API success
      }
    },

    async checkAuth() {
      /**
       * Called when the app first loads.
       * Checks if the user's session cookie is still valid.
       * (The user might have logged in yesterday and still has the cookie.)
       */
      try {
        const response = await api.get('/auth/me')
        this.user = response.data
      } catch {
        this.user = null    // Session expired or invalid
      }
    }
  }
})
