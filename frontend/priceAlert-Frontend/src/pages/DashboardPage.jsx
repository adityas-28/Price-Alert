import { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { useAuth } from "../contexts/AuthContext";
import { productAPI, alertAPI, extractASINFromURL } from "../services/api";
import { useNavigate } from "react-router-dom";

// Register Chart.js components - wrap in try-catch to handle errors
try {
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );
  console.log("Chart.js registered successfully");
} catch (error) {
  console.error("Error registering Chart.js:", error);
}

const DashboardPage = () => {
  const [url, setUrl] = useState("");
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [thresholdPrice, setThresholdPrice] = useState("");
  const [alertSuccess, setAlertSuccess] = useState("");
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      navigate("/login");
    }
  }, [user, navigate]);

  const handleScrape = async () => {
    if (!url.trim()) {
      setError("Please enter a valid Tanishq product URL");
      return;
    }

    setLoading(true);
    setError("");
    setProduct(null);

    try {
      // Extract ASIN from URL
      const asin = extractASINFromURL(url);
      if (!asin) {
        setError(
          "Could not extract product identifier from URL. Please check the URL format."
        );
        setLoading(false);
        return;
      }

      // First scrape the product to ensure it's in the database
      const scrapeResult = await productAPI.scrapeProduct(asin);
      if (scrapeResult.status === "error") {
        setError(scrapeResult.message || "Failed to scrape product");
        setLoading(false);
        return;
      }

      // Then fetch the product with price history
      const productData = await productAPI.getProduct(asin);
      setProduct(productData);
    } catch (err) {
      setError(
        err.response?.data?.detail || "An error occurred. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSetAlert = async () => {
    if (!product || !thresholdPrice) {
      setError("Please enter a threshold price");
      return;
    }

    const price = parseFloat(thresholdPrice);
    if (isNaN(price) || price <= 0) {
      setError("Please enter a valid threshold price");
      return;
    }

    try {
      await alertAPI.addAlert({
        asin: product.asin,
        email: user.email,
        threshold_price: price,
      });
      setAlertSuccess(
        `Alert set successfully! You'll be notified when price drops below ₹${price}`
      );
      setThresholdPrice("");
      setTimeout(() => setAlertSuccess(""), 5000);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to set alert");
    }
  };

  const prepareChartData = () => {
    if (!product || !product.prices || product.prices.length === 0) {
      return null;
    }

    const prices = product.prices.map((p) => parseFloat(p.price));
    const labels = product.prices.map((p, index) => {
      if (p.timestamp) {
        const date = new Date(p.timestamp);
        return date.toLocaleDateString("en-IN", {
          month: "short",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        });
      }
      return `Point ${index + 1}`;
    });

    return {
      labels,
      datasets: [
        {
          label: "Price (₹)",
          data: prices,
          borderColor: "rgb(79, 70, 229)",
          backgroundColor: "rgba(79, 70, 229, 0.1)",
          tension: 0.4,
          fill: true,
        },
      ],
    };
  };

  const chartData = prepareChartData();
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: product ? `${product.name} - Price History` : "Price History",
        font: {
          size: 18,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: false,
        ticks: {
          callback: function (value) {
            return "₹" + value.toLocaleString("en-IN");
          },
        },
      },
    },
  };

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-2xl font-bold text-indigo-600">Price Alert</h1>
            <div className="flex items-center gap-4">
              <span className="text-gray-700">Welcome, {user.email}</span>
              <button
                onClick={logout}
                className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-xl p-6 mb-6">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800">
            Enter Tanishq Product URL
          </h2>
          <div className="flex gap-4">
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://www.tanishq.co.in/product/..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
            <button
              onClick={handleScrape}
              disabled={loading}
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? "Loading..." : "Fetch Product"}
            </button>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {alertSuccess && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-6">
            {alertSuccess}
          </div>
        )}

        {product && (
          <>
            <div className="bg-white rounded-lg shadow-xl p-6 mb-6">
              <h2 className="text-2xl font-semibold mb-4 text-gray-800">
                {product.name}
              </h2>
              {product.prices && product.prices.length > 0 && (
                <div className="mb-4">
                  <p className="text-lg text-gray-600">
                    Current Price:{" "}
                    <span className="font-bold text-indigo-600">
                      ₹
                      {parseFloat(
                        product.prices[product.prices.length - 1].price
                      ).toLocaleString("en-IN")}
                    </span>
                  </p>
                  <p className="text-sm text-gray-500">
                    Last Updated:{" "}
                    {new Date(product.last_updated).toLocaleString("en-IN")}
                  </p>
                </div>
              )}
              {chartData && (
                <div className="mt-6">
                  <Line data={chartData} options={chartOptions} />
                </div>
              )}
            </div>

            <div className="bg-white rounded-lg shadow-xl p-6">
              <h2 className="text-2xl font-semibold mb-4 text-gray-800">
                Set Price Alert
              </h2>
              <p className="text-gray-600 mb-4">
                Get notified when the price drops below your threshold
              </p>
              <div className="flex gap-4">
                <input
                  type="number"
                  value={thresholdPrice}
                  onChange={(e) => setThresholdPrice(e.target.value)}
                  placeholder="Enter threshold price (₹)"
                  min="0"
                  step="0.01"
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                />
                <button
                  onClick={handleSetAlert}
                  className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors"
                >
                  Set Alert
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
