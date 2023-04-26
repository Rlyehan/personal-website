import React from 'react';

const AboutMe: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8 w-3/4">
      <div className="flex items-center justify-center">
        <img
          className="rounded-full w-32 h-32 mr-8"
          src="https://via.placeholder.com/150"
          alt="Profile"
        />
        <div className="flex flex-col items-center">
          <p className="text-white text-lg mb-4">
            Hi, I&apos;m Max! I&apos;m a full-stack developer with experience in
            Python, JavaScript, Go, and Rust. I love learning new technologies
            and building creative solutions for complex problems.
          </p>
          <div className="flex justify-center space-x-8">
            <a
              href="https://www.linkedin.com/in/your-linkedin-profile/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dark-orange hover:text-dark-orange-light transition-colors duration-200"
            >
              [LinkedIn]
            </a>
            <a
              href="https://github.com/your-github-profile"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dark-orange hover:text-dark-orange-light transition-colors duration-200"
            >
              [GitHub]
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutMe;
