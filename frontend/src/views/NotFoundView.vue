<!--
  NotFoundView — Shown when the user visits a URL that doesn't exist.
  
  Example: /blahblah or /settings (if that route doesn't exist)
  
  🔑 KEY CONCEPT: 404 Page
  
  In web development, "404" means "Not Found."
  Every good app should have a custom 404 page instead of showing
  a blank page or a confusing browser error.
  
  To make this work, you need a "catch-all" route in the router:
  
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView
  }
  
  :pathMatch(.*)* matches ANY URL that didn't match the other routes.
  It's like a safety net that catches everything else.
-->

<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1 class="error-code">404</h1>
      <h2>Page Not Found</h2>
      <p>
        Oops! The page you're looking for doesn't exist or has been moved.
      </p>
      <router-link to="/" class="btn btn-primary">
        ← Back to Home
      </router-link>
    </div>
  </div>
</template>

<script setup>
/*
  This component has no logic — it's purely visual.
  That's perfectly fine! Not every component needs JavaScript.
  
  <script setup> is still included (even if empty) as a good practice,
  making it easy to add logic later if needed.
*/
</script>

<style scoped>
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
  text-align: center;
}

.not-found-content {
  padding: 40px;
}

.error-code {
  font-size: 8rem;
  /*
    8rem ≈ 128px — a very large number for visual impact.
    The "404" number is the focal point of this page.
  */
  
  font-weight: 800;
  color: #e0e0e0;
  line-height: 1;
  /*
    line-height: 1 means the line height equals the font size.
    Without this, there would be extra space above/below the "404" text
    because default line-height is typically 1.5.
  */
  
  margin-bottom: 10px;
}

h2 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

p {
  color: #7f8c8d;
  font-size: 1.1rem;
  margin-bottom: 30px;
}

.btn {
  display: inline-block;
  padding: 14px 30px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.2s, transform 0.1s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}
</style>