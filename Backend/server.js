const express = require("express");
const cors = require("cors");

const PORT = 5000;
const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Test route
app.get("/", (req, res) => {
  res.send("Backend is running ");
});

//  testapi route
app.get("/api/data", (req, res) => {
  res.json({ message: "Hello from backend!" });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});