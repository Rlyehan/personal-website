// src/components/ColoredTypewriter.tsx

import React, { useState, useEffect } from 'react';

interface CustomTypewriterProps {
  strings: { text: string; color?: string }[];
  delay?: number;
  loop?: boolean;
}

const CustomTypewriter: React.FC<CustomTypewriterProps> = ({
  strings,
  delay = 75,
  loop = true,
}) => {
  const [currentStringIndex, setCurrentStringIndex] = useState(0);
  const [currentCharIndex, setCurrentCharIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    const timer = setTimeout(
      () => {
        if (isDeleting) {
          setCurrentCharIndex((prevIndex) => prevIndex - 1);
          if (currentCharIndex === 0) {
            setIsDeleting(false);
            setCurrentStringIndex(
              (prevIndex) => (prevIndex + 1) % strings.length,
            );
          }
        } else {
          setCurrentCharIndex((prevIndex) => prevIndex + 1);
          if (currentCharIndex === strings[currentStringIndex].text.length) {
            setIsDeleting(true);
          }
        }
      },
      isDeleting ? delay / 2 : delay,
    );

    return () => clearTimeout(timer);
  }, [currentCharIndex, isDeleting, delay, strings, currentStringIndex]);

  const currentString = strings[currentStringIndex].text.substr(
    0,
    currentCharIndex,
  );

  return (
    <span className="whitespace-nowrap">
      <span
        className={
          strings[currentStringIndex].color
            ? `text-${strings[currentStringIndex].color}`
            : ''
        }
      >
        {currentString}
      </span>
      <span className="text-darkOrange animate-blink">|</span>
    </span>
  );
};

export default CustomTypewriter;
