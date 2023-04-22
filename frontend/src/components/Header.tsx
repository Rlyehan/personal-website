import React from 'react';

const Header = () => {
  return (
    <header className="bg-dark-gray text-dark-orange p-4">
      <h1 className="text-xl font-bold">Your Name</h1>
      <nav>
        <a className="mx-2 hover:text-white" href="#about">
          About
        </a>
        <a className="mx-2 hover:text-white" href="#projects">
          Projects
        </a>
        <a className="mx-2 hover:text-white" href="#contact">
          Contact
        </a>
      </nav>
    </header>
  );
};

export default Header;
