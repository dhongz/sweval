'use client'

import { apiClientSide } from './client';
import { ApiResponse } from '../types';
// import { mutate } from 'swr';


export const generateApi = {
    generate: async (data: {
        topic: string;
        content_type: string;
    }): Promise<ApiResponse<string>> => {
        const response = await apiClientSide.post('generate', data, {
            'Content-Type': 'application/json'
        })
        // await mutate((key) => typeof key === 'string' && key.startsWith('accounts'))
        return await response.json()
    },
    
};