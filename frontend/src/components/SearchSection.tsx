import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";

interface SearchSectionProps {
  query: string;
  onChange: (value: string) => void;
}

export default function SearchSection({ query, onChange }: SearchSectionProps) {
  return (
    <section
      className="mx-auto max-w-2xl px-4"
      style={{ paddingBottom: "2rem" }}
    >
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
        <Input
          type="text"
          placeholder="Search by title, author, or keyword…"
          value={query}
          onChange={(e) => onChange(e.target.value)}
          className="pl-10 text-base"
        />
      </div>
    </section>
  );
}
