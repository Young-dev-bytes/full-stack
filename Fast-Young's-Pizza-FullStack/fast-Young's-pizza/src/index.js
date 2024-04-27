import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom/client";
import "./index.css";

function App() {
  return (
    <div className="container">
      <Header />
      <Menu />
      <Footer />
    </div>
  );
}

function Header() {
  // const style = { color: "red", fontSize: "48px", textTransform: "uppercase" };
  const style = {};
  return (
    <header className="header">
      <h1 style={style}>Fast React Pizza Co.</h1>
    </header>
  );
}

function Menu() {
  // const pizzas = pizzaData;

  const [pizzas, setPizzas] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function retrievePizzas() {
      setIsLoading(true);
      const resOfPizzas = await fetch("http://127.0.0.1:8080/retrievePizzas");
      const dataOfPizzas = await resOfPizzas.json();
      console.log(dataOfPizzas);
      setPizzas(dataOfPizzas);
      setIsLoading(false);
    }

    retrievePizzas();
  }, []);

  // const pizzas = [];
  const pizzasLength = pizzas.length;

  if (isLoading) {
    return <Loader />;
  }

  if (pizzasLength < 1)
    return <h3>Sorry, Pizzas have sold out, please come visit tomorrow :)</h3>;

  return (
    <main className="menu">
      <h2>Our menu</h2>
      {/* {pizzasLength > 0 && (
        <ul className="pizzas">
          {pizzas.map((pizza, index) => (
            <Pizza key={index} pizza={pizza} />
          ))}
        </ul>
      )} */}

      {pizzasLength > 0 ? (
        <>
          <p>
            Authentic Italian cuisine. 6 creative dishes to choose from. All
            from our stone oven, all organic, all delicious.
          </p>
          <ul className="pizzas">
            {pizzas.map((pizza, index) => (
              <Pizza key={index} pizza={pizza} />
            ))}
          </ul>
        </>
      ) : (
        <h3>Sorry, Pizzas have sold out, please come visit tomorrow! 😐</h3>
      )}
    </main>
  );
}

function Pizza({ pizza }) {
  const { photoName, name, ingredients, price, soldOut } = pizza;
  // {
  //   name: "Focaccia",
  //   ingredients: "Bread with italian olive oil and rosemary",
  //   price: 6,
  //   photoName: "pizzas/focaccia.jpg",
  //   soldOut: false,
  // },

  // if (soldOut) return null;
  return (
    // <li className="pizza""sold-out">
    // <li className={soldOut ? "pizza sold-out" : "pizza"}>
    <li className={`pizza ${soldOut ? "sold-out" : ""}`}>
      <img src={photoName} alt={name} />
      <div>
        <h3>{name}</h3>
        <p>{ingredients}</p>
        <span>{soldOut ? "SOLD OUT" : price}</span>
      </div>
    </li>
  );
}

function Footer() {
  const hour = new Date().getHours();
  const openHour = 8;
  const closeHour = 22;
  const isOpen = hour >= openHour && hour <= closeHour;
  console.log(isOpen);
  // return React.createElement("footer", null, "We're currently open!");
  return (
    <footer className="footer">
      {/* {isOpen && (
        <div className="order">
          <p>
            We're currently open until {closeHous}:00. Come visit us or order
            online.
          </p>
          <button className="btn">Order</button>
        </div>
      )} */}

      {isOpen ? (
        <Order closeHour={closeHour} />
      ) : (
        <p>
          We're happy to welcome you between {openHour}:00 and {closeHour}:00 😉
        </p>
      )}
    </footer>
  );
}

function Order({ closeHour }) {
  return (
    <div className="order">
      <p>
        We're currently open until {closeHour}:00. Come visit us or order
        online.
      </p>

      <button className="btn">
        Order<span>{true && " Yes 👍"}</span>
      </button>
    </div>
  );
}

const Loader = () => {
  return <p className="loader">Loading...</p>;
};

// ReactDOM.createRoot(document.getElementById("root")).render(
//   React.createElement(App)
// );

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
