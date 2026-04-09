const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";

async function parseResponse(response) {
  const contentType = response.headers.get("content-type") || "";

  if (contentType.includes("application/json")) {
    return response.json();
  }

  return response.text();
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);
  const data = await parseResponse(response);

  if (!response.ok) {
    const message =
      (data && typeof data === "object" && (data.detail || data.error)) ||
      (typeof data === "string" && data) ||
      `Request failed with status ${response.status}`;

    throw new Error(message);
  }

  return data;
}

export function analyzeText(text) {
  return request("/text", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });
}

export function analyzeImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  return request("/image", {
    method: "POST",
    body: formData,
  });
}

export function analyzeVideo(file) {
  const formData = new FormData();
  formData.append("file", file);

  return request("/video", {
    method: "POST",
    body: formData,
  });
}

export function getVideoResult(taskId) {
  return request(`/video-result/${taskId}`);
}

export function analyzePlagiarism(file) {
  const formData = new FormData();
  formData.append("file", file);

  return request("/plagiarism", {
    method: "POST",
    body: formData,
  });
}

export function signUp(username, password) {
  return request("/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });
}

export function signIn(username, password) {
  return request("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });
}
