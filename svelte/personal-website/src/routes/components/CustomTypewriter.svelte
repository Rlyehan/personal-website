<script lang="ts">
    import { onMount, onDestroy, afterUpdate } from 'svelte';
    import { writable } from 'svelte/store';
    import { fade } from 'svelte/transition';
    import { circOut } from 'svelte/easing';
    import { crossfade } from 'svelte/transition';

    const [send, receive] = crossfade({
    duration: 1000,
    fallback(node, params) {
      return fade(node, { ...params, duration: 500 });
    },

  });
  
    export let strings: { text: string; color?: string }[] = [];
    export let delay: number = 75;
  
    let currentStringIndex = writable(0);
    let currentCharIndex = writable(0);
    let isDeleting = writable(false);
    let timer: number;
    let completed = false;
  
    $: currentString = strings[$currentStringIndex]?.text.substr(0, $currentCharIndex);
    $: color = strings[$currentStringIndex]?.color;
  
    onMount(() => {
      timer = window.setInterval(() => {
        if ($isDeleting) {
          currentCharIndex.update(n => n - 1);
          if ($currentCharIndex === 0) {
            isDeleting.set(false);
            currentStringIndex.update(n => (n + 1) % strings.length);
          }
        } else {
          currentCharIndex.update(n => n + 1);
          if ($currentCharIndex === strings[$currentStringIndex]?.text.length) {
            isDeleting.set(true);
            if ($currentStringIndex === strings.length - 1) {
              completed = true;
              clearInterval(timer);
            }
          }
        }
      }, $isDeleting ? delay / 2 : delay);
    });
  
    onDestroy(() => {
      clearInterval(timer);
    });
  </script>
  
  <style>
    .whitespace-nowrap {
      white-space: nowrap;
    }
  
    /* replace darkOrange with the actual color value */
    .text-darkOrange {
      color: #DD6B20;
    }
  
    /* replace animate-blink with the actual animation */
    .animate-blink {
      animation: blink 1s infinite;
    }
  
    /* Add your custom styles for the completed state */
    .completed {
      font-size: 1.5rem;
    }
  
    @keyframes blink {
      0%, 49% {
        opacity: 1;
      }
      50%, 100% {
        opacity: 0;
      }
    }
  </style>
  
  {#if !completed}
  <span class="whitespace-nowrap" out:send={{ key: currentString, duration: 1000, easing: circOut }}>
    <span class={color ? `text-${color}` : ''}>
      {currentString}
    </span>
    <span class="text-darkOrange animate-blink">|</span>
  </span>
{:else}
  <span class="whitespace-nowrap completed" in:receive={{ key: currentString, duration: 1000, easing: circOut }}>
    {#each strings as string, index (string.text)}
      <span class={string.color ? `text-${string.color}` : ''}>
        {string.text}{index < strings.length - 1 ? ' | ' : ''}
      </span>
    {/each}
  </span>
{/if}
  