import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-gray-200 py-6">
      <div className="container mx-auto">
        <div className="flex flex-col md:flex-row justify-center items-center space-y-4 md:space-y-0 md:space-x-96 lg:space-x-96">
          <div className="text-center md:text-left">
            <p className="text-lg font-medium mb-2">Maximilian Huber</p>
            <p className="text-sm">
              Copyright &copy; {new Date().getFullYear()} - All rights reserved
            </p>
          </div>
          <div className="flex mt-4 md:mt-0">
            <a
              href="https://www.linkedin.com/in/your-linkedin-profile/"
              target="_blank"
              rel="noreferrer"
              className="mx-2"
            >
              <img
                src="/path/to/linkedin-placeholder.png"
                alt="LinkedIn"
                className="w-6 h-6"
              />
            </a>
            <a
              href="https://github.com/your-github-profile"
              target="_blank"
              rel="noreferrer"
              className="mx-2"
            >
              <img
                src="/path/to/github-placeholder.png"
                alt="GitHub"
                className="w-6 h-6"
              />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
