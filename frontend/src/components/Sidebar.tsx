import { Link } from "react-router-dom"
import { FiHome, FiShoppingCart, FiBox, FiUsers, FiBriefcase, FiSettings } from "react-icons/fi"
import { useEffect, useState } from "react"
import { doc, getDoc } from "firebase/firestore"
import { auth, db } from "../services/firebase"

import "../styles/sidebar.css"

export default function Sidebar(){

  const [role,setRole] = useState("")


  useEffect(()=>{

  async function carregar(){

    if(!auth.currentUser) return

    const ref = doc(db,"users",auth.currentUser.uid)

    const snap = await getDoc(ref)

    if(snap.exists()){

      setRole(snap.data().role)

    }

  }

  carregar()

},[])

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

       {role === "admin" && (

  <Link to="/configuracoes">
    <FiSettings />
    Configurações
  </Link>

)}

      </nav>

    </aside>

  )

}