// components/Results.jsx
import React from "react";

export default function Results({ summary }) {
  if (!summary) {
    return (
      <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-md mt-8 text-gray-700">
        <p>No summary available.</p>
      </div>
    );
  }

  // Split summary by lines, filter out empty, and parse bullet points and headings
  const lines = summary.split("\n").filter(Boolean);

  // Separate normal text, bullet points, and headings like "Icebreakers:"
  const formattedContent = [];
  let bulletPoints = [];
  let inBulletList = false;

  lines.forEach((line, i) => {
    const trimmed = line.trim();

    if (trimmed.startsWith("->")) {
      // Bullet point line
      bulletPoints.push(trimmed.replace("->", "").trim());
      inBulletList = true;
    } else {
      // Flush previous bullets if any
      if (inBulletList) {
        formattedContent.push(
          <ul
            key={"bullet-" + i}
            className="list-disc list-inside mb-4 text-gray-800 font-medium"
          >
            {bulletPoints.map((point, idx) => (
              <li key={idx} className="mb-1">
                {point}
              </li>
            ))}
          </ul>
        );
        bulletPoints = [];
        inBulletList = false;
      }

      // Check if line is a heading (e.g. Icebreakers)
      if (trimmed.toLowerCase().includes("icebreaker")) {
        formattedContent.push(
          <h3
            key={"heading-" + i}
            className="text-xl font-semibold mb-3 text-blue-600"
          >
            {trimmed}
          </h3>
        );
      } else {
        // Normal paragraph
        formattedContent.push(
          <p key={"para-" + i} className="mb-3 text-gray-700">
            {trimmed}
          </p>
        );
      }
    }
  });

  // Flush any remaining bullets at end
  if (inBulletList && bulletPoints.length) {
    formattedContent.push(
      <ul
        key={"bullet-last"}
        className="list-disc list-inside mb-4 text-gray-800 font-medium"
      >
        {bulletPoints.map((point, idx) => (
          <li key={idx} className="mb-1">
            {point}
          </li>
        ))}
      </ul>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-8 bg-white rounded-lg shadow-md mt-8">
      <h2 className="text-3xl font-bold mb-6 text-blue-700">User Information</h2>
      <div>{formattedContent}</div>
    </div>
  );
}
