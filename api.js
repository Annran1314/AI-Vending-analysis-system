// API配置
const API_CONFIG = {
    BASE_URL: 'http://localhost:5000/api',
    TIMEOUT: 10000
};

// API客户端类
class APIClient {
    constructor(baseURL = API_CONFIG.BASE_URL) {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('access_token') || null;
    }

    setToken(token) {
        this.token = token;
        if (token) {
            localStorage.setItem('access_token', token);
        } else {
            localStorage.removeItem('access_token');
        }
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const config = {
            ...options,
            headers
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || '请求失败');
            }
            
            return data;
        } catch (error) {
            console.error('API请求错误:', error);
            throw error;
        }
    }

    async get(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'GET' });
    }

    async post(endpoint, data, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async put(endpoint, data, options = {}) {
        return this.request(endpoint, {
            ...options,
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async delete(endpoint, options = {}) {
        return this.request(endpoint, { ...options, method: 'DELETE' });
    }
}

// 创建API客户端实例
const apiClient = new APIClient();

// 认证API
const AuthAPI = {
    async register(userData) {
        return await apiClient.post('/auth/register', userData);
    },

    async login(credentials) {
        const response = await apiClient.post('/auth/login', credentials);
        if (response.data.access_token) {
            apiClient.setToken(response.data.access_token);
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
        return response;
    },

    async logout() {
        apiClient.setToken(null);
        localStorage.removeItem('user');
    },

    async getProfile() {
        return await apiClient.get('/auth/profile');
    },

    async updateProfile(userData) {
        return await apiClient.put('/auth/profile', userData);
    }
};

// 产品API
const ProductAPI = {
    async getProducts(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const endpoint = queryString ? `?${queryString}` : '';
        return await apiClient.get(`/products${endpoint}`);
    },

    async getProduct(id) {
        return await apiClient.get(`/products/${id}`);
    },

    async createProduct(productData) {
        return await apiClient.post('/products', productData);
    },

    async updateProduct(id, productData) {
        return await apiClient.put(`/products/${id}`, productData);
    },

    async deleteProduct(id) {
        return await apiClient.delete(`/products/${id}`);
    },

    async importProducts(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_CONFIG.BASE_URL}/products/import`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiClient.token}`
            },
            body: formData
        });
        
        return await response.json();
    }
};

// 分析API
const AnalysisAPI = {
    async compareProducts(productIds) {
        return await apiClient.post('/analysis/compare', { products: productIds });
    },

    async aiAnalysis(productIds) {
        return await apiClient.post('/analysis/ai', { products: productIds });
    },

    async brandAnalysis(brands) {
        return await apiClient.post('/analysis/brand', { brands: brands });
    },

    async getTrends() {
        return await apiClient.get('/analysis/trends');
    }
};

// 报告API
const ReportAPI = {
    async getReports() {
        return await apiClient.get('/reports');
    },

    async getReport(id) {
        return await apiClient.get(`/reports/${id}`);
    },

    async createReport(reportData) {
        return await apiClient.post('/reports', reportData);
    },

    async updateReport(id, reportData) {
        return await apiClient.put(`/reports/${id}`, reportData);
    },

    async deleteReport(id) {
        return await apiClient.delete(`/reports/${id}`);
    },

    async exportReport(reportId, format = 'json') {
        return await apiClient.post('/reports/export', { report_id: reportId, format });
    }
};

// 用户管理API（管理员）
const UserAPI = {
    async getUsers() {
        return await apiClient.get('/users');
    },

    async getUser(id) {
        return await apiClient.get(`/users/${id}`);
    },

    async updateUser(id, userData) {
        return await apiClient.put(`/users/${id}`, userData);
    },

    async deleteUser(id) {
        return await apiClient.delete(`/users/${id}`);
    }
};

// 工具函数
const APIUtils = {
    getCurrentUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },

    isAuthenticated() {
        return !!localStorage.getItem('access_token');
    },

    isAdmin() {
        const user = this.getCurrentUser();
        return user && user.role === 'admin';
    },

    handleAPIError(error, defaultMessage = '操作失败') {
        console.error('API错误:', error);
        showNotification(error.message || defaultMessage, 'error');
    },

    async safeAPICall(apiFunction, ...args) {
        try {
            return await apiFunction(...args);
        } catch (error) {
            this.handleAPIError(error);
            throw error;
        }
    }
};

// 导出API模块
window.API = {
    auth: AuthAPI,
    products: ProductAPI,
    analysis: AnalysisAPI,
    reports: ReportAPI,
    users: UserAPI,
    utils: APIUtils,
    client: apiClient
};