import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
}

export function Pagination({ currentPage, totalPages }: PaginationProps) {
  const pageNumbers = [];
  const maxVisiblePages = 5;

  let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
  const endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

  if (endPage - startPage + 1 < maxVisiblePages) {
    startPage = Math.max(1, endPage - maxVisiblePages + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    pageNumbers.push(i);
  }

  return (
    <nav className="flex justify-center items-center space-x-2 mt-8">
      <a
        href={`/page/1`}
        className={`p-2 rounded ${currentPage === 1 ? "text-gray-400 cursor-not-allowed" : "text-blue-600 hover:bg-blue-100"}`}
        aria-label="First page"
      >
        <ChevronsLeft className="w-5 h-5" />
      </a>
      <a
        href={`/page/${currentPage - 1}`}
        className={`p-2 rounded ${currentPage === 1 ? "text-gray-400 cursor-not-allowed" : "text-blue-600 hover:bg-blue-100"}`}
        aria-label="Previous page"
      >
        <ChevronLeft className="w-5 h-5" />
      </a>
      {startPage > 1 && (
        <>
          <a href="/page/1" className="px-3 py-2 rounded text-blue-600 hover:bg-blue-100">
            1
          </a>
          {startPage > 2 && <span className="px-3 py-2">...</span>}
        </>
      )}
      {pageNumbers.map((number) => (
        <a
          key={number}
          href={`/page/${number}`}
          className={`px-3 py-2 rounded ${currentPage === number ? "bg-blue-600 text-white" : "text-blue-600 hover:bg-blue-100"}`}
        >
          {number}
        </a>
      ))}
      {endPage < totalPages && (
        <>
          {endPage < totalPages - 1 && <span className="px-3 py-2">...</span>}
          <a href={`/page/${totalPages}`} className="px-3 py-2 rounded text-blue-600 hover:bg-blue-100">
            {totalPages}
          </a>
        </>
      )}
      <a
        href={`/page/${currentPage + 1}`}
        className={`p-2 rounded ${currentPage === totalPages ? "text-gray-400 cursor-not-allowed" : "text-blue-600 hover:bg-blue-100"}`}
        aria-label="Next page"
      >
        <ChevronRight className="w-5 h-5" />
      </a>
      <a
        href={`/page/${totalPages}`}
        className={`p-2 rounded ${currentPage === totalPages ? "text-gray-400 cursor-not-allowed" : "text-blue-600 hover:bg-blue-100"}`}
        aria-label="Last page"
      >
        <ChevronsRight className="w-5 h-5" />
      </a>
    </nav>
  );
}
