import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="bg-gray-800 text-gray-200 py-4">
      <nav className="container mx-auto">
        <ul className="flex justify-center space-x-8">
          {[
            { to: '/', text: 'Home' },
            { to: '/projects', text: 'Projects' },
            { to: '/blog', text: 'Blog' },
            { to: '/playground', text: 'Playground' },
            { to: '/contact', text: 'Contact' },
          ].map(({ to, text }) => (
            <li key={to}>
              <Link
                to={to}
                className="font-medium text-lg hover:text-dark-orange transition-colors duration-200"
              >
                {text}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}

export default Header;
