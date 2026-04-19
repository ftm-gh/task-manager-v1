/**
 * api/axios.js — Configured HTTP Client
 *
 * WHAT IS AXIOS?
 * Axios is a library for making HTTP requests from JavaScript.
 * It's like the "waiter" that carries orders (requests) from the
 * frontend (dining room) to the backend (kitchen) and brings back food (responses).
 *
 * WHY CONFIGURE IT IN ONE PLACE?
 * Every request to our backend needs the same base URL and settings.
 * Instead of repeating this everywhere, we configure it once.
 * This is the DRY principle again!
 */

import axios from 'axios'

// Create a custom Axios instance with default settings
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  //   All requests will be prefixed with this URL
  //   So api.get('/tasks') actually calls http://localhost:5000/api/tasks

  withCredentials: true,
  //   Send cookies with every request
  //   This is needed for session-based authentication to work
  //   (the session ID is stored in a cookie)

  headers: {
    'Content-Type': 'application/json'
    //   Tell the backend we're sending JSON data
  }
})

// INTERCEPTOR: Code that runs for every response
// An interceptor is like a filter — it processes responses before your code sees them
api.interceptors.response.use(
  // If the request SUCCEEDED, just pass the response through
  (response) => response,

  // If the request FAILED, handle common errors
  (error) => {
    if (error.response && error.response.status === 401) {
      // 401 = Unauthorized → user's session expired
      // Redirect to login page
    //   window.location.href = '/login'
        
    }
    // Re-throw the error so the calling code can also handle it
    return Promise.reject(error)
  }
)

export default api