import { FiBell, FiUser } from "react-icons/fi"
import "../styles/header.css"

export default function Header(){

  return(

    <header className="header">

      <div className="header-title">
        Painel Administrativo
      </div>

      <div className="header-actions">

        <FiBell size={20}/>

        <FiUser size={20}/>

      </div>

    </header>

  )

}