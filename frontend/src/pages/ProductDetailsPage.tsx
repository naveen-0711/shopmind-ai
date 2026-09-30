import {
  ArrowLeft,
  BarChart3,
  BadgeCheck,
  Check,
  ExternalLink,
  ShoppingBag,
  Star,
  Store,
  TrendingDown,
  X,
} from "lucide-react";

interface ProductOffer {
  source: string;
  price: number | null;
  currency: string;
  product_url: string;
  rating: number | null;
  review_count: number | null;
}

export interface ProductDetails {
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

  pros: string[];
  cons: string[];
}

interface ProductDetailsPageProps {
  product: ProductDetails | null;
  onBack: () => void;
}

export default function ProductDetailsPage({
  product,
  onBack,
}: ProductDetailsPageProps) {
  const formatPrice = (
    price: number | null,
    currency = "INR"
  ) => {
    if (price === null) return "Price unavailable";

    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
    }).format(price);
  };

  if (!product) {
    return (
      <main className="details-page">
        <div className="details-container">
          <button className="back-button" onClick={onBack}>
            <ArrowLeft size={18} />
            Back to search
          </button>

          <div className="empty-state">
            <ShoppingBag size={40} />
            <h3>Product not found</h3>
            <p>Select a product from the search results.</p>
          </div>
        </div>
      </main>
    );
  }

  const sortedOffers = [...product.offers].sort(
    (a, b) => (a.price ?? Infinity) - (b.price ?? Infinity)
  );

  return (
    <main className="details-page">
      <div className="details-container">
        <button className="back-button" onClick={onBack}>
          <ArrowLeft size={18} />
          Back to search
        </button>

        {/* ------------------------------------------------ */}
        {/* Product Hero */}
        {/* ------------------------------------------------ */}

        <section className="details-hero">
          <div className="details-image-wrapper">
            {product.image_url ? (
              <img
                src={product.image_url}
                alt={product.title}
                className="details-image"
              />
            ) : (
              <div className="details-image-placeholder">
                <ShoppingBag size={48} />
              </div>
            )}
          </div>

          <div className="details-main">
            <div className="product-source">
              <Store size={14} />
              {product.source}
            </div>

            <h1>{product.title}</h1>

            <div className="details-rating">
              <Star size={18} fill="currentColor" />
              <strong>{product.rating ?? "N/A"}</strong>

              {product.review_count !== null && (
                <span>
                  {product.review_count.toLocaleString("en-IN")}{" "}
                  reviews
                </span>
              )}
            </div>

            <div className="best-price-card">
              <div>
                <span className="eyebrow">Best price</span>

                <strong>
                  {formatPrice(
                    product.price,
                    product.currency
                  )}
                </strong>

                <span>{product.source}</span>
              </div>

              {product.savings !== null &&
                product.savings > 0 && (
                  <div className="details-savings">
                    <TrendingDown size={17} />
                    Save{" "}
                    {formatPrice(
                      product.savings,
                      product.currency
                    )}
                  </div>
                )}
            </div>

            <a
              href={product.product_url}
              target="_blank"
              rel="noreferrer"
              className="primary-product-button"
            >
              View Best Offer
              <ExternalLink size={17} />
            </a>
          </div>
        </section>

        {/* ------------------------------------------------ */}
        {/* Price Intelligence */}
        {/* ------------------------------------------------ */}

        <section className="details-section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">
                Price intelligence
              </span>

              <h2>Is this a good time to buy?</h2>
            </div>

            <BarChart3 size={24} />
          </div>

          <div className="price-stats">
            <div className="price-stat">
              <span>Current price</span>

              <strong>
                {formatPrice(
                  product.price,
                  product.currency
                )}
              </strong>
            </div>

            <div className="price-stat">
              <span>Lowest price</span>

              <strong>
                {formatPrice(
                  product.lowest_price,
                  product.currency
                )}
              </strong>
            </div>

            <div className="price-stat">
              <span>Average price</span>

              <strong>
                {formatPrice(
                  product.average_price,
                  product.currency
                )}
              </strong>
            </div>

            <div className="price-stat">
              <span>Deal status</span>

              <strong>{product.deal_status}</strong>
            </div>
          </div>
        </section>

        {/* ------------------------------------------------ */}
        {/* Offer Comparison */}
        {/* ------------------------------------------------ */}

        <section className="details-section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">
                Compare offers
              </span>

              <h2>Where should you buy?</h2>
            </div>

            <Store size={24} />
          </div>

          <div className="details-offers">
            {sortedOffers.length > 0 ? (
              sortedOffers.map((offer, index) => (
                <div
                  className={`details-offer-row ${
                    index === 0 ? "best-offer" : ""
                  }`}
                  key={`${offer.product_url}-${index}`}
                >
                  <div className="details-offer-retailer">
                    <Store size={18} />

                    <div>
                      <strong>{offer.source}</strong>

                      {index === 0 && (
                        <small className="best-offer-badge">
                          <BadgeCheck size={12} />
                          Best price
                        </small>
                      )}
                    </div>
                  </div>

                  <div className="details-offer-rating">
                    {offer.rating !== null && (
                      <>
                        <Star
                          size={14}
                          fill="currentColor"
                        />
                        {offer.rating}
                      </>
                    )}
                  </div>

                  <strong className="details-offer-price">
                    {formatPrice(
                      offer.price,
                      offer.currency
                    )}
                  </strong>

                  <a
                    href={offer.product_url}
                    target="_blank"
                    rel="noreferrer"
                    className="offer-link"
                  >
                    View
                    <ExternalLink size={14} />
                  </a>
                </div>
              ))
            ) : (
              <div className="empty-state">
                <Store size={32} />
                <h3>No offers available</h3>
                <p>
                  No retailer offers are currently available
                  for this product.
                </p>
              </div>
            )}
          </div>
        </section>

        {/* ------------------------------------------------ */}
        {/* ShopMind Recommendation */}
        {/* ------------------------------------------------ */}

        <section className="details-section why-section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">
                ShopMind analysis
              </span>

              <h2>Why ShopMind recommends this</h2>
            </div>

            {product.recommendation_score !== null && (
              <div className="recommendation-score">
                <strong>
                  {Math.round(
                    product.recommendation_score
                  )}
                </strong>

                <span>/100</span>
              </div>
            )}
          </div>

          <div className="reason-list">
            {product.recommendation_reasons.length > 0 ? (
              product.recommendation_reasons.map(
                (reason, index) => (
                  <div
                    key={`${reason}-${index}`}
                  >
                    <BadgeCheck size={18} />
                    <span>{reason}</span>
                  </div>
                )
              )
            ) : (
              <div>
                <BadgeCheck size={18} />
                <span>
                  Matches the available product signals
                </span>
              </div>
            )}
          </div>
        </section>

        {/* ------------------------------------------------ */}
        {/* Pros & Cons */}
        {/* ------------------------------------------------ */}

        <section className="details-section pros-cons-section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">
                Buying analysis
              </span>

              <h2>Pros & Cons</h2>
            </div>
          </div>

          <div className="pros-cons-grid">
            {/* Pros */}
            <div className="pros-column">
              <div className="pros-cons-heading">
                <Check size={18} />
                <h3>Pros</h3>
              </div>

              {product.pros.length > 0 ? (
                <div className="pros-cons-list">
                  {product.pros.map((pro, index) => (
                    <div
                      className="pros-cons-item"
                      key={`pro-${index}`}
                    >
                      <Check size={16} />
                      <span>{pro}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="pros-cons-empty">
                  No strong positive signals available.
                </div>
              )}
            </div>

            {/* Cons */}
            <div className="cons-column">
              <div className="pros-cons-heading">
                <X size={18} />
                <h3>Cons</h3>
              </div>

              {product.cons.length > 0 ? (
                <div className="pros-cons-list">
                  {product.cons.map((con, index) => (
                    <div
                      className="pros-cons-item"
                      key={`con-${index}`}
                    >
                      <X size={16} />
                      <span>{con}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="pros-cons-empty">
                  No significant negative signals available.
                </div>
              )}
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}