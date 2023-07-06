<script>
    import linkedinPlaceholder from '../../static/favicon.png';
    import githubPlaceholder from '../../static/favicon.png';
  
    let year = new Date().getFullYear();
  </script>

<style>
    footer {
  background-color: #2D2D2D;
  color: #edf2f7;
  padding: 1.5rem 0;
}

.container {
  margin-left: auto;
  margin-right: auto;
  max-width: 64rem;
  padding-left: 1rem;
  padding-right: 1rem;
}

.flex {
  display: flex;
  flex-direction: column;
}

@media (min-width: 768px) {
  .flex {
    flex-direction: row;
  }
}

.justify-center {
  justify-content: center;
}

.items-center {
  align-items: center;
}

.space-y-4 > :not(template) ~ :not(template) {
  margin-top: 1rem;
}

@media (min-width: 768px) {
  .space-y-4 > :not(template) ~ :not(template) {
    margin-top: 0;
  }
}

@media (min-width: 768px) {
  .md\:space-x-96 > :not(template) ~ :not(template) {
    margin-left: 24rem;
  }
}

.text-center {
  text-align: center;
}

@media (min-width: 768px) {
  .md\:text-left {
    text-align: left;
  }
}

.text-lg {
  font-size: 1.125rem;
}

.font-medium {
  font-weight: 500;
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.text-sm {
  font-size: 0.875rem;
}

.mt-4 {
  margin-top: 1rem;
}

@media (min-width: 768px) {
  .md\:mt-0 {
    margin-top: 0;
  }
}

.mx-2 {
  margin-left: 0.5rem;
  margin-right: 0.5rem;
}

.w-6 {
  width: 1.5rem;
}

.h-6 {
  height: 1.5rem;
}

  </style>
  
  
  <footer class="bg-gray-800 text-gray-200 py-6">
    <div class="container mx-auto">
      <div class="flex flex-col md:flex-row justify-center items-center space-y-4 md:space-y-0 md:space-x-96 lg:space-x-96">
        <div class="text-center md:text-left">
          <p class="text-lg font-medium mb-2">Maximilian Huber</p>
          <p class="text-sm">
            Copyright &copy; {year} - All rights reserved
          </p>
        </div>
        <div class="flex mt-4 md:mt-0">
          <a
            href="https://www.linkedin.com/in/your-linkedin-profile/"
            target="_blank"
            rel="noreferrer"
            class="mx-2"
          >
            <img
              src={linkedinPlaceholder}
              alt="LinkedIn"
              class="w-6 h-6"
            />
          </a>
          <a
            href="https://github.com/your-github-profile"
            target="_blank"
            rel="noreferrer"
            class="mx-2"
          >
            <img
              src={githubPlaceholder}
              alt="GitHub"
              class="w-6 h-6"
            />
          </a>
        </div>
      </div>
    </div>
  </footer>  