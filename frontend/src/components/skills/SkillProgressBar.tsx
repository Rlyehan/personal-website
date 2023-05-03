import React from 'react';

interface SkillProgressBarProps {
  skill: string;
  percentage: number;
  isFirst: boolean;
}

const SkillProgressBar: React.FC<SkillProgressBarProps> = ({
  skill,
  percentage,
  isFirst,
}) => {
  return (
    <div className="my-4 w-full md:w-3/4 mx-auto">
      <div className="flex justify-between items-center mb-1">
        <span className="text-white font-semibold text-lg w-1/5 pr-4 flex items-center">
          {skill}
        </span>
        <div className="relative w-4/5">
          {isFirst && (
            <>
              <div className="absolute top-0 left-1/4 text-base text-white -mt-12 transform -translate-x-1/2">
                <span className="font-semibold">Junior</span>
              </div>
              <div className="absolute top-0 left-1/2 text-base text-white -mt-12 transform -translate-x-1/2">
                <span
                  className="font-semibold"
                  style={{ transform: 'translate(-50%, 0)' }}
                >
                  Mid
                </span>
              </div>
              <div className="absolute top-0 left-3/4 text-base text-white -mt-12 transform -translate-x-1/2">
                <span className="font-semibold">Senior</span>
              </div>
            </>
          )}
          <div
            className={`w-full h-3 md:h-6 rounded-lg bg-gray-800 mb-4 relative`}
          >
            <div
              className={`h-full rounded-lg transition-all duration-500`}
              style={{
                width: `${percentage}%`,
                backgroundImage: 'linear-gradient(to right, #FF5E5B, #FFAA00)',
              }}
            ></div>
            <div className="absolute top-0 left-1/4 w-0.5 h-full bg-white opacity-40"></div>
            <div className="absolute top-0 left-1/2 w-0.5 h-full bg-white opacity-40"></div>
            <div className="absolute top-0 left-3/4 w-0.5 h-full bg-white opacity-40"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SkillProgressBar;
