<!--
  FilterBar — Lets users filter tasks by status and category.
  
  🔑 KEY CONCEPT: "Controlled" vs "Uncontrolled" Components
  
  This component does NOT manage its own filter state.
  Instead, the PARENT (TaskList) owns the state, and passes it
  down as props. When the user changes a filter, this component
  EMITS an event to tell the parent.
  
  This is called a "controlled component" — the parent controls it.
  
  Why? Because the parent needs the filter values to fetch/filter tasks.
  If FilterBar managed its own state, the parent wouldn't know
  what filters are active.
  
  Data flow:
  TaskList (parent) owns: activeFilter, selectedCategory
    ↓ passes as props ↓
  FilterBar (child) displays the current filter values
    ↑ emits events ↑
  User clicks a filter → FilterBar emits 'update:filter' → TaskList updates state
-->

<template>
  <div class="filter-bar">
    <!-- ── Status Filter Buttons ── -->
    <div class="filter-group">
      <span class="filter-label">Status:</span>
      <div class="filter-buttons">
        <!--
          We create a button for each filter option.
          v-for iterates over the filters array (defined in script).
        -->
        <button
          v-for="filter in statusFilters"
          :key="filter.value"
          @click="$emit('update:filter', filter.value)"
          :class="['filter-btn', { active: activeFilter === filter.value }]"
        >
          <!--
            🔑 $emit('update:filter', filter.value)

            $emit is how a child component sends a message to its parent.
            
            'update:filter' is the EVENT NAME.
            filter.value is the DATA sent with the event (e.g., 'all', 'active', 'completed').
            
            The parent listens with: @update:filter="handleFilterChange"
            
            The "update:" prefix is a Vue convention for two-way binding with v-model.
            It allows the parent to use: v-model:filter="activeFilter"
            
            
            🔑 :class with array syntax
            
            :class="['filter-btn', { active: activeFilter === filter.value }]"
            
            This combines:
            1. A static class: 'filter-btn' (always applied)
            2. A conditional class: 'active' (only if this is the selected filter)
            
            Array syntax lets you mix strings and objects in one :class binding.
          -->
          {{ filter.icon }} {{ filter.label }}
        </button>
      </div>
    </div>

    <!-- ── Category Filter Dropdown ── -->
    <div class="filter-group" v-if="categories.length > 0">
      <!--
        Only show the category filter if there ARE categories.
        No point showing an empty dropdown.
      -->
      <span class="filter-label">Category:</span>
      <select
        :value="selectedCategory"
        @change="$emit('update:category', $event.target.value)"
        class="category-select"
      >
        <!--
          🔑 HTML <select> Element
          
          <select> creates a dropdown menu.
          Each <option> is one choice in the dropdown.
          
          :value binds the currently selected value (controlled by parent).
          @change fires when the user picks a different option.
          
          $event.target.value is:
          $event → the native DOM event object
          .target → the HTML element that fired the event (the <select>)
          .value → the value of the selected <option>
        -->
        <option value="">All Categories</option>
        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup>
/*
  🔑 defineProps:
  Declares what data this component expects from its parent.
  
  Think of props like function parameters:
  A function says "I need a number and a string."
  A component says "I need activeFilter, selectedCategory, and categories."
*/

defineProps({
  activeFilter: {
    type: String,
    default: 'all'
    /*
      Expected values: 'all', 'active', 'completed'
      default: 'all' means if the parent doesn't pass this prop, use 'all'.
    */
  },
  selectedCategory: {
    type: [String, Number],
    default: ''
    /*
      type: [String, Number] — this prop can be EITHER a string or number.
      It's a string when empty (''), or a number when a category is selected (1, 2, 3).
      
      Vue validates the type and warns you in the console if it's wrong.
    */
  },
  categories: {
    type: Array,
    default: () => []
    /*
      For arrays and objects, the default must be a FUNCTION that returns the value.
      
      Why? If you wrote default: [], ALL component instances would share
      the SAME array in memory. Changing one would change all.
      
      Using a function () => [] creates a FRESH array for each instance.
      
      This is similar to why Python uses None as default for mutable parameters.
    */
  }
})

defineEmits(['update:filter', 'update:category'])
/*
  Declares what events this component can emit.
  Serves as documentation and enables Vue's type checking.
*/

// The filter options — a simple data array
const statusFilters = [
  { value: 'all', label: 'All', icon: '📋' },
  { value: 'active', label: 'Active', icon: '⏳' },
  { value: 'completed', label: 'Done', icon: '✅' }
]
/*
  This is a plain JavaScript array (not reactive with ref).
  Why? Because it NEVER changes — it's static data.
  There's no need for reactivity on data that doesn't change.
  Using ref() unnecessarily would waste a tiny bit of memory.
*/
</script>

<style scoped>
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  /*
    flex-wrap: wrap means items can wrap to the next line
    if there's not enough horizontal space.
    Without this, items would overflow off-screen on small screens.
  */
  
  gap: 20px;
  align-items: center;
  padding: 16px 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  /*
    text-transform: uppercase converts all text to UPPERCASE.
    "Status" becomes "STATUS"
    This is a design pattern for labels — makes them look like section headers.
  */
  
  letter-spacing: 0.5px;
}

.filter-buttons {
  display: flex;
  gap: 6px;
}

.filter-btn {
  padding: 6px 14px;
  border: 1px solid #ddd;
  border-radius: 20px;
  /*
    border-radius: 20px with a short element creates a "pill" shape.
    The corners are so rounded they form semicircles.
  */
  
  background-color: white;
  color: #555;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: #3498db;
  color: #3498db;
}

.filter-btn.active {
  background-color: #3498db;
  color: white;
  border-color: #3498db;
}

.category-select {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: white;
  font-size: 0.9rem;
  color: #555;
  cursor: pointer;
  min-width: 150px;
  /*
    min-width ensures the dropdown is at least 150px wide,
    even if all category names are short.
    This prevents the dropdown from looking too small.
  */
}

.category-select:focus {
  outline: none;
  border-color: #3498db;
}
</style>