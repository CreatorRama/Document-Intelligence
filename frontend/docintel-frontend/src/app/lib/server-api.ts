// lib/server-api.ts
const API_BASE_URL = 'https://weed-divorce-sd-sega.trycloudflare.com/api';

export async function fetchDocumentsServer() {
  try {
    const response = await fetch(`${API_BASE_URL}/documents/`, {
      cache: 'no-store', // or 'force-cache' for caching
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching documents:', error);
    throw error;
  }
}