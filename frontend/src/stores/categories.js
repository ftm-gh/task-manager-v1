import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useCategoryStore = defineStore('categories', {
  state: () => ({
    categories: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchCategories() {
      this.loading = true
      this.error = null
      try {
        const res = await api.get('/categories')
        // backend returns { categories: [...] }
        this.categories = res.data.categories ?? res.data ?? []
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to load categories'
        this.categories = []
      } finally {
        this.loading = false
      }
    },
    async addCategory(name, color = '#3498db') {
      const res = await api.post('/categories', { name, color })
      const created = res.data.category ?? res.data
      this.categories.push(created)
      return created
    },
  },
})
