import React from 'react';
import { BlogPostData } from './BlogPostCard';

interface BlogPostProps extends BlogPostData {
  onBack: () => void;
}

const BlogPost: React.FC<BlogPostProps> = ({
  id,
  title,
  content,
  date,
  onBack,
}) => {
  return (
    <div className="bg-gray-800 rounded-lg p-4">
      <button
        onClick={onBack}
        className="bg-dark-orange text-white px-3 py-1 rounded-lg mb-4"
      >
        Back
      </button>
      <h2 className="text-3xl text-dark-orange font-semibold mb-2">{title}</h2>
      <p className="text-gray-200 mb-4">{content}</p>
      <p className="text-gray-400 text-xs">{date}</p>
    </div>
  );
};

export default BlogPost;
