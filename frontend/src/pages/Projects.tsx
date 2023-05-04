import React, { useState } from 'react';
import ProjectCard from '../components/ProjectCard';

const projectsData = [
  {
    id: 1,
    title: 'Project 1',
    description: 'This is a short description for Project 1',
    imageUrl: 'https://via.placeholder.com/300',
    githubUrl: 'https://github.com/username/project1',
  },
];

const Projects: React.FC = () => {
  const [search, setSearch] = useState('');

  //TODO: Implement search functionality
  const performSearch = (query: string) => {
    setSearch(query);
  };

  return (
    <div className="container mx-auto p-4">
      <input
        type="text"
        className="w-full p-2 mb-4 bg-gray-800 text-white rounded"
        placeholder="Search projects..."
        value={search}
        onChange={(e) => performSearch(e.target.value)}
      />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {projectsData.map((project) => (
          <ProjectCard key={project.id} {...project} />
        ))}
      </div>
    </div>
  );
};

export default Projects;
