import React from 'react';

interface ProjectCardProps {
  id: number;
  title: string;
  description: string;
  githubUrl: string;
}

const ProjectCard: React.FC<ProjectCardProps> = ({
  id,
  title,
  description,
  githubUrl,
}) => {
  return (
    <div
      className="bg-gray-800 rounded-lg p-4 cursor-pointer transition-colors duration-200 hover:bg-gray-700"
      onClick={() => window.open(githubUrl, '_blank')}
    >
      <h2 className="text-2xl text-dark-orange font-semibold mb-2">{title}</h2>
      <p className="text-gray-200 text-sm mb-4">{description}</p>
    </div>
  );
};

export default ProjectCard;
