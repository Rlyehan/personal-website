import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="bg-dark-gray text-dark-orange p-4">
      <nav>
        <Link to="/" className="mr-4">
          Home
        </Link>
        <Link to="/interactive-projects" className="mr-4">
          Interactive Projects (Python)
        </Link>
        <Link to="/dynamic-blog" className="mr-4">
          Dynamic Blog (Go)
        </Link>
        <Link to="/api-playground" className="mr-4">
          API Playground (Rust)
        </Link>
        <Link to="/about" className="mr-4">
          About
        </Link>
        <Link to="/contact" className="mr-4">
          Contact
        </Link>
      </nav>
    </header>
  );
}

export default Header;
