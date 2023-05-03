import React, { useState } from 'react';
import SkillProgressBar from './SkillProgressBar';

const skillData = {
  dataEngineer: [
    { skill: 'Placholder1', percentage: 80 },
    { skill: 'Placholder2', percentage: 75 },
    { skill: 'Placholder3', percentage: 60 },
    { skill: 'Placholder4', percentage: 50 },
  ],
  devopsEngineer: [
    { skill: 'Placholder5', percentage: 80 },
    { skill: 'Placholder6', percentage: 70 },
    { skill: 'Placholder7', percentage: 60 },
    { skill: 'Placholder8', percentage: 50 },
  ],
  backendDeveloper: [
    { skill: 'Python', percentage: 80 },
    { skill: 'Typrscript', percentage: 70 },
    { skill: 'Go', percentage: 60 },
    { skill: 'SQL Databases', percentage: 50 },
    { skill: 'NoSQL Databases', percentage: 40 },
    { skill: 'Rust', percentage: 30 },
  ],
};

const SkillProgressTabs: React.FC = () => {
  const [activeTab, setActiveTab] = useState('dataEngineer');

  const renderSkillProgress = (
    skills: Array<{ skill: string; percentage: number }>,
  ) => {
    return skills.map((skill, index) => (
      <SkillProgressBar
        key={skill.skill}
        skill={skill.skill}
        percentage={skill.percentage}
        isFirst={index === 0}
      />
    ));
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-center mb-8 py-8">
        <button
          className={`px-4 py-2 font-semibold text-sm ${
            activeTab === 'dataEngineer'
              ? 'bg-darkGray text-darkOrange'
              : 'text-gray-300 hover:text-darkOrange hover:bg-gray-800'
          }`}
          onClick={() => setActiveTab('dataEngineer')}
        >
          Data Engineer
        </button>
        <button
          className={`px-4 py-2 font-semibold text-sm ${
            activeTab === 'backendDeveloper'
              ? 'bg-darkGray text-darkOrange'
              : 'text-gray-300 hover:text-darkOrange hover:bg-gray-800'
          }`}
          onClick={() => setActiveTab('backendDeveloper')}
        >
          Backend Developer
        </button>
        <button
          className={`px-4 py-2 font-semibold text-sm ${
            activeTab === 'devopsEngineer'
              ? 'bg-darkGray text-darkOrange'
              : 'text-gray-300 hover:text-darkOrange hover:bg-gray-800'
          }`}
          onClick={() => setActiveTab('devopsEngineer')}
        >
          DevOps Engineer
        </button>
      </div>
      {renderSkillProgress(skillData[activeTab as keyof typeof skillData])}
    </div>
  );
};

export default SkillProgressTabs;
