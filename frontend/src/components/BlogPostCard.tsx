import React from 'react';

export interface BlogPostData {
  id: number;
  title: string;
  excerpt: string;
  content: string;
  date: string;
}

interface BlogPostCardProps extends BlogPostData {
  onClick: () => void;
}

const BlogPostCard: React.FC<BlogPostCardProps> = ({
  title,
  excerpt,
  date,
  onClick,
}) => {
  return (
    <div
      className="bg-gray-800 rounded-lg p-4 cursor-pointer transition-colors duration-200 hover:bg-gray-700"
      onClick={onClick}
    >
      <h2 className="text-2xl text-dark-orange font-semibold mb-2">{title}</h2>
      <p className="text-gray-200 text-sm mb-4">{excerpt}</p>
      <p className="text-gray-400 text-xs">{date}</p>
    </div>
  );
};

export default BlogPostCard;
