<script>
    import CustomTypewriter from './CustomTypewriter.svelte';
    let strings = [
      { text: 'Full Stack Developer' },
      { text: 'Data Engineer' },
      { text: 'DevOps Enthusiast' }
    ];
  </script>
  
  <style>
    .hero {
      background-color: #2D2D2D;
      height: auto;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      padding: 5rem 1rem;
      margin-bottom: 8rem;
    }
  
    .hero h1 {
      font-size: 1.875rem;
      font-weight: bold;
      margin-bottom: 1rem;
      color: #DD6B20;
    }
  
    .hero h2 {
      font-size: 1.125rem;
      color: white;
    }
  
    /* Adjust font sizes for larger screens */
    @media (min-width: 768px) {
      .hero h1 {
        font-size: 2.25rem;
      }
  
      .hero h2 {
        font-size: 1.25rem;
      }
    }
  
    @media (min-width: 1024px) {
      .hero h1 {
        font-size: 3rem;
      }
  
      .hero h2 {
        font-size: 1.5rem;
      }
    }
  
    @media (min-width: 1280px) {
      .hero h1 {
        font-size: 4rem;
      }
  
      .hero h2 {
        font-size: 1.875rem;
      }
    }
  </style>
  
  <div class="hero">
    <h1>Maximilian Huber</h1>
    <h2>
      <CustomTypewriter {strings} />
    </h2>
  </div>
  