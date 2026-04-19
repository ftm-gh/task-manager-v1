<template>
  <div class="dashboard">

    <!-- Progress summary -->
    <div class="stats">
      <div class="stat-card">
        <span class="stat-number">{{ taskStore.tasks.length }}</span>
        <span class="stat-label">Total Tasks</span>
      </div>
      <div class="stat-card">
        <span class="stat-number">{{ taskStore.completedTasks.length }}</span>
        <span class="stat-label">Completed</span>
      </div>
      <div class="stat-card">
        <span class="stat-number">{{ taskStore.completionRate }}%</span>
        <span class="stat-label">Progress</span>
      </div>
    </div>




    <!-- Banner shown only while editing -->
    <div v-if="taskBeingEdited" class="edit-banner">
      ✏️ Editing: <strong>{{ taskBeingEdited.title }}</strong>
    </div>

    <!--
      ONE TaskForm. The :key makes Vue REMOUNT it whenever we switch
      between "creating" (key='new') and "editing task X" (key=X).
      That's how `existingTask` is re-read fresh — solves issue #6.
    -->
    <TaskForm
      :key="taskBeingEdited?.id ?? 'new'"
      :existing-task="taskBeingEdited"
      :categories="categoryStore.categories"
      @submit="handleFormSubmit"
      @cancel="cancelEdit"
    />

    <!-- Filter bar -->
    <FilterBar
      :active-filter="activeFilters.completed || 'all'"
      :selected-category="activeFilters.category_id || ''"
      :categories="categoryStore.categories"
      @update:filter="onFilterChange"
      @update:category="onCategoryChange"
    />

    <!-- Loading and error states -->
    <div v-if="taskStore.loading" class="loading">Loading tasks...</div>
    <div v-else-if="taskStore.error" class="error">{{ taskStore.error }}</div>

    <!-- Task list -->
    <div v-else-if="taskStore.tasks.length === 0" class="empty-state">
      <p>🎉 No tasks yet! Add your first task above.</p>
    </div>

    <TaskList
      v-else
      :tasks="taskStore.tasks"
      @toggle="handleToggle"
      @edit="handleEdit"
      @delete="handleDelete"
    />
    <!--
      HERE'S THE COMPONENT CHAIN:
      DashboardView → TaskList → TaskItem

      Data flows DOWN through props:
        DashboardView passes :tasks to TaskList
        TaskList passes :task to each TaskItem

      Events flow UP through emits:
        TaskItem emits 'toggle' → TaskList re-emits 'toggle' → DashboardView handles it
    -->
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useTaskStore } from '@/stores/tasks'
import AppHeader from '@/components/AppHeader.vue'
import TaskForm from '@/components/TaskForm.vue'
import TaskList from '@/components/TaskList.vue'
import FilterBar from '@/components/FilterBar.vue'
import { useCategoryStore } from '@/stores/categories'

const categoryStore = useCategoryStore()

const taskStore = useTaskStore()

const activeFilters = reactive({})


// The task currently being edited (null = creating a new one)
const taskBeingEdited = ref(null)

// onMounted runs ONCE when the component first appears on screen
// This is called a LIFECYCLE HOOK — it lets you run code at specific
// moments in a component's life (created, mounted, updated, destroyed)
onMounted(() => {
  loadTasks()
  categoryStore.fetchCategories()

})

function loadTasks() {
  // Convert UI filters into backend query params
  const params = {}
  if (activeFilters.completed === 'active')    params.completed = 0
  if (activeFilters.completed === 'completed') params.completed = 1
  if (activeFilters.category_id) params.category_id = activeFilters.category_id
  taskStore.fetchTasks(params)}

// ── Filter handlers ──
function onFilterChange(value) {
  activeFilters.completed = value
  loadTasks()
}
function onCategoryChange(value) {
  activeFilters.category_id = value
  loadTasks()
}

// ── Form handler — works for both create AND update ──
async function handleFormSubmit(taskData) {
  try {
    if (taskBeingEdited.value) {
      // EDIT mode
      await taskStore.updateTask(taskBeingEdited.value.id, taskData)
      taskBeingEdited.value = null   // exit edit mode → form remounts as "new"
    } else {
      // CREATE mode
      await taskStore.addTask(taskData)
    }
  } catch (err) {
    alert('Failed to save task: ' + (err.response?.data?.error || err.message))
  }
}

// ── Edit / cancel ──
function handleEdit(task) {
  taskBeingEdited.value = { ...task }   // copy so the form can edit safely
  // Optional: scroll to top so the user sees the form
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
function cancelEdit() {
  taskBeingEdited.value = null
}

// ── Toggle / delete ──
async function handleToggle(taskId) {
  await taskStore.toggleTask(taskId)
}
async function handleDelete(taskId) {
  if (confirm('Are you sure you want to delete this task?')) {
    await taskStore.deleteTask(taskId)
    // If we were editing the deleted task, exit edit mode
    if (taskBeingEdited.value?.id === taskId) taskBeingEdited.value = null
  }
}
</script>

<style scoped>
.dashboard { max-width: 700px; margin: 0 auto; padding: 20px; }
.stats { display: flex; gap: 12px; margin-bottom: 20px; }
.stat-card {
  flex: 1; background: #fff; padding: 16px; border-radius: 12px;
  text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.stat-number {
  display: block; font-size: 1.8rem; font-weight: bold; color: #2c3e50;
}
.stat-label { font-size: 0.8rem; color: #999; text-transform: uppercase; }

.edit-banner {
  background: #fff7e6;
  border: 1px solid #ffd591;
  color: #ad6800;
  padding: 10px 14px;
  border-radius: 8px;
  margin-bottom: 12px;
  font-size: 0.9rem;
}

.loading, .error, .empty-state {
  text-align: center; padding: 40px; color: #999;
}
.error { color: #e74c3c; }
</style>
