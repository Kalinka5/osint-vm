import { useState, useEffect } from "react";
import type { Company, CompanyImage } from "../types";

import { API_URL } from "../contants.js";

interface CompanyListProps {
  companies: Company[];
}

export function CompanyList({ companies }: CompanyListProps) {
  const [companyImages, setCompanyImages] = useState<Record<number, string>>({});

  useEffect(() => {
    const fetchImages = async () => {
      try {
        const imagePromises = companies
          .filter((company) => company.image_id)
          .map((company) =>
            fetch(`${API_URL}/company-images/${company.image_id}`)
              .then((res) => res.json())
              .then((data: CompanyImage) => ({ id: company.image_id, url: data.image_url }))
              .catch(() => ({ id: company.image_id, url: "/placeholder.svg" }))
          );

        const images = await Promise.all(imagePromises);
        const imageMap = images.reduce((acc, { id, url }) => ({ ...acc, [id]: url }), {} as Record<number, string>);

        setCompanyImages(imageMap);
      } catch (error) {
        console.error("Error fetching company images:", error);
      }
    };

    fetchImages();
  }, [companies]);

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {companies.map((company) => (
        <div key={company.id} className="border rounded-lg p-4 shadow-sm flex flex-col items-center">
          <div className="mb-4 w-20 h-20 flex items-center justify-center">
            <img
              src={companyImages[company.image_id] || "/placeholder.svg"}
              alt={`${company.website} logo`}
              className="w-20 h-20 object-contain"
              onError={(e) => {
                e.currentTarget.src = "/placeholder.svg";
              }}
            />
          </div>
          <h2 className="text-xl font-semibold text-center mb-2">{company.website}</h2>
          <p className="text-sm text-gray-600 mb-2 text-center">Founded: {company.year_founded || "N/A"}</p>
          <p className="text-sm mb-4 text-center">{company.about.slice(0, 150)}...</p>
          <a href={company.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline text-center">
            Visit Website
          </a>
        </div>
      ))}
    </div>
  );
}
