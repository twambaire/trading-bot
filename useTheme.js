import { useState, useEffect } from 'react';

export function useTheme() {
  const [theme, setTheme] = useState(() => {
    // Check for stored theme preference or use system preference
    const storedTheme = localStorage.getItem('theme');
    if (storedTheme) {
      return storedTheme;
    }
    
    // Check system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    
    return 'light';
  });

  useEffect(() => {
    // Update document class when theme changes
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);
    
    // Store theme preference
    localStorage.setItem('theme', theme);
  }, [theme]);

  return { theme, setTheme };
}

