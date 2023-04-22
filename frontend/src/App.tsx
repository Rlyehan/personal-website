import React from 'react';
import './App.css';
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App min-h-screen flex flex-col bg-dark-gray text-white">
      <Header />
      <main className="flex-grow p-4 md:p-8">
        <section id="about" className="md:flex md:items-center md:space-x-8">
          <img
            src="https://via.placeholder.com/150"
            alt="Your Profile"
            className="w-32 h-32 md:w-64 md:h-64 mx-auto md:mx-0 rounded-full mb-4 md:mb-0"
          />
          <div>
            <h2 className="text-dark-orange text-2xl md:text-4xl font-bold mb-4">
              About Me
            </h2>
            <p className="text-lg md:text-xl">
              I am a full-stack developer with experience in backend, data, ML,
              and DevOps-related topics as well as test automation. My portfolio
              showcases my expertise in various areas, including front-end
              development, back-end development, and machine learning.
            </p>
          </div>
        </section>

        <section id="projects" className="mt-16">
          <h2 className="text-dark-orange text-2xl md:text-4xl font-bold mb-8">
            Projects
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Add your project cards here */}
            <div className="bg-white text-dark-gray p-4 rounded-lg">
              <h3 className="text-xl font-bold mb-2">Project 1</h3>
              <p>
                A short description of the project goes here. Mention the
                technologies used and what the project does.
              </p>
            </div>
            <div className="bg-white text-dark-gray p-4 rounded-lg">
              <h3 className="text-xl font-bold mb-2">Project 2</h3>
              <p>
                A short description of the project goes here. Mention the
                technologies used and what the project does.
              </p>
            </div>
            <div className="bg-white text-dark-gray p-4 rounded-lg">
              <h3 className="text-xl font-bold mb-2">Project 3</h3>
              <p>
                A short description of the project goes here. Mention the
                technologies used and what the project does.
              </p>
            </div>
          </div>
        </section>

        <section id="contact" className="mt-16">
          <h2 className="text-dark-orange text-2xl md:text-4xl font-bold mb-4">
            Contact
          </h2>
          <p className="text-lg md:text-xl">
            If youre interested in working together or have any questions,
            please feel free to get in touch.
          </p>
          <p className="mt-4">
            Email:{' '}
            <a
              href="mailto:your.email@example.com"
              className="text-dark-orange hover:text-white"
            >
              your.email@example.com
            </a>
          </p>
        </section>
      </main>
      <Footer />
    </div>
  );
}

export default App;
