import React from 'react';
import Hero from '../components/Hero';
import SkillTabs from '../components/skills/SkillPRogressTabs';
import AboutMe from '../components/AboutMe';

const Home: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-grow">
        <Hero />
        <AboutMe />
        <SkillTabs />
      </main>
    </div>
  );
};

export default Home;
