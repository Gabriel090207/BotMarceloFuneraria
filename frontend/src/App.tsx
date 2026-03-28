import { Routes, Route } from "react-router-dom"


import ScrollToTop from "./components/ScrollToTop"

import AdminLayout from "./layout/AdminLayout"
import ProtectedRoute from "./components/ProtectedRoute"

import Login from "./pages/Login"

import Dashboard from "./pages/Dashboard"
import Pedidos from "./pages/Pedidos"

import Urnas from "./pages/Pacotes"
import NovaUrna from "./pages/NovoPacote"
import EditarUrna from "./pages/EditarPacote"

import Produtos from "./pages/Produtos"
import PlanosFamiliares from "./pages/PlanosFamiliares"
import PlanosEmpresariais from "./pages/PlanosEmpresariais"

import Configuracoes from "./pages/Configuracoes"

export default function App(){

  return(


      <>
    <ScrollToTop/>

    <Routes>

      {/* LOGIN */}

      <Route path="/login" element={<Login />} />

      {/* ROTAS PROTEGIDAS */}

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AdminLayout />
          </ProtectedRoute>
        }
      >

        <Route index element={<Dashboard />} />

        <Route path="pedidos" element={<Pedidos />} />


        <Route path="pacotes" element={<Urnas />} />
        <Route path="novo-pacote" element={<NovaUrna />} />
        <Route path="editar-pacote/:id" element={<EditarUrna />} />
        
        <Route path="produtos" element={<Produtos />} />

        <Route path="planos-familiares" element={<PlanosFamiliares />} />
        <Route path="planos-empresariais" element={<PlanosEmpresariais />} />

        {/* CONFIGURAÇÕES */}

        <Route path="configuracoes" element={<Configuracoes />} />

      </Route>

    </Routes>
</>

  )

}