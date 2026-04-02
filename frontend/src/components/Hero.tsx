import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";

interface HeroProps {
  query: string;
  onChange: (value: string) => void;
}

export default function Hero({ query, onChange }: HeroProps) {
  return (
    <section
      className="mx-auto max-w-xl px-4 flex flex-col items-center text-center"
      style={{ paddingTop: "5rem", paddingBottom: "2.5rem", gap: "0.75rem" }}
    >
      <h1 className="text-4xl font-bold text-gray-900">OffShelf</h1>
      <p className="text-base text-gray-500" style={{ maxWidth: "26rem", marginBottom: "1rem" }}>
        Search millions of books by title, author, or keyword.
      </p>
      <div className="relative w-full" style={{ maxWidth: "28rem" }}>
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
        <Input
          type="text"
          placeholder='Try "Kafka", "sci-fi", "Murakami"…'
          value={query}
          onChange={(e) => onChange(e.target.value)}
          className="pl-10 text-base"
        />
      </div>
    </section>
  );
}
