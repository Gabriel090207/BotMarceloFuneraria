import { Routes, Route } from "react-router-dom"

import ScrollToTop from "./components/ScrollToTop"

import AdminLayout from "./layout/AdminLayout"
import ProtectedRoute from "./components/ProtectedRoute"

import Login from "./pages/Login"


import Pedidos from "./pages/Pedidos"

import Servicos from "./pages/Servicos"
import NovoServico from "./pages/NovoServico"
import EditarServico from "./pages/EditarServico"

import Produtos from "./pages/Produtos"


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

          <Route index element={<Servicos />} />

          <Route path="pedidos" element={<Pedidos />} />

          {/* SERVIÇOS FUNERÁRIOS */}
          <Route path="servicos" element={<Servicos />} />
          <Route path="novo-servico" element={<NovoServico />} />
          <Route path="editar-servico/:id" element={<EditarServico />} />

          {/* PRODUTOS */}
          <Route path="produtos" element={<Produtos />} />

          {/* PLANOS */}
        

          {/* CONFIGURAÇÕES */}
          <Route path="configuracoes" element={<Configuracoes />} />

        </Route>

      </Routes>
    </>

  )

}