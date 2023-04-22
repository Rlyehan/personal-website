import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';

const Home: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow">
        {/* Add your main content here */}
        <h2 className="text-xl font-bold">Welcome to my portfolio!</h2>
      </main>
      <Footer />
    </div>
  );
};

export default Home;
