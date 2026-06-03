import React, { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell, ResponsiveContainer } from "recharts";
import axios from "axios";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884D8", "#82CA9D", "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"];

function App() {
  const [cityData, setCityData] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [sourceData, setSourceData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [city, category, source] = await Promise.all([
          axios.get("http://127.0.0.1:8000/city-wise"),
          axios.get("http://127.0.0.1:8000/category-wise"),
          axios.get("http://127.0.0.1:8000/source-wise"),
        ]);
        setCityData(city.data);
        setCategoryData(category.data);
        setSourceData(source.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", fontSize: "24px", color: "#666" }}>
      Loading Dashboard...
    </div>
  );

  return (
    <div style={{ fontFamily: "Arial, sans-serif", backgroundColor: "#f5f5f5", minHeight: "100vh", padding: "20px" }}>
      <div style={{ maxWidth: "1200px", margin: "0 auto" }}>
        <h1 style={{ textAlign: "center", color: "#333", marginBottom: "10px", fontSize: "28px" }}>
          Business Listings Dashboard
        </h1>
        <p style={{ textAlign: "center", color: "#666", marginBottom: "30px" }}>
          Aggregated data from Sulekha, Justdial & Google Maps
        </p>

        {/* Summary Cards */}
        <div style={{ display: "flex", gap: "20px", marginBottom: "30px", justifyContent: "center" }}>
          <div style={{ background: "#0088FE", color: "white", padding: "20px 40px", borderRadius: "10px", textAlign: "center" }}>
            <div style={{ fontSize: "32px", fontWeight: "bold" }}>250</div>
            <div>Total Listings</div>
          </div>
          <div style={{ background: "#00C49F", color: "white", padding: "20px 40px", borderRadius: "10px", textAlign: "center" }}>
            <div style={{ fontSize: "32px", fontWeight: "bold" }}>{cityData.length}</div>
            <div>Cities Covered</div>
          </div>
          <div style={{ background: "#FFBB28", color: "white", padding: "20px 40px", borderRadius: "10px", textAlign: "center" }}>
            <div style={{ fontSize: "32px", fontWeight: "bold" }}>{categoryData.length}</div>
            <div>Categories</div>
          </div>
          <div style={{ background: "#FF8042", color: "white", padding: "20px 40px", borderRadius: "10px", textAlign: "center" }}>
            <div style={{ fontSize: "32px", fontWeight: "bold" }}>{sourceData.length}</div>
            <div>Sources</div>
          </div>
        </div>

        {/* City Wise Bar Chart */}
        <div style={{ background: "white", borderRadius: "10px", padding: "20px", marginBottom: "20px", boxShadow: "0 2px 4px rgba(0,0,0,0.1)" }}>
          <h2 style={{ color: "#333", marginBottom: "20px" }}>City-wise Business Count</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={cityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="city" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#0088FE" name="Businesses" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Category and Source Charts */}
        <div style={{ display: "flex", gap: "20px" }}>
          <div style={{ flex: 1, background: "white", borderRadius: "10px", padding: "20px", boxShadow: "0 2px 4px rgba(0,0,0,0.1)" }}>
            <h2 style={{ color: "#333", marginBottom: "20px" }}>Category-wise Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={categoryData} dataKey="count" nameKey="category" cx="50%" cy="50%" outerRadius={100} label={({ category, percent }) => `${category} ${(percent * 100).toFixed(0)}%`}>
                  {categoryData.map((entry, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div style={{ flex: 1, background: "white", borderRadius: "10px", padding: "20px", boxShadow: "0 2px 4px rgba(0,0,0,0.1)" }}>
            <h2 style={{ color: "#333", marginBottom: "20px" }}>Source-wise Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={sourceData} dataKey="count" nameKey="source" cx="50%" cy="50%" outerRadius={100} label={({ source, percent }) => `${source} ${(percent * 100).toFixed(0)}%`}>
                  {sourceData.map((entry, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
