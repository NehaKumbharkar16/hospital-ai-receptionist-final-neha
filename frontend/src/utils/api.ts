/**
 * Get the API base URL from environment variables
 * Handles both local development and production deployments
 */
export function getApiUrl(endpoint: string): string {
  const rawApiEnv = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  const apiBase = rawApiEnv.replace(/\/$/, '') // drop trailing slash
  const apiRoot = apiBase.endsWith('/api') ? apiBase : `${apiBase}/api`
  
  // Clean endpoint path
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint
  
  return `${apiRoot}/${cleanEndpoint}`
}
