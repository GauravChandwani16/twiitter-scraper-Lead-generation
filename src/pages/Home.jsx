import { useState } from "react";
import Searchbar from "../components/Searchbar";
import Results from "../components/Results";
import Loader from "../components/Loader";
import { analyzeTwitter } from "../services/api";

export default function Home() {
  const [data, setData] = useState(null);        // holds full response including summary
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);      // track error state

  const handleSearch = async (username, company) => {
    setLoading(true);
    setData(null);
    setError(null);
    try {
      const result = await analyzeTwitter(username, company);
      setData(result);
    } catch {
      setError("Failed to fetch data");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4">
      <h1 className="text-center text-4xl font-bold text-gray-900 mb-8">
        Lead Information
      </h1>
      <Searchbar onSearch={handleSearch} />

      {loading && <Loader />}

      {!loading && error && (
        <p className="text-center text-red-600 mt-6">{error}</p>
      )}

      {!loading && !error && data && data.summary ? (
        <Results summary={data.summary} />
      ) : null}

      {!loading && !error && data && !data.summary && (
        <p className="text-center text-gray-600 mt-6">No summary available.</p>
      )}
    </div>
  );
}
