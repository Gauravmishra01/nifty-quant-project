"use client";

import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import {
  Activity,
  TrendingUp,
  AlertTriangle,
  RefreshCw,
  Server,
} from "lucide-react";

export default function Home() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [regime, setRegime] = useState("Unknown");

  // YOUR BACKEND URL
  // We use the production URL you confirmed earlier
  const API_URL = "https://nifty-quant-project.onrender.com/api/data";
  const REFRESH_URL = "https://nifty-quant-project.onrender.com/api/refresh";

  const fetchData = async () => {
    setLoading(true);
    try {
      console.log("Fetching data from:", API_URL);
      const res = await fetch(API_URL);
      const jsonData = await res.json();

      // SAFETY CHECK: Ensure we actually got a List (Array) of data
      if (Array.isArray(jsonData) && jsonData.length > 0) {
        setData(jsonData);

        // Detect Regime from the last data point
        const lastPoint = jsonData[jsonData.length - 1];
        if (lastPoint.regime !== undefined) {
          // Map numeric regime to text if needed, or just use the value
          setRegime(
            lastPoint.regime === 0
              ? "Bull/Bear Trend"
              : lastPoint.regime === 1
                ? "High Volatility"
                : "Choppy/Sideways",
          );
        }
      } else {
        console.warn("Received non-array data:", jsonData);
        setData([]); // Set to empty array to prevent crash
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      setData([]); // Set to empty array on error
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    try {
      await fetch(REFRESH_URL, { method: "POST" });
      // After triggering refresh, fetch the new data
      setTimeout(fetchData, 4000); // Wait 4s for backend to finish processing
    } catch (error) {
      console.error("Refresh failed:", error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Calculate KPIs safely
  const lastPrice =
    data.length > 0 ? data[data.length - 1].close.toFixed(2) : "---";
  const rsi = data.length > 0 ? data[data.length - 1].rsi.toFixed(1) : "---";
  const signal =
    data.length > 0
      ? data[data.length - 1].signal === 1
        ? "BUY"
        : "WAIT"
      : "WAIT";

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 font-sans">
      {/* HEADER */}
      <header className="flex justify-between items-center mb-8 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
            Nifty 50 Quant Dashboard
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            AI-Driven Regime Detection & Strategy
          </p>
        </div>
        <button
          onClick={handleRefresh}
          disabled={loading}
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg transition-all disabled:opacity-50"
        >
          {loading ? (
            <RefreshCw className="animate-spin w-4 h-4" />
          ) : (
            <Server className="w-4 h-4" />
          )}
          {loading ? "Syncing..." : "Refresh Data"}
        </button>
      </header>

      {/* KPI CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center gap-3 mb-2">
            <Activity className="text-blue-400 w-5 h-5" />
            <span className="text-slate-400 text-sm">Nifty Spot Price</span>
          </div>
          <div className="text-2xl font-bold">{lastPrice}</div>
        </div>

        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center gap-3 mb-2">
            <TrendingUp className="text-green-400 w-5 h-5" />
            <span className="text-slate-400 text-sm">RSI (14)</span>
          </div>
          <div
            className={`text-2xl font-bold ${Number(rsi) > 70 ? "text-red-400" : Number(rsi) < 30 ? "text-green-400" : "text-slate-200"}`}
          >
            {rsi}
          </div>
        </div>

        <div className="bg-slate-900 p-4 rounded-xl border border-slate-800">
          <div className="flex items-center gap-3 mb-2">
            <AlertTriangle className="text-yellow-400 w-5 h-5" />
            <span className="text-slate-400 text-sm">Market Regime (AI)</span>
          </div>
          <div className="text-xl font-bold text-yellow-300">{regime}</div>
        </div>

        <div
          className={`p-4 rounded-xl border ${signal === "BUY" ? "bg-green-900/30 border-green-800" : "bg-slate-900 border-slate-800"}`}
        >
          <div className="flex items-center gap-3 mb-2">
            <Activity className="text-purple-400 w-5 h-5" />
            <span className="text-slate-400 text-sm">Live Signal</span>
          </div>
          <div
            className={`text-2xl font-bold ${signal === "BUY" ? "text-green-400" : "text-slate-500"}`}
          >
            {signal}
          </div>
        </div>
      </div>

      {/* MAIN CHART SECTION */}
      <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-xl">
        <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-blue-400" />
          Price Trend & EMA Crossover Strategy
        </h2>

        {/* --- SAFETY GUARD: PREVENTS CRASH --- */}
        <div className="h-[400px] w-full flex items-center justify-center">
          {data && Array.isArray(data) && data.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#334155"
                  opacity={0.5}
                />
                <XAxis
                  dataKey="timestamp"
                  stroke="#94a3b8"
                  fontSize={12}
                  tickFormatter={(str) => {
                    const d = new Date(str);
                    return d.toLocaleDateString() ===
                      new Date().toLocaleDateString()
                      ? d.toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })
                      : d.toLocaleDateString(undefined, {
                          month: "short",
                          day: "numeric",
                        });
                  }}
                  minTickGap={30}
                />
                <YAxis
                  stroke="#94a3b8"
                  domain={["auto", "auto"]}
                  fontSize={12}
                  tickFormatter={(val) => `₹${val}`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#0f172a",
                    borderColor: "#334155",
                    color: "#f1f5f9",
                  }}
                  itemStyle={{ color: "#e2e8f0" }}
                  labelStyle={{ color: "#94a3b8", marginBottom: "0.5rem" }}
                  formatter={(value: any) => [
                    typeof value === "number" ? value.toFixed(2) : value,
                  ]}
                  labelFormatter={(label) => new Date(label).toLocaleString()}
                />
                <Legend verticalAlign="top" height={36} />
                <Line
                  type="monotone"
                  dataKey="close"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  dot={false}
                  name="Price"
                  activeDot={{ r: 6 }}
                />
                <Line
                  type="monotone"
                  dataKey="ema_9"
                  stroke="#10b981"
                  strokeWidth={1.5}
                  dot={false}
                  name="Fast EMA (9)"
                />
                <Line
                  type="monotone"
                  dataKey="ema_21"
                  stroke="#ef4444"
                  strokeWidth={1.5}
                  dot={false}
                  name="Slow EMA (21)"
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-center py-10">
              <div className="inline-block p-4 rounded-full bg-slate-800 mb-4 animate-pulse">
                <Server className="w-8 h-8 text-blue-400" />
              </div>
              <h3 className="text-xl font-medium text-slate-200">
                Connecting to Cloud Server...
              </h3>
              <p className="text-slate-400 mt-2 max-w-md mx-auto">
                The Render backend is waking up (Free Tier). This usually takes
                30-50 seconds.
                <br />
                <span className="text-yellow-400 text-sm mt-2 block">
                  Don't worry, the chart will appear automatically!
                </span>
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
