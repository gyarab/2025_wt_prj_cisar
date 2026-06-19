<script setup>
import { on } from 'node:cluster';
import { onMounted, ref } from 'vue';

const players = ref([]);

async function load () {

    const response = await fetch('/api/players', window.location.origin);
   players.value = await response.json();
   if (!response.ok) throw new Error(`HTTP returned ${response.status}`);
   const data = await response.json();

   players.value = data;
}

onMounted(load);
</script>

<template>
    <h2>Players</h2>
</template>