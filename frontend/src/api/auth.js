import api from './axios';

export const authAPI = {
    // Login
    login: async (email, password) => {
        const response = await api.post('/auth/login/', { email, password });
        return response.data;
    },

    // Logout
    logout: async (refreshToken) => {
        const response = await api.post('/auth/logout/', { refresh: refreshToken });
        return response.data;
    },

    // Dados do usuário autenticado
    me: async () => {
        const response = await api.get('/auth/me/');
        return response.data;
    },

    // Refresh token
    refresh: async (refreshToken) => {
        const response = await api.post('/auth/refresh/', { refresh: refreshToken });
        return response.data;
    },
};