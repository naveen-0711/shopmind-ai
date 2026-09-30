import { useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  useNavigate,
} from "react-router-dom";

import SearchPage, {
  type Product,
  type ProductComparison,
} from "./pages/SearchPage";

import ProductDetailsPage, {
  type ProductDetails,
} from "./pages/ProductDetailsPage";

import "./App.css";

interface ParsedQuery {
  product_query: string;
  max_price: number | null;
  min_price: number | null;
  min_rating: number | null;
}

function AppRoutes() {
  const navigate = useNavigate();

  // ----------------------------------------
  // Search state
  // ----------------------------------------

  const [query, setQuery] = useState(
    "best Samsung phone under 30000 with rating 4.5+"
  );

  const [products, setProducts] = useState<Product[]>(
    []
  );

  const [interpretedQuery, setInterpretedQuery] =
    useState<ParsedQuery | null>(null);

  // ----------------------------------------
  // Comparison / Decision Summary
  // ----------------------------------------

  const [comparison, setComparison] =
    useState<ProductComparison | null>(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [expandedOffers, setExpandedOffers] =
    useState<number | null>(null);

  // ----------------------------------------
  // Selected product
  // ----------------------------------------

  const [selectedProduct, setSelectedProduct] =
    useState<ProductDetails | null>(null);

  // ----------------------------------------
  // Product selection
  // ----------------------------------------

  const handleProductSelect = (product: Product) => {
    setSelectedProduct(product);
    navigate("/product");
  };

  // ----------------------------------------
  // Back to search
  // ----------------------------------------

  const handleBackToSearch = () => {
    navigate("/search");
  };

  return (
    <Routes>
      {/* ---------------------------------- */}
      {/* Search Page */}
      {/* ---------------------------------- */}

      <Route
        path="/"
        element={
          <SearchPage
            query={query}
            setQuery={setQuery}
            products={products}
            setProducts={setProducts}
            interpretedQuery={interpretedQuery}
            setInterpretedQuery={
              setInterpretedQuery
            }
            comparison={comparison}
            setComparison={setComparison}
            loading={loading}
            setLoading={setLoading}
            error={error}
            setError={setError}
            expandedOffers={expandedOffers}
            setExpandedOffers={
              setExpandedOffers
            }
            onProductSelect={
              handleProductSelect
            }
          />
        }
      />

      {/* ---------------------------------- */}
      {/* Explicit Search Page */}
      {/* ---------------------------------- */}

      <Route
        path="/search"
        element={
          <SearchPage
            query={query}
            setQuery={setQuery}
            products={products}
            setProducts={setProducts}
            interpretedQuery={interpretedQuery}
            setInterpretedQuery={
              setInterpretedQuery
            }
            comparison={comparison}
            setComparison={setComparison}
            loading={loading}
            setLoading={setLoading}
            error={error}
            setError={setError}
            expandedOffers={expandedOffers}
            setExpandedOffers={
              setExpandedOffers
            }
            onProductSelect={
              handleProductSelect
            }
          />
        }
      />

      {/* ---------------------------------- */}
      {/* Product Details */}
      {/* ---------------------------------- */}

      <Route
        path="/product"
        element={
          <ProductDetailsPage
            product={selectedProduct}
            onBack={handleBackToSearch}
          />
        }
      />
    </Routes>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}

export default App;