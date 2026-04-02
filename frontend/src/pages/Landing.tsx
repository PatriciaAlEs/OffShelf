import { useState } from "react";
import { useBookSearch } from "@/hooks/useBookSearch";
import Hero from "@/components/Hero";
import ResultsSection from "@/components/ResultsSection";
import HowItWorks from "@/components/HowItWorks";

export default function Landing() {
  const [query, setQuery] = useState("");
  const { data: books, isLoading, isError } = useBookSearch(query);

  return (
    <div className="min-h-screen bg-gray-50">
      <Hero query={query} onChange={setQuery} />
      <ResultsSection books={books} query={query} isLoading={isLoading} isError={isError} />
      <HowItWorks />
    </div>
  );
}
