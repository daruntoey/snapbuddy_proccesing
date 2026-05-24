"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function UploadPage() {
  const [description, setDescription] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Handle upload and analysis
    console.log("Analyzing...", { description, files });
    router.push("/results");
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="container mx-auto px-4 max-w-3xl">
        <h1 className="text-4xl font-bold mb-8 text-center">Describe Your Vision</h1>
        
        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-lg p-8">
          <div className="mb-6">
            <label className="block text-lg font-semibold mb-2">
              What aesthetic are you looking for?
            </label>
            <textarea
              className="w-full p-4 border rounded-lg h-32"
              placeholder="E.g., Cozy Korean cafe aesthetic with warm natural lighting and minimal poses..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div className="mb-6">
            <label className="block text-lg font-semibold mb-2">
              Upload Reference Images
            </label>
            <div className="border-2 border-dashed rounded-lg p-12 text-center">
              <input
                type="file"
                multiple
                accept="image/*"
                onChange={(e) => setFiles(Array.from(e.target.files || []))}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <div className="text-4xl mb-2">📷</div>
                <p className="text-gray-600">Click to upload images</p>
                <p className="text-sm text-gray-400">Up to 5 images</p>
              </label>
              {files.length > 0 && (
                <p className="mt-4 text-sm text-gray-600">{files.length} files selected</p>
              )}
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            Find My Photographers
          </button>
        </form>
      </div>
    </main>
  );
}
