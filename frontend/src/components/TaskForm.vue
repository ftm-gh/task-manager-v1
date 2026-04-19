<template>
  <form @submit.prevent="handleSubmit" class="task-form">
    <!--
      @submit.prevent = listen for form submission AND prevent the default behavior
      By default, forms RELOAD THE PAGE when submitted (old-school HTML behavior)
      .prevent stops that — we handle it in JavaScript instead
    -->

    <div class="form-group">
      <label for="title">Title *</label>
      <input
        id="title"
        v-model="form.title"
        type="text"
        placeholder="What needs to be done?"
        required
      />
      <!--
        v-model is TWO-WAY BINDING:
          - When the user types, form.title is automatically updated
          - If form.title changes in code, the input field updates too
        It's "synced" in both directions.

        Without v-model, you'd need:
          :value="form.title"                    (data → input)
          @input="form.title = $event.target.value"  (input → data)
        v-model combines both into one!
      -->
    </div>

    <div class="form-group">
      <label for="description">Description</label>
      <textarea
        id="description"
        v-model="form.description"
        placeholder="Add details (optional)"
        rows="3"
      ></textarea>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="priority">Priority</label>
        <select id="priority" v-model="form.priority">
          <option value="low">🟢 Low</option>
          <option value="medium">🟡 Medium</option>
          <option value="high">🔴 High</option>
        </select>
      </div>

      <div class="form-group">
        <label for="due_date">Due Date</label>
        <input id="due_date" v-model="form.due_date" type="date" />
      </div>
    </div>

    <div class="form-group" v-if="categories.length > 0">
      <label for="category_id">Category</label>
      <select id="category_id" v-model="form.category_id">
        <option :value="null">— No category —</option>
        <option
          v-for="cat in categories"
          :key="cat.id"
          :value="cat.id"
        >
          {{ cat.name }}
        </option>
      </select>
    </div>

    <div class="form-actions">
      <button type="submit" :disabled="!form.title.trim()">
        {{ isEditing ? 'Update Task' : 'Add Task' }}
      </button>

      <!-- Cancel only appears in edit mode -->
      <button
        v-if="isEditing"
        type="button"
        class="btn-cancel"
        @click="$emit('cancel')"
      >
        Cancel
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, computed } from 'vue'

// PROPS: The parent can optionally pass an existing task (for editing)
const props = defineProps({
  existingTask: {
    type: Object,
    default: null    // null = creating a new task, object = editing existing
  },
  categories: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['submit', 'cancel'])

// reactive() is like ref() but for OBJECTS
// It makes every property of the object reactive
// Because the parent will use :key to force a remount when switching
// between "new" and "editing task X", we can safely initialize from
// props.existingTask once. No watch() needed.
const form = reactive({
  title: props.existingTask?.title || '',
  description: props.existingTask?.description || '',
  priority: props.existingTask?.priority || 'medium',
  due_date: props.existingTask?.due_date || '',
  category_id: props.existingTask?.category_id ?? null,
})

const isEditing = computed(() => props.existingTask !== null)

function handleSubmit() {
  // Don't submit if title is empty (extra safety beyond the 'required' attribute)
  if (!form.title.trim()) return

  // Emit the form data up to the parent
  // The parent will call the appropriate store action (addTask or updateTask)
  emit('submit', {
    title: form.title.trim(),
    description: form.description.trim() || null,
    priority: form.priority,
    due_date: form.due_date || null,
    category_id: form.category_id || null,
  })


  // Clear the form if we're creating (not editing)
  if (!isEditing.value) {
    form.title = ''
    form.description = ''
    form.priority = 'medium'
    form.due_date = ''
    form.category_id = null
  }
}
</script>

<style scoped>
.task-form {
  background: #fff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 12px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: 600;
  font-size: 0.85rem;
  color: #555;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
}

.form-row {
  display: flex;
  gap: 12px;
}

.form-row .form-group { flex: 1; }

.form-actions {
  display: flex;
  gap: 10px;
}

button[type="submit"] {
  width: 100%;
  padding: 10px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
}

button[type="submit"]:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.btn-cancel {
  flex: 0 0 auto;
  padding: 10px 16px;
  background: #ecf0f1;
  color: #555;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
}
.btn-cancel:hover { background: #e0e6e8; }
</style>
