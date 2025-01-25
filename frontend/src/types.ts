export interface Company {
  id: number;
  about: string;
  year_founded: string;
  website: string;
  number_of_employees_id: number;
  linkedin: string | null;
  facebook: string | null;
  twitter: string | null;
  favicon: string | null;
}

export interface ApiResponse {
  items: Company[];
  total: number;
  page: number;
  size: number;
  pages: number;
}
