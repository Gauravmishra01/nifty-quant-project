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

  // --- CONFIGURATION ---
  // ✅ LIVE SERVER (Use this for your Final Submission)
  const API_URL = "https://nifty-quant-project.onrender.com/api/data";
  const REFRESH_URL = "https://nifty-quant-project.onrender.com/api/refresh";

  // 🛠️ LOCALHOST (Uncomment these only if testing locally)
  // const API_URL = "http://127.0.0.1:5000/api/data";
  // const REFRESH_URL = "http://127.0.0.1:5000/refresh";

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
        // Check for 'regime' (lowercase) or 'Regime' (uppercase)
        const regimeVal =
          lastPoint.regime !== undefined ? lastPoint.regime : lastPoint.Regime;

        if (regimeVal !== undefined) {
          setRegime(
            regimeVal === 0
              ? "Bull/Bear Trend"
              : regimeVal === 1
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
      setTimeout(fetchData, 4000);
    } catch (error) {
      console.error("Refresh failed:", error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // --- ROBUST KPI CALCULATION ---
  const lastPoint = data.length > 0 ? data[data.length - 1] : null;

  const rawPrice = lastPoint ? (lastPoint.close ?? lastPoint.Close) : null;
  const lastPrice =
    rawPrice !== undefined && rawPrice !== null
      ? Number(rawPrice).toFixed(2)
      : "---";

  const rawRsi = lastPoint ? (lastPoint.rsi ?? lastPoint.RSI) : null;
  const rsi =
    rawRsi !== undefined && rawRsi !== null ? Number(rawRsi).toFixed(1) : "---";

  const rawSignal = lastPoint ? (lastPoint.signal ?? lastPoint.Signal) : null;
  const signal = rawSignal === 1 ? "BUY" : "WAIT";

  // --- CHART FIX: REMOVE ZEROS ---
  const chartData = data.filter((item) => {
    const price = item.close ?? item.Close ?? 0;
    const ema21 = item.ema_21 ?? item.EMA_21 ?? 0;
    // Only show valid data > 1 to fix zoom
    return price > 1 && ema21 > 1;
  });

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

        {/* --- FIXED CHART CONTAINER --- */}
        {/* We use explicit style={{ width: '100%', height: 400 }} to satisfy Recharts requirements */}
        <div
          style={{ width: "100%", height: 400 }}
          className="flex items-center justify-center"
        >
          {data && Array.isArray(data) && data.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
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
                  domain={["dataMin", "dataMax"]}
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
                  dataKey={data[0]?.close !== undefined ? "close" : "Close"}
                  stroke="#3b82f6"
                  strokeWidth={2}
                  dot={false}
                  name="Price"
                  activeDot={{ r: 6 }}
                />
                <Line
                  type="monotone"
                  dataKey={data[0]?.ema_9 !== undefined ? "ema_9" : "EMA_9"}
                  stroke="#10b981"
                  strokeWidth={1.5}
                  dot={false}
                  name="Fast EMA (9)"
                />
                <Line
                  type="monotone"
                  dataKey={data[0]?.ema_21 !== undefined ? "ema_21" : "EMA_21"}
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
