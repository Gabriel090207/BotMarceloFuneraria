import React from "react"
import Sidebar from "../components/Sidebar"
import Header from "../components/Header"

import "../styles/layout.css"

type Props = {
  children: React.ReactNode
}

export default function AdminLayout({ children }: Props){

  return(

    <div>

      <Header />

      <div className="layout">

        <Sidebar />

        <main className="content">

          {children}

        </main>

      </div>

    </div>

  )

}