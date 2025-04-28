<template>
  <div class="form-group">
    <label :for="id">
      {{ label }}
    </label>
    <input
        :id="id"
        v-model="modelValue"
        :type="props.type"
        :placeholder="props.placeholder"
        :required="props.required"
        :autocomplete="props.autocomplete"
        :minlength="props.minlength"
        :maxlength="props.maxlength"
    />
  </div>
</template>

<script setup lang="ts">
import {computed} from "vue";

const props = defineProps({
  modelValue: {
    type: [String, Number],
    required: true
  },
  label: String,
  type: {
    type: String,
    default: "text"
  },
  placeholder: {
    type: String,
    default: "Text"
  },
  required: {
    type: Boolean,
    default: false
  },
  autocomplete: {
    type: String,
    default: "off"
  },
  minlength: {
    type: [String, Number],
    default: null
  },
  maxlength: {
    type: [String, Number],
    default: null
  }
});

const emits = defineEmits(["update:modelValue"]);

const modelValue = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emits("update:modelValue", value);
  }
});
const id = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`);
</script>

<style scoped>
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 500;
  color: #555;
}

.form-group input {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-group input:focus {
  border-color: #42b983;
  outline: none;
}
</style>
