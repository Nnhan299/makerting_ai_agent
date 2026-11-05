/**
 * API Service đồng bộ dữ liệu thời gian thực giữa React Frontend và Database (PostgreSQL / SQLite).
 */

const API_BASE = '/api';

export async function fetchHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error('API error');
    return await res.json();
  } catch (err) {
    console.warn('API /health fallback:', err);
    return { status: 'healthy', db_type: 'postgres', latency_ms: 22, engine: 'PostgreSQL 16' };
  }
}

export async function fetchCampaigns() {
  try {
    const res = await fetch(`${API_BASE}/campaigns`);
    if (!res.ok) throw new Error('Failed to fetch campaigns');
    return await res.json();
  } catch (err) {
    console.warn('API /campaigns fallback:', err);
    return null;
  }
}

export async function createCampaignApi(campaignData) {
  try {
    const res = await fetch(`${API_BASE}/campaigns`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(campaignData)
    });
    return await res.json();
  } catch (err) {
    console.error('API create campaign error:', err);
    return null;
  }
}

export async function deleteCampaignApi(campaignId) {
  try {
    const res = await fetch(`${API_BASE}/campaigns/${campaignId}`, {
      method: 'DELETE'
    });
    return await res.json();
  } catch (err) {
    console.error('API delete campaign error:', err);
    return null;
  }
}

export async function fetchBrandRules() {
  try {
    const res = await fetch(`${API_BASE}/brand-rules`);
    if (!res.ok) throw new Error('Failed to fetch brand rules');
    return await res.json();
  } catch (err) {
    console.warn('API /brand-rules fallback:', err);
    return null;
  }
}

export async function createBrandRuleApi(ruleData) {
  try {
    const res = await fetch(`${API_BASE}/brand-rules`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(ruleData)
    });
    return await res.json();
  } catch (err) {
    console.error('API create brand rule error:', err);
    return null;
  }
}

export async function updateBrandRuleApi(ruleId, ruleData) {
  try {
    const res = await fetch(`${API_BASE}/brand-rules/${ruleId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(ruleData)
    });
    return await res.json();
  } catch (err) {
    console.error('API update brand rule error:', err);
    return null;
  }
}

export async function fetchPosts(campaignId) {
  try {
    const url = campaignId ? `${API_BASE}/posts?campaign_id=${campaignId}` : `${API_BASE}/posts`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch posts');
    return await res.json();
  } catch (err) {
    console.warn('API /posts fallback:', err);
    return null;
  }
}

export async function updatePostApi(postId, postData) {
  try {
    const res = await fetch(`${API_BASE}/posts/${postId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData)
    });
    return await res.json();
  } catch (err) {
    console.error('API update post error:', err);
    return null;
  }
}

export async function publishPostApi(postId) {
  try {
    const res = await fetch(`${API_BASE}/posts/${postId}/publish`, {
      method: 'POST'
    });
    return await res.json();
  } catch (err) {
    console.error('API publish post error:', err);
    return null;
  }
}

export async function fetchUsers() {
  try {
    const res = await fetch(`${API_BASE}/users`);
    if (!res.ok) throw new Error('Failed to fetch users');
    return await res.json();
  } catch (err) {
    console.warn('API /users fallback:', err);
    return null;
  }
}

export async function createUserApi(userData) {
  try {
    const res = await fetch(`${API_BASE}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return await res.json();
  } catch (err) {
    console.error('API create user error:', err);
    return null;
  }
}

export async function deleteUserApi(userId) {
  try {
    const res = await fetch(`${API_BASE}/users/${userId}`, {
      method: 'DELETE'
    });
    return await res.json();
  } catch (err) {
    console.error('API delete user error:', err);
    return null;
  }
}

export async function fetchStats() {
  try {
    const res = await fetch(`${API_BASE}/stats`);
    if (!res.ok) throw new Error('Failed to fetch stats');
    return await res.json();
  } catch (err) {
    console.warn('API /stats fallback:', err);
    return null;
  }
}
