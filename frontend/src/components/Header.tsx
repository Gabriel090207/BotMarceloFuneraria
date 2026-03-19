import { useState, useEffect } from "react"
import { FiBell, FiChevronDown, FiLogOut, FiMenu } from "react-icons/fi"

import { auth, db } from "../services/firebase"
import { doc, getDoc } from "firebase/firestore"
import { signOut } from "firebase/auth"

import "../styles/header.css"

export default function Header(){

  const [menu,setMenu] = useState(false)
  const [user,setUser] = useState<any>(null)

  useEffect(()=>{

    async function carregar(){

      if(!auth.currentUser) return

      const ref = doc(db,"users",auth.currentUser.uid)

      const snap = await getDoc(ref)

      if(snap.exists()){

        setUser(snap.data())

      }

    }

    carregar()

  },[])

  function sair(){

    signOut(auth)

    window.location.href="/login"

  }

  const inicial = user?.nome?.charAt(0)?.toUpperCase() || "U"

  return(

    <header className="header">

  <div className="header-left">

    <button
      className="menu-btn"
      onClick={() => window.dispatchEvent(new Event("toggleSidebar"))}
    >
      <FiMenu size={22} />
    </button>

    <div className="header-title">
      Painel Administrativo
    </div>

  </div>

      <div className="header-actions">

        <FiBell size={20}/>

        <div
          className="user-box"
          onClick={()=>setMenu(!menu)}
        >

          <div className="user-avatar">
            {inicial}
          </div>

          <div className="user-info">

            <span className="user-name">
              {user?.nome} {user?.sobrenome}
            </span>

            <span className="user-role">
              {user?.role}
            </span>

          </div>

          <FiChevronDown className={`user-arrow ${menu ? "rotate":""}`}/>

        </div>

        {menu && (

          <div className="user-menu">

            <button
              className="logout-btn"
              onClick={sair}
            >

              <FiLogOut/>

              Sair

            </button>

          </div>

        )}

      </div>

    </header>

  )

}