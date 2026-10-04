import now from "@content/now.json";

export const GET = () =>
  new Response(JSON.stringify(now, null, 2), {
    headers: { "Content-Type": "application/json" },
  });
