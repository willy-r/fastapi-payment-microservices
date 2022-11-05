import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

import Wrapper from "./Wrapper"

export default function ProductsCreate() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [price, setPrice] = useState(0);
  const [quantity, setQuantity] = useState(0);

  const submitForm = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const r = await toast.promise(
      fetch(`${import.meta.env.VITE_INVENTORY_API_URL}/api/products`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          price,
          quantity_available: quantity,
        }),
      }),
      {
        pending: "Creating product...",
        success: "Product created!",
        error: "Unexpected error occurred, please try again..."
      }
    );
    if (r.ok) {
      navigate("/");
    }
  }

  return (
    <Wrapper>
      <form className="mt-3" onSubmit={submitForm}>
        <div className="form-floating pb-3">
          <input id="name" className="form-control" type="text" placeholder="Name" required
            onChange={(event) => setName(event.target.value)}
          />
          <label htmlFor="name">Name</label>
        </div>

        <div className="form-floating pb-3">
          <input id="price" className="form-control" type="number" min="1" step="any" placeholder="Price" required
            onChange={(event) => setPrice(parseFloat(event.target.value))}
          />
          <label htmlFor="price">Price</label>
        </div>

        <div className="form-floating pb-3">
          <input id="quantity" className="form-control" type="number" placeholder="Quantity available" required
            onChange={(event) => setQuantity(parseInt(event.target.value))}
          />
          <label htmlFor="quantity">Quantity Available</label>
        </div>

        <button type="submit" className="w-100 btn btn-lg btn-secondary">Submit</button>
      </form>
    </Wrapper>
  );
}
