/**
 * Get the API base URL from environment variables
 * Handles both local development and production deployments
 */
export function getApiUrl(endpoint: string): string {
  // Use environment variable, with fallback for development
  const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  
  // Remove /api from endpoint if it already exists there
  let cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint
  cleanEndpoint = cleanEndpoint.startsWith('api/') ? cleanEndpoint.slice(4) : cleanEndpoint
  
  // Build final URL - only add /api if the base doesn't already have it
  const apiRoot = apiBase.endsWith('/api') ? apiBase : `${apiBase}/api`
  const finalUrl = `${apiRoot}/${cleanEndpoint}`
  
  return finalUrl
}
