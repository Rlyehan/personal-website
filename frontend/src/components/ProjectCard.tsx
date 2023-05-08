import React from 'react';

interface ProjectCardProps {
  repository_name: string;
  description: string;
}

const ProjectCard: React.FC<ProjectCardProps> = ({
  repository_name,
  description,
}) => {
  return (
    <div className="bg-gray-800 rounded-lg p-4 cursor-pointer transition-colors duration-200 hover:bg-gray-700">
      <h2 className="text-2xl text-dark-orange font-semibold mb-2">
        {repository_name}
      </h2>
      <p className="text-gray-200 text-sm mb-4">{description}</p>
    </div>
  );
};

export default ProjectCard;
