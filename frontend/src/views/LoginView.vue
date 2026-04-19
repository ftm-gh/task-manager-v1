<!--
  LoginView — The login form page.

  What happens when a user logs in:
  ?

  This is the full flow from button click to seeing your tasks!
-->

<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h2>📋 Welcome Back</h2>
        <p>Log in to manage your tasks</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <!--
          🔑 @submit.prevent explained step by step:

          1. The user clicks "Login" or presses Enter inside the form
          2. The browser fires a "submit" event on the <form>
          3. @submit catches that event
          4. .prevent calls event.preventDefault() — stops the browser from
             reloading the page (the old HTML way of handling forms)
          5. "handleLogin" is our function that runs instead

          Modifiers (.prevent, .stop, .once) are a Vue convenience feature.
          Without .prevent, you'd have to write:
            function handleLogin(event) {
              event.preventDefault()
              // ... rest of logic
            }
        -->

        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="Enter your username"
            autocomplete="username"
            required
          />
          <!--
            autocomplete="username" tells the browser:
            "This field is for a username — you can offer to auto-fill it
            from the user's saved credentials."

            required: The browser won't submit the form if this is empty.
            It shows a built-in tooltip like "Please fill out this field."
          -->
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Enter your password"
            autocomplete="current-password"
            required
          />
        </div>

        <!-- Error message — only appears when errorMessage is not empty -->
        <transition name="fade">
          <!--
            🔑 <transition> is a Vue built-in component for animations.

            When the element inside appears or disappears (v-if toggling),
            Vue automatically adds CSS classes:
            - .fade-enter-from    → starting state when APPEARING
            - .fade-enter-active  → transition while appearing
            - .fade-leave-to      → ending state when DISAPPEARING
            - .fade-leave-active  → transition while disappearing

            We define these classes in <style> below.
            Without <transition>, the error message would just pop in/out instantly.
          -->
          <p v-if="errorMessage" class="error-message">
            ⚠️ {{ errorMessage }}
          </p>
        </transition>

        <button type="submit" class="btn btn-primary" :disabled="isLoading">
          <span v-if="isLoading" class="spinner"></span>
          <!--
            A CSS spinner (loading animation) shown while waiting for the server.
            Better UX than just changing button text.
          -->
          {{ isLoading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <div class="auth-footer">
        <p>
          Don't have an account?
          <router-link to="/register" class="link">Create one here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// ── Reactive state ──
const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const router = useRouter()
const authStore = useAuthStore()

async function handleLogin() {
  // Reset error message from previous attempts
  errorMessage.value = ''

  // Basic client-side validation
  if (username.value.trim().length < 3) {
    errorMessage.value = 'Username must be at least 3 characters.'
    return
  }

  isLoading.value = true

  try {
    const result = await authStore.login(
      username.value.trim(),
      password.value
    )

    if (result.success) {
      // Navigate to tasks page
      router.push({ name: 'Dashboard' })
      return { success: true }
    } else {
      errorMessage.value = result.message
      return { success: false, reason: result.message }
    }
  } catch (err) {
    errorMessage.value = 'An unexpected error occurred. Please try again.'
    return { success: false, reason: err.message }
    /*
      This catch handles truly unexpected errors (network failure,
      JavaScript bugs, etc.) — not server-returned errors,
      which are handled by the result.success check above.
    */
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  /*
    flex-start = align to the top (not vertically centered).
    For a login page, centering vertically can look weird on tall screens.
  */
  padding-top: 60px;
  min-height: 80vh;
  /*
    vh = "viewport height" — a percentage of the browser window height.
    80vh = 80% of the window. This ensures the page takes up most of the screen.
  */
}

.auth-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 40px;
  width: 100%;
  max-width: 420px;
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-header h2 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 8px;
}

.auth-header p {
  color: #7f8c8d;
  font-size: 0.95rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-weight: 600;
  color: #555;
  font-size: 0.9rem;
}

input {
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.15);
  /*
    A subtle blue glow around the focused input.
    The "0 0 0 3px" creates a "ring" (no offset, no blur, 3px spread).
    This is a modern design pattern for accessible focus indicators.
  */
}

.error-message {
  color: #e74c3c;
  background-color: #fdf0ef;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
}

/* Fade transition for error message */
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.btn {
  padding: 14px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background-color 0.2s, transform 0.1s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2980b9;
  transform: translateY(-1px);
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* CSS-only loading spinner */
.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  /*
    animation: name duration timing-function iteration-count
    - spin: the keyframe animation name (defined below)
    - 0.6s: one full rotation takes 0.6 seconds
    - linear: constant speed (no acceleration)
    - infinite: loops forever
  */
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
  /*
    @keyframes defines an animation.
    "to" means the END state (from 0deg to 360deg = one full rotation).
    The browser smoothly transitions from the start (0deg) to the end (360deg).
  */
}

.auth-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  color: #777;
  font-size: 0.9rem;
}

.link {
  color: #3498db;
  text-decoration: none;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}
</style>
