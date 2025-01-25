import type { Company } from "../types";

interface CompanyListProps {
  companies: Company[];
}

export function CompanyList({ companies }: CompanyListProps) {
  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {companies.map((company) => (
        <div key={company.id} className="border rounded-lg p-4 shadow-sm flex flex-col items-center">
          <div className="mb-4 w-20 h-20 flex items-center justify-center">
            {company.favicon ? (
              <img
                src={company.favicon || "/placeholder.svg"}
                alt={`${company.website} favicon`}
                className="w-20 h-20 object-contain"
                onError={(e) => {
                  e.currentTarget.src = "/placeholder.svg?height=80&width=80";
                }}
              />
            ) : (
              <div className="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center">
                <span className="text-gray-500 text-3xl">{company.website.charAt(0).toUpperCase()}</span>
              </div>
            )}
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
