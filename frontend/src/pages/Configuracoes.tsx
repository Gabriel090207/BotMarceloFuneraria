import { useState } from "react"
import { FiUsers, FiSettings, FiTool } from "react-icons/fi"

import Usuarios from "../components/config/Usuarios"
import Empresa from "../components/config/Empresa"

import "../styles/configuracoes.css"

export default function Configuracoes(){

  const [secao,setSecao] = useState("usuarios")

  return(

    <div className="config-page">

      <div className="config-header">

        <h1>Configurações</h1>
        <p>Gerencie as configurações do sistema</p>

      </div>

      <div className="config-grid">

        <div
          className={`config-card ${secao==="usuarios" ? "ativo":""}`}
          onClick={()=>setSecao("usuarios")}
        >

          <div className="config-icon">
            <FiUsers/>
          </div>

          <div>

            <h3>Usuários</h3>
            <p>Gerenciar administradores e funcionários</p>

          </div>

        </div>

        <div
          className={`config-card ${secao==="empresa" ? "ativo":""}`}
          onClick={()=>setSecao("empresa")}
        >

          <div className="config-icon">
            <FiSettings/>
          </div>

          <div>

            <h3>Empresa</h3>
            <p>Dados da funerária</p>

          </div>

        </div>

        <div
          className={`config-card ${secao==="integracoes" ? "ativo":""}`}
          onClick={()=>setSecao("integracoes")}
        >

          <div className="config-icon">
            <FiTool/>
          </div>

          <div>

            <h3>Integrações</h3>
            <p>Configuração de APIs</p>

          </div>

        </div>

      </div>

      {/* CONTEÚDO */}

      {secao && (

        <div className="config-content">

          {secao === "usuarios" && <Usuarios/>}

          {secao === "empresa" && <Empresa/>}

          {secao === "integracoes" && (
            <div className="config-placeholder">
              Em breve: integrações
            </div>
          )}

        </div>

      )}

    </div>

  )

}