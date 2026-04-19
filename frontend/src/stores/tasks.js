/**
 * stores/tasks.js — Tasks Store
 *
 * Manages the list of tasks: fetching, adding, updating, deleting.
 */

import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useTaskStore = defineStore('tasks', {
  state: () => ({
    tasks: [],        // Array of task objects
    loading: false,
    error: null
  }),

  getters: {
    // GETTERS are like "live filters" — they recalculate automatically
    completedTasks: (state) => state.tasks.filter(t => t.is_completed),
    //   .filter() creates a NEW array with only the items that pass the test
    //   t => t.is_completed means "keep tasks where is_completed is truthy"

    pendingTasks: (state) => state.tasks.filter(t => !t.is_completed),
    //   ! means NOT — keep tasks that are NOT completed

    completionRate: (state) => {
      if (state.tasks.length === 0) return 0
      return Math.round(
        (state.tasks.filter(t => t.is_completed).length / state.tasks.length) * 100
      )
      // Example: 3 completed out of 10 tasks → (3/10) * 100 = 30%
    },

    // This getter is a FUNCTION — it takes a parameter
    tasksByPriority: (state) => {
      return (priority) => state.tasks.filter(t => t.priority === priority)
    }
    // Usage in a component: taskStore.tasksByPriority('high')
  },

  actions: {
    async fetchTasks(filters = {}) {
      this.loading = true
      this.error = null
      try {
        // Convert the filters object to URL parameters
        // {completed: 1, priority: 'high'} → "completed=1&priority=high"
        const params = new URLSearchParams(filters).toString()
        const response = await api.get(`/tasks?${params}`)

        this.tasks = response.data
        //   Replace the entire tasks array with fresh data from the server
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to load tasks'
      } finally {
        this.loading = false
      }
    },

    async addTask(taskData) {
      // taskData = { title: "Buy milk", priority: "high" }
      const response = await api.post('/tasks', taskData)
      this.tasks.unshift(response.data)
      //   .unshift() adds an item to the BEGINNING of an array
      //   (so the new task appears at the top of the list)
    },

    async toggleTask(taskId) {
      // Find the task in our local array
      const task = this.tasks.find(t => t.id === taskId)
      //   .find() returns the FIRST item that matches

      if (!task) return

      // Send the opposite value to the server
      const response = await api.put(`/tasks/${taskId}`, {
        is_completed: !task.is_completed
        //   ! flips the value: true → false, false → true
      })

      // Update the local copy with the server's response
      Object.assign(task, response.data)
      //   Object.assign() copies properties from one object to another
      //   This updates the task IN PLACE (Vue detects this and re-renders)
    },

    async updateTask(taskId, updates) {
      const response = await api.put(`/tasks/${taskId}`, updates)
      const idx = this.tasks.findIndex(t => t.id === taskId)
      if (idx !== -1) Object.assign(this.tasks[idx], response.data)
    },

    async deleteTask(taskId) {
      await api.delete(`/tasks/${taskId}`)
      this.tasks = this.tasks.filter(t => t.id !== taskId)
      //   Keep all tasks EXCEPT the one we deleted
    }
  }
})
