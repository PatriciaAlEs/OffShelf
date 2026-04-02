import type { Book } from "@/types/book";

interface BookCardProps {
  book: Book;
}

export default function BookCard({ book }: BookCardProps) {
  return (
    <div className="flex gap-4 rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition hover:shadow-md">
      {book.thumbnail ? (
        <img
          src={book.thumbnail}
          alt={book.title}
          className="h-28 w-20 flex-shrink-0 rounded object-cover"
        />
      ) : (
        <div className="flex h-28 w-20 flex-shrink-0 items-center justify-center rounded bg-gray-100 text-xs text-gray-400">
          No cover
        </div>
      )}

      <div className="flex flex-col gap-1 overflow-hidden">
        <h2 className="truncate text-lg font-semibold text-gray-900">
          {book.title}
        </h2>

        {book.authors.length > 0 && (
          <p className="text-sm text-gray-600">{book.authors.join(", ")}</p>
        )}

        {book.categories.length > 0 && (
          <p className="text-xs text-gray-400">{book.categories.join(", ")}</p>
        )}

        {book.language && (
          <span className="inline-block w-fit rounded bg-gray-100 px-2 py-0.5 text-xs text-gray-500">
            {book.language.toUpperCase()}
          </span>
        )}

        {book.is_indie && (
          <span className="inline-block w-fit rounded bg-indigo-100 px-2 py-0.5 text-xs font-medium text-indigo-700">
            Indie
          </span>
        )}

        {book.description && (
          <p className="mt-1 line-clamp-2 text-sm text-gray-500">
            {book.description}
          </p>
        )}
      </div>
    </div>
  );
}
