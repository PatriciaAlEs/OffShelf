export interface Book {
    id: number;
    title: string;
    authors: string[];
    description: string | null;
    language: string | null;
    isbn: string | null;
    thumbnail: string | null;
    categories: string[];
    is_indie: boolean;
    created_at: string | null;
    updated_at: string | null;
}
