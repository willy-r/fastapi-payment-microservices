import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";

import Wrapper from "./Wrapper";

type Product = {
  id: string;
  name: string;
  price: number;
  quantity_available: number;
}

export default function Products() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    (async () => {
      const r = await fetch(`${import.meta.env.VITE_INVENTORY_API_URL}/api/products`);
      const data = await r.json();
      setProducts(data);
    })();
  }, []);

  const deleteProduct = async (id: string) => {
    const deleteConfirmation = window.confirm(`Are you sure to delete the product ${id}?`)

    if (deleteConfirmation) {
      const r = await toast.promise(
        fetch(`${import.meta.env.VITE_INVENTORY_API_URL}/api/products/${id}`, {
          method: "DELETE",
        }),
        {
          pending: "Deleting product...",
          success: `Product ${id} deleted!`,
          error: "Unexpected error occurred, please try again..."
        }
      );
      if (r.ok) {
        setProducts(products.filter((product: Product) => product.id !== id));
      }
    }
  }

  return (
    <Wrapper>
      <div className="pt-3 pb-2 mb-3 border-bottom">
        <Link to={"/create-product"} className="btn btn-sm btn-outline-secondary" role="button">
          Create
        </Link>
      </div>

      <div className="table-responsive">
        <table className="table table-striped table-sm">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">Price</th>
              <th scope="col">Quantity</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product: Product) => {
              return (
                <tr key={product.id}>
                  <td>{product.id}</td>
                  <td>{product.name}</td>
                  <td>{product.price}</td>
                  <td>{product.quantity_available}</td>
                  <td>
                    <a href="#" role="button" className="btn btn-sm btn-outline-secondary"
                      onClick={(event) => deleteProduct(product.id)}
                    >
                      Delete
                    </a>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Wrapper>
  );
}
