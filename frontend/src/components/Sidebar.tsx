import { Link } from "react-router-dom"
import { FiHome, FiShoppingCart, FiBox, FiUsers, FiBriefcase } from "react-icons/fi"

import "../styles/sidebar.css"

export default function Sidebar(){

  return(

    <aside className="sidebar">

    

      <nav>

        <Link to="/">
          <FiHome />
          Dashboard
        </Link>

        <Link to="/pedidos">
          <FiShoppingCart />
          Pedidos
        </Link>

        <Link to="/urnas">
          <FiBox />
          Urnas
        </Link>

        <Link to="/planos-familiares">
  <FiUsers />
  Planos Familiares
</Link>

<Link to="/planos-empresariais">
  <FiBriefcase />
  Planos Empresariais
</Link>

      </nav>

    </aside>

  )

}