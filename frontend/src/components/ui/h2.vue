<template>
  <h2 class="is-size-4 has-text-weight-bold middle">
    <slot />
  </h2>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class H2 extends Vue {}
</script>

<style scoped>
h2 {
  padding-bottom: 10px;
  margin-bottom: 10px;
  border-bottom: 2px solid lightgray;
}
</style>
