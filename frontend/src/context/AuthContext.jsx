import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('libraai_user');
    return saved ? JSON.parse(saved) : { email: 'admin@libraai.com', role: 'Administrator' };
  });

  const login = (email, password) => {
    const userData = { email, role: 'Administrator' };
    setUser(userData);
    localStorage.setItem('libraai_user', JSON.stringify(userData));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('libraai_user');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
