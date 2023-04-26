import React, { useState } from 'react';
import SkillProgressBar from './SkillProgressBar';

const skillData = {
  languages: [
    { skill: 'Python', percentage: 80 },
    { skill: 'JavaScript', percentage: 75 },
    { skill: 'Go', percentage: 60 },
    { skill: 'Rust', percentage: 50 },
  ],
  roles: [
    { skill: 'Backend Developer', percentage: 80 },
    { skill: 'Frontend Developer', percentage: 70 },
    { skill: 'DevOps Engineer', percentage: 60 },
    { skill: 'Data Engineer', percentage: 50 },
  ],
};

const SkillProgressTabs: React.FC = () => {
  const [activeTab, setActiveTab] = useState('languages');

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
      <div className="flex justify-center mb-8">
        <button
          className={`px-4 py-2 font-semibold text-sm ${
            activeTab === 'languages'
              ? 'bg-darkGray text-darkOrange'
              : 'text-gray-300 hover:text-darkOrange hover:bg-gray-800'
          }`}
          onClick={() => setActiveTab('languages')}
        >
          Languages
        </button>
        <button
          className={`px-4 py-2 font-semibold text-sm ${
            activeTab === 'roles'
              ? 'bg-darkGray text-darkOrange'
              : 'text-gray-300 hover:text-darkOrange hover:bg-gray-800'
          }`}
          onClick={() => setActiveTab('roles')}
        >
          Roles
        </button>
      </div>
      {renderSkillProgress(skillData[activeTab as keyof typeof skillData])}
    </div>
  );
};

export default SkillProgressTabs;
