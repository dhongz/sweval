export const TAGS = {
    ACCOUNTS: 'accounts',
    CONTACTS: 'contacts',
    DOCUMENTS: 'documents',
    COMPANIES: 'companies',
    USERS: 'users',
    TEMPLATES: 'templates',
    ENTRIES: 'entries',
    AUTH: 'auth',
  } as const;
  
  import { JsonValue, HeadersConfig } from '@/lib/types';
  
  export const apiClientSide = {
    post: async (endpoint: string, data: JsonValue | FormData, headers: HeadersConfig = {}, signal?: AbortSignal) => {
      const defaultHeaders: HeadersConfig = {
        ...headers
      };
      const body = data instanceof FormData ? data : JSON.stringify(data);
  
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${endpoint}`, {
        method: 'POST',
        headers: defaultHeaders as HeadersInit,
        body,
        credentials: 'include',
        signal,
      });
      
      if (!response.ok) {
        // if (response.status === 401) {
        //   // Using window.location for client-side navigation to signin
        //   window.location.href = '/signin';
        //   return;
        // }
        const error = await response.json();
        throw new Error(error.message || 'Error');
      }
      
      return response;
    },
  
    get: async (endpoint: string, signal?: AbortSignal, token?: string, tags?: string[], headers: HeadersConfig = {}) => {
      const defaultHeaders: HeadersConfig = {
        ...headers
      };
  
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${endpoint}`, {
        method: 'GET',
        headers: defaultHeaders as HeadersInit,
        next: { tags: tags || [] },
        credentials: 'include',
        signal,
      });
  
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Error');
      }
  
      return response;
    },
  
    put: async (endpoint: string, data: JsonValue, headers: HeadersConfig = {}) => {
      const defaultHeaders: HeadersConfig = {
        ...headers
      };
  
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${endpoint}`, {
        method: 'PUT',
        headers: defaultHeaders as HeadersInit,
        body: JSON.stringify(data),
        credentials: 'include',
      });
  
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Error');
      }
  
      return response; 
    },
  
    patch: async (endpoint: string, data: JsonValue, headers: HeadersConfig = {}) => {
      const defaultHeaders: HeadersConfig = {
          ...headers
      };
  
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${endpoint}`, {
          method: 'PATCH',
          headers: defaultHeaders as HeadersInit,
          body: JSON.stringify(data),
          credentials: 'include',
      });
  
      if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message || 'Error');
      }
  
      return response;
  },
  
    delete: async (endpoint: string, headers: HeadersConfig = {}) => {
      const defaultHeaders: HeadersConfig = {
        ...headers
      };
  
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${endpoint}`, {
        method: 'DELETE',
        headers: defaultHeaders as HeadersInit,
        credentials: 'include',
      });
  
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Error');
      }
  
      return response;
    },
  };
  
  export const apiServerSide = {
    post: async (endpoint: string, data: JsonValue | FormData, headers: HeadersConfig = {}) => {
      const defaultHeaders: HeadersConfig = {
        // "Origin": "https://nidoai.app",
        // "Host": "api.nidoai.app",
        ...headers
      };
      const body = data instanceof FormData ? data : JSON.stringify(data);
  
      const response = await fetch(`${process.env.API_SERVER_URL}/${endpoint}`, {
        method: 'POST',
        headers: defaultHeaders as HeadersInit,
        body,
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error');
      }
      
      return response;
    },
  
    get: async (endpoint: string, headers: HeadersConfig = {}) => {
      const defaultHeaders: HeadersConfig = {
        // "Origin": "https://nidoai.app",
        // "Host": "api.nidoai.app",
        ...headers
      };
  
      const response = await fetch(`${process.env.API_SERVER_URL}/${endpoint}`, {
        method: 'GET',
        headers: defaultHeaders as HeadersInit,
      });
  
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Error');
      }
  
      return response;
    },
  
    put: async (endpoint: string, data: JsonValue, headers: HeadersConfig = {}) => {
      const defaultHeaders: HeadersConfig = {
        ...headers
      };
  
      const response = await fetch(`${process.env.API_SERVER_URL}/${endpoint}`, {
        method: 'PUT',
        headers: defaultHeaders as HeadersInit,
        body: JSON.stringify(data),
      });
  
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Error');
      }
  
      return response; 
    },
  
    delete: async (endpoint: string, headers: HeadersConfig = {}) => {
      const defaultHeaders: HeadersConfig = {
        ...headers
      };
  
      const response = await fetch(`${process.env.API_SERVER_URL}/${endpoint}`, {
        method: 'DELETE',
        headers: defaultHeaders as HeadersInit,
      });
  
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Error');
      }
  
      return response;
    },
  };