import { useState, useEffect } from "react"
import { FiSearch } from "react-icons/fi"

import { collection, getDocs, query} from "firebase/firestore"
import { db } from "../services/firebase"

import "../styles/pedidos.css"
import "../styles/dashboard.css"

export default function Pedidos(){

  const [busca,setBusca] = useState("")
  const [filtro,setFiltro] = useState("todos")
  const [pedidos,setPedidos] = useState<any[]>([])

  useEffect(()=>{

    async function carregarPedidos(){

      const q = query(
  collection(db,"pedidos")
)

      const snapshot = await getDocs(q)

      const lista:any[] = []

      snapshot.forEach((doc)=>{
        lista.push({
          id:doc.id,
          ...doc.data()
        })
      })

      setPedidos(lista)

    }

    carregarPedidos()

  },[])

function renderStatus(status:string){

  if(status === "aberto"){
    return <span className="status status-open">Aberto</span>
  }

  if(status === "finalizado"){
    return <span className="status status-paid">Finalizado</span>
  }

  if(status === "cancelado"){
    return <span className="status status-cancelado">Cancelado</span>
  }

  return <span>{status}</span>
}

  const pedidosFiltrados = pedidos.filter((pedido:any)=>{

    const buscaMatch =
      pedido.nome?.toLowerCase().includes(busca.toLowerCase()) ||
      pedido.telefone?.includes(busca)

    const filtroMatch =
      filtro === "todos" || pedido.status === filtro

    return buscaMatch && filtroMatch

  })

  return(

    <div className="pedidos-page">

      <div className="pedidos-header">

        <h1>Pedidos</h1>

        <div className="pedidos-filtros">

          <div className="search">

            <FiSearch />

            <input
              placeholder="Buscar cliente"
              value={busca}
              onChange={(e)=>setBusca(e.target.value)}
            />

          </div>

          <select
            className="filtro"
            value={filtro}
            onChange={(e)=>setFiltro(e.target.value)}
          >

            <option value="todos">Todos</option>
            <option value="aberto">Aberto</option>
            <option value="finalizado">Finalizado</option>
            <option value="cancelado">Cancelado</option>

          </select>

        </div>

      </div>

      <div className="pedidos-table">

        <table>

          <thead>

            <tr>

              <th>Cliente</th>
              <th>Telefone</th>
              <th>Serviço</th>
              <th>Urna</th>
              <th>Status</th>
              <th>Ações</th>

            </tr>

          </thead>

          <tbody>

            {pedidosFiltrados.map((pedido:any)=>(

              <tr key={pedido.id}>

                <td>{pedido.nome}</td>

                <td>{pedido.telefone || "-"}</td>

                <td>{pedido.tipo}</td>

               <td>{pedido.urna?.nome || "-"}</td>

                <td>{renderStatus(pedido.status)}</td>

                <td>

                  <div className="pedido-acoes">

                    <button className="btn btn-ver">
                      Ver
                    </button>

                    <button className="btn btn-cancelar">
                      Cancelar
                    </button>

                  </div>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>

  )

}