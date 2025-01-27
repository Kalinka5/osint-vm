// src/api/company-image/[id].ts
import type { APIRoute } from "astro";

export const GET: APIRoute = async ({ params }) => {
  const { id } = params;

  try {
    // Fetch the data from the backend service
    const response = await fetch(`http://127.0.0.1:8000/company-images/${id}`);
    if (!response.ok) {
      throw new Error("Failed to fetch image");
    }

    const data = await response.json();

    // Return the fetched data as a response
    return new Response(JSON.stringify(data), { status: 200 });
  } catch (err) {
    console.error("Error fetching image:", err);

    // Return an error response in case of failure
    return new Response(JSON.stringify({ error: "Internal Server Error" }), { status: 500 });
  }
};
