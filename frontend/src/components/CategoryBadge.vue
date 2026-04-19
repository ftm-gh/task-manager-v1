<!--
  CategoryBadge — A small colored label showing a task's category.
  
  Example output: [🔴 Work] or [🔵 Personal]
  
  This is a very SMALL component — just a colored pill with text.
  
  🔑 WHY make such a small thing a component?
  
  1. REUSABILITY: Used in TaskItem, and could be used in other places too.
  2. ENCAPSULATION: The styling logic (how to show a color badge) is in one place.
  3. SINGLE RESPONSIBILITY: This component does ONE thing and does it well.
  
  Even tiny components are worth creating if they encapsulate a piece of UI
  that could be reused or that has its own styling concerns.
-->

<template>
  <span
    class="category-badge"
    :style="{ backgroundColor: color, color: textColor }">
    <!--
      🔑  :style for inline dynamic styles

      :style="{ backgroundColor: color }" sets the CSS background-color
      dynamically based on the "color" prop.
      
      Notice: CSS properties with hyphens (background-color) become
      camelCase in JavaScript (backgroundColor).
      
      Why inline style here instead of CSS class?
      Because the color is DIFFERENT for each category — it comes from the database.
      You can't predict all possible colors in advance with CSS classes.
      Inline styles are appropriate when the value is truly dynamic.
    -->
    {{ name }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    required: true
    // The category name, e.g., "Work"
  },
  color: {
    type: String,
    default: '#3498db'
    // The hex background color, e.g., "#e74c3c"
  }
})

/*
  Compute whether text should be white or dark based on the background color.
  
  🔑 This is an ACCESSIBILITY consideration.
  White text on a light background is unreadable.
  Dark text on a dark background is also unreadable.
  We need to pick the right text color based on the background brightness.
*/
const textColor = computed(() => {
  // Convert hex color to RGB and calculate brightness
  const hex = props.color.replace('#', '')
  
  const r = parseInt(hex.substring(0, 2), 16)
  const g = parseInt(hex.substring(2, 4), 16)
  const b = parseInt(hex.substring(4, 6), 16)
  /*
    parseInt(string, 16) converts a hexadecimal string to a decimal number.
    
    For "#e74c3c":
    hex = "e74c3c"
    r = parseInt("e7", 16) = 231
    g = parseInt("4c", 16) = 76
    b = parseInt("3c", 16) = 60
  */
  
  // Calculate perceived brightness (human eyes are more sensitive to green)
  const brightness = (r * 299 + g * 587 + b * 114) / 1000
  /*
    This is a standard formula for "perceived luminance."
    Humans see green most brightly, red next, blue least.
    That's why the weights are: green (587) > red (299) > blue (114).
    
    Result ranges from 0 (black) to 255 (white).
  */
  
  return brightness > 150 ? '#333333' : '#ffffff'
  // If the background is bright → use dark text
  // If the background is dark → use white text
})
</script>

<style scoped>
.category-badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.3px;
  white-space: nowrap;
  /* Prevent the category name from wrapping to a second line */
}
</style>