import { Search, BookOpen, ListChecks } from "lucide-react";

export default function HowItWorks() {
  return (
    <section
      className="mx-auto max-w-xl px-4"
      style={{ paddingTop: "2rem", paddingBottom: "5rem", borderTop: "1px solid #e5e7eb" }}
    >
      <h2
        className="text-sm font-semibold text-gray-400 text-center"
        style={{ letterSpacing: "0.05em", textTransform: "uppercase", marginBottom: "2rem" }}
      >
        How It Works
      </h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr",
          gap: "1.25rem",
        }}
      >
        <StepCard
          step={1}
          icon={<Search size={20} className="text-gray-500" />}
          title="Search"
          description="Type a title, author, or keyword."
        />
        <StepCard
          step={2}
          icon={<ListChecks size={20} className="text-gray-500" />}
          title="Discover"
          description="Browse results and find hidden gems."
        />
        <StepCard
          step={3}
          icon={<BookOpen size={20} className="text-gray-500" />}
          title="Explore"
          description="See covers, categories, and details."
        />
      </div>
    </section>
  );
}

function StepCard({
  step,
  icon,
  title,
  description,
}: {
  step: number;
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="flex flex-col items-center gap-3 text-center" style={{ padding: "1rem 0.5rem" }}>
      <span
        className="text-xs font-semibold text-gray-500"
        style={{
          backgroundColor: "#f3f4f6",
          borderRadius: "50%",
          width: "1.75rem",
          height: "1.75rem",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {step}
      </span>
      {icon}
      <h3 className="font-semibold text-gray-900 text-sm">{title}</h3>
      <p className="text-xs text-gray-400">{description}</p>
    </div>
  );
}
