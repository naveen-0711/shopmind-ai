import { useState } from "react";
import {
  Search,
  Star,
  ExternalLink,
  TrendingDown,
  BarChart3,
  Sparkles,
  ShoppingBag,
} from "lucide-react";
import "./App.css";

interface Product {
  title: string;
  price: number | null;
  currency: string;
  rating: number | null;
  review_count: number | null;
  image_url: string | null;
  product_url: string;
  source: string;
  lowest_price: number | null;
  average_price: number | null;
  deal_status: string;
}

interface ParsedQuery {
  product_query: string;
  max_price: number | null;
  min_price: number | null;
  min_rating: number | null;
}

interface SearchResponse {
  query: string;
  interpreted_query: ParsedQuery | null;
  products: Product[];
  total: number;
}

const API_URL = "http://127.0.0.1:8000";

function formatPrice(
  price: number | null,
  currency = "INR"
): string {
  if (price === null) {
    return "Price unavailable";
  }

  if (currency === "INR") {
    return `₹${price.toLocaleString("en-IN")}`;
  }

  return `${currency} ${price.toLocaleString()}`;
}

function getDealClass(status: string): string {
  switch (status) {
    case "Great Deal":
      return "deal-great";

    case "Good Deal":
      return "deal-good";

    case "Fair Price":
      return "deal-fair";

    case "Expensive":
      return "deal-expensive";

    default:
      return "deal-unknown";
  }
}

function App() {
  const [query, setQuery] = useState(
    "best Samsung phone under 30000 with rating 4.5+"
  );

  const [products, setProducts] = useState<Product[]>([]);
  const [interpretedQuery, setInterpretedQuery] =
    useState<ParsedQuery | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const searchProducts = async () => {
    if (!query.trim()) {
      setError("Please enter a shopping query.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/api/v1/products/search`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: query.trim(),
            limit: 10,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Search failed with status ${response.status}`
        );
      }

      const data: SearchResponse = await response.json();

      setProducts(data.products);
      setInterpretedQuery(data.interpreted_query);
    } catch (err) {
      console.error(err);

      setError(
        "Unable to search products. Make sure the ShopMind backend is running."
      );

      setProducts([]);
      setInterpretedQuery(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();
    searchProducts();
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-inner">
          <div className="brand">
            <div className="brand-icon">
              <ShoppingBag size={22} />
            </div>

            <div>
              <div className="brand-name">
                ShopMind AI
              </div>

              <div className="brand-tagline">
                Intelligent shopping decisions
              </div>
            </div>
          </div>

          <div className="status">
            <span className="status-dot" />
            AI Shopping Assistant
          </div>
        </div>
      </header>

      {/* Hero */}
      <main>
        <section className="hero">
          <div className="hero-badge">
            <Sparkles size={15} />
            AI-powered product intelligence
          </div>

          <h1>
            Find the right product.
            <br />
            <span>Make the smarter choice.</span>
          </h1>

          <p className="hero-description">
            Describe what you want in natural language.
            ShopMind searches products, compares prices,
            and identifies the best deals.
          </p>

          {/* Search */}
          <form
            className="search-box"
            onSubmit={handleSubmit}
          >
            <Search
              className="search-icon"
              size={23}
            />

            <input
              value={query}
              onChange={(event) =>
                setQuery(event.target.value)
              }
              placeholder="Try: best Samsung phone under ₹30,000..."
            />

            <button
              type="submit"
              disabled={loading}
            >
              {loading ? "Searching..." : "Search"}
            </button>
          </form>

          {/* Examples */}
          <div className="examples">
            <span>Try:</span>

            <button
              onClick={() =>
                setQuery(
                  "best Samsung phone under 30000 with rating 4.5+"
                )
              }
            >
              Samsung phone under ₹30k
            </button>

            <button
              onClick={() =>
                setQuery(
                  "gaming laptop under 70000 with rating 4.5+"
                )
              }
            >
              Gaming laptop under ₹70k
            </button>

            <button
              onClick={() =>
                setQuery(
                  "best wireless headphones under 10000"
                )
              }
            >
              Headphones under ₹10k
            </button>
          </div>
        </section>

        {/* Error */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* Interpreted Query */}
        {interpretedQuery && !loading && (
          <section className="interpretation">
            <div className="interpretation-title">
              <Sparkles size={17} />
              ShopMind understood your request
            </div>

            <div className="query-tags">
              <span className="query-tag">
                {interpretedQuery.product_query}
              </span>

              {interpretedQuery.max_price !== null && (
                <span className="query-tag">
                  Under{" "}
                  {formatPrice(
                    interpretedQuery.max_price
                  )}
                </span>
              )}

              {interpretedQuery.min_price !== null && (
                <span className="query-tag">
                  Above{" "}
                  {formatPrice(
                    interpretedQuery.min_price
                  )}
                </span>
              )}

              {interpretedQuery.min_rating !== null && (
                <span className="query-tag">
                  <Star size={13} fill="currentColor" />
                  {interpretedQuery.min_rating}+
                </span>
              )}
            </div>
          </section>
        )}

        {/* Results */}
        {loading && (
          <section className="results-section">
            <div className="results-heading">
              <div>
                <h2>Finding the best products</h2>
                <p>
                  Searching marketplaces and analyzing
                  prices...
                </p>
              </div>
            </div>

            <div className="loading-grid">
              {[1, 2, 3].map((item) => (
                <div
                  className="skeleton-card"
                  key={item}
                >
                  <div className="skeleton-image" />
                  <div className="skeleton-line large" />
                  <div className="skeleton-line" />
                  <div className="skeleton-line short" />
                </div>
              ))}
            </div>
          </section>
        )}

        {!loading && products.length > 0 && (
          <section className="results-section">
            <div className="results-heading">
              <div>
                <h2>
                  {products.length} products found
                </h2>

                <p>
                  Ranked using price, ratings and
                  product signals
                </p>
              </div>

              <div className="results-badge">
                <BarChart3 size={16} />
                AI ranked
              </div>
            </div>

            <div className="product-grid">
              {products.map((product, index) => (
                <article
                  className="product-card"
                  key={`${product.product_url}-${index}`}
                >
                  {/* Product Image */}
                  <div className="product-image-container">
                    {product.image_url ? (
                      <img
                        src={product.image_url}
                        alt={product.title}
                        className="product-image"
                      />
                    ) : (
                      <div className="image-placeholder">
                        <ShoppingBag size={38} />
                      </div>
                    )}

                    {index === 0 && (
                      <div className="top-pick">
                        <Sparkles size={13} />
                        Top Pick
                      </div>
                    )}
                  </div>

                  {/* Product Information */}
                  <div className="product-content">
                    <div className="product-source">
                      {product.source}
                    </div>

                    <h3>{product.title}</h3>

                    {/* Rating */}
                    <div className="rating-row">
                      {product.rating !== null && (
                        <>
                          <span className="rating">
                            <Star
                              size={15}
                              fill="currentColor"
                            />
                            {product.rating}
                          </span>

                          {product.review_count !==
                            null && (
                            <span className="reviews">
                              (
                              {product.review_count.toLocaleString(
                                "en-IN"
                              )}{" "}
                              reviews)
                            </span>
                          )}
                        </>
                      )}
                    </div>

                    {/* Price */}
                    <div className="price">
                      {formatPrice(
                        product.price,
                        product.currency
                      )}
                    </div>

                    {/* Price Intelligence */}
                    <div className="price-intelligence">
                      <div className="intelligence-row">
                        <span>
                          <TrendingDown size={14} />
                          Lowest
                        </span>

                        <strong>
                          {formatPrice(
                            product.lowest_price,
                            product.currency
                          )}
                        </strong>
                      </div>

                      <div className="intelligence-row">
                        <span>
                          <BarChart3 size={14} />
                          Average
                        </span>

                        <strong>
                          {formatPrice(
                            product.average_price,
                            product.currency
                          )}
                        </strong>
                      </div>
                    </div>

                    {/* Deal */}
                    <div
                      className={`deal-status ${getDealClass(
                        product.deal_status
                      )}`}
                    >
                      {product.deal_status}
                    </div>

                    {/* View Product */}
                    <a
                      href={product.product_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="view-product"
                    >
                      View Product
                      <ExternalLink size={16} />
                    </a>
                  </div>
                </article>
              ))}
            </div>
          </section>
        )}

        {/* Empty state */}
        {!loading &&
          products.length === 0 &&
          !error && (
            <section className="empty-state">
              <div className="empty-icon">
                <Search size={30} />
              </div>

              <h2>What are you looking for?</h2>

              <p>
                Search for phones, laptops,
                headphones, TVs, or any other product.
              </p>
            </section>
          )}
      </main>

      {/* Footer */}
      <footer>
        <span>ShopMind AI</span>
        <span>
          Product intelligence powered by AI
        </span>
      </footer>
    </div>
  );
}

export default App;