<script>
	import { page } from '$app/stores';
	let links = [
	  { to: '/', text: 'Home' },
	  { to: '/projects', text: 'Projects' },
	  { to: '/blog', text: 'Blog' },
	  { to: '/playground', text: 'Playground' },
	  { to: '/contact', text: 'Contact' },
	];
  </script>
  
  <header>
	<nav>
		<ul>
			{#each links as link (link.to)}
			  <li aria-current={$page.path === link.to ? 'page' : undefined}>
				<a href={link.to}>{link.text}</a>
			  </li>
			{/each}
		  </ul>
	</nav>
  </header>
  
  <style>
	:root {
    --dark-gray: #2D2D2D;
    --dark-orange: #F57C00;
    }

  	header {
    background-color: var(--dark-gray);
    color: white;
    padding: 1em;
  	}
  
	nav {
	  margin: 0 auto;
	  max-width: 60em;
	}
  
	ul {
	  list-style: none;
	  padding: 0;
	  display: flex;
	  justify-content: center;
	  gap: 2em;
	}
  
	a {
	  font-weight: 500;
	  font-size: 1.5em;
	  color: inherit;
	  text-decoration: none;
	}
  
	a:hover {
	  color: var(--dark-orange);
	  transition: color 0.2s;
	}
  </style>
  