import React from 'react';
import Hero from '../components/Hero';
import SkillTabs from '../components/skills/SkillPRogressTabs';

const Home: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-grow">
        <Hero />
        <SkillTabs />
      </main>
    </div>
  );
};

export default Home;
