import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ProjectCard from '../components/ProjectCard';

interface ProjectData {
  repository_name: string;
  description: string;
  tags: string[];
}

interface SearchResult {
  repository_name: string;
  description: string;
  tags: string[];
  score: number;
}

const ProjectsPage: React.FC = () => {
  const [search, setSearch] = useState<string>('');
  const [projects, setProjects] = useState<ProjectData[]>([]);
  const [displayedProjects, setDisplayedProjects] = useState<ProjectData[]>([]);

  const fetchProjects = async () => {
    const response = await axios.get('http://localhost/repositories', {
      headers: { accept: 'application/json' },
    });
    setProjects(response.data);
    setDisplayedProjects(response.data);
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const performSearch = async (query: string) => {
    setSearch(query);
    if (query) {
      const response = await axios.post(`http://localhost/search`, {
        text: query,
      });
      const searchResults: SearchResult[] = response.data;
      console.log(searchResults);
      const sortedResults = searchResults.sort((a, b) => b.score - a.score);
      console.log(sortedResults);
      const sortedProjects: ProjectData[] = sortedResults.map((result) => ({
        repository_name: result.repository_name,
        description: result.description,
        tags: result.tags,
      }));
      console.log(sortedProjects);
      setDisplayedProjects(sortedProjects);
      setProjects(sortedProjects);
    } else {
      fetchProjects();
    }
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
        {displayedProjects.map((project, index) => (
          <ProjectCard key={index} {...project} />
        ))}
      </div>
    </div>
  );
};

export default ProjectsPage;
