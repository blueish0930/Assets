const TYPES = {
  ".json": "application/json; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".webp": "image/webp",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".mp4": "video/mp4",
  ".blend": "application/octet-stream",
  ".svg": "image/svg+xml",
  ".html": "text/html; charset=utf-8",
};

function contentTypeFor(key) {
  const lower = key.toLowerCase();
  const dot = lower.lastIndexOf(".");
  if (dot < 0) return "application/octet-stream";
  return TYPES[lower.slice(dot)] || "application/octet-stream";
}

export default {
  async fetch(request, env) {
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method Not Allowed", { status: 405 });
    }

    const url = new URL(request.url);
    // Blender appends ?hash=SHA256:... — ignore query strings.
    let key = decodeURIComponent(url.pathname.replace(/^\/+/, ""));
    if (!key || key.endsWith("/")) {
      key += "_asset-library-meta.json";
    }

    const object = await env.ASSETS.get(key);
    if (!object) {
      return new Response("Not Found", { status: 404 });
    }

    const headers = new Headers();
    headers.set("Content-Type", object.httpMetadata?.contentType || contentTypeFor(key));
    headers.set("Content-Length", String(object.size));
    headers.set("ETag", object.httpEtag);
    headers.set("Accept-Ranges", "bytes");
    headers.set("Cache-Control", key.endsWith(".json") ? "public, max-age=60" : "public, max-age=31536000, immutable");
    headers.set("Access-Control-Allow-Origin", "*");
    headers.set("Access-Control-Allow-Methods", "GET, HEAD");

    const ifNoneMatch = request.headers.get("If-None-Match");
    if (ifNoneMatch && ifNoneMatch === object.httpEtag) {
      return new Response(null, { status: 304, headers });
    }

    if (request.method === "HEAD") {
      return new Response(null, { status: 200, headers });
    }

    return new Response(object.body, { status: 200, headers });
  },
};
