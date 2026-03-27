import { useState, useEffect } from "react"
import { FiSearch, FiMoreVertical } from "react-icons/fi"

import { collection, getDocs, query, updateDoc, doc } from "firebase/firestore"
import { db } from "../services/firebase"

import "../styles/pedidos.css"
import "../styles/dashboard.css"

export default function Pedidos(){

  const [busca,setBusca] = useState("")
  const [filtro,setFiltro] = useState("todos")
  const [pedidos,setPedidos] = useState<any[]>([])

  const [pedidoSelecionado, setPedidoSelecionado] = useState<any | null>(null)
  const [modalAcoesAberto, setModalAcoesAberto] = useState(false)
  const [modalDetalhesAberto, setModalDetalhesAberto] = useState(false)

  useEffect(()=>{

    async function carregarPedidos(){

      const q = query(collection(db,"pedidos"))

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

  function abrirAcoes(pedido:any){
    setPedidoSelecionado(pedido)
    setModalAcoesAberto((prev)=> pedidoSelecionado?.id !== pedido.id || !prev)
  }

  function fecharAcoes(){
    setPedidoSelecionado(null)
    setModalAcoesAberto(false)
  }

  function abrirDetalhes(pedido:any){
    setPedidoSelecionado(pedido)
    setModalDetalhesAberto(true)
  }

  function fecharDetalhes(){
    setPedidoSelecionado(null)
    setModalDetalhesAberto(false)
  }

  async function atualizarStatus(novoStatus:string){
    if(!pedidoSelecionado) return

    try{
      await updateDoc(doc(db,"pedidos",pedidoSelecionado.id),{
        status: novoStatus
      })

      setPedidos(prev =>
        prev.map(p =>
          p.id === pedidoSelecionado.id
            ? { ...p, status: novoStatus }
            : p
        )
      )

      fecharAcoes()

    }catch(err){
      console.error(err)
      alert("Erro ao atualizar status")
    }
  }

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

                  <div className="acoes-wrapper">

                    <button
                      className="btn-acoes"
                      onClick={()=>abrirAcoes(pedido)}
                    >
                      <FiMoreVertical size={18}/>
                    </button>

                    {modalAcoesAberto && pedidoSelecionado?.id === pedido.id && (
                      <div className="dropdown-acoes">

                        <button onClick={()=>{
                          fecharAcoes()
                          abrirDetalhes(pedidoSelecionado)
                        }}>
                          Ver detalhes
                        </button>

                        <button onClick={()=>atualizarStatus("finalizado")}>
                          Finalizar
                        </button>

                        <button onClick={()=>atualizarStatus("cancelado")}>
                          Cancelar
                        </button>

                      </div>
                    )}

                  </div>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

      {/* MODAL DETALHES */}
{modalDetalhesAberto && pedidoSelecionado && (
  <div className="modal-overlay" onClick={fecharDetalhes}>
    <div className="modal-detalhes" onClick={(e)=>e.stopPropagation()}>

      <h2>Detalhes do Pedido</h2>

      <p><strong>Cliente:</strong> {pedidoSelecionado.nome || "-"}</p>
      <p><strong>Telefone:</strong> {pedidoSelecionado.telefone || "-"}</p>
      <p><strong>Serviço:</strong> {pedidoSelecionado.tipo || "-"}</p>
      <p><strong>Status:</strong> {pedidoSelecionado.status || "-"}</p>

      <hr />

      <p><strong>Velório:</strong> {pedidoSelecionado.dados?.velorio || "-"}</p>
      <p><strong>Local do velório:</strong> {pedidoSelecionado.dados?.local_velorio || "-"}</p>
      <p><strong>Endereço do velório:</strong> {pedidoSelecionado.dados?.endereco_velorio || "-"}</p>
      <p><strong>Data do velório:</strong> {pedidoSelecionado.dados?.data_velorio || "-"}</p>
      <p><strong>Horário do velório:</strong> {pedidoSelecionado.dados?.horario_velorio || "-"}</p>

      <p><strong>Local do ente querido:</strong> {pedidoSelecionado.dados?.local_corpo || "-"}</p>
      <p><strong>Endereço do local:</strong> {pedidoSelecionado.dados?.endereco_local_corpo || "-"}</p>
      <p><strong>Porte:</strong> {pedidoSelecionado.dados?.porte || "-"}</p>

      <p><strong>Cemitério:</strong> {pedidoSelecionado.dados?.cemiterio || "-"}</p>
      <p><strong>Horário do sepultamento:</strong> {pedidoSelecionado.dados?.horario_sepultamento || "-"}</p>

      <p><strong>Cerimônia cremação:</strong> {pedidoSelecionado.dados?.cerimonia_cremacao || "-"}</p>
      <p><strong>Horário da cremação:</strong> {pedidoSelecionado.dados?.horario_cremacao || "-"}</p>
      <p><strong>Crematório:</strong> {pedidoSelecionado.dados?.crematorio || "-"}</p>
      <p><strong>Outro crematório:</strong> {pedidoSelecionado.dados?.crematorio_outro_nome || "-"}</p>

      {pedidoSelecionado.urna && (
        <p><strong>Urna:</strong> {pedidoSelecionado.urna.nome}</p>
      )}

      {pedidoSelecionado.urna_cinzas && (
        <p><strong>Urna de cinzas:</strong> {pedidoSelecionado.urna_cinzas.nome}</p>
      )}

      {pedidoSelecionado.pagamento && (
        <>
          <hr />
          <p><strong>Valor total:</strong> {pedidoSelecionado.pagamento.total || "-"}</p>
          <p><strong>Entrada:</strong> {pedidoSelecionado.pagamento.sinal || "-"}</p>
        </>
      )}

      <button onClick={fecharDetalhes} className="btn-fechar">
        Fechar
      </button>

    </div>
  </div>
)}

    </div>

  )

}