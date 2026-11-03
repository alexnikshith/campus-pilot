import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import apiClient, { TOKEN_STORAGE_KEY, USER_STORAGE_KEY } from '../lib/api';
import { AuthUser, UserLoginRequest, UserRegisterRequest, TokenResponse, ApiResponse } from '../types';

interface AuthContextType {
  user: AuthUser | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: UserLoginRequest) => Promise<void>;
  register: (payload: UserRegisterRequest) => Promise<void>;
  logout: () => void;
  updateUser: (updates: Partial<AuthUser>) => void;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<AuthUser | null>(() => {
    try {
      const savedUser = localStorage.getItem(USER_STORAGE_KEY);
      return savedUser ? JSON.parse(savedUser) : null;
    } catch {
      return null;
    }
  });

  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem(TOKEN_STORAGE_KEY);
  });

  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Validate or refresh active profile on mount if token exists
  const refreshProfile = useCallback(async () => {
    const activeToken = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (!activeToken) {
      setUser(null);
      setIsLoading(false);
      return;
    }

    try {
      const response = await apiClient.get<ApiResponse<AuthUser>>('/auth/me');
      if (response.data && response.data.data) {
        setUser(response.data.data);
        localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(response.data.data));
      }
    } catch {
      // In case token is invalid, clear credentials
      localStorage.removeItem(TOKEN_STORAGE_KEY);
      localStorage.removeItem(USER_STORAGE_KEY);
      setToken(null);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshProfile();

    const handleUnauthorized = () => {
      setToken(null);
      setUser(null);
    };

    window.addEventListener('auth:unauthorized', handleUnauthorized);
    return () => {
      window.removeEventListener('auth:unauthorized', handleUnauthorized);
    };
  }, [refreshProfile]);

  const login = async (credentials: UserLoginRequest) => {
    setIsLoading(true);
    try {
      const response = await apiClient.post<ApiResponse<TokenResponse>>('/auth/login', credentials);
      const tokenData = response.data.data;
      const accessToken = tokenData.access_token;

      localStorage.setItem(TOKEN_STORAGE_KEY, accessToken);
      setToken(accessToken);

      // Immediately fetch user profile with the newly set token
      const meResponse = await apiClient.get<ApiResponse<AuthUser>>('/auth/me', {
        headers: { Authorization: `Bearer ${accessToken}` },
      });

      const userData = meResponse.data.data;
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(userData));
      setUser(userData);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (payload: UserRegisterRequest) => {
    setIsLoading(true);
    try {
      const response = await apiClient.post<ApiResponse<TokenResponse>>('/auth/register', payload);
      const tokenData = response.data.data;
      const accessToken = tokenData.access_token;

      localStorage.setItem(TOKEN_STORAGE_KEY, accessToken);
      setToken(accessToken);

      // Fetch newly created user profile
      const meResponse = await apiClient.get<ApiResponse<AuthUser>>('/auth/me', {
        headers: { Authorization: `Bearer ${accessToken}` },
      });

      const userData = meResponse.data.data;
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(userData));
      setUser(userData);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    try {
      apiClient.post('/auth/logout').catch(() => {
        // Stateless logout; ignore network failure on teardown
      });
    } finally {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
      localStorage.removeItem(USER_STORAGE_KEY);
      setToken(null);
      setUser(null);
    }
  };

  const updateUser = (updates: Partial<AuthUser>) => {
    setUser((prev) => {
      if (!prev) return null;
      const updated = { ...prev, ...updates };
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(updated));
      return updated;
    });
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        isAuthenticated: !!token && !!user,
        login,
        register,
        logout,
        updateUser,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
