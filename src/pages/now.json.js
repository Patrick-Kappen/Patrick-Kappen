import { getSite } from "../lib/content";

export const GET = async () => {
  const { now } = await getSite();
  return new Response(JSON.stringify(now, null, 2), {
    headers: { "Content-Type": "application/json" },
  });
};
