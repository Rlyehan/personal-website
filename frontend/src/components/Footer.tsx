import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-dark-gray text-dark-orange p-4">
      <p className="text-sm">
        &copy; {new Date().getFullYear()} Your Name. All rights reserved.
      </p>
    </footer>
  );
};

export default Footer;
