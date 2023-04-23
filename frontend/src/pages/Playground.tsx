import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';

const Playground: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow">
        {/* Add your projects content here */}
        <h2 className="text-xl font-bold">Interactive playground</h2>
      </main>
      <Footer />
    </div>
  );
};

export default Playground;
