import { useQuery } from "@tanstack/react-query";
import type { Book } from "@/types/book";

async function fetchBooks(query: string): Promise<Book[]> {
    if (!query.trim()) return [];
    const res = await fetch(`/books/search?q=${encodeURIComponent(query.trim())}`);
    if (!res.ok) throw new Error("Failed to fetch books");
    return res.json();
}

export function useBookSearch(query: string) {
    return useQuery<Book[]>({
        queryKey: ["books", query],
        queryFn: () => fetchBooks(query),
        enabled: query.trim().length > 0,
        staleTime: 1000 * 60 * 5,
        placeholderData: (prev) => prev,
    });
}
