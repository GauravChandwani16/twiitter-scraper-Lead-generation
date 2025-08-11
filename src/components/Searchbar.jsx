// components/SearchBar.jsx
import React, { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [username, setUsername] = useState("");
  const [company, setCompany] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!username.trim()) return; // username required
    onSearch(username.trim(), company.trim() );
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-lg mx-auto bg-white p-8 rounded-xl shadow-lg"
    >
      {/* <h2 className="text-3xl font-semibold mb-6 text-gray-800 text-center">
        Twitter Profile Analyzer
      </h2> */}

      <div className="mb-6">
        <label
          htmlFor="username"
          className="block text-sm font-medium text-gray-600 mb-2"
        >
          Twitter Username <span className="text-red-500">*</span>
        </label>
        <input
          id="username"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="e.g. elonmusk"
          className="w-full px-5 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition"
          required
          autoFocus
        />
      </div>

      <div className="mb-8">
        <label
          htmlFor="company"
          className="block text-sm font-medium text-gray-600 mb-2"
        >
          Company Twitter Username (Optional)
        </label>
        <input
          id="company"
          type="text"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          placeholder="e.g. Tesla"
          className="w-full px-5 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition"
        />
      </div>

      <button
        type="submit"
        className="w-full bg-green-600 text-white font-semibold py-3 rounded-lg shadow-md hover:bg-green-700 active:bg-green-800 transition"
      >
        Fetch Lead Insights
      </button>
    </form>
  );
}
