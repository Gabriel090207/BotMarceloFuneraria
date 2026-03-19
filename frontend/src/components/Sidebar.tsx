import { Link } from "react-router-dom"
import { FiHome, FiShoppingCart, FiBox, FiUsers, FiBriefcase, FiSettings } from "react-icons/fi"
import { useEffect, useState } from "react"
import { doc, getDoc } from "firebase/firestore"
import { auth, db } from "../services/firebase"

import "../styles/sidebar.css"

export default function Sidebar(){

  const [role,setRole] = useState("")
  const [open,setOpen] = useState(false)

  useEffect(()=>{

    async function carregar(){

      if(!auth.currentUser) return

      const ref = doc(db,"users",auth.currentUser.uid)

      const snap = await getDoc(ref)

      if(snap.exists()){
        setRole(snap.data().role)
      }

    }

    function handleToggle(){
      setOpen(prev => !prev)
    }

    window.addEventListener("toggleSidebar", handleToggle)

    carregar()

    return () => {
      window.removeEventListener("toggleSidebar", handleToggle)
    }

  },[])

  return(

    <>
      <div
        className={`sidebar-overlay ${open ? "active" : ""}`}
        onClick={() => setOpen(false)}
      />

      <aside className={`sidebar ${open ? "open" : ""}`}>

        <nav>

          <Link to="/" onClick={()=>setOpen(false)}>
            <FiHome />
            Dashboard
          </Link>

          <Link to="/pedidos" onClick={()=>setOpen(false)}>
            <FiShoppingCart />
            Pedidos
          </Link>

          <Link to="/urnas" onClick={()=>setOpen(false)}>
            <FiBox />
            Urnas
          </Link>

          <Link to="/planos-familiares" onClick={()=>setOpen(false)}>
            <FiUsers />
            Planos Familiares
          </Link>

          <Link to="/planos-empresariais" onClick={()=>setOpen(false)}>
            <FiBriefcase />
            Planos Empresariais
          </Link>

          {role === "admin" && (
            <Link to="/configuracoes" onClick={()=>setOpen(false)}>
              <FiSettings />
              Configurações
            </Link>
          )}

        </nav>

      </aside>
    </>
  )

}