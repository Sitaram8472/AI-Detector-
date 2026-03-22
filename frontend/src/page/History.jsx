import React from "react";

const History = () => {
  const scans = [
    {
      id: 1,
      type: "Image",
      date: "2026-03-20",
      result: "98% Human",
      status: "Safe",
    },
    {
      id: 2,
      type: "Text",
      date: "2026-03-19",
      result: "85% AI (GPT-4)",
      status: "Flagged",
    },
    {
      id: 3,
      type: "Video",
      date: "2026-03-18",
      result: "92% Deepfake",
      status: "Danger",
    },
  ];

  return (
    <div className="max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Scan History</h1>
      <div className="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b border-gray-100">
            <tr>
              <th className="p-4 font-semibold text-gray-600">Type</th>
              <th className="p-4 font-semibold text-gray-600">Date</th>
              <th className="p-4 font-semibold text-gray-600">Result</th>
              <th className="p-4 font-semibold text-gray-600">Status</th>
            </tr>
          </thead>
          <tbody>
            {scans.map((scan) => (
              <tr
                key={scan.id}
                className="border-b border-gray-50 hover:bg-gray-50 transition"
              >
                <td className="p-4 font-medium">{scan.type}</td>
                <td className="p-4 text-gray-500">{scan.date}</td>
                <td className="p-4 text-gray-700">{scan.result}</td>
                <td className="p-4">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-bold ${
                      scan.status === "Safe"
                        ? "bg-green-100 text-green-700"
                        : "bg-red-100 text-red-700"
                    }`}
                  >
                    {scan.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default History;
