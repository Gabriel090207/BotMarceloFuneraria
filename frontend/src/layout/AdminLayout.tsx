import Sidebar from "../components/Sidebar"
import Header from "../components/Header"

import { Outlet } from "react-router-dom"

import "../styles/layout.css"

export default function AdminLayout(){

  return(

    <div>

      <Header />

      <div className="layout">

        <Sidebar />

        <main className="content">

          <Outlet />

        </main>

      </div>

    </div>

  )

}