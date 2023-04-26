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
    <div className="my-2 mt-2">
      <div className="flex justify-between items-center mb-1">
        <span className="text-white w-1/5 mr-4">{skill}</span>
        <div className="relative w-4/5">
          {isFirst && (
            <>
              <div className="absolute top-0 left-1/4 text-s text-white -mt-8 transform -translate-x-1/2">
                <span className="font-bold">Junior</span>
              </div>
              <div className="absolute top-0 left-1/2 text-s text-white -mt-8 transform -translate-x-1/2">
                <span className="font-bold">Mid</span>
              </div>
              <div className="absolute top-0 left-3/4 text-s text-white -mt-8 transform -translate-x-1/2">
                <span className="font-bold">Senior</span>
              </div>
            </>
          )}
          <div className={`w-full h-5 rounded-lg bg-gray-800 mb-4 relative`}>
            <div
              className={`h-full rounded-lg ${
                percentage >= 66
                  ? 'bg-orange-800'
                  : percentage >= 33
                  ? 'bg-orange-500'
                  : 'bg-orange-300'
              } transition-all duration-500`}
              style={{ width: `${percentage}%` }}
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
