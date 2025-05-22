export type JsonPrimitive = string | number | boolean | null;
export type JsonObject = { [key: string]: JsonValue };
export type JsonArray = JsonValue[];
export type JsonValue = JsonPrimitive | JsonObject | JsonArray;
export type HeadersConfig = Record<string, string>;


export type ApiResponse<T = unknown> = {
    success: boolean;
    message: string;
    data?: T | null;
    status: number;
    errors?: Record<string, string[]> | null;
}









