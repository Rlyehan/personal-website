import React from 'react';
import Hero from '../components/Hero';

const Home: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-grow">
        <Hero />
        <h2 className="text-xl font-bold">Welcome to my portfolio!</h2>
      </main>
    </div>
  );
};

export default Home;
