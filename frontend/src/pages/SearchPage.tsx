import React from "react";
import {
  Search,
  Star,
  ExternalLink,
  TrendingDown,
  BarChart3,
  Sparkles,
  ShoppingBag,
  ChevronDown,
  Store,
  BadgeCheck,
  Trophy,
  WalletCards,
  Tag,
} from "lucide-react";

export interface ProductOffer {
  source: string;
  price: number | null;
  currency: string;
  product_url: string;
  rating: number | null;
  review_count: number | null;
}

export interface Product {
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
  offers: ProductOffer[];
  offer_count: number;
  savings: number | null;

  recommendation_score: number | null;
  recommendation_reasons: string[];
  cons: string[];
  pros: string[];
}

interface ParsedQuery {
  product_query: string;
  max_price: number | null;
  min_price: number | null;
  min_rating: number | null;
}

export interface ProductComparison {
  best_overall: Product | null;
  best_value: Product | null;
  cheapest: Product | null;
  best_rated: Product | null;
  best_deal: Product | null;
}

interface SearchResponse {
  query: string;
  interpreted_query: ParsedQuery | null;
  products: Product[];
  total: number;
  comparison: ProductComparison | null;
}

interface SearchPageProps {
  query: string;
  setQuery: React.Dispatch<React.SetStateAction<string>>;

  products: Product[];
  setProducts: React.Dispatch<React.SetStateAction<Product[]>>;

  interpretedQuery: ParsedQuery | null;
  setInterpretedQuery: React.Dispatch<
    React.SetStateAction<ParsedQuery | null>
  >;

  comparison: ProductComparison | null;
  setComparison: React.Dispatch<
    React.SetStateAction<ProductComparison | null>
  >;

  loading: boolean;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;

  error: string;
  setError: React.Dispatch<React.SetStateAction<string>>;

  expandedOffers: number | null;
  setExpandedOffers: React.Dispatch<
    React.SetStateAction<number | null>
  >;

  onProductSelect: (product: Product) => void;
}

const API_BASE_URL = "http://127.0.0.1:8000";

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

export default function SearchPage({
  query,
  setQuery,
  products,
  setProducts,
  interpretedQuery,
  setInterpretedQuery,
  comparison,
  setComparison,
  loading,
  setLoading,
  error,
  setError,
  expandedOffers,
  setExpandedOffers,
  onProductSelect,
}: SearchPageProps) {
  const searchProducts = async (
    searchQuery = query
  ) => {
    if (!searchQuery.trim()) {
      setError("Please enter a shopping query.");
      return;
    }

    setLoading(true);
    setError("");
    setExpandedOffers(null);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/products/search`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: searchQuery.trim(),
            limit: 15,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `Search failed with status ${response.status}`
        );
      }

      const data: SearchResponse =
        await response.json();

      setProducts(data.products);

      setInterpretedQuery(
        data.interpreted_query
      );

      setComparison(
        data.comparison ?? null
      );
    } catch (err) {
      console.error("Search failed:", err);

      setError(
        "Unable to search products. Make sure the ShopMind backend is running."
      );

      setProducts([]);
      setInterpretedQuery(null);
      setComparison(null);
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

  const toggleOffers = (index: number) => {
    setExpandedOffers((current) =>
      current === index ? null : index
    );
  };

  return (
    <div className="app">
      {/* =====================================================
          Header
          ===================================================== */}

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

      {/* =====================================================
          Main
          ===================================================== */}

      <main>
        {/* ===================================================
            Hero
            =================================================== */}

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
              {loading
                ? "Searching..."
                : "Search"}
            </button>
          </form>

          {/* Examples */}

          <div className="examples">
            <span>Try:</span>

            <button
              type="button"
              onClick={() => {
                const example =
                  "best Samsung phone under 30000 with rating 4.5+";

                setQuery(example);
                searchProducts(example);
              }}
            >
              Samsung phone under ₹30k
            </button>

            <button
              type="button"
              onClick={() => {
                const example =
                  "gaming laptop under 70000 with rating 4.5+";

                setQuery(example);
                searchProducts(example);
              }}
            >
              Gaming laptop under ₹70k
            </button>

            <button
              type="button"
              onClick={() => {
                const example =
                  "best wireless headphones under 10000";

                setQuery(example);
                searchProducts(example);
              }}
            >
              Headphones under ₹10k
            </button>
          </div>
        </section>

        {/* ===================================================
            Error
            =================================================== */}

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* ===================================================
            Interpreted Query
            =================================================== */}

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

              {interpretedQuery.max_price !==
                null && (
                <span className="query-tag">
                  Under{" "}
                  {formatPrice(
                    interpretedQuery.max_price
                  )}
                </span>
              )}

              {interpretedQuery.min_price !==
                null && (
                <span className="query-tag">
                  Above{" "}
                  {formatPrice(
                    interpretedQuery.min_price
                  )}
                </span>
              )}

              {interpretedQuery.min_rating !==
                null && (
                <span className="query-tag">
                  <Star
                    size={13}
                    fill="currentColor"
                  />
                  {interpretedQuery.min_rating}+
                </span>
              )}
            </div>
          </section>
        )}

        {/* ===================================================
            Loading
            =================================================== */}

        {loading && (
          <section className="results-section">
            <div className="results-heading">
              <div>
                <h2>
                  Finding the best products
                </h2>

                <p>
                  Searching marketplaces and
                  analyzing prices...
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

        {/* ===================================================
            Results
            =================================================== */}

        {!loading && products.length > 0 && (
          <section className="results-section">
            {/* Results Heading */}

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

            {/* =================================================
                ShopMind Decision Summary
                ================================================= */}

            {comparison && (
              <section className="decision-summary">
                <div className="decision-summary-header">
                  <div>
                    <div className="decision-summary-eyebrow">
                      <Sparkles size={15} />
                      ShopMind intelligence
                    </div>

                    <h2>
                      Decision Summary
                    </h2>

                    <p>
                      We analyzed the available
                      products to highlight the
                      strongest choices for your
                      search.
                    </p>
                  </div>
                </div>

                <div className="decision-grid">
                  {/* =========================================
                      Best Overall
                      ========================================= */}

                  {comparison.best_overall && (
                    <button
                      type="button"
                      className="decision-card decision-card-featured"
                      onClick={() =>
                        onProductSelect(
                          comparison.best_overall!
                        )
                      }
                    >
                      <div className="decision-card-top">
                        <span className="decision-icon">
                          <Trophy size={18} />
                        </span>

                        <span className="decision-label">
                          Best Overall
                        </span>
                      </div>

                      <h3>
                        {
                          comparison.best_overall
                            .title
                        }
                      </h3>

                      <div className="decision-product-price">
                        {formatPrice(
                          comparison.best_overall
                            .price,
                          comparison.best_overall
                            .currency
                        )}
                      </div>

                      {comparison.best_overall
                        .recommendation_score !==
                        null && (
                        <div className="decision-score">
                          <strong>
                            {Math.round(
                              comparison
                                .best_overall
                                .recommendation_score
                            )}
                          </strong>

                          <span>
                            /100 ShopMind score
                          </span>
                        </div>
                      )}

                      <span className="decision-action">
                        View product
                        <ExternalLink size={14} />
                      </span>
                    </button>
                  )}

                  {/* =========================================
                      Best Value
                      ========================================= */}

                  {comparison.best_value && (
                    <button
                      type="button"
                      className="decision-card"
                      onClick={() =>
                        onProductSelect(
                          comparison.best_value!
                        )
                      }
                    >
                      <div className="decision-card-top">
                        <span className="decision-icon">
                          <WalletCards size={18} />
                        </span>

                        <span className="decision-label">
                          Best Value
                        </span>
                      </div>

                      <h3>
                        {
                          comparison.best_value
                            .title
                        }
                      </h3>

                      <div className="decision-product-price">
                        {formatPrice(
                          comparison.best_value
                            .price,
                          comparison.best_value
                            .currency
                        )}
                      </div>

                      {comparison.best_value
                        .rating !== null && (
                        <div className="decision-meta">
                          <Star
                            size={14}
                            fill="currentColor"
                          />

                          {
                            comparison.best_value
                              .rating
                          }

                          {comparison.best_value
                            .review_count !==
                            null && (
                            <span>
                              ·{" "}
                              {comparison.best_value.review_count.toLocaleString(
                                "en-IN"
                              )}{" "}
                              reviews
                            </span>
                          )}
                        </div>
                      )}

                      <span className="decision-action">
                        View product
                        <ExternalLink size={14} />
                      </span>
                    </button>
                  )}

                  {/* =========================================
                      Best Deal
                      ========================================= */}

                  {comparison.best_deal && (
                    <button
                      type="button"
                      className="decision-card"
                      onClick={() =>
                        onProductSelect(
                          comparison.best_deal!
                        )
                      }
                    >
                      <div className="decision-card-top">
                        <span className="decision-icon">
                          <Tag size={18} />
                        </span>

                        <span className="decision-label">
                          Best Deal
                        </span>
                      </div>

                      <h3>
                        {
                          comparison.best_deal
                            .title
                        }
                      </h3>

                      <div className="decision-product-price">
                        {formatPrice(
                          comparison.best_deal
                            .price,
                          comparison.best_deal
                            .currency
                        )}
                      </div>

                      <div
                        className={`decision-deal ${getDealClass(
                          comparison.best_deal
                            .deal_status
                        )}`}
                      >
                        <BadgeCheck size={14} />

                        {
                          comparison.best_deal
                            .deal_status
                        }
                      </div>

                      <span className="decision-action">
                        View product
                        <ExternalLink size={14} />
                      </span>
                    </button>
                  )}

                  {/* =========================================
                      Cheapest
                      ========================================= */}

                  {comparison.cheapest && (
                    <button
                      type="button"
                      className="decision-card"
                      onClick={() =>
                        onProductSelect(
                          comparison.cheapest!
                        )
                      }
                    >
                      <div className="decision-card-top">
                        <span className="decision-icon">
                          <TrendingDown size={18} />
                        </span>

                        <span className="decision-label">
                          Cheapest
                        </span>
                      </div>

                      <h3>
                        {
                          comparison.cheapest
                            .title
                        }
                      </h3>

                      <div className="decision-product-price">
                        {formatPrice(
                          comparison.cheapest
                            .price,
                          comparison.cheapest
                            .currency
                        )}
                      </div>

                      {comparison.cheapest
                        .rating !== null && (
                        <div className="decision-meta">
                          <Star
                            size={14}
                            fill="currentColor"
                          />

                          {
                            comparison.cheapest
                              .rating
                          }
                        </div>
                      )}

                      <span className="decision-action">
                        View product
                        <ExternalLink size={14} />
                      </span>
                    </button>
                  )}

                  {/* =========================================
                      Best Rated
                      ========================================= */}

                  {comparison.best_rated && (
                    <button
                      type="button"
                      className="decision-card"
                      onClick={() =>
                        onProductSelect(
                          comparison.best_rated!
                        )
                      }
                    >
                      <div className="decision-card-top">
                        <span className="decision-icon">
                          <Star
                            size={18}
                            fill="currentColor"
                          />
                        </span>

                        <span className="decision-label">
                          Best Rated
                        </span>
                      </div>

                      <h3>
                        {
                          comparison.best_rated
                            .title
                        }
                      </h3>

                      <div className="decision-rating">
                        <Star
                          size={18}
                          fill="currentColor"
                        />

                        <strong>
                          {
                            comparison.best_rated
                              .rating
                          }
                        </strong>

                        <span>
                          / 5
                        </span>
                      </div>

                      {comparison.best_rated
                        .review_count !==
                        null && (
                        <div className="decision-meta">
                          Based on{" "}
                          {comparison.best_rated.review_count.toLocaleString(
                            "en-IN"
                          )}{" "}
                          reviews
                        </div>
                      )}

                      <span className="decision-action">
                        View product
                        <ExternalLink size={14} />
                      </span>
                    </button>
                  )}
                </div>
              </section>
            )}

            {/* =================================================
                Product Grid
                ================================================= */}

            <div className="product-grid">
              {products.map((product, index) => {
                const isExpanded =
                  expandedOffers === index;

                const sortedOffers = [
                  ...product.offers,
                ].sort(
                  (a, b) =>
                    (a.price ?? Infinity) -
                    (b.price ?? Infinity)
                );

                return (
                  <article
                    className={`product-card ${
                      isExpanded
                        ? "product-card-expanded"
                        : ""
                    }`}
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
                        <Store size={13} />
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

                      {/* Savings */}

                      {product.savings !== null &&
                        product.savings > 0 && (
                          <div className="savings-banner">
                            <TrendingDown size={15} />

                            Save{" "}
                            {formatPrice(
                              product.savings,
                              product.currency
                            )}{" "}
                            compared with the
                            highest offer
                          </div>
                        )}

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
                        <BadgeCheck size={14} />
                        {product.deal_status}
                      </div>

                      {/* Recommendation */}

                      {product.recommendation_score !==
                        null && (
                        <div className="product-recommendation">
                          <div className="product-recommendation-header">
                            <span>
                              <Sparkles size={13} />
                              ShopMind Score
                            </span>

                            <strong>
                              {Math.round(
                                product.recommendation_score
                              )}
                              /100
                            </strong>
                          </div>

                          {product
                            .recommendation_reasons
                            .length > 0 && (
                            <ul>
                              {product.recommendation_reasons
                                .slice(0, 2)
                                .map(
                                  (
                                    reason,
                                    reasonIndex
                                  ) => (
                                    <li
                                      key={`${reason}-${reasonIndex}`}
                                    >
                                      <BadgeCheck
                                        size={13}
                                      />

                                      <span>
                                        {reason}
                                      </span>
                                    </li>
                                  )
                                )}
                            </ul>
                          )}
                        </div>
                      )}

                      {/* Offer Comparison */}

                      {product.offer_count > 0 && (
                        <div className="offer-section">
                          <button
                            type="button"
                            className={`offer-toggle ${
                              isExpanded
                                ? "offer-toggle-active"
                                : ""
                            }`}
                            onClick={() =>
                              toggleOffers(index)
                            }
                            aria-expanded={
                              isExpanded
                            }
                          >
                            <span className="offer-toggle-left">
                              <Store size={16} />

                              <span>
                                {product.offer_count}{" "}
                                {product.offer_count ===
                                1
                                  ? "offer"
                                  : "offers"}{" "}
                                available
                              </span>
                            </span>

                            <span className="offer-toggle-right">
                              {isExpanded
                                ? "Hide"
                                : "Compare"}

                              <ChevronDown
                                size={16}
                                className={
                                  isExpanded
                                    ? "chevron-up"
                                    : ""
                                }
                              />
                            </span>
                          </button>

                          {isExpanded && (
                            <div className="offer-list">
                              {sortedOffers.map(
                                (
                                  offer,
                                  offerIndex
                                ) => {
                                  const isBestOffer =
                                    offerIndex ===
                                      0 &&
                                    offer.price !==
                                      null;

                                  return (
                                    <div
                                      className={`offer-row ${
                                        isBestOffer
                                          ? "best-offer"
                                          : ""
                                      }`}
                                      key={`${offer.source}-${offer.product_url}-${offerIndex}`}
                                    >
                                      <div className="offer-info">
                                        <div className="offer-store">
                                          {isBestOffer && (
                                            <span className="best-offer-badge">
                                              Best price
                                            </span>
                                          )}

                                          <strong>
                                            {
                                              offer.source
                                            }
                                          </strong>
                                        </div>

                                        {offer.rating !==
                                          null && (
                                          <span className="offer-rating">
                                            <Star
                                              size={12}
                                              fill="currentColor"
                                            />

                                            {
                                              offer.rating
                                            }

                                            {offer.review_count !==
                                              null &&
                                              ` · ${offer.review_count.toLocaleString(
                                                "en-IN"
                                              )} reviews`}
                                          </span>
                                        )}
                                      </div>

                                      <div className="offer-price">
                                        {formatPrice(
                                          offer.price,
                                          offer.currency
                                        )}
                                      </div>

                                      <a
                                        href={
                                          offer.product_url
                                        }
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="offer-link"
                                      >
                                        View

                                        <ExternalLink
                                          size={14}
                                        />
                                      </a>
                                    </div>
                                  );
                                }
                              )}
                            </div>
                          )}
                        </div>
                      )}

                      {/* Open Product Details */}

                      <button
                        type="button"
                        className="view-product"
                        onClick={() =>
                          onProductSelect(
                            product
                          )
                        }
                      >
                        View Product
                        <ExternalLink size={16} />
                      </button>
                    </div>
                  </article>
                );
              })}
            </div>
          </section>
        )}

        {/* ===================================================
            Empty State
            =================================================== */}

        {!loading &&
          products.length === 0 &&
          !error && (
            <section className="empty-state">
              <div className="empty-icon">
                <Search size={30} />
              </div>

              <h2>
                What are you looking for?
              </h2>

              <p>
                Search for phones, laptops,
                headphones, TVs, or any other
                product.
              </p>
            </section>
          )}
      </main>

      {/* =====================================================
          Footer
          ===================================================== */}

      <footer>
        <span>ShopMind AI</span>

        <span>
          Product intelligence powered by AI
        </span>
      </footer>
    </div>
  );
}