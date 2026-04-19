<!--
  TaskItem.vue — Displays a single task

  WHAT IS A .vue FILE?
  A .vue file is called a "Single File Component" (SFC).
  It bundles THREE things together:
    1. <template> — the HTML (what it LOOKS like)
    2. <script>   — the JavaScript (how it BEHAVES)
    3. <style>    — the CSS (how it's STYLED)

  This keeps everything about one component in one place.
  Compare this to traditional web development where HTML, CSS, and JS
  are in separate files — it's harder to see how they relate.
-->

<template>
  <!--
    :class is "dynamic class binding"
    It adds CSS classes based on conditions:
    - 'completed' class is added if task.is_completed is true
    - The priority name (e.g., 'high') is always added as a class
    This lets us style completed tasks and different priorities differently.
  -->
  <div class="task-item" :class="{ completed: task.is_completed, [task.priority]: true }">

    <!-- Checkbox to toggle completion -->
    <input
      type="checkbox"
      :checked="task.is_completed"
      @change="$emit('toggle', task.id)"
    />
    <!--
      :checked  → "bind" the checked state to our data (one-way: data → UI)
      @change   → "listen" for when the user clicks the checkbox
      $emit('toggle', task.id) → EMIT a custom event called 'toggle' UP to the parent

      WHY EMIT INSTEAD OF UPDATING DIRECTLY?
      This is the principle of "Props Down, Events Up":
        - Parent passes DATA to child via props (downward)
        - Child NOTIFIES parent via events (upward)
        - Parent decides what to do (call the API, update the store, etc.)

      The TaskItem component doesn't KNOW how to update the database.
      It just says "hey parent, the user toggled task #5" and lets the
      parent handle the logic. This makes TaskItem REUSABLE — it doesn't
      depend on any specific store or API.
    -->

    <div class="task-content">
      <h3>{{ task.title }}</h3>
      <!--
        {{ }} is called INTERPOLATION — it inserts a JavaScript value into HTML
        Whatever is inside the curly braces gets evaluated and displayed as text
      -->

      <p v-if="task.description">{{ task.description }}</p>
      <!--
        v-if is CONDITIONAL RENDERING
        This <p> tag ONLY appears if task.description exists (is not empty/null)
        If there's no description, this element isn't even in the HTML
      -->

      <div class="task-meta">
        <span class="priority-tag">{{ task.priority }}</span>

        <span v-if="task.due_date" class="due-date" :class="{ overdue: isOverdue }">
          📅 {{ formattedDate }}
        </span>
      </div>
    </div>

    <div class="task-actions">
      <button @click="$emit('edit', task)" title="Edit">✏️</button>
      <button @click="$emit('delete', task.id)" title="Delete">🗑️</button>
    </div>
  </div>
</template>

<script setup>
/**
 * <script setup> is Vue 3's "Composition API" syntax.
 * It's a simpler way to write component logic.
 * Everything declared here is automatically available in the template.
 */

import { computed } from 'vue'
// computed() creates a REACTIVE COMPUTED VALUE — it recalculates
// automatically whenever its dependencies change.
// Think of it like a spreadsheet formula: =A1+B1 recalculates
// whenever A1 or B1 changes.

// PROPS: Data passed from the parent component
// The parent will use: <TaskItem :task="someTaskObject" />
const props = defineProps({
  task: {
    type: Object,     // Must be an object (not a string, number, etc.)
    required: true    // Parent MUST provide this prop — it's not optional
  }
})

// EMITS: Declare which events this component can emit
// This is documentation + validation (Vue warns if you emit undeclared events)
defineEmits(['toggle', 'edit', 'delete'])

// Computed: formatted due date
const formattedDate = computed(() => {
  if (!props.task.due_date) return ''
  return new Date(props.task.due_date).toLocaleDateString()
  //   Converts "2026-04-15" to the user's local format (e.g., "4/15/2026")
})

// Computed: is the task overdue?
const isOverdue = computed(() => {
  if (!props.task.due_date || props.task.is_completed) return false
  return new Date(props.task.due_date) < new Date()
  //   Compare the due date to right now
  //   If due date is in the past AND the task isn't completed → overdue!
})
</script>

<style scoped>
/*
  "scoped" means these styles ONLY apply to THIS component.
  Without scoped, a .task-item class here could accidentally
  affect elements in OTHER components. Scoped styles are ISOLATED.
*/

.task-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: background-color 0.2s;
}

.task-item:hover {
  background-color: #f5f5f5;
}

/* When task is completed, fade it out and strike through the title */
.task-item.completed {
  opacity: 0.6;
  background-color: #f9f9f9;
}

.task-item.completed h3 {
  text-decoration: line-through;
  color: #999;
}

/* Priority colors on the left border */
.task-item.high { border-left: 4px solid #e74c3c; }
.task-item.medium { border-left: 4px solid #f39c12; }
.task-item.low { border-left: 4px solid #2ecc71; }

.task-content { flex: 1; }
.task-content h3 { margin: 0 0 4px 0; font-size: 1rem; }
.task-content p { margin: 0 0 4px 0; color: #666; font-size: 0.85rem; }

.task-meta { display: flex; gap: 8px; font-size: 0.75rem; }
.priority-tag { text-transform: uppercase; font-weight: bold; }
.due-date.overdue { color: #e74c3c; font-weight: bold; }

.task-actions button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 4px;
}
</style>