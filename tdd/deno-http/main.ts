const port = parseInt(Deno.env.get("PORT") || "8000");

const handler = (_req: Request): Response => {
  return new Response("Hello, World!", {
    headers: { "content-type": "text/plain" },
  });
};

console.log(`Server running at http://localhost:${port}`);
Deno.serve({ port }, handler);
