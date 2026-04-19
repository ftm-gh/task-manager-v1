<!--
  RegisterView — Create a new account.

  Differences from LoginView:
  1. Extra "confirm password" field
  2. Calls authStore.register() instead of .login()
  3. On success, redirects to /login (user must log in after registering)
  4. Has more client-side validation (password strength, matching passwords)
-->

<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h2>📝 Create Account</h2>
        <p>Sign up to start managing your tasks</p>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="Choose a username (min. 3 characters)"
            autocomplete="username"
            required
            minlength="3"
          />
          <!-- Show a hint below the input -->
          <small class="field-hint">Must be at least 3 characters</small>
          <!--
            <small> is a semantic HTML tag for "fine print" or secondary text.
            We use it for form field hints.
          -->
        </div>

        <div class="form-group">
        <label for="email">Email</label>
        <input
            id="email"
            v-model="email"
            type="email"
            placeholder="Enter your email"
            required
        />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Choose a password (min. 6 characters)"
            autocomplete="new-password"
            required
            minlength="6"
          />
          <small class="field-hint">Must be at least 6 characters</small>
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            placeholder="Re-enter your password"
            autocomplete="new-password"
            required
          />

          <!-- Real-time password match indicator -->
          <small
            v-if="confirmPassword.length > 0"
            :class="passwordsMatch ? 'match-ok' : 'match-error'"
          >
            {{ passwordsMatch ? '✓ Passwords match' : '✗ Passwords do not match' }}
          </small>
          <!--
            This shows real-time feedback as the user types the confirmation password.

            v-if="confirmPassword.length > 0"
              Only show AFTER the user starts typing (not on an empty field).

            :class="passwordsMatch ? 'match-ok' : 'match-error'"
              Dynamically apply a CSS class based on whether passwords match.
              Green text if they match, red if they don't.
          -->
        </div>

        <transition name="fade">
          <p v-if="errorMessage" class="error-message">
            ⚠️ {{ errorMessage }}
          </p>
        </transition>

        <transition name="fade">
          <p v-if="successMessage" class="success-message">
            ✅ {{ successMessage }}
          </p>
        </transition>

        <button type="submit" class="btn btn-primary" :disabled="isLoading">
          <span v-if="isLoading" class="spinner"></span>
          {{ isLoading ? 'Creating Account...' : 'Register' }}
        </button>
      </form>

      <div class="auth-footer">
        <p>
          Already have an account?
          <router-link to="/login" class="link">Log in here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
/*
  🔑 What is computed()?

  A computed property is a value that is AUTOMATICALLY RECALCULATED
  whenever its dependencies change.

  It's like a formula in a spreadsheet:
  If cell A1 = 5, and cell B1 = "=A1 * 2", then B1 = 10.
  If you change A1 to 7, B1 automatically becomes 14.

  computed() works the same way:
  If password changes or confirmPassword changes,
  passwordsMatch automatically recalculates.

  You COULD use a regular function instead, but computed is:
  1. Cached — it only recalculates when dependencies change
  2. Accessed like a variable, not called like a function
     passwordsMatch.value (not passwordsMatch())
*/

import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isLoading = ref(false)
const email = ref('')

const router = useRouter()
const authStore = useAuthStore()

// Computed property: do the two passwords match?
const passwordsMatch = computed(() => {
  return password.value === confirmPassword.value
})
/*
  Every time password.value or confirmPassword.value changes
  (i.e., every keystroke), this recalculates.

  The template uses passwordsMatch (without .value) because
  Vue auto-unwraps computed values in templates, just like ref.
*/

async function handleRegister() {
  errorMessage.value = ''
  successMessage.value = ''

  // ── Client-side validations ──
  const trimmedUsername = username.value.trim()

  if (trimmedUsername.length < 3) {
    errorMessage.value = 'Username must be at least 3 characters.'
    return
  }

  if (password.value.length < 6) {
    errorMessage.value = 'Password must be at least 6 characters.'
    return
  }

  if (!passwordsMatch.value) {
    errorMessage.value = 'Passwords do not match.'
    return
  }

  isLoading.value = true

  try {
    const result = await authStore.register(trimmedUsername, email.value.trim(), password.value)

    if (result.success) {
      successMessage.value = 'Account created! Redirecting to dashboard...'

      // Wait 1.5 seconds, then redirect
      setTimeout(() => router.push({ name: 'Dashboard' }), 1500)

    } else {
      errorMessage.value = result.message
    }
  } catch (err) {
    errorMessage.value = 'An unexpected error occurred. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Same layout styles as LoginView */
.auth-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 40px;
  min-height: 80vh;
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
}

.field-hint {
  color: #999;
  font-size: 0.8rem;
}

.match-ok {
  color: #27ae60;
  font-size: 0.8rem;
  font-weight: 600;
}

.match-error {
  color: #e74c3c;
  font-size: 0.8rem;
  font-weight: 600;
}

.error-message {
  color: #e74c3c;
  background-color: #fdf0ef;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
}

.success-message {
  color: #27ae60;
  background-color: #eafaf1;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
}

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

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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
