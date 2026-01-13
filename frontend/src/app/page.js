"use client";

import { useState } from "react";

function ScoreBar({ label, value, max = 100 }) {
  const percentage = Math.min((value / max) * 100, 100);

  let color = "bg-red-500";
  if (percentage >= 70) color = "bg-green-500";
  else if (percentage >= 40) color = "bg-yellow-500";

  return (
    <div className="mb-4">
      <div className="flex justify-between mb-1 text-sm font-medium text-slate-700">
        <span>{label}</span>
        <span>{value.toFixed(1)}</span>
      </div>
      <div className="w-full bg-slate-200 rounded-full h-2.5">
        <div
          className={`${color} h-2.5 rounded-full transition-all`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

export default function Home() {
  const [resume, setResume] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!resume || !jobDesc) return;

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDesc);

    try {
      const res = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Request failed");

      const data = await res.json();
      setResult(data);
    } catch {
      setError("Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 flex justify-center px-4 py-12">
      <div className="max-w-3xl w-full bg-white rounded-2xl shadow-xl p-8">

        {/* Header */}
        <h1 className="text-3xl font-bold text-slate-800">
          AI Resume Intelligence
        </h1>
        <p className="text-slate-600 mt-2 mb-8">
          Heuristic AI‑assisted resume and job description analysis.
        </p>

        {/* Inputs */}
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Resume (PDF)
            </label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setResume(e.target.files[0])}
              className="block w-full text-sm text-slate-600
                file:mr-4 file:py-2 file:px-4
                file:rounded-lg file:border-0
                file:bg-slate-100 file:text-slate-700
                hover:file:bg-slate-200"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Job Description
            </label>
            <textarea
              rows={6}
              placeholder="Paste the job description here..."
              value={jobDesc}
              onChange={(e) => setJobDesc(e.target.value)}
              className="w-full rounded-lg border border-slate-300 p-3 text-sm focus:ring-2 focus:ring-slate-400"
            />
          </div>

          <button
            onClick={handleAnalyze}
            disabled={!resume || !jobDesc || loading}
            className={`w-full py-3 rounded-lg font-semibold transition ${
              loading
                ? "bg-slate-400 cursor-not-allowed"
                : "bg-slate-800 hover:bg-slate-900"
            } text-white`}
          >
            {loading ? "Analyzing Resume..." : "Analyze Resume"}
          </button>
        </div>

        {error && (
          <p className="text-red-600 text-sm mt-4">{error}</p>
        )}

        {/* Results */}
        {result && (
          <div className="mt-10 border-t pt-8">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">
              Match Overview
            </h2>

            <div className="mb-6 p-4 rounded-xl bg-slate-100">
              <p className="text-sm text-slate-600">Overall Match Score</p>
              <p className="text-4xl font-bold text-slate-900">
                {result.scores.final_score}%
              </p>
              <p className="text-xs text-slate-500 mt-1">
                Heuristic score — intended for relative comparison, not hiring decisions
              </p>
            </div>

            <ScoreBar
              label="Skill Alignment"
              value={result.scores.skill_score}
              max={40}
            />
            <ScoreBar
              label="Experience Signals"
              value={result.scores.experience_score}
              max={30}
            />
            <ScoreBar
              label="Keyword Coverage"
              value={result.scores.keyword_score}
              max={30}
            />

            <div className="mt-6 text-sm text-slate-600">
              <p>
                This analysis combines rule‑based matching with AI‑assisted heuristics.
                Scores are conservative by design to avoid inflated confidence.
              </p>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
