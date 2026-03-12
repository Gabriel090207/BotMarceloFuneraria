import { Routes, Route } from "react-router-dom"

import AdminLayout from "./layout/AdminLayout"

import Dashboard from "./pages/Dashboard"
import Pedidos from "./pages/Pedidos"
import Urnas from "./pages/Urnas"
import Produtos from "./pages/Produtos"
import PlanosFamiliares from "./pages/PlanosFamiliares"
import PlanosEmpresariais from "./pages/PlanosEmpresariais"

export default function App(){

  return(

    <AdminLayout>

      <Routes>

        <Route path="/" element={<Dashboard />} />

        <Route path="/pedidos" element={<Pedidos />} />

        <Route path="/urnas" element={<Urnas />} />

        <Route path="/produtos" element={<Produtos />} />

        <Route path="/planos-familiares" element={<PlanosFamiliares />} />
        <Route path="/planos-empresariais" element={<PlanosEmpresariais />} />

      </Routes>

    </AdminLayout>

  )

}