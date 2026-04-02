import type { Book } from "@/types/book";
import BookCard from "@/components/BookCard";

interface ResultsSectionProps {
  books: Book[] | undefined;
  query: string;
  isLoading: boolean;
  isError: boolean;
}

export default function ResultsSection({
  books,
  query,
  isLoading,
  isError,
}: ResultsSectionProps) {
  const hasQuery = query.trim().length > 0;

  if (!hasQuery && !isLoading) return null;

  return (
    <section
      className="mx-auto max-w-xl px-4"
      style={{ paddingBottom: "3rem" }}
    >
      {isLoading && <p className="text-center text-gray-400">Searching…</p>}

      {isError && (
        <p className="text-center text-red-500">
          Something went wrong. Please try again.
        </p>
      )}

      {books && books.length === 0 && hasQuery && !isLoading && (
        <p className="text-center text-gray-400">
          No books found for "{query}".
        </p>
      )}

      {books && books.length > 0 && (
        <div className="flex flex-col gap-3">
          {books.map((book, i) => (
            <BookCard key={`${book.title}-${i}`} book={book} />
          ))}
        </div>
      )}
    </section>
  );
}
