import React from 'react';
import CustomTypewriter from './customTypewriter';

const Hero: React.FC = () => {
  return (
    <div className="bg-darkGray h-screen flex flex-col justify-start items-center pt-10 md:pt-30 lg:pt-40">
      <h1 className="text-3xl md:text-4xl lg:text-6xl xl:text-8xl font-bold mb-4 text-dark-orange">
        Maximilian Huber
      </h1>
      <h2 className="text-lg md:text-xl lg:text-2xl xl:text-3xl text-white">
        <CustomTypewriter
          strings={[
            { text: 'Full Stack Developer' },
            { text: 'Data Engineer' },
            { text: 'DevOps Enthusiast' },
          ]}
          delay={75}
          loop
        />
      </h2>
    </div>
  );
};

export default Hero;
