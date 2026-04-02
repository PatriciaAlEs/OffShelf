import { useState } from "react";
import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { useBookSearch } from "@/hooks/useBookSearch";
import BookCard from "@/components/BookCard";

const Index = () => {
  const [query, setQuery] = useState("");
  const { data: books, isLoading, isError } = useBookSearch(query);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="mx-auto max-w-2xl px-4 py-16">
        <h1 className="mb-8 text-center text-4xl font-bold text-gray-900">
          Book Search
        </h1>

        <div className="relative mb-10">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
          <Input
            type="text"
            placeholder="Search by title, author, or keyword…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pl-10 text-base"
          />
        </div>

        {isLoading && <p className="text-center text-gray-400">Searching…</p>}

        {isError && (
          <p className="text-center text-red-500">
            Something went wrong. Please try again.
          </p>
        )}

        {books && books.length === 0 && query.trim() && !isLoading && (
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

        {!query.trim() && (
          <p className="text-center text-gray-400">
            Start typing to discover books.
          </p>
        )}
      </div>
    </div>
  );
};

export default Index;
