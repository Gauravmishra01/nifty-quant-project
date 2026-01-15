"use client";

import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Activity, TrendingUp, AlertTriangle } from "lucide-react";

export default function Home() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const [refreshing, setRefreshing] = useState(false);

  // Function to Trigger Python Script
  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      // 1. Tell Python to update data
      const res = await fetch(
        "https://nifty-quant-project.onrender.com/api/refresh",
        {
          method: "POST",
        }
      );

      if (!res.ok) throw new Error("Refresh failed");

      // 2. If successful, reload the page data
      const newData = await fetch(
        "https://nifty-quant-project.onrender.com/api/data"
      ).then((r) => r.json());
      setData(newData);
      alert("✅ Market Data Updated Successfully!");
    } catch (error) {
      console.error(error);
      alert("❌ Failed to update data. Check console.");
    } finally {
      setRefreshing(false);
    }
  };
  // Fetch Data from Python Backend
  useEffect(() => {
    fetch("https://nifty-quant-project.onrender.com/api/data")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((err) => console.error("Failed to fetch data:", err));
  }, []);

  if (loading)
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white">
        <div className="text-center">
          <h2 className="text-2xl font-bold animate-pulse">
            Connecting to Quant Engine...
          </h2>
          <p className="text-slate-400 mt-2">Ensure server.py is running</p>
        </div>
      </div>
    );

  // Get latest values for the cards
  const latest = data[data.length - 1] || {};

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-8 font-sans">
      {/* Header */}
      <header className="mb-8 flex justify-between items-center border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-4xl font-extrabold bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
            NIFTY 50 Quant Dashboard
          </h1>
          <p className="text-slate-400 mt-1">Live AI-Driven Market Analysis</p>
        </div>

        <div className="flex items-center gap-4">
          {/* NEW REFRESH BUTTON */}
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className={`px-4 py-2 rounded-lg font-bold text-sm transition-all flex items-center gap-2
              ${
                refreshing
                  ? "bg-slate-800 text-slate-500 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-500/20"
              }`}
          >
            {refreshing ? (
              <>
                <span className="animate-spin h-4 w-4 border-2 border-slate-500 border-t-transparent rounded-full"></span>
                UPDATING...
              </>
            ) : (
              "⚡ REFRESH DATA"
            )}
          </button>

          <div className="flex items-center gap-2 bg-slate-900 px-4 py-2 rounded-full border border-slate-700">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            </span>
            <span className="text-green-400 text-sm font-mono font-bold">
              ONLINE
            </span>
          </div>
        </div>
      </header>

      {/* Bento Grid Layout */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* Card 1: Latest Price */}
        <div className="bg-slate-900/50 p-6 rounded-2xl border border-slate-800 hover:border-blue-500/50 transition-all shadow-lg hover:shadow-blue-500/10">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-blue-500/10 rounded-lg">
              <Activity className="text-blue-400" size={24} />
            </div>
            <h3 className="text-slate-400 font-medium">Current Price</h3>
          </div>
          <p className="text-4xl font-bold tracking-tight">
            ₹
            {latest.Close?.toLocaleString("en-IN", {
              maximumFractionDigits: 2,
            })}
          </p>
        </div>

        {/* Card 2: RSI Momentum */}
        <div className="bg-slate-900/50 p-6 rounded-2xl border border-slate-800 hover:border-purple-500/50 transition-all shadow-lg hover:shadow-purple-500/10">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-purple-500/10 rounded-lg">
              <TrendingUp className="text-purple-400" size={24} />
            </div>
            <h3 className="text-slate-400 font-medium">RSI Momentum</h3>
          </div>
          <div className="flex items-end gap-3">
            <p className="text-4xl font-bold tracking-tight">
              {latest.rsi?.toFixed(1)}
            </p>
            <span
              className={`px-2 py-1 rounded text-xs font-bold mb-2 ${
                latest.rsi > 70
                  ? "bg-red-500/20 text-red-400"
                  : latest.rsi < 30
                  ? "bg-green-500/20 text-green-400"
                  : "bg-slate-700 text-slate-300"
              }`}
            >
              {latest.rsi > 70
                ? "OVERBOUGHT"
                : latest.rsi < 30
                ? "OVERSOLD"
                : "NEUTRAL"}
            </span>
          </div>
        </div>

        {/* Card 3: Market Regime */}
        <div className="bg-slate-900/50 p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/50 transition-all shadow-lg hover:shadow-emerald-500/10">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 bg-emerald-500/10 rounded-lg">
              <AlertTriangle className="text-emerald-400" size={24} />
            </div>
            <h3 className="text-slate-400 font-medium">AI Regime</h3>
          </div>
          <p className="text-4xl font-bold tracking-tight">
            Mode {latest.regime}
          </p>
          <p className="text-slate-500 text-sm mt-1">
            {latest.regime === 0
              ? "Low Volatility (Trending)"
              : "High Volatility (Choppy)"}
          </p>
        </div>
      </div>

      {/* Main Chart */}
      <div className="bg-slate-900/50 p-6 rounded-2xl border border-slate-800 shadow-xl h-[500px]">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-semibold text-slate-200">
            Price Trend & EMA Crossover Strategy
          </h3>
          <div className="flex gap-4 text-sm">
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-blue-500"></span>Price
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-emerald-500"></span>Fast
              EMA (9)
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-red-500"></span>Slow EMA
              (21)
            </div>
          </div>
        </div>

        <ResponsiveContainer width="100%" height="85%">
          <LineChart data={data}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#1e293b"
              vertical={false}
            />
            <XAxis dataKey="Datetime" hide />
            <YAxis
              domain={["auto", "auto"]}
              orientation="right"
              tick={{ fill: "#64748b" }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                borderColor: "#334155",
                borderRadius: "12px",
                boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.5)",
              }}
              itemStyle={{ color: "#e2e8f0" }}
              labelStyle={{ color: "#94a3b8", marginBottom: "0.5rem" }}
            />
            <Line
              type="monotone"
              dataKey="Close"
              stroke="#3b82f6"
              strokeWidth={3}
              dot={false}
              activeDot={{ r: 8 }}
            />
            <Line
              type="monotone"
              dataKey="ema_9"
              stroke="#10b981"
              strokeWidth={2}
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="ema_21"
              stroke="#ef4444"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </main>
  );
}
