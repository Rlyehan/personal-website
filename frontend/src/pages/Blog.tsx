import React, { useState } from 'react';
import BlogPostCard, { BlogPostData } from '../components/BlogPostCard';
import { blogPosts } from '../mocks/blogPosts';
import BlogPost from '../components/BlogPost';

const Blog: React.FC = () => {
  const [selectedPost, setSelectedPost] = useState<BlogPostData | null>(null);

  const handlePostClick = (post: BlogPostData) => {
    setSelectedPost(post);
  };

  return (
    <div className="container mx-auto py-16">
      {selectedPost ? (
        <BlogPost {...selectedPost} onBack={() => setSelectedPost(null)} />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {blogPosts.map((post) => (
            <BlogPostCard
              key={post.id}
              {...post}
              onClick={() => handlePostClick(post)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Blog;
