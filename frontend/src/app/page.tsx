import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            SnapBuddy
          </h1>
          <p className="text-2xl text-gray-700 mb-8">
            Find Your Perfect Photographer with AI
          </p>
          <p className="text-lg text-gray-600 mb-12">
            Upload your aesthetic inspiration, describe your vision, and let our AI match you with photographers who truly get your vibe.
          </p>
          
          <div className="flex gap-4 justify-center">
            <Link
              href="/upload"
              className="px-8 py-4 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
            >
              Start Matching
            </Link>
            <Link
              href="/photographers"
              className="px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold border-2 border-blue-600 hover:bg-blue-50 transition"
            >
              Browse Photographers
            </Link>
          </div>

          <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <div className="text-4xl mb-4">📸</div>
              <h3 className="text-xl font-bold mb-2">Upload Inspiration</h3>
              <p className="text-gray-600">Share reference images that capture your desired aesthetic</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-bold mb-2">AI Matching</h3>
              <p className="text-gray-600">Our AI analyzes your style and matches you with perfect photographers</p>
            </div>
            
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <div className="text-4xl mb-4">✨</div>
              <h3 className="text-xl font-bold mb-2">Book Your Shoot</h3>
              <p className="text-gray-600">Connect with your match and create stunning photos together</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
