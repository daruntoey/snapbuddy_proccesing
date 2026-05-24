"use client";

export default function ResultsPage() {
  const mockMatches = [
    {
      id: 1,
      name: "Studio Seoul",
      score: 95,
      image: "/placeholder.jpg",
      rate: "$150/hr",
      rating: 4.9,
      location: "Seoul",
    },
  ];

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="container mx-auto px-4 max-w-6xl">
        <h1 className="text-4xl font-bold mb-8 text-center">Your Perfect Matches</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockMatches.map((match) => (
            <div key={match.id} className="bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="h-48 bg-gray-200"></div>
              <div className="p-6">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-bold">{match.name}</h3>
                  <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
                    {match.score}% Match
                  </span>
                </div>
                <p className="text-gray-600 mb-2">{match.location}</p>
                <p className="text-gray-800 font-semibold mb-4">{match.rate}</p>
                <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700">
                  View Profile
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
