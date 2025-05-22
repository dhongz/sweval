'use client'
import { useState } from 'react';
import { generateApi } from '@/lib/api/generate';

export default function TestComponent() {
    const [topic, setTopic] = useState('');
    const [contentType, setContentType] = useState('');
    const [content, setContent] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    
    const handleGenerate = async () => {
        if (!topic.trim() || !contentType.trim()) {
            setError('Please fill in all fields');
            return;
        }

        try {
            setIsLoading(true);
            setError(null);
            const response = await generateApi.generate({
                topic: topic.trim(),
                content_type: contentType.trim()
            });
            setContent(response.data || '');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred while generating content');
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="max-w-2xl mx-auto p-6 space-y-6">
            <div className="space-y-4">
                <div className="space-y-2">
                    <label htmlFor="topic" className="block text-sm font-medium text-gray-700">
                        Topic
                    </label>
                    <input
                        id="topic"
                        type="text"
                        value={topic}
                        onChange={(e) => setTopic(e.target.value)}
                        placeholder="Enter your topic"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <div className="space-y-2">
                    <label htmlFor="contentType" className="block text-sm font-medium text-gray-700">
                        Content Type
                    </label>
                    <input
                        id="contentType"
                        type="text"
                        value={contentType}
                        onChange={(e) => setContentType(e.target.value)}
                        placeholder="Enter content type"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <button
                    onClick={handleGenerate}
                    disabled={isLoading}
                    className="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {isLoading ? 'Generating...' : 'Generate'}
                </button>

                {error && (
                    <div className="p-3 text-sm text-red-700 bg-red-100 rounded-md">
                        {error}
                    </div>
                )}
            </div>

            {content && (
                <div className="pt-4 border-t border-gray-200">
                    <h3 className="text-lg font-medium text-gray-900">Generated Content:</h3>
                    <div className="mt-2 text-gray-700 whitespace-pre-wrap">{content}</div>
                </div>
            )}
        </div>
    );
}