import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from "lucide-react";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
}

export function Pagination({ currentPage, totalPages }: PaginationProps) {
  const maxVisiblePages = 5;
  const pageNumbers: number[] = [];

  let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
  const endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

  if (endPage - startPage + 1 < maxVisiblePages) {
    startPage = Math.max(1, endPage - maxVisiblePages + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    pageNumbers.push(i);
  }

  const createPageLink = (page: number, label: React.ReactNode, isDisabled: boolean) => (
    <a
      href={isDisabled ? undefined : `/page/${page}`}
      className={`p-2 rounded ${isDisabled ? "text-gray-400 cursor-not-allowed" : "text-blue-600 hover:bg-blue-100"}`}
      aria-disabled={isDisabled}
    >
      {label}
    </a>
  );

  return (
    <nav className="flex justify-center items-center space-x-2 mt-8">
      {createPageLink(1, <ChevronsLeft className="w-5 h-5" />, currentPage === 1)}
      {createPageLink(currentPage - 1, <ChevronLeft className="w-5 h-5" />, currentPage === 1)}

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

      {createPageLink(currentPage + 1, <ChevronRight className="w-5 h-5" />, currentPage === totalPages)}
      {createPageLink(totalPages, <ChevronsRight className="w-5 h-5" />, currentPage === totalPages)}
    </nav>
  );
}
