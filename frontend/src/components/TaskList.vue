<!--
  TaskList (component version) — Renders a list of TaskItem components.
  
  🔑 IMPORTANT: Don't confuse this with views/TaskList.vue (the PAGE).
  
  This is the COMPONENT version that lives in /components/.
  It's a reusable piece that just renders a list of tasks.
  
  The PAGE (views/TaskList.vue) is the full page that includes:
  - The "Add Task" form
  - The FilterBar
  - THIS TaskList component
  - Loading/error states
  
  Why separate them?
  - The VIEW handles page-level concerns (fetching data, routing)
  - The COMPONENT handles display concerns (rendering the list)
  
  This separation makes both easier to maintain and test.
  
  NOTE: If your project only uses ONE task list, you could combine them.
  This separation is shown here to teach the component vs view distinction.
-->

<template>
  <div class="task-list-wrapper">
    <!-- Empty state -->
    <div v-if="tasks.length === 0" class="empty-state">
      <div class="empty-icon">{{ emptyIcon }}</div>
      <p class="empty-text">{{ emptyMessage }}</p>
      <!--
        We use props for the empty state content so the parent
        can customize the message based on context:
        - No tasks at all → "Add your first task!"
        - No matching filter → "No completed tasks yet."
      -->
    </div>

    <!-- Task items -->
    <transition-group name="task-list" tag="div" class="task-items" v-else>
      <!--
        🔑 <transition-group> — Animated List
        
        <transition> (seen earlier) animates ONE element entering/leaving.
        <transition-group> animates MULTIPLE elements in a LIST.
        
        When a task is added → it smoothly slides/fades in
        When a task is removed → it smoothly slides/fades out
        When tasks reorder → they smoothly move to new positions
        
        name="task-list" → CSS classes will be prefixed with "task-list-"
        tag="div" → render the wrapper as a <div> (default is <span>)
        
        Each child MUST have a unique :key (which TaskItem gets via v-for).
      -->
      <slot
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        name="task"
      >
        <!--
          🔑 KEY CONCEPT: Slots
          
          A slot is a PLACEHOLDER that the parent can fill with custom content.
          
          Default behavior (if parent doesn't provide content):
          Show a simple <div> with the task title.
          
          But the parent CAN provide a custom template:
          <TaskList :tasks="tasks">
            <template #task="{ task }">
              <MyCustomTaskItem :task="task" />
            </template>
          </TaskList>
          
          This makes TaskList flexible — different pages could render tasks
          differently using the same list component.
          
          For our project, the parent (views/TaskList.vue) will use the
          default rendering, but this demonstrates the slot pattern.
        -->
        <div class="default-task-item">
          <span>{{ task.title }}</span>
        </div>
      </slot>
    </transition-group>
  </div>
</template>

<script setup>
defineProps({
  tasks: {
    type: Array,
    required: true
    // The array of task objects to display
  },
  emptyMessage: {
    type: String,
    default: 'No tasks to show.'
  },
  emptyIcon: {
    type: String,
    default: '📭'
  }
})
</script>

<style scoped>
.task-list-wrapper {
  width: 100%;
}

.empty-state {
  text-align: center;
  padding: 50px 20px;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 12px;
}

.empty-text {
  color: #999;
  font-size: 1.05rem;
}

.task-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* ── Transition animations ── */
.task-list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.task-list-enter-active {
  transition: all 0.3s ease;
  /*
    "ease" is a timing function:
    The animation starts slow, speeds up in the middle, and slows down at the end.
    Other options: linear (constant speed), ease-in (slow start), ease-out (slow end).
  */
}

.task-list-leave-active {
  transition: all 0.3s ease;
}

.task-list-leave-to {
  opacity: 0;
  transform: translateX(30px);
  /* Tasks slide to the right and fade out when removed */
}

.task-list-move {
  transition: transform 0.3s ease;
  /*
    .task-list-move animates items that CHANGE POSITION.
    When a task is deleted, the tasks below smoothly slide up to fill the gap.
  */
}

.default-task-item {
  padding: 14px 18px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}
</style>