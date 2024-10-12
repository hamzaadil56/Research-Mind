import React, { useState } from "react";
import Navbar from "./Navbar";

const ResearchAIDashboard: React.FC = () => {
  const [query, setQuery] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = async () => {
    if (query.trim() === "") {
      alert("Please enter a project description.");
      return;
    }

    setIsLoading(true); // Start the loader

    try {
      const res = await fetch("http://localhost:8000/research-project", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      if (res.ok) {
        const data = await res.json();
        setResponse(data.response);
      } else {
        console.error("Failed to fetch response from the server.");
      }
    } catch (error) {
      console.error("Error while calling the API:", error);
    } finally {
      setIsLoading(false); // Stop the loader after the request completes
    }
  };

  return (
    <div
      className="relative flex size-full min-h-screen flex-col bg-[#141414] dark group/design-root overflow-x-hidden"
      style={{ fontFamily: 'Inter, "Noto Sans", sans-serif' }}
    >
      <div className="layout-container flex h-full grow flex-col">
        <Navbar />
        <div className="px-40 flex flex-1 justify-center py-5">
          <div className="layout-content-container flex flex-col w-[512px] max-w-[512px] py-5 max-w-[960px] flex-1">
            <h1 className="text-[#FFFFFF] tracking-light text-[32px] font-bold leading-tight px-4 text-center pb-3 pt-6">
              Get help with your research
            </h1>
            <p className="text-[#FFFFFF] text-base font-normal leading-normal pb-3 pt-1 px-4 text-center">
              Describe your project and get feedback from Research Mind
            </p>
            <div className="flex items-center gap-4 px-4 py-3">
              <label className="flex flex-col w-full">
                <input
                  className="form-input w-full resize-none overflow-hidden rounded-xl text-[#FFFFFF] focus:outline-0 focus:ring-0 border border-[#2F3B46] bg-[#1B2127] focus:border-[#2F3B46]  placeholder:text-[#9BACBB] px-4 py-2 text-base font-normal leading-normal"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Describe your project..."
                />
              </label>
              <div className="flex justify-center px-4 py-3">
                <button
                  onClick={handleSubmit}
                  disabled={isLoading}
                  className={`flex cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#27313A] text-[#FFFFFF] text-sm font-bold leading-normal tracking-[0.015em] ${
                    isLoading ? "opacity-50 cursor-not-allowed" : ""
                  }`}
                >
                  {isLoading ? (
                    <svg
                      className="animate-spin h-5 w-5 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8v8H4z"
                      ></path>
                    </svg>
                  ) : (
                    <span className="truncate">Submit</span>
                  )}
                </button>
              </div>
            </div>
            {response && (
              <div className="mt-4 px-4 py-3 bg-[#1B2127] rounded-xl text-[#FFFFFF]">
                <p>{response}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResearchAIDashboard;
